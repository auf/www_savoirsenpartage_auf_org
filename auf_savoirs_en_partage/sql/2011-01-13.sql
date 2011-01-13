CREATE TABLE `south_migrationhistory` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `app_name` varchar(255) NOT NULL,
    `migration` varchar(255) NOT NULL,
    `applied` datetime NOT NULL
);

INSERT INTO south_migrationhistory (app_name, migration, applied)
VALUES ('savoirs', '0001_initial', '2011-01-12 00:00:00'),
       ('sitotheque', '0001_initial', '2011-01-12 00:00:00'),
       ('chercheurs', '0001_initial', '2011-01-12 00:00:00');
