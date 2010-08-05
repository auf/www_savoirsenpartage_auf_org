# -*- encoding: utf-8 -*-
from exceptions import Exception
import sys, time

from auf_savoirs_en_partage.backend_config import RESOURCES
from savoirs.globals import *
from backend import Backend


class SEP:
    """
    """
    backend = None

    def __init__ (self):
        self.backend = Backend ()
    
    def __del__ (self):
        self.backend.close ()

#############
# API public
    def search (self, q = {}):
        """Effectue une recherche multi-critères, en fonction du dictionnaire 
        `q`. Retourne une list d'`id`s uniquement. Les données pour chaque 
        résultat doivent être chargées ulterieurement.
        """
        return self.backend.search (q)

    def get (self, id):
        """Recupérer la structure de métadonnées pour la ressource identifiée 
        par `id`. `id` peut être une liste si on veut les structures de 
        plusieurs ressources.
        """
        if isinstance (id, tuple) or isinstance (id, list):
            rc = []
            for i in id:
                rc.append (self.backend.get (int(i[0])))
        else:
            rc = self.backend.get (int(id))
        return rc

    def add (self, metadata):
        """Ajouter la ressource définie par `metadata`. Si on trouve une 
        ressource avec le même `identifier`, on le met a jour.

        Retourne l'id de la ressource créée ou mise à jour.
        """
        exists = self.search (q = {URI: metadata[URI]})
        if len (exists) > 0:
            id = exists[0][0]
            return self.update (int(id), metadata)
        else:
            return self.backend.add (metadata)

    def update (self, id, metadata):
        """Met a jour la ressource identifiée par `id`, avec les données de 
        `metadata`. Une exception est levée si elle n'existe pas.
        """
        if self.get (int(id)) is not None:
            self.backend.update (int(id), metadata)
        else:
            raise Exception ("Objet inexistant")

    def delete (self, id):
        """Supprime la ressource identifiée par `id`.
        """
        self.backend.delete (int(id))

    def add_log (self, name, count):
        if hasattr (self.backend, 'add_log'):
            self.backend.add_log (name, count)

    def logs (self):
        rc = {}
        if hasattr (self.backend, 'logs'):
            rc = self.backend.logs()
        return rc

