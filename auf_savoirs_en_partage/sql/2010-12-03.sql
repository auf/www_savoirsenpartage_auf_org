-- Nouveau champ pays dans les événements de l'agenda
ALTER TABLE `savoirs_evenement` ADD COLUMN `pays_id` varchar(2);

-- S'assurer que tous les sites sont actifs
UPDATE `sitotheque_site` SET actif = 1;
