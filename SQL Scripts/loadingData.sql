LOAD DATA INFILE "X:\\Aspring 2022\\Database\\project\\MS2\\submission\\CSV Files\\stadiumsTable.csv" INTO TABLE Stadium
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(`Name`,Area,City,PostCode,BuildingDate,Capacity,@record,LengthMeter,WidthMeter)
SET RecordLeagueAttendance = NULLIF(@record, ''); 

LOAD DATA INFILE "X:\\Aspring 2022\\Database\\project\\MS2\\submission\\CSV Files\\clubsTable.csv" INTO TABLE Club
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA INFILE "X:\\Aspring 2022\\Database\\project\\MS2\\submission\\CSV Files\\playersTable.csv" INTO TABLE Player
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(ID,FullName,@nation,Position,@Bdate,@height,@weight)
SET
Nationaility = NULLIF(@nation, ''),
BirthDate = STR_TO_DATE(@Bdate,'%d/%m/%Y'),
Height = NULLIF(@height, ''),
Weight = NULLIF(@weight, '');

LOAD DATA INFILE "X:\\Aspring 2022\\Database\\project\\MS2\\submission\\CSV Files\\playersInClubsTable.csv" INTO TABLE PlayersInClubs
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA INFILE "X:\\Aspring 2022\\Database\\project\\MS2\\submission\\CSV Files\\matchesTableDateAdjusted.csv" INTO TABLE `Match`
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

INSERT INTO `User`
VALUES('amer.elsheikh@aucegypt.edu','amer','EPL_Pass', '2001-06-28','M', 'Liverpool');

INSERT INTO MatchsReviews
VALUES('amer.elsheikh@aucegypt.edu', '2021/22', 'Manchester City', 'Liverpool', 9.5, 'Very Exciting Till Last Moment.')

