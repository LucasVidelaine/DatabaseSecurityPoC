-- Creation de la base de données --
CREATE DATABASE IF NOT EXISTS `TP2022_VIDELAINE-LUBISHTANI-BIZET`;

-- Création d'un user à notre nom et attribution de tout les privilèges--
USE `TP2022_VIDELAINE-LUBISHTANI-BIZET`;
CREATE USER IF NOT EXISTS 'lulutoto'@'%' IDENTIFIED BY 'Ensibs2022!';
GRANT ALL PRIVILEGES ON *.* to 'lulutoto'@'%';

-- Création de la table des ages --
USE `TP2022_VIDELAINE-LUBISHTANI-BIZET`;
DROP TABLE IF EXISTS age;
CREATE TABLE age
(
    nom VARCHAR(30),
    ORE_age int,
    HOM_age VARCHAR(2000)
);
GO

-- Insertion des valeurs automatiquement --
INSERT INTO age (nom, ORE_age, HOM_age)
VALUES 
-- ANSSI RECOMMANDATIONS FOR PASSWORD ageDefaut = 20 for all--
('VIDELAINE','1709961','{"public_key": 2161831391, "ciphertext": "2144252966386228984", "exponent": 0}'),
('LUBISHTANI-BIZET','1709961','{"public_key": 2161831391, "ciphertext": "2144252966386228984", "exponent": 0}'),
('BLOCH','1709961','{"public_key": 2161831391, "ciphertext": "2144252966386228984", "exponent": 0}'),
('NEYRA','1709961','{"public_key": 2161831391, "ciphertext": "2144252966386228984", "exponent": 0}'),
('HUYGHE','1709961','{"public_key": 2161831391, "ciphertext": "2144252966386228984", "exponent": 0}'),
('KINIE','1709961','{"public_key": 2161831391, "ciphertext": "2144252966386228984", "exponent": 0}'),
('DALLOYAU','1709961','{"public_key": 2161831391, "ciphertext": "2144252966386228984", "exponent": 0}');
GO

