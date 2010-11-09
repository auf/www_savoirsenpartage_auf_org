-- Pièces jointes dans l'agenda

ALTER TABLE savoirs_evenement ADD COLUMN `piece_jointe` varchar(100) NOT NULL;

-- Les établissements codés 0 devraient être codés NULL

UPDATE chercheurs_chercheur SET etablissement = NULL WHERE etablissement = 0;
