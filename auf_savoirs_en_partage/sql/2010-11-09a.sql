-- Un chercheur a plusieurs expertises et non le contraire

ALTER TABLE chercheurs_expertise ADD COLUMN `chercheur_id` integer NOT NULL AFTER id;

UPDATE chercheurs_expertise e 
INNER JOIN chercheurs_chercheur c ON c.expertise = e.id
SET e.chercheur_id = c.id;

ALTER TABLE chercheurs_chercheur DROP COLUMN expertise;
