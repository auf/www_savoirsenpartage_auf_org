# -*- coding: utf-8 -*-

import base64
import hashlib
import os
import re

from django.utils.encoding import smart_str
from django.contrib.auth.models import User

from django_exportateur.exportateur import exportateur


def get_django_user_for_email(email):
    """Retourne un utilisateur Django avec le courriel donné.

       S'il y a déjà un utilisateur avec ce courriel, on s'assure qu'il est activé.

       Sinon, on crée un nouvel utilisateur."""
    candidates = User.objects.filter(email=email)
    if candidates.count() > 0:
        user = candidates[0]
        if not user.is_active:
            user.is_active = True
            user.save()
    else:
        username = email.split('@')[0]
        username = re.sub('\W', '_', username)[:30]
        i = 1
        while User.objects.filter(username=username).count() > 0:
            suffix = '_' + str(i)
            username = username[:30-len(suffix)] + suffix
            i += 1
        # XXX: possible race condition here...
        user = User.objects.create_user(username, email)
        user.save()
    return user

def export(queryset, type):
    from chercheurs.models import These

    if queryset.count() == 0:
        return None
    obj = queryset[0]
    headers = ['Nom', 'Prénom', 'Genre', 'Courriel', 'Téléphone', 'Adresse postale',
               'Statut', 'Diplôme', 'Établissement', 'Pays', 'Domaines de recherche',
               'Thèse', 'Directeur', 'Discipline', 'Thèmes de recherche', 'Équipe de recherche', 'Mots-clés',
               'Site web', 'Blog', 'Réseau social',
               'Membre instance AUF', "Sollicité par l'OIF", 'Membre société francophone',
               'Membre instance réseau institutionnel AUF', 'Expertises', 'Solliciter pour expertises',
               'Publications']
    data = []
    for c in queryset:
        row = []
        row.append(c.nom)
        row.append(c.prenom)
        row.append(c.get_genre_display())
        row.append(c.courriel)
        row.append(c.telephone)
        row.append(c.adresse_postale)
        row.append(c.get_statut_display())
        row.append(c.diplome)
        row.append(c.nom_etablissement)
        row.append(c.pays)
        row.append(', '.join(g.nom for g in c.groupes.all()))
        try:
            t = c.these
            row.append('%s, %s, %s, %s pages.' % (t.titre, t.etablissement, t.annee, t.nb_pages))
            row.append(t.directeur)
        except These.DoesNotExist:
            row.append('')
            row.append('')
        row.append(c.discipline.nom if c.discipline else '')
        row.append(c.theme_recherche)
        row.append(c.equipe_recherche)
        row.append(c.mots_cles)
        row.append(c.url_site_web)
        row.append(c.url_blog)
        row.append(c.url_reseau_social)
        if c.membre_instance_auf:
            row.append(', '.join([c.membre_instance_auf_nom, c.membre_instance_auf_fonction, c.membre_instance_auf_dates]))
        else:
            row.append('')
        if c.expert_oif:
            row.append(', '.join([c.expert_oif_details, c.expert_oif_dates]))
        else:
            row.append('')
        if c.membre_association_francophone:
            row.append(c.membre_association_francophone_details)
        else:
            row.append('')
        if c.membre_reseau_institutionnel:
            row.append(', '.join([c.membre_reseau_institutionnel_nom, c.membre_reseau_institutionnel_fonction, c.membre_reseau_institutionnel_dates]))
        else:
            row.append('')
        row.append('; '.join(', '.join([e.nom, e.date, e.organisme_demandeur]) for e in c.expertises.all()))
        if c.expertises_auf is None:
            row.append('')
        else:
            row.append('Oui' if c.expertises_auf else 'Non')
        row.append('; '.join(p.publication_affichage if p.publication_affichage else
                             '%s, %s, %s, %s, %s, %s, %s pages.' %
                             (p.auteurs, p.titre, p.revue, p.annee, p.editeur, p.lieu_edition, p.nb_pages)
                             for p in c.publications.all()))
        data.append([smart_str(x) if x else '' for x in row])
    return exportateur(headers, data, type, filename='chercheurs.%s' % type)

def create_ldap_hash(password):
    salt = os.urandom(4)
    raw_hash = hashlib.sha1(password.encode('utf-8') + salt).digest()
    ldap_hash = '{SSHA}' + base64.b64encode(raw_hash + salt)

    return ldap_hash

def check_ldap_hash(ldap_hash, password):
    hash_salt = base64.b64decode(ldap_hash[6:])
    hash = hash_salt[:-4]
    salt = hash_salt[-4:]
    test = hashlib.sha1(password.encode('utf-8') + salt).digest()
    return test == hash
