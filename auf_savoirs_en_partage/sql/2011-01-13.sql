CREATE TABLE `south_migrationhistory` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `app_name` varchar(255) NOT NULL,
    `migration` varchar(255) NOT NULL,
    `applied` datetime NOT NULL
);

