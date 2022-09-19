CREATE SCHEMA IF NOT EXISTS `premiereleague`
COLLATE utf8mb4_unicode_ci;
USE `premiereleague`;


CREATE TABLE IF NOT EXISTS Stadium(
`Name` VARCHAR(50) NOT NULL PRIMARY KEY,
Area VARCHAR(200) NOT NULL,
City VARCHAR(70) NOT NULL,
PostCode VARCHAR(8) NOT NULL,
BuildingDate CHAR(4) NOT NULL,
Capacity INT NOT NULL,
RecordLeagueAttendance INT,
LengthMeter DECIMAL(5,2) NOT NULL,
WidthMeter DECIMAL(5,2) NOT NULL
);


CREATE TABLE IF NOT EXISTS Club(
`Name` VARCHAR(30) NOT NULL PRIMARY KEY,
Website VARCHAR(200) NOT NULL UNIQUE,
StadiumName VARCHAR(50) NOT NULL,
FOREIGN KEY (StadiumName) REFERENCES Stadium(Name)
ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS `User`(
Email VARCHAR(256) NOT NULL PRIMARY KEY,	
UserName VARCHAR(30) NOT NULL,
`Password` VARCHAR(25) BINARY NOT NULL, -- binary makes it case sensitive
BirthDate DATE, 
Gender CHAR(1),
-- User can refuse to enter his Birthdate and/or gender
FavoriteClubName VARCHAR(30) NOT NULL,
FOREIGN KEY (FavoriteClubName) REFERENCES Club(`Name`)
ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE IF NOT EXISTS Player(
ID VARCHAR(6) NOT NULL PRIMARY KEY,
FullName VARCHAR(60) NOT NULL,
Nationaility VARCHAR(30),
Position VARCHAR(15) NOT NULL,
BirthDate DATE,  
Height varchar(3),
Weight varchar(3)
);


CREATE TABLE IF NOT EXISTS `Match`( -- I assume we only need to scrab mathces already played so I mark all features as NOT NUL
Season CHAR(7) NOT NULL,
-- the season would be like "2020/21" so always 7 characters
HomeTeamName VARCHAR(30) NOT NULL,
AwayTeamName VARCHAR(30) NOT NULL,
`Date` DATE NOT NULL,
HomePossession DECIMAL(3, 1) NOT NULL,
-- AwayPossession can be deduced from 100-HomePossession
HomeYellowCards INT NOT NULL,
HomeRedCards INT NOT NULL,
HomeFouls INT NOT NULL,
HomeShots INT NOT NULL,
HomeGoals INT NOT NULL,
AwayYellowCards INT NOT NULL,
AwayRedCards INT NOT NULL,
AwayFouls INT NOT NULL,
AwayShots INT NOT NULL,
AwayGoals INT NOT NULL,
StadiumName VARCHAR(50) NOT NULL,
PRIMARY KEY(Season, HomeTeamName, AwayTeamName),
FOREIGN KEY (HomeTeamName) REFERENCES Club(`Name`)
ON UPDATE CASCADE ON DELETE RESTRICT,
FOREIGN KEY (AwayTeamName) REFERENCES Club(`Name`)
ON UPDATE CASCADE ON DELETE RESTRICT,
FOREIGN KEY (StadiumName) REFERENCES Stadium(`Name`)
ON UPDATE CASCADE ON DELETE RESTRICT
);



CREATE TABLE IF NOT EXISTS PlayersInClubs(
PlayerID VARCHAR(6) NOT NULL,
Season CHAR(7) NOT NULL,
ClubName VARCHAR(30) NOT NULL,
PRIMARY KEY (PlayerID, Season, ClubName),
FOREIGN KEY (ClubName) REFERENCES Club(`Name`)
ON UPDATE CASCADE ON DELETE RESTRICT,
FOREIGN KEY (PlayerID) REFERENCES Player(`ID`)
ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS MatchsReviews(
UserEmail VARCHAR(256) NOT NULL,
Season CHAR(7) NOT NULL,
HomeTeamName VARCHAR(30) NOT NULL,
AwayTeamName VARCHAR(30) NOT NULL,
Rating Decimal(2, 1) NOT NULL CHECK(Rating>=1 AND Rating<=10),
TextReview VARCHAR(1000),
PRIMARY KEY(UserEmail, Season,HomeTeamName, AwayTeamName),
FOREIGN KEY(UserEmail) REFERENCES `User`(Email)
ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY(Season, HomeTeamName, AwayTeamName) REFERENCES `Match`(Season, HomeTeamName, AwayTeamName)
ON UPDATE CASCADE ON DELETE RESTRICT
);


