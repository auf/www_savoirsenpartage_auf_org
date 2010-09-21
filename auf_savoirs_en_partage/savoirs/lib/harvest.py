# -*- encoding: utf-8 -*-
import sys, os, time, traceback
from auf_savoirs_en_partage.backend_config import RESOURCES
from savoirs.models import HarvestLog
from sep import SEP

def import_all ():
    """Cette méthode effectue l'importation des données pour toutes les 
    sources définies dans `conf.py`, et les ajoute dans le système de stockage 
    en passant par SEP (:doc:`../sep/index`)
    """
    sep = SEP ()

    resources = RESOURCES
    if len(sys.argv) == 2:
        name = sys.argv[1]
        if RESOURCES.get(name) is not None:
            resources = {name: RESOURCES.get(name)}
        else:
            print "Ressource %s non existante" % name
            sys.exit(-1)

    for name in resources.keys ():
        print "Import:", name
        options = RESOURCES[name]
        options['server'] = name

        module = 'harvesters.%s.%s' \
                % (options['type'], options['acces'])
        __import__ (module)
        harvester = sys.modules[module]
        try:
            nodes = harvester.harvest (options)
        except:
            print "Exception:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
            nodes = []

        added = updated = 0
        for node in nodes:
            node['server'] = name

            try:
                status = sep.add (node)
            except:
                message.update({'context':'error', 'name':name, 'processed':0})
                HarvestLog.add(message)
                continue

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
