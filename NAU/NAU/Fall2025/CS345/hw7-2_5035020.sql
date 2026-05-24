--
-- Homework 7-2: SQL-DML
-- @author: Tyler Vander Mooren, tjv55
-- NAU, CS 345
--

--
-- DDL Statements
-- --------------
-- IMPORTANT NOTE: use the following DDL statements to create your initial 
-- database.

-- drop the database
DROP DATABASE IF EXISTS airline_db;
-- create the database
CREATE DATABASE IF NOT EXISTS airline_db;
-- select airline_db as the context
USE airline_db;
-- create the table Pilot
CREATE TABLE Pilot (
    identification INT PRIMARY KEY NOT NULL,
    pilot_name VARCHAR(100) NOT NULL,
    salary DECIMAL(10, 2),
    gratification DECIMAL(10, 2),
    airline_name VARCHAR(30),
    country VARCHAR(15)
);
-- create the table Airport
CREATE TABLE Airport(acronym VARCHAR(3) PRIMARY KEY NOT NULL,
                    airport_name VARCHAR(100) NOT NULL,
                    city VARCHAR(50),
                    country VARCHAR(15));
-- create the table Flight
CREATE TABLE Flight(flight_number VARCHAR(6) PRIMARY KEY NOT NULL,
                    departure_airport VARCHAR(3) NOT NULL,
                    destination_airport VARCHAR(3) NOT NULL,
                    departure_time TIME,
                    FOREIGN KEY (departure_airport) REFERENCES 
						Airport(acronym) ON DELETE CASCADE,
                    FOREIGN KEY (destination_airport) REFERENCES 
						Airport(acronym) ON DELETE CASCADE);
-- create the table Stopover
CREATE TABLE Stopover(flight_number VARCHAR(6) NOT NULL,
                    flight_date DATE NOT NULL,
                    pilot_id INT NOT NULL,
                    aircraft VARCHAR(30),
                    PRIMARY KEY(flight_number, flight_date),
                    FOREIGN KEY (flight_number) REFERENCES 
						Flight(flight_number) ON DELETE CASCADE,
                    FOREIGN KEY (pilot_id) REFERENCES Pilot(identification) ON 
						DELETE CASCADE
);

--
-- DML Statements
-- --------------
-- IMPORTANT NOTE: use the following DML statements to populate your initial
-- database.

insert into Pilot values
	(279, "Steven Grant Rogers", 30000.00, 500.00, "American Airlines", "USA"),
    (627, "Wanda Maximoff", 30000.00, 500.00, "American Airlines", "USA"),
    (947, "Natasha Romanoff", 25000.00, 800.00, "United", "USA"),
    (463, "Anthony Edward Stark", 20000.00, 800.00, "United", "USA"),
    (839, "Robert Bruce Banner", 35000.00, 500.00, "American Airlines", "USA"),
    (628, "Carol Susan Jane Danvers", 30000.00, 500.00, "Air France", "France"),
    (832, "Clinton Francis Barton", 20000.00, 800.00, "Air Canada", "Canada"),
    (602, "Stephen Vincent Strange", 25000.00, 800.00, "Air Canada", "Canada"),
    (633, "Victor Shade", 28000.00, 600.00, "Air France", "France"),
    (382, "Jessica Jones", 35000.00, 700.00, "Japan Airlines", "Japan"),
    (489, "Clark Joseph Kent", 29000.00, 500.00, "American Airlines", "USA"),
    (847, "Oliver Jonas Queen", 32000.00, 400.00, "Air Canada", "Canada"),
    (932, "Wade Winston Wilson", 35000.00, 200.00, "Air France", "France"),
    (887, "Stephen Vincent Strange", 29000.00, 500.00, "Japan Airlines", "Japan");

insert into Airport values
    ("LAS", "Harry Reid International Airport", "Las Vegas", "USA"),
    ("PHX", "Phoenix Sky Harbor Airport", "Phoenix", "USA"),
    ("DFW", "Dallas Fort Worth Airport", "Dallas", "USA"),
    ("IAH", "George Bush Intercontinental Airport", "Houston", "USA"),
    ("LAX", "Los Angeles International Airport", "Los Angeles", "USA"),
    ("GRU", "Guarulhos International Airport", "Guarulhos", "Brazil"),
    ("BSB", "Presidente Juscelino Kubitschek International Airport", "Brasilia",
		"Brazil"),
    ("MAO", "Eduardo Gomes International Airport", "Manaus", "Brazil"),
    ("CDG", "Aéroport Paris-Charles de Gaulle", "Paris", "France"),
    ("LYS", "Aéroport Lyon Saint-Exupéry", "Lyon", "France"),
    ("MRS", "Marseille Provence Airport", "Marselha", "France");

insert into Flight values
    ("RG230", "LAX", "PHX", "23:05"),
    ("PR231", "IAH", "LAS", "12:15"),
    ("TG331", "DFW", "LAX", "17:22"),
    ("AV431", "PHX", "GRU", "02:10"),
    ("KI356", "IAH", "MAO", "23:55"),
    ("OD468", "BSB", "LAX", "11:45"),
    ("PS324", "PHX", "GRU", "22:19"),
    ("OO677", "GRU", "DFW", "18:52"),
    ("TW873", "GRU", "LYS", "18:52"),
    ("IE832", "LYS", "MRS", "04:40"),
    ("JD646", "CDG", "LYS", "05:00"),
    ("MD342", "CDG", "BSB", "08:34"),
    ("UJ658", "LAS", "IAH", "08:34"),
    ("GF774", "LAS", "DFW", "08:34");

insert into Stopover values
    ("RG230", "2022-12-30", 279, "Boeing 747"),
    ("RG230", "2022-09-24", 628, "Boeing 747"),
    ("PR231", "2022-08-15", 279, "Airbus A380"),
    ("PR231", "2022-01-12", 947, "Airbus A380"),
    ("TG331", "2022-02-05", 947, "Boeing 747"),
    ("TG331", "2022-01-12", 627, "Airbus A380"),
    ("AV431", "2022-12-04", 463, "Embraer 195"),
    ("AV431", "2022-10-30", 839, "Airbus A380"),
    ("KI356", "2022-09-07", 463, "Embraer 195"),
    ("KI356", "2022-08-13", 463, "Embraer 175"),
    ("OD468", "2022-03-13", 839, "Airbus A330"),
    ("OD468", "2022-04-01", 839, "Airbus A330"),
    ("OD468", "2022-04-02", 839, "Airbus A330"),
    ("PS324", "2022-03-15", 627, "Airbus A320"),
    ("PS324", "2022-03-18", 627, "Embraer 195"),
    ("OO677", "2022-02-09", 832, "Embraer 195"),
    ("OO677", "2022-02-01", 832, "Boeing 797"),
    ("TW873", "2022-12-11", 602, "Boeing 797"),
    ("TW873", "2022-11-17", 633, "Boeing 797"),
    ("IE832", "2022-05-17", 633, "Embraer 195"),
    ("IE832", "2022-08-16", 602, "Embraer 175"),
    ("JD646", "2022-09-27", 602, "Embraer 175"),
    ("JD646", "2022-09-29", 832, "Airbus A320"),
    ("MD342", "2022-09-29", 382, "Airbus A320"),
    ("MD342", "2022-10-31", 382, "Airbus A330"),
    ("UJ658", "2022-03-30", 633, "Boeing 797"),
    ("UJ658", "2022-02-25", 279, "Boeing 797"),
    ("GF774", "2022-01-22", 602, "Boeing 747"),
    ("GF774", "2022-01-12", 633, "Boeing 747");

--
-- end script
-- 
--
-- DML Statements
-- --------------
-- 

-- IMPORTANT NOTE: add the DML statements here. After Homework 6 deadline has 
-- passed, the statements to be added here will be provided on Canvas (same
-- script used in hw7-1).


--
-- DQL Statements
-- --------------

--
-- Output 1: pilot's total income (salary + gratification) for pilots with
-- flight date before 2022-11-14
-- -----------------------------------------------------------------------
-- AI PROMPT: None used.
SELECT DISTINCT identification, pilot_name, (pilot.salary + pilot.gratification) as "(p.salary + p.gratification)" FROM Pilot 
JOIN Stopover ON identification = pilot_id
WHERE flight_date < '2022-11-14';


--
-- Output 2: airport info for flight RG230
-- ---------------------------------------
-- AI PROMPT: None used.
SELECT DISTINCT city, country FROM Flight 
JOIN Airport ON destination_airport = acronym
WHERE flight_number = 'RG230';

--
-- Output 3: airlines of pilots who flew on 2022-01-12
-- ---------------------------------------------------
-- AI PROMPT: None used.
SELECT DISTINCT airline_name FROM Pilot 
JOIN Stopover ON identification = pilot_id
WHERE flight_date = '2022-01-12';

--
-- Output 4: detailed stopover information
-- ---------------------------------------
-- AI PROMPT: None used.
SELECT DISTINCT flight_number, pilot_name, aircraft, airline_name FROM Stopover
JOIN Pilot ON pilot_id = identification
ORDER BY flight_number, aircraft;

--
-- Output 5: detailed stopover information for airlines with pilots from
-- outside the USA
-- ---------------------------------------------------------------------
-- AI PROMPT: None used.
SELECT DISTINCT 
    Stopover.flight_number,
    Flight.departure_time,
    Pilot.pilot_name,
    Stopover.aircraft,
    Pilot.airline_name
FROM Stopover
JOIN Pilot ON Stopover.pilot_id = Pilot.identification
JOIN Flight ON Stopover.flight_number = Flight.flight_number
WHERE Pilot.country <> 'USA'
ORDER BY Stopover.flight_number;

--
-- Output 6: pilot's name with flight information, if any
-- ------------------------------------------------------
-- AI PROMPT: None used.
SELECT DISTINCT
    Pilot.pilot_name,
    Stopover.flight_number,
    Stopover.flight_date
FROM Pilot
LEFT JOIN Stopover 
    ON Pilot.identification = Stopover.pilot_id;


--
-- Output 7: flights that departure in the morning (0-11) OR in January
-- (month 01)
-- --------------------------------------------------------------------
-- AI PROMPT: SQL statement for MySQL where hour is 0-11(morning) or in month(january)
SELECT DISTINCT Flight.flight_number FROM Flight
JOIN Stopover ON Flight.flight_number = Stopover.flight_number
WHERE HOUR(Flight.departure_time) BETWEEN 0 AND 11
OR MONTH(Stopover.flight_date) = 1;

--
-- Output 8: Canadian pilots who have flown three or more flights in
-- order of salary
-- ------------------------------------------------------------------
-- AI PROMPT: None used.
SELECT 
    Pilot.pilot_name,
    COUNT(Stopover.flight_number) AS total_flights,
    avg(Pilot.salary) AS avg_salary
FROM Pilot
JOIN Stopover 
    ON Pilot.identification = Stopover.pilot_id
WHERE Pilot.country = 'Canada'
GROUP BY Pilot.identification
HAVING COUNT(Stopover.flight_number) >= 3
ORDER BY Pilot.salary DESC;
-- ------------------------------------------------------
-- THE FOLLOWING STATEMENTS REQUIRE AT LEAST ONE SUBQUERY 
-- ------------------------------------------------------

--
-- Output 9: flight information for flights to Brazil or France
-- ------------------------------------------------------------
-- AI Prompt: MySQL query using one subquery to display each flight_number, country, departure_time and flight_date for flights to Brazil or France.
SELECT 
    flight.flight_number,
    airport.country,
    flight.departure_time,
    stopover.flight_date
FROM Flight AS flight
JOIN Airport AS airport 
    ON flight.destination_airport = airport.acronym
JOIN Stopover AS stopover 
    ON flight.flight_number = stopover.flight_number
WHERE flight.destination_airport IN (
    SELECT acronym 
    FROM Airport 
    WHERE country IN ('Brazil', 'France')
);

--
-- Output 10: pilot information for pilots in Wanda Maximoff's
-- airline
-- -----------------------------------------------------------
-- AI PROMPT: None used.
SELECT pilot_name, airline_name FROM Pilot
WHERE airline_name = (
    SELECT airline_name FROM Pilot
    WHERE pilot_name = 'Wanda Maximoff'
);

--
-- Output 11: airlines that have France as destination
-- ---------------------------------------------------
-- AI PROMPT: None used.
SELECT DISTINCT 
    pilot.airline_name
FROM Pilot AS pilot
JOIN Stopover AS stopover 
    ON pilot.identification = stopover.pilot_id
WHERE stopover.flight_number IN (
    SELECT flight.flight_number
    FROM Flight AS flight
    JOIN Airport AS airport 
        ON flight.destination_airport = airport.acronym
    WHERE airport.country = 'France'
);

--
-- Output 12: American Airlines' destination airports
-- --------------------------------------------------
-- AI PROMPT: None used.
SELECT DISTINCT 
	flight.flight_number,
    airport.airport_name,
    airport.city,
    airport.country
FROM Airport AS airport
JOIN Flight AS flight 
    ON airport.acronym = flight.destination_airport
WHERE flight.flight_number IN (
    SELECT DISTINCT stopover.flight_number
    FROM Stopover AS stopover
    JOIN Pilot AS pilot 
        ON stopover.pilot_id = pilot.identification
    WHERE pilot.airline_name = 'American Airlines'
);


--
-- Output 13: destination of flights with more than two stopovers
-- --------------------------------------------------------------
-- AI PROMPT: None used.
SELECT DISTINCT
	airport.airport_name
FROM Airport AS airport
JOIN Flight AS flight 
    ON airport.acronym = flight.destination_airport
WHERE flight.flight_number IN (
    SELECT stopover.flight_number
    FROM Stopover AS stopover
    GROUP BY stopover.flight_number
    HAVING COUNT(*) > 2
);


--
-- Output 14: airports for flights on 2022-01-12
-- ---------------------------------------------
-- AI PROMT: use one subquery to list flight’s number with the full names of its departure and destination airports for flights on 2022-01-12.
SELECT DISTINCT
    flight.flight_number,
    dep.airport_name AS departure,
    dest.airport_name AS destination
FROM Flight AS flight
JOIN Airport AS dep 
    ON flight.departure_airport = dep.acronym
JOIN Airport AS dest 
    ON flight.destination_airport = dest.acronym
WHERE flight.flight_number IN (
    SELECT stopover.flight_number
    FROM Stopover AS stopover
    WHERE stopover.flight_date = '2022-01-12'
);
--
-- Output 15: destination of United-operated flights in Embraer
-- aircraft
-- ------------------------------------------------------------
-- AI PROMPT: None used.
SELECT DISTINCT
    flight.flight_number,
    dest.airport_name,
    dest.city
FROM Flight AS flight
JOIN Airport AS dest 
    ON flight.destination_airport = dest.acronym
WHERE flight.flight_number IN (
    SELECT stopover.flight_number
    FROM Stopover AS stopover
    JOIN Pilot AS pilot 
        ON stopover.pilot_id = pilot.identification
    WHERE pilot.airline_name = 'United'
      AND stopover.aircraft LIKE 'Embraer%'
);

--
-- Output 16: domestic flights
-- ---------------------------
-- AI PROMT: SQL statment with showing only domestic flights where two countries match.
SELECT DISTINCT
    flight.flight_number,
    flight.departure_time,
    departure.country AS departureCountry,
    destination.country AS destinationCountry
FROM Flight AS flight
JOIN Airport AS departure 
    ON flight.departure_airport = departure.acronym
JOIN Airport AS destination 
    ON flight.destination_airport = destination.acronym
WHERE departure.country = (
    SELECT airport.country
    FROM Airport AS airport
    WHERE airport.acronym = flight.destination_airport
)
ORDER BY flight.flight_number;
--
-- Output 17: airports where American Airlines operates
-- ----------------------------------------------------
-- AI PROMPT: None used.
SELECT DISTINCT 
    airport.airport_name
FROM Airport AS airport
JOIN Flight AS flight 
    ON airport.acronym IN (flight.departure_airport, flight.destination_airport)
WHERE flight.flight_number IN (
    SELECT stopover.flight_number
    FROM Stopover AS stopover
    JOIN Pilot AS pilot 
        ON stopover.pilot_id = pilot.identification
    WHERE pilot.airline_name = 'American Airlines'
);

--
-- Output 18: total income for pilots with the lowest gratification
-- ----------------------------------------------------------------
-- AI PROMPT: None used.
SELECT 
    identification,
    (salary + gratification) AS total_income
FROM Pilot
WHERE gratification = (
    SELECT MIN(gratification)
    FROM Pilot
);

--
-- Output 19: pilots who fly to their own country in Boing aircraft
-- ----------------------------------------------------------------
-- AI Prompt: MYSQL query to list identification and name of pilots AND flew 'boeing' aircraft to destinations located in their own country.
SELECT DISTINCT
    pilot.identification,
    pilot.pilot_name
FROM Pilot AS pilot
JOIN Stopover AS stopover 
    ON pilot.identification = stopover.pilot_id
JOIN Flight AS flight 
    ON stopover.flight_number = flight.flight_number
WHERE pilot.country = (
    SELECT destination_country.country
    FROM Airport AS destination_country
    WHERE destination_country.acronym = flight.destination_airport
)
AND stopover.aircraft LIKE 'Boeing%';

--
-- Output 20: international flights departing from the pilot's country
-- -------------------------------------------------------------------
-- AI prompt: using only one subquery international flights departing from the pilot’s country outputting only flight_number
SELECT DISTINCT
    flight.flight_number
FROM Flight AS flight
JOIN Stopover AS stopover 
    ON flight.flight_number = stopover.flight_number
JOIN Pilot AS pilot 
    ON stopover.pilot_id = pilot.identification
JOIN Airport AS departure 
    ON flight.departure_airport = departure.acronym
JOIN Airport AS destination 
    ON flight.destination_airport = destination.acronym
WHERE pilot.country = departure.country
AND destination.country <> (
      SELECT dep_sub.country
      FROM Airport AS dep_sub
      WHERE dep_sub.acronym = flight.departure_airport
  )
ORDER BY flight.flight_number;
--
-- Output 21:flight information for flights by American pilots with
-- greater salary than the average salaries of American pilots
-- -----------------------------------------------------------------
-- AI PROMPT: using one subquery flight information for flights by American pilots with greater salaries than the average salaries of American pilots
SELECT DISTINCT
    flight.flight_number,
    flight.departure_time,
    stopover.aircraft
FROM Flight AS flight
JOIN Stopover AS stopover 
    ON flight.flight_number = stopover.flight_number
JOIN Pilot AS pilot 
    ON stopover.pilot_id = pilot.identification
WHERE pilot.country = 'USA'
  AND pilot.salary > (
      SELECT AVG(p2.salary)
      FROM Pilot AS p2
      WHERE p2.country = 'USA'
  );

--
-- Output 22: salaries per airlines who have pilots who have not flown
-- -------------------------------------------------------------------
-- AI PROMPT: None used.
SELECT 
    pilot.airline_name,
    AVG(pilot.salary) AS 'AVG(salary)'
FROM Pilot AS pilot
WHERE pilot.airline_name IN (
    SELECT DISTINCT notflown.airline_name
    FROM Pilot AS notflown
    WHERE notflown.identification NOT IN (
        SELECT stopover.pilot_id
        FROM Stopover AS stopover
    )
)
GROUP BY pilot.airline_name;

--
-- Output 23: airlines with the highest salary average 
-- ---------------------------------------------------
-- AI PROMPT: MYSql query using one subquery to list Airlines with the highest salary average and return only the one with the highest
SELECT 
    pilot.airline_name,
    AVG(pilot.salary) AS average_salary
FROM Pilot AS pilot
GROUP BY pilot.airline_name
HAVING AVG(pilot.salary) = (
    SELECT MAX(avg_salary)
    FROM (
        SELECT AVG(p2.salary) AS avg_salary
        FROM Pilot AS p2
        GROUP BY p2.airline_name
    ) AS sub
);

--
-- end script
-- 