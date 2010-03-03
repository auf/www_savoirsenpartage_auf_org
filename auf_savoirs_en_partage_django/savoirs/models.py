from django.db import models


class Discipline(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id_discipline')
    nom = models.CharField(max_length=765, db_column='nom_discipline')

    def __unicode__ (self):
        return "Discipline: %s" % self.nom

    class Meta:
        db_table = u'discipline'
        ordering = ["nom",]

class Actualite(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id_actualite')
    titre = models.CharField(max_length=765, db_column='titre_actualite')
    texte = models.TextField(db_column='texte_actualite')
    url = models.CharField(max_length=765, db_column='url_actualite')
    logo = models.CharField(max_length=765, db_column='logo_actualite')
    date = models.DateField(db_column='date_actualite')
    visible = models.CharField(max_length=3, db_column='visible_actualite')
    ancienid = models.IntegerField(db_column='ancienId_actualite') # Field name made lowercase.

    def __unicode__ (self):
        return "Actualite %d: %s" % (self.id, self.titre)

    class Meta:
        db_table = u'actualite'
        ordering = ["-date",]

