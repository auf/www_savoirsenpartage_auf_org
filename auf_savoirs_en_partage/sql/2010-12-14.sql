ALTER TABLE `chercheurs_chercheur`
    ADD COLUMN `membre_reseau_institutionnel_nom` varchar(15) NOT NULL,
    CHANGE COLUMN membre_reseau_institutionnel_details `membre_reseau_institutionnel_fonction` varchar(255) NOT NULL;

ALTER TABLE `chercheurs_chercheur`
    ADD COLUMN `membre_instance_auf_nom` varchar(10) NOT NULL,
    CHANGE COLUMN membre_instance_auf_details `membre_instance_auf_fonction` varchar(255) NOT NULL;
