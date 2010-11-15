-- Suppression des personnes fantômes

DELETE p FROM chercheurs_personne p 
LEFT JOIN chercheurs_chercheur c ON c.personne = p.id 
WHERE c.id IS NULL;
