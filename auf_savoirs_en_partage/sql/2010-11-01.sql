-- Ajout des tables many-to-many pour les régions et les disciplines

BEGIN;
CREATE TABLE `savoirs_evenement_regions` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `evenement_id` integer NOT NULL,
    `region_id` integer NOT NULL,
    UNIQUE (`evenement_id`, `region_id`)
)
;
ALTER TABLE `savoirs_evenement_regions` ADD CONSTRAINT `evenement_id_refs_id_5e92e839` FOREIGN KEY (`evenement_id`) REFERENCES `savoirs_evenement` (`id`);
ALTER TABLE `savoirs_evenement_regions` ADD CONSTRAINT `region_id_refs_id_771e693` FOREIGN KEY (`region_id`) REFERENCES `ref_region` (`id`);
CREATE TABLE `actualite_regions` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `actualite_id` integer NOT NULL,
    `region_id` integer NOT NULL,
    UNIQUE (`actualite_id`, `region_id`)
)
;
ALTER TABLE `actualite_regions` ADD CONSTRAINT `actualite_id_refs_id_actualite_7d8ac265` FOREIGN KEY (`actualite_id`) REFERENCES `actualite` (`id_actualite`);
ALTER TABLE `actualite_regions` ADD CONSTRAINT `region_id_refs_id_57ede84a` FOREIGN KEY (`region_id`) REFERENCES `ref_region` (`id`);
CREATE TABLE `actualite_disciplines` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `actualite_id` integer NOT NULL,
    `discipline_id` integer NOT NULL,
    UNIQUE (`actualite_id`, `discipline_id`)
)
;
ALTER TABLE `actualite_disciplines` ADD CONSTRAINT `actualite_id_refs_id_actualite_23f21297` FOREIGN KEY (`actualite_id`) REFERENCES `actualite` (`id_actualite`);
ALTER TABLE `actualite_disciplines` ADD CONSTRAINT `discipline_id_refs_id_discipline_682cd4d8` FOREIGN KEY (`discipline_id`) REFERENCES `discipline` (`id_discipline`);
CREATE TABLE `sitotheque_site_regions` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `site_id` integer NOT NULL,
    `region_id` integer NOT NULL,
    UNIQUE (`site_id`, `region_id`)
)
;
ALTER TABLE `sitotheque_site_regions` ADD CONSTRAINT `site_id_refs_id_637ee69d` FOREIGN KEY (`site_id`) REFERENCES `sitotheque_site` (`id`);
ALTER TABLE `sitotheque_site_regions` ADD CONSTRAINT `region_id_refs_id_63442bff` FOREIGN KEY (`region_id`) REFERENCES `ref_region` (`id`);
COMMIT;
