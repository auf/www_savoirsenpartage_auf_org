# -*- encoding: utf-8 -*-
import sys, os, time, traceback

from auf_savoirs_en_partage.backend_config import RESOURCES
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
        print "Ajout de", len(nodes), "references"
        print "S:", time.time ()
        for node in nodes:
            sep.add (node)
        sep.add_log (name, len(nodes))
        print "F:", time.time ()

    del (sep)

if __name__ == '__main__':
    import_all()
