-- Ramenons le mot de passe dans la fiche personne

ALTER TABLE chercheurs_personne ADD COLUMN password varchar(35) NOT NULL;

UPDATE chercheurs_personne p INNER JOIN chercheurs_utilisateur u ON u.personne_ptr_id = p.id
SET p.password = u.password;

DROP TABLE chercheurs_utilisateur;

-- Utilisons l'héritage Django pour garder un lien entre le chercheur et la
-- personne.
ALTER TABLE chercheurs_chercheur CHANGE COLUMN personne personne_ptr_id integer NOT NULL;

UPDATE chercheurs_chercheurgroupe cg 
INNER JOIN chercheurs_chercheur c ON c.id = cg.chercheur
SET cg.chercheur = c.personne_ptr_id;

UPDATE chercheurs_expertise ce 
INNER JOIN chercheurs_chercheur c ON c.id = ce.chercheur_id
SET ce.chercheur_id = c.personne_ptr_id;

UPDATE chercheurs_publication cp 
INNER JOIN chercheurs_chercheur c ON c.id = cp.chercheur_id
SET cp.chercheur_id = c.personne_ptr_id;

ALTER TABLE chercheurs_these DROP PRIMARY KEY;
UPDATE chercheurs_these t 
INNER JOIN chercheurs_chercheur c ON c.id = t.chercheur_id
SET t.chercheur_id = c.personne_ptr_id;
ALTER TABLE chercheurs_these ADD PRIMARY KEY (chercheur_id);

ALTER TABLE chercheurs_chercheur 
    DROP COLUMN id,
    ADD PRIMARY KEY (personne_ptr_id);
