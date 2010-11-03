ALTER TABLE chercheurs_chercheur CHANGE COLUMN url_facebook url_reseau_social varchar(255);
ALTER TABLE chercheurs_chercheur DROP COLUMN url_linkedin;
