# English Premier League Database Project
## Overview 
This repo includes my design and implemenation of the EPL project for the database course. The project allows the user to draw useful statistics and ask for meaningful queries on the English premiere league for the seasons 2018/19 to 2021/22. The inital Entity Relationship Diagram is uploaded in the EPL ERD file. The project helped me understand the whole relational database management system (RDBMS) development cycle.

## Data Scraping
The data was scraped frpm the offical [EPL](https://www.premierleague.com/) website using selenium. The scrappers used can be found inside [Crawling Scrips directory]() along with their descriptions. The data scraped can be found inside the [CSV files directory](). Also, the dumb file is provided [here]() for convenience. 

## Requirments
You must install the following dependencies if you want to compile the application or:
- mysql.connector (for connecting to the database)
- stdiomask (for password input)
- tabulate (for table printing)

## Running the program
The program is a simple CLI with plenty of options.you can just run the [executable]() to use the program. Notice that you must have an internet connection for the program to connect to the hosted database at [db4free](db4free.net).

One account you can use is amer.elsheikh@aucegypt.edu with password EPL_Pass (or you can simply create an account or use the guest mode)

