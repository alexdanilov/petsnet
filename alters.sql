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



RENAME TABLE  `petsnet_ua`.`catalog_clinics` TO  `petsnet_ua`.`clinics` ;
RENAME TABLE  `petsnet_ua`.`catalog_clinics_services` TO  `petsnet_ua`.`clinics_services` ;
RENAME TABLE  `petsnet_ua`.`catalog_clinic_services` TO  `petsnet_ua`.`clinic_services` ;


DROP TABLE `catalog_clubs`, `catalog_clubs_members`, `catalog_events`, `catalog_meetings`, `catalog_meetings_members`;
RENAME TABLE  `petsnet_ua`.`catalog_exhibitions` TO  `petsnet_ua`.`exhibitions` ;
RENAME TABLE  `petsnet_ua`.`catalog_news` TO  `petsnet_ua`.`news` ;
RENAME TABLE  `petsnet_ua`.`catalog_nurseries` TO  `petsnet_ua`.`nurseries` ;
RENAME TABLE  `petsnet_ua`.`catalog_nurseries_breeds` TO  `petsnet_ua`.`nurseries_breeds` ;
RENAME TABLE  `petsnet_ua`.`catalog_nurseries_images` TO  `petsnet_ua`.`nurseries_images` ;
RENAME TABLE  `petsnet_ua`.`catalog_nurseries_services` TO  `petsnet_ua`.`nurseries_services` ;
RENAME TABLE  `petsnet_ua`.`catalog_nursery_services` TO  `petsnet_ua`.`nursery_services` ;
RENAME TABLE  `petsnet_ua`.`catalog_pharmacies` TO  `petsnet_ua`.`pharmacies` ;
DROP TABLE  `catalog_services`;

