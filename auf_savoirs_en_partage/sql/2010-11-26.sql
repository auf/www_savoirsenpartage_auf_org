-- Le chercheur n'a pas besoin d'une colonne "actif". C'est la "personne" qui a
-- le champ "actif".

ALTER TABLE chercheurs_chercheur DROP COLUMN actif;

-- On déplace les thèses dans leur propre table pour les isoler des
-- publications.

CREATE TABLE `chercheurs_these` (
    `chercheur_id` integer NOT NULL PRIMARY KEY,
    `titre` varchar(255) NOT NULL,
    `annee` integer NOT NULL,
    `directeur` varchar(255) NOT NULL,
    `etablissement` varchar(255) NOT NULL,
    `nb_pages` integer,
    `url` varchar(255) NOT NULL
)
;
ALTER TABLE `chercheurs_these` ADD CONSTRAINT `chercheur_id_refs_id_727f1a45` FOREIGN KEY (`chercheur_id`) REFERENCES `chercheurs_chercheur` (`id`);

INSERT INTO chercheurs_these (chercheur_id, titre, annee, directeur, etablissement, nb_pages, url)
SELECT c.id, p.titre, p.annee, p.editeur, p.lieu_edition, NULLIF(p.nb_pages, ''), p.url
FROM chercheurs_publication p
INNER JOIN chercheurs_chercheur c ON c.these = p.id;

DELETE p FROM chercheurs_publication p
INNER JOIN chercheurs_chercheur c ON c.these = p.id;

ALTER TABLE chercheurs_chercheur DROP COLUMN these;

-- Les publications auront maintenant une foreign key vers les chercheurs
-- plutôt que le contraire.

ALTER TABLE chercheurs_publication ADD COLUMN `chercheur_id` integer NOT NULL AFTER id;
ALTER TABLE `chercheurs_publication` ADD CONSTRAINT `chercheur_id_refs_id_4bd3fee4` FOREIGN KEY (`chercheur_id`) REFERENCES `chercheurs_chercheur` (`id`);

UPDATE chercheurs_publication p 
INNER JOIN chercheurs_chercheur c ON p.id IN (c.publication1, c.publication2, c.publication3, c.publication4)
SET p.chercheur_id = c.id;

ALTER TABLE chercheurs_chercheur 
    DROP COLUMN publication1,
    DROP COLUMN publication2,
    DROP COLUMN publication3,
    DROP COLUMN publication4;

ANALYZE TABLE chercheurs_chercheur;

-- On ne peut pas à la fois forcer une clé unique sur le courriel et conserver
-- les comptes inactifs dans la table.

ALTER TABLE chercheurs_personne
    DROP KEY courriel,
    ADD KEY courriel (courriel);

-- Certains chercheurs ont un nom qui commence par un espace

UPDATE chercheurs_personne SET nom = TRIM(nom), prenom = TRIM(prenom);
UPDATE chercheurs_chercheur SET etablissement_autre_nom = TRIM(etablissement_autre_nom);
UPDATE chercheurs_chercheur SET diplome = '' WHERE diplome = '.';
UPDATE chercheurs_chercheur SET etablissement_autre_nom = '' WHERE etablissement_autre_nom = '.';
UPDATE chercheurs_chercheur SET theme_recherche = '' WHERE theme_recherche = '.';
