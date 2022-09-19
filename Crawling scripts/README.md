## Scarpers
The scraping process happens through the crawling scipt in this directory, and it proceeds as follows:
- ClubsWithStadiumLinksScrapper is used to get [clubsTables](https://github.com/QEDady/Premier-League-Database-Project/blob/master/CSV%20Files/clubsTable.csv) along with [stadiumLinks](https://github.com/QEDady/Premier-League-Database-Project/blob/master/CSV%20Files/stadiumsLinks.csv).
- Then, StadiumsScrapper uses stadiumLinks to get [stadumsTable](https://github.com/QEDady/Premier-League-Database-Project/blob/master/CSV%20Files/stadiumsTable.csv).
- Then, playerInClubsScrapper generates [playersInClubsTable](https://github.com/QEDady/Premier-League-Database-Project/blob/master/CSV%20Files/playersInClubsTable.csv) and [playerLinks](https://github.com/QEDady/Premier-League-Database-Project/blob/master/CSV%20Files/playerLinks.csv).
- Then, PlayersScrapper uses playerLinks to generate [playersTable](https://github.com/QEDady/Premier-League-Database-Project/blob/master/CSV%20Files/playersTable.csv).
- Lastly, MatchesScrapper generates all matches data in [matchesTable](https://github.com/QEDady/Premier-League-Database-Project/blob/master/CSV%20Files/matchesTable.csv).
