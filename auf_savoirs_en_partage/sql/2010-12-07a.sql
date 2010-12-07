-- Corriger des url mal formées

UPDATE chercheurs_publication SET url = CONCAT('http://', url)
WHERE LENGTH(url) > 0 AND url NOT LIKE 'http://%';
UPDATE chercheurs_these SET url = CONCAT('http://', url)
WHERE LENGTH(url) > 0 AND url NOT LIKE 'http://%';
