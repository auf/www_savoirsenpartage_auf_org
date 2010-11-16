ALTER TABLE chercheurs_chercheur
    ADD COLUMN `membre_instance_auf_details` varchar(255) NOT NULL,
    ADD COLUMN `expert_oif_details` varchar(255) NOT NULL,
    ADD COLUMN `expert_oif_dates` varchar(255) NOT NULL;
