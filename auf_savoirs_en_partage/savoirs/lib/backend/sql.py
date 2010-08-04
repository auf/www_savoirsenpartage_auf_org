# -*- encoding: utf-8 -*-
import simplejson, re, datetime, operator
from globals import *
from savoirs.models import Record, HarvestLog


class Backend:
    def close (self):
        pass

    def add (self, metadata):
        r = Record ()
        for k in metadata.keys ():
            setattr (r, k, simplejson.dumps(metadata[k]))
        r.save()

    def delete (self, id):
        r = Record.objects.get(id = id)
        r.delete()

    def update (self, id, metadata):
        r = Record.objects.get(id = id)
        for k in metadata.keys ():
            setattr (r, k, simplejson.dumps(metadata[k]))
        r.save()

    def get (self, id):
        r = Record.objects.get(id = id)
        meta = {}
        for k in META.keys ():
            if hasattr (r, k):
                v = getattr (r, k)
                if v is not None:
                    meta[k] = simplejson.loads(v)
        return meta

    def ids (self):
        return [x.id for x in Record.objects.all()]

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

        q = "SELECT id, (" + m + ") AS score FROM savoirs_record WHERE (" \
                + m + ") HAVING score > 0 ORDER BY score DESC"

        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute(q)
        rc = cursor.fetchall()
        return rc

    def filter_string_contains (self, set, q, key):
        rc = []
        words = q.get (key)
        if words:
            r = re.compile (r'%s' % words, re.IGNORECASE)
            for k in set:
                str = self.get(k).get(key, "").encode("utf-8")
                if r.search (str) is not None:
                    rc.append (k)
        else:
            rc = set
        return rc

    def filter_string_equals (self, q, key):
        rc = []
        keys = self.ids ()
        for k in keys:
            str = self.get(k).get(key, "")
            if str.lower() == q[key].lower():
                rc.append ((k, 1))
        return rc

    def _score (self, matches):
        rc = 0
        for i in matches:
            for j in i:
                if len (j.strip()) > 0:
                    rc += 1
        return rc

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

    def search (self, q):
        rc = []
        sets = []

        if len (q) > 0:
            # Recherche "simple"
            ww = simplejson.dumps(q.get ("q", "").strip())[1:-1]
            if len (ww) > 0:
                s = self._text_search (ww)
                if len(s) > 0:
                    rc.append (s)
            # Recherche URL
            elif q.get (URI) is not None:
                s = []
                try:
                    s.append((Record.objects.get(uri__iexact = q).id, 1))
                    rc.append(s)
                except: pass
            # Recherche avancée
            else:
                creator = simplejson.dumps(q.get ("creator", ""))[1:-1]
                title = simplejson.dumps(q.get ("title", ""))[1:-1]
                description = simplejson.dumps(q.get ("description", ""))[1:-1]
                subject = simplejson.dumps(q.get ("subject", ""))[1:-1]

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

    def add_log (self, name, count):
        try:
            t = HarvestLog.objects.get(name = name)
        except:
            t = HarvestLog(name = name)

        t.count = count
        t.date = datetime.datetime.today()
        t.save()

    def logs (self):
        rc = {}
        tmp = HarvestLog.objects.all()
        for r in tmp:
            rc[r.name] = (r.date, r.count)
        return rc



