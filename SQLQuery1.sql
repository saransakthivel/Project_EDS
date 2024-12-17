--select * from sys.databases;
--create database CASeds;
use PSGedsData;

--CREATE TABLE EDSdata(
--	id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
--	d_name VARCHAR(100),
--	d_value FLOAT,
--	date_time DATETIME,
--	date DATE,
--	time TIME
--);

--CREATE TABLE TechData(
--	id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
--	d_name VARCHAR(100),
--	d_value FLOAT,
--	date_time DATETIME,
--	date DATE,
--	time TIME
--);

--DROP TABLE IF EXISTS Techdata;

--ALTER TABLE EDSdata
--ADD date DATE, time TIME;

--SELECT *FROM CasData
--WHERE d_name = 'F-01 EB Incomer.API'
--ORDER BY date_time DESC;

SELECT * FROM TechData;

--SELECT *FROM CasData
--WHERE date_time >= '2024-12-14 12:11:30.000'
--ORDER BY date_time DESC;

--SELECT * FROM CasData  ORDER BY date_time DESC;
