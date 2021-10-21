-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema belt
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema belt
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `belt` DEFAULT CHARACTER SET utf8 ;
USE `belt` ;

-- -----------------------------------------------------
-- Table `belt`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belt`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `password` VARCHAR(255) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `belt`.`thoughts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belt`.`thoughts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(45) NULL,
  `users_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_thoughts_users_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_thoughts_users`
    FOREIGN KEY (`users_id`)
    REFERENCES `belt`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `belt`.`likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belt`.`likes` (
  `users_id` INT NOT NULL,
  `thoughts_id` INT NOT NULL,
  INDEX `fk_users_has_thoughts_thoughts1_idx` (`thoughts_id` ASC) VISIBLE,
  INDEX `fk_users_has_thoughts_users1_idx` (`users_id` ASC) VISIBLE,
  PRIMARY KEY (`thoughts_id`, `users_id`),
  CONSTRAINT `fk_users_has_thoughts_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `belt`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_thoughts_thoughts1`
    FOREIGN KEY (`thoughts_id`)
    REFERENCES `belt`.`thoughts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
