ALTER TABLE savoirs_record ADD FULLTEXT INDEX title_index (title);
ALTER TABLE savoirs_record ADD FULLTEXT INDEX alt_title_index (alt_title);
ALTER TABLE savoirs_record ADD FULLTEXT INDEX creator_index (creator);
ALTER TABLE savoirs_record ADD FULLTEXT INDEX contributor_index (contributor);
ALTER TABLE savoirs_record ADD FULLTEXT INDEX description_index (description);
ALTER TABLE savoirs_record ADD FULLTEXT INDEX abstract_index (abstract);
ALTER TABLE savoirs_record ADD FULLTEXT INDEX subject_index (subject);
