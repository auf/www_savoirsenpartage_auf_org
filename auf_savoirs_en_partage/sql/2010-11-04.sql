-- Activités en francophonie d'un chercheur

BEGIN;
ALTER TABLE `chercheurs_chercheur`
    ADD COLUMN `membre_instance_auf` bool NOT NULL,
    ADD COLUMN `membre_instance_auf_dates` varchar(255) NOT NULL,
    ADD COLUMN `expert_oif` bool NOT NULL,
    ADD COLUMN `membre_fipf` bool NOT NULL,
    ADD COLUMN `membre_fipf_association` varchar(255) NOT NULL;

ALTER TABLE chercheurs_expertise CHANGE COLUMN date_expertise `date` varchar(255) NOT NULL;
ALTER TABLE chercheurs_chercheur ADD COLUMN groupe_recherche varchar(255) NOT NULL;
COMMIT;


