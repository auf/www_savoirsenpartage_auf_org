# -*- encoding: utf-8 -*-
import sys, os, time, traceback
from auf_savoirs_en_partage.backend_config import RESOURCES
from savoirs.models import HarvestLog, Record
from sep import SEP

class HarvestStats:

    libelles = {'site':50, 'url':50, 'type':10, 'acces':10, 'ref_importees':20, 'date':30, 'obs':10}
    separateur = " "

    def dernier_logs_moisson(self, site):
        return HarvestLog.objects.filter(name=site, context='moisson').order_by('-date')

    def date(self, site):
        logs = self.dernier_logs_moisson(site)
        if len(logs) > 0:
            return str(logs[0].date)
        else:
            return "pas d'import"

    def ref_importees(self, site):
        records = Record.all_objects.filter(server=site)
        return str(len(records))

    def stats(self,):
        stats = []
        tableau = []
        for site, options in RESOURCES.items():
            options['site'] = site
            tableau.append(options)
        
        # libelles
        libelles_formates = []
        for l, largeur in self.libelles.items():
            l = "*%s*" % l
            libelles_formates.append(l.ljust(largeur, self.separateur))
        stats.append(libelles_formates)
        
        # lignes
        for ligne in tableau:
            ligne_ordonnee = []
            for l,largeur in self.libelles.items():
                method = getattr(self, l, None)
                if method is not None:
                    value = method(ligne['site'])
                elif ligne.has_key(l):
                    value = ligne[l]
                else:
                    value = ""
                value = value.ljust(largeur, self.separateur)
                ligne_ordonnee.append(value)
            stats.append(ligne_ordonnee)
        return stats

    def wiki(self,):
        for s in self.stats():
            print "|%s|" % "|".join(s)

def import_all ():
    """Cette méthode effectue l'importation des données pour toutes les 
    sources définies dans `conf.py`, et les ajoute dans le système de stockage 
    en passant par SEP (:doc:`../sep/index`)
    """
    sep = SEP ()

    resources = RESOURCES
    if len(sys.argv) == 2:
        name = sys.argv[1]

        if name == 'stats':
            stats = HarvestStats()
            stats.wiki()
            sys.exit(1)

        if RESOURCES.get(name) is not None:
            resources = {name: RESOURCES.get(name)}
        else:
            print "Ressource %s non existante" % name
            sys.exit(-1)

    for name in resources.keys ():
        print "Import:", name.encode('utf-8')
        options = RESOURCES[name]
        options['server'] = name

        module = 'harvesters.%s.%s' \
                % (options['type'], options['acces'])
        __import__ (module)
        harvester = sys.modules[module]
        try:
            nodes = harvester.harvest (options)
        except:
            print >> sys.stderr, "Exception:"
            print >> sys.stderr, '-'*60
            traceback.print_exc(file=sys.stderr)
            print >> sys.stderr, '-'*60
            nodes = []

        added = updated = 0
        for node in nodes:
            node['server'] = name
            status = sep.add(node)

            if status['added']:
                added += 1
            if status['updated']:
                updated += 1
            message = status
            message.update({'context':'record', 'name':name, 'processed':1})
            HarvestLog.add(message)

        message = {'context':'moisson', 'name':name, 'added':added, 'updated':updated, 'processed':len(nodes)}
        HarvestLog.add(message)

    del (sep)

if __name__ == '__main__':
    import_all()
