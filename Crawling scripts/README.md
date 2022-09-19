## Scarpers
The scraping process happens through the crawling scipt in this directory, and it proceeds as follows:
- ClubsWithStadiumLinksScrapper is used to get [clubsTables.]() along with [stadiumLinks]()
- Then, StadiumsScrapper uses stadiumLinks to get [stadumsTable]()
- Then, playerInClubsScrapper generates [playersInClubsTable]() and [playerLinks]()
- Then, PlayersScrapper uses [playerLinks]() to generate [playersTable]()
- Lastly, MatchesScrapper generates all matches data in [matchesTable]()