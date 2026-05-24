--
-- Homework 5: SQL-DDL
-- @author: <Tyler Vander Mooren>, <tjv55>
-- NAU, CS 345, Fall 2025
--

--
-- Output 1: start fresh
-- ---------------------
-- Delete the database if it exists still, show that it doesnt.
-- AI PROMPT: none used
DROP DATABASE IF EXISTS airline_DB;
SHOW DATABASES;

--
-- Output 2: initialization
-- ------------------------
-- Create the database if it doesnt exist, make sure to switch to it, then show that it exists.
-- AI PROMPT: none used
CREATE DATABASE IF NOT EXISTS airline_DB;
USE airline_DB;
SHOW DATABASES;
--
-- Output 3: inspect the database
-- ---------------------------
-- Show all tables from airline_DB.
-- AI PROMPT: NONE USED
SHOW TABLES;

--
-- Output 4: the Pilot table
-- -------------------------
-- Start filling the database, CREATE pilot table first, then show contents of Pilot.
-- AI PROMPT: None used.
CREATE TABLE Pilot(
identification INT PRIMARY KEY,
pilot_name VARCHAR(100) NOT NULL,
salary DECIMAL(10,2) NULL,
gratification decimal(10,2) NULL,
airline_name VARCHAR(30) NULL,
airline_address VARCHAR(255) NULL,
country VARCHAR(15) NULL
);
DESCRIBE PILOT;
--
-- Output 5: the Airport table
-- ---------------------------
-- CREATE airport table then show contents of airport.
-- AI PROMPT: none used.
CREATE TABLE Airport(
acronym VARCHAR(3) PRIMARY KEY,
airport_name VARCHAR(100) NOT NULL,
city VARCHAR(50) NULL,
country VARCHAR(15) NULL
);
DESCRIBE Airport;
--
-- Output 6: the Flight table
-- --------------------------
-- CREATE flight table then shwo contents of flight
-- AI PROMPT: none used.
CREATE TABLE Flight(
flight_number VARCHAR(6) PRIMARY KEY,
departure_airport VARCHAR(3) NOT NULL,
destination_airport VARCHAR(3) NOT NULL,
departure_time TIME NULL,
FOREIGN KEY (departure_airport) REFERENCES Airport(acronym),
FOREIGN KEY (destination_airport) REFERENCES Airport(acronym)
);
DESCRIBE Flight;
--
-- Output 7: the Connect table
-- ---------------------------
-- CREATE connect table then show contents of connect
-- AI PROMPT: none used.
CREATE TABLE Connect(
flight_number VARCHAR(6) NOT NULL,
flight_date DATE NOT NULL,
aircarft VARCHAR(30) NULL,
PRIMARY KEY(flight_number, flight_date)
);
DESCRIBE Connect;
--
-- Output 8: check the work so far
-- -------------------------------
-- Display all tables in database airline_DB, then display contents of each table.
-- AI PROMPT: none used;
SHOW TABLES;

--
-- Output 9: change Connect
-- ------------------------
-- ALTER table, Add pilot_identification to Connect Table, then list its contents
-- AI PROMPT: None used.
ALTER TABLE Connect ADD pilot_identification VARCHAR(10) NOT NULL;
DESCRIBE Connect;
-- 
-- Output 10: change Connect
-- -------------------------
-- Change the name of field pilot_identification to pilot_id and then list the contents of Connect.
-- AI PROMPT: how to rename a Table field in SQL
ALTER TABLE Connect CHANGE pilot_identification pilot_id VARCHAR(10) NOT NULL;
DESCRIBE Connect;
--
-- Output 11: change Connect
-- -------------------------
-- ALTER table field pilot_id to change type from VARCHAR to int, then display contents of Connect
-- AI PROMT: None used
ALTER TABLE Connect MODIFY pilot_id INT NOT NULL;
DESCRIBE Connect;

--
-- Output 12: change Connect
-- -------------------------
-- Alter table field pilot_id to be a Foreign key that refences pilot id from Pilot(identification)
-- AI PROMPT: NONE USED
ALTER TABLE Connect ADD CONSTRAINT FOREIGN KEY (pilot_id) references Pilot(identification);
DESCRIBE Connect;
--
-- Output 13: change Pilot
-- ----------------------------
-- Alter table to drop the field airline_address, then display its contents
-- AI PROMPT: None used.
ALTER TABLE Pilot DROP COLUMN airline_address;
DESCRIBE Pilot;


--
-- Output 14: change Connect
-- -------------------------
-- Rename the table Connect to stopover. Then list the tables in database airline_db
-- AI PROMT: how to change name of table in SQL
RENAME TABLE Connect TO Stopover;
SHOW TABLES;

--
-- Output 15: clean up
-- -------------------
-- Delete all the tables in airline_db, then display contents of airline_db. Remove Foreign Keys first, then drop tables from database. Then display airline_db.
-- AI Prompt: None used.
ALTER TABLE stopover DROP FOREIGN KEY stopover_ibfk_1;
ALTER TABLE Flight DROP FOREIGN KEY flight_ibfk_1;
ALTER TABLE Flight DROP FOREIGN KEY flight_ibfk_2;
DROP TABLE IF EXISTS Stopover;
DROP TABLE IF EXISTS Flight;
DROP TABLE IF EXISTS Airport;
DROP TABLE IF EXISTS Pilot;
SHOW TABLES;
--
-- Output 16: clean up
-- -------------------
-- Delete the database airline_db then display, confirming its removed.
-- AI PROMT: none used.
DROP DATABASE IF EXISTS airline_DB;
SHOW DATABASES;

--
-- end script
-- 