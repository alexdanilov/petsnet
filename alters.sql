ALTER TABLE  `catalog_clinics` ADD  `working_hours_saturday` VARCHAR( 255 ) NULL AFTER  `working_hours`;
ALTER TABLE  `catalog_clinics` ADD  `working_hours_sanday` VARCHAR( 30 ) NULL AFTER  `working_hours_saturday`;

ALTER TABLE  `catalog_pharmacies` ADD  `working_hours_saturday` VARCHAR( 255 ) NULL AFTER  `working_hours`;
ALTER TABLE  `catalog_pharmacies` ADD  `working_hours_sanday` VARCHAR( 30 ) NULL AFTER  `working_hours_saturday`;

ALTER TABLE  `catalog_clinics` ADD  `is_top` BOOLEAN NULL AFTER  `working_hours_sanday` ,
ADD  `is_sale` BOOLEAN NULL AFTER  `is_top`;

ALTER TABLE  `catalog_pharmacies` ADD  `is_top` BOOLEAN NULL AFTER  `working_hours_sanday` ,
ADD  `is_sale` BOOLEAN NULL AFTER  `is_top`;

ALTER TABLE  `catalog_nurseries` ADD  `is_top` BOOLEAN NULL AFTER  `description` ,
ADD  `is_sale` BOOLEAN NULL AFTER  `is_top`;


ALTER TABLE  `catalog_exhibitions` CHANGE  `description`  `about` VARCHAR( 1000 ) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;
ALTER TABLE  `catalog_exhibitions` ADD  `program` TEXT NULL AFTER  `experts`;

ALTER TABLE  `catalog_clinics` CHANGE  `description`  `about` VARCHAR( 1000 ) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;
ALTER TABLE  `catalog_clinics` ADD  `coworkers` TEXT NULL AFTER  `prices`;
ALTER TABLE  `catalog_clinics` CHANGE  `coworkers`  `coworkers` TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;