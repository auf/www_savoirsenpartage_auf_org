-- Par défaut, on veut que les questions oui/non du formulaire d'inscription
-- soient NULL

ALTER TABLE `chercheurs_chercheur` 
    MODIFY COLUMN `expert_oif` bool,
    MODIFY COLUMN `membre_association_francophone` bool,
    MODIFY COLUMN `membre_reseau_institutionnel` bool,
    MODIFY COLUMN `expertises_auf` bool;

-- Remettre les réponses des vieilles fiches à NULL.

UPDATE chercheurs_chercheur SET expertises_auf = NULL WHERE date_modification < '2010-12-09';
UPDATE chercheurs_chercheur 
SET expert_oif = NULL,
    membre_association_francophone = NULL, 
    membre_reseau_institutionnel = NULL 
WHERE date_modification < '2010-11-17';
