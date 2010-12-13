-- Certains chercheurs ont des espaces dans leur adresse courriel...

UPDATE chercheurs_personne SET courriel = REPLACE(courriel, ' ', '');

-- On crée des users Django pour chaque chercheur et on change l'objet
-- "personne" en profil Django

ALTER TABLE auth_user ADD INDEX email (email);

INSERT INTO auth_user (username, first_name, last_name, email, password, is_staff, is_active, is_superuser)
SELECT REPLACE(REPLACE(LEFT(courriel, LOCATE('@', courriel) - 1), '-', '_'), '.', '_'), prenom, nom, courriel, password, 0, 1, 0
FROM chercheurs_personne
WHERE actif AND courriel NOT IN (SELECT email FROM auth_user)
GROUP BY LEFT(courriel, LOCATE('@', courriel) - 1)
HAVING COUNT(*) = 1;

INSERT INTO auth_user (username, first_name, last_name, email, password, is_staff, is_active, is_superuser)
SELECT CONCAT(REPLACE(REPLACE(LEFT(courriel, LOCATE('@', courriel) - 1), '-', '_'), '.', '_'), '_', id), prenom, nom, courriel, password, 0, 1, 0
FROM chercheurs_personne
WHERE actif AND courriel NOT IN (SELECT email FROM auth_user);

ALTER TABLE chercheurs_personne ADD COLUMN `user_id` integer;

UPDATE chercheurs_personne p INNER JOIN auth_user u ON u.email = p.courriel
SET p.user_id = u.id
WHERE p.actif;

ALTER TABLE chercheurs_personne DROP COLUMN password;

-- On a viré le CascadeBackend, alors on doit virer toutes les sessions, car le
-- backend d'authentification est stocké dans la session.

TRUNCATE django_session;
