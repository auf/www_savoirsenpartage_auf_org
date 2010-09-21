# -*- encoding: utf-8 -*-
import simplejson, re, datetime, operator, hashlib
from savoirs.globals import *
from savoirs.models import Record, ListSet

class SEPEncoder:
    """
    Classe permettant de d'encoder et de décoder les données moissonnées.
    """
    separator = ", "

    def encode(self, field, data):
        if field in META.keys() and META[field]['type'] == 'array': 
            return self.separator.join(data)
        else:
            return data

    def decode(self, field, data):
        if field in META.keys() and META[field]['type'] == 'array': 
            return data.split(self.separator)
        else:
            return data
    
    #def migrate(self,):
    #    for r in Record.objects.all():
    #        for f in META.keys():
    #            json = getattr(r, f)
    #            if json is not None:
    #                normal = simplejson.loads(json)
    #                new = self.encode(f, normal)
    #                setattr(r, f, new)
    #        r.save()

class SEP:
    """
    Classe utilisée pour réaliser manipuler les données moisonnées.
    """

    encoder = SEPEncoder()

    ############################################################################
    # MÉTHODES INTERNES
    ############################################################################

    def _load (self, id):
        """Recupérer la structure de métadonnées pour un record selon un `id`."""
        r = Record.objects.get(id = id)
        meta = {}
        for k in META.keys ():
            if hasattr (r, k):
                v = getattr (r, k)
                if v is not None:
                    meta[k] = self.encoder.decode(k, v)
        return meta

    # traitement spécial pour certaines clef de la structure
    def listsets(self, record, value):
        
        # doit avoir un id pour créer les relations multivaluées
        record.save()
        for set in  [ls for ls in ListSet.objects.all() if ls.spec in value]:
            record.listsets.add(set)

    def _update_record(self, r, metadata):
        for k in metadata.keys ():
            if hasattr(self, k):
                method = getattr(self, k)
                method(r, metadata[k])
            else:
                setattr (r, k, self.encoder.encode(k, metadata[k]))

        r.last_checksum = hashlib.md5(str(metadata)).hexdigest()
        r.last_update = datetime.datetime.today()
        r.save()


    def _save (self, metadata):
        r = Record ()
        self._update_record(r, metadata)
        return r.id

    def _modify (self, id, metadata):
        r = Record.objects.get(id = id)

        # test si le fichier a été modifié
        if hashlib.md5(str(metadata)).hexdigest() == r.last_checksum:
            return False

        self._update_record(r, metadata)

        return True

    def _combine (self, result_lists, op):
        scores = {}
        simple_sets = []

        for list in result_lists:
            simple_sets.append (set([x[0] for x in list]))
            for (id, score) in list:
                if scores.get (id) is None:
                    scores[id] = 0
                scores[id] += score

        matches = []
        for s in simple_sets:
            if op == "|":
                matches = set(matches) | s
            elif op == "&":
                if len (matches) == 0:
                    matches = s
                else:
                    matches = set(matches) & s
            #print "EE", matches

        return [(x, scores[x]) for x in matches]


    def _text_search (self, q, fields = None):
        if fields is None:
            fields = [x for x in META.keys() if META[x].get("text_search", False)]

        w = re.compile (r'\W+', re.U)
        words = w.split (q)
        
        matches = []
        suffix = ""
        if len(fields)==1 and fields[0] == "subject":
            suffix = " IN BOOLEAN MODE"

        for k in fields:
            matches.append ("MATCH(`%s`) AGAINST ('%s'%s)" % (k, " ".join(words), suffix))
        m = "+".join (matches)

        q = "SELECT r.id, (%s) AS score FROM savoirs_record AS r \
             LEFT JOIN savoirs_record_listsets AS rl ON r.id = rl.record_id \
             JOIN savoirs_listset AS l ON rl.listset_id = l.spec \
             WHERE (%s) AND r.validated = 1 AND l.validated = 1 \
             HAVING score > 0 ORDER BY score DESC" % (m, m)

        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute(q)
        rc = cursor.fetchall()
        return rc

    ############################################################################
    # API
    ############################################################################

    def add (self, metadata):
        """Ajouter la ressource définie par `metadata`. Si on trouve une 
        ressource avec le même `identifier`, on le met a jour.

        Retourne l'id de la ressource créée ou mise à jour.
        """
        added = updated = False
        exists = self.search (q = {URI: metadata[URI]})
        if len (exists) > 0:
            id = exists[0][0]
            updated = self.update (int(id), metadata)
        else:
            added = True
            id = self._save (metadata)
        return {'record_id': id, 'added':added, 'updated':updated}

    def delete (self, id):
        """Supprime la ressource identifiée par `id`.
        """
        r = Record.objects.get(id = id)
        r.delete()

    def update (self, id, metadata):
        """Met a jour la ressource identifiée par `id`, avec les données de 
        `metadata`. Une exception est levée si elle n'existe pas.
        """
        if self.get (int(id)) is not None:
            return self._modify (int(id), metadata)
        else:
            raise Exception ("Objet inexistant")
        return False

    def get (self, id):
        """Recupérer la structure de métadonnées pour la ressource identifiée 
        par `id`. `id` peut être une liste si on veut les structures de 
        plusieurs ressources.
        """
        if isinstance (id, tuple) or isinstance (id, list):
            rc = []
            for i in id:
                try:
                    i = i[0]
                except: pass
                rc.append (self._load (int(i)))
        else:
            rc = self._load (int(id))
        return rc

    def ids (self):
        """ Retourner la liste complète des ids des ressources."""
        return [x.id for x in Record.objects.all()]

    def search (self, q):
        """Effectue une recherche multi-critères, en fonction du dictionnaire 
        `q`. Retourne une list d'`id`s uniquement. Les données pour chaque 
        résultat doivent être chargées ulterieurement.
        """
        rc = []
        sets = []

        if len (q) > 0:
            # Recherche "simple"
            ww = q.get ("q", "").strip()
            if len (ww) > 0:
                s = self._text_search (ww)
                if len(s) > 0:
                    rc.extend(s)
            # Recherche URL
            elif q.get (URI) is not None:
                s = []
                try:
                    s.append((Record.objects.get(uri__iexact = q.get(URI)).id, 1))
                    rc.append(s)
                except: pass
            # Recherche avancée
            else:
                creator = q.get ("creator", "")
                title = q.get ("title", "")
                description = q.get ("description", "")
                subject = q.get ("subject", "")

                if len (creator) > 0:
                    sets.append (self._text_search (creator, [CREATOR, CONTRIBUTOR]))
                if len (title) > 0:
                    sets.append (self._text_search (title, [TITLE, ALT_TITLE]))
                if len (description) > 0:
                    sets.append (self._text_search (description, [DESCRIPTION, ABSTRACT]))
                if len (subject) > 0:
                    sets.append (self._text_search (subject, [SUBJECT,]))
                rc = self._combine (sets, q.get ("operator", "|"))
                rc.sort (key = operator.itemgetter(1), reverse = True)

            if len(rc) > 0:
                rc = [x[0] for x in rc]

        else:
            rc = self.ids()
        return rc
