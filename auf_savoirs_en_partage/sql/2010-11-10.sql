-- On change la question "Êtes-vous membre de la FIPF?"

ALTER TABLE chercheurs_chercheur
    DROP COLUMN membre_fipf,
    DROP COLUMN membre_fipf_association;

ALTER TABLE chercheurs_chercheur
    ADD COLUMN `membre_association_francophone` bool NOT NULL,
    ADD COLUMN `membre_association_francophone_details` varchar(255) NOT NULL,
    ADD COLUMN `membre_reseau_institutionnel` bool NOT NULL,
    ADD COLUMN `membre_reseau_institutionnel_details` varchar(255) NOT NULL,
    ADD COLUMN `membre_reseau_institutionnel_dates` varchar(255) NOT NULL;
