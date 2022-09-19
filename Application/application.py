import mysql.connector
import stdiomask
import re
from decimal import Decimal
from tabulate import tabulate
import os
import time

# Global Variables
try:
    db = mysql.connector.connect(
    host="sql11.db4free.net" ,
    user="qedady" ,
    password="sample_password",
    database="epl_amer"
    )
    cursor = db.cursor(buffered=True)
except:
    print("Something wrong happened while connecting to the database. Check your network and restart the program.")
    os.system('pause')
    exit()

guestMode = False
userEmail = ""
userName = ""
userFavoriteTeam = ""


def QueryTheDatabase(query):
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except:
        print("Something wrong happened while connecting to the database. Check your network and restart the program.")
        os.system('pause')
        exit()


def TakeOptionNumeric(option, lower, upper):
    correct_options = set()
    tmp = lower
    while tmp <= upper:
        correct_options.add(str(tmp))
        tmp+= 1

    while option not in correct_options:
        print("You did not enter a number between", lower, "and", upper)
        option = input("Please enter your choice: ")

    return option

#Check if the given club exists in the database
def CheckClubExists(club):
    checkClub = ("select * from club where `Name` = '{}' ".format(club))
    res = QueryTheDatabase(checkClub)
    return len(res)!= 0

# checks if the email given exist in the database
# If it does, it returns True and the user info
# Otherwise, it returns False
def GetUserByEmail(email):
    checkEmail = (
        "Select * from `user` where Email={} ".format("'{}'".format(email))
    )


    res = QueryTheDatabase(checkEmail)
    if len(res) ==0:
        return (False, res)
    else:
        return (True, res)

# Checks if the email is valid
def IsValidEmail(email):
    emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(emailRegex, email)):
        return True
    else:
        return False


def SignIn():
    global userEmail, userName, userFavoriteTeam
    givenEmail = input("Please, enter your email: ")
    countFailed = 0
    while GetUserByEmail(givenEmail)[0] == False:
        countFailed+=1
        if countFailed == 5:
            print("You tried so many emails incorrectly. You would be returned to original menu")
            return False
        print("The email given does not exist")
        givenEmail = input("Please, enter your email: ")

    res = GetUserByEmail(givenEmail)[1]
    correctPass = res[0][2]

    countFailed=0
    while True:
       givenPass = stdiomask.getpass("Please, enter your password. Passwords are case sensitive: ")
       if givenPass != correctPass:
           countFailed+=1
       else:
           break 
       print("The password is wrong")  
       if countFailed == 5:
           print("You tried so many wrong passwords. You would be returned to original menu")
           return False

    userEmail = res[0][0]
    userName = res[0][1]
    userFavoriteTeam = res[0][-1]
    print("Welcome,",userName, "to the application. You have signed in successfully!")
    return True

def CreateAccount():
    global userEmail, userName, userFavoriteTeam
    email = input("Please, enter an email for the new account : ")
    while IsValidEmail(email) == False:
        print("The email you entered is not valid")
        email = input("Please, enter an email for the new account : ")
    if GetUserByEmail(email)[0]==True:
        print("The email is already linked to a registered user")
        print("You will be returned to the original menu")
        return False
    user_name = input("Please, enter your user name for the new account : ")
    while len(user_name) <3:
        print("The user name should be at least 3 characters!")
        user_name = input("Please, enter your user name for the new account : ")

    password = stdiomask.getpass("Please, enter password for the new account. Passwords are case sensitive: ")
    while len(password<3):
        print("The password should be at least 3 characters!")
        password = stdiomask.getpass("Please, enter password for the new account. Passwords are case sensitive: ")

    while True:
        birth_date = input('Enter your birth date in the format YYYY-MM-DD: ')
        try:
            year, month, day = map(int, birth_date.split('-'))
            if month<=0 or month>=13 or day<=0 or day>=32 or year<= 1900 or year>=2020:
                raise ValueError()
            break
        except:
            print("The format given is incorrect")

    gender = input("Please, Enter your gender. M for Male or F for Female: ")
    while gender not in {'F', 'f', 'M', 'm'}:
        print("The format of gender is incorrect")
        gender = input("Please, Enter your gender. M for Male or F for Female: ")

    favorite_club = input("Please, enter your favorite club: ")
    while CheckClubExists(favorite_club) == False:
        print("This club does not exist in our database. Please, try again")
        favorite_club = input("Please, enter your favorite club: ")


    create_account_sql = ("INSERT INTO `user` values(%s, %s, %s, %s, %s, %s);")
    val = (email, user_name, password, birth_date, gender, favorite_club)

    try:
        cursor.execute(create_account_sql, val)
        db.commit()
    except:
        print("Something wrong happened while connecting to the database. Check your network and restart the program.")
        os.system('pause')
        exit()


    userEmail = email
    userName = user_name
    userFavoriteTeam = favorite_club
    print("Welcome,", userName, "to the application. You have created the account and signed in successfully!")
    return True


def LogInOptions():
    global guestMode
    print("Write 1, 2, or 3 to choose from the following:")
    print("1. Sign into the application (already have an account)")
    print("2. Create a new account")
    print("3. Sign in as guest user without account (You will have all functionalities but you will not be able to add a review)")
    choice = input("Choice: ")
    while True:
        if choice =="1":
            if SignIn() == False:
                LogInOptions()
            break
        elif choice =="2":
            if CreateAccount() == False:
                LogInOptions()
            break
        elif choice == "3":
            guestMode = True
            break
        else:
            print("You entered a wrong input")
            choice = input("Please enter 1, 2, or 3: ")


# Auxilary Views that will help in the team quereis
def CreateAuxilaryViews():
    homeWonView = ("create or replace view HomeWonSeason AS select HomeTeamName AS 'TeamName',  Season, count(*) AS 'MathcesWon'FROM `match` "
                   "where HomeGoals > AwayGoals GROUP BY 1, 2; ")

    try:
        cursor.execute(homeWonView)
    except:
        print("Something wrong happened while connecting to the database. Check your network and restart the program.")
        os.system('pause')
        exit()

    awayWonView = ("create or replace view AwayWonSeason AS select AwayTeamName AS 'TeamName',  Season, count(*) AS 'MathcesWon' FROM `match` "
                   "where HomeGoals < AwayGoals GROUP BY 1, 2; ")


    try:
        cursor.execute(awayWonView)
    except:
        print("Something wrong happened while connecting to the database. Check your network and restart the program.")
        os.system('pause')
        exit()




# Implements the logic of "Show the top 10 teams by certain criteria".
def ShowTopTen():

    print("Choose criteria from the following: ")
    # Show the top 10 teams by matches won, home matches won, yellow cards, fouls,
    # and shots
    print("1. Total Matches Won")
    print("2. Home Matches Won")
    print("3. Away Matches Won")
    print("4. Yellow Cards Taken")
    print("5. Red Cards Taken")
    print("6. fouls conceded")
    print("7. Shots Done")


    top_option = input("Please, Enter the number, 1 to 7, of the required criteria: ")
    top_option = TakeOptionNumeric(top_option, 1, 7)

    print("Choose for which season of the last four seasons you want the answer: ")
    print("1. All four seasons"); print("2. Season 2021/22"); print("3. Season 2020/21"); print("4. Season 2019/20"); print("5. Season 2018/19")
    season_option = input("Please, Enter the number, 1 to 5, of the season: ")
    season_option = TakeOptionNumeric(season_option, 1, 5)

    if top_option == "1":
        query = (
            "Select TeamName, SUM(MathcesWon) As 'Number of Mathces Won'"
            "FROM (SELECT * from HomeWonSeason UNION ALL Select * from AwayWonSeason) AS AllWon {}"
            "group by 1 ORDER BY 2 DESC Limit 10;"
        )
        headers = ["Team Name", "Number of Matches Won"]
    elif top_option== "2":
        query = (
            "select TeamName, SUM(MathcesWon) AS 'Number of Home Mathces Won'from HomeWonSeason {} "
            "group by 1 order by 2 DESC Limit 10;"
        )
        headers = ["Team Name", "Number of Home Matches Won"]
    elif top_option== "3":
        query = (
            "select TeamName, SUM(MathcesWon) AS 'Number of Away Mathces Won' from AwayWonSeason {} "
            "group by 1 order by 2 DESC Limit 10;"
        )
        headers = ["Team Name", "Number of Away Matches Won"]
    else:
        query = (
            "Select `Name`, SUM(CASE WHEN `Name` = `HomeTeamName` THEN {} WHEN `Name` = `AwayTeamName` THEN {} ELSE 0 END) As `Answer` "
            "FROM club INNER JOIN `match` ON club.`Name`= `match`.`HomeTeamName` OR club.`Name`= `match`.`AwayTeamName` {} "
            "Group by 1 Order BY 2 DESC LIMIT 10;"
        )
        if top_option == "4":
            query = query.format("HomeYellowCards", "AwayYellowCards", {})
            headers = ["Team Name", "Number of Yellow Cards"]
        elif top_option == "5":
            query = query.format("HomeRedCards", "AwayRedCards", {})
            headers = ["Team Name", "Number of Red Cards"]
        elif top_option == "6":
            query = query.format("HomeFouls", "AwayFouls", {})
            headers = ["Team Name", "Number of Fouls Conceded"]
        else:
            query = query.format("HomeShots", "AwayShots", {})
            headers = ["Team Name", "Number of Shots"]

    #adjusting the season
    map_option_to_season = {"1": "", "2": "where season = '2021/22'", "3": "where season = '2020/21'",
                            "4": "where season = '2019/20'",
                            "5": "where season = '2018/19'"}
    query = query.format(map_option_to_season[season_option])
    res = QueryTheDatabase(query)
    print(tabulate(res, headers))

# Implements the logic of "Show teams who won the most games in each season"
def ShowTopTeamBySeason():
    changeGroupBy = "SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));"

    try:
        cursor.execute(changeGroupBy)
    except:
        print("Something wrong happened while connecting to the database. Check your network and restart the program.")
        os.system('pause')
        exit()

    query = (
        "Select * FROM(Select Season, TeamName, SUM(MathcesWon) As 'Matches Won' FROM (SELECT * from HomeWonSeason UNION ALL Select * from AwayWonSeason) AS `AllWon` "
        "group by 1, 2 order by 3 desc) AS `TMP` group by Season HAVING `TMP`.`Matches Won` = MAX(`TMP`.`Matches Won`) order by Season Desc;"
    )
    res = QueryTheDatabase(query)
    print(tabulate(res, headers=["Season", "Team Name", "Number of won matches"]))

# Implements the logic of "Query and view a given team information, including team players"
def QueryTeamInfo():
    option = 0
    if guestMode == False:
        print("choose from the following: ")
        print("1. Show the information for your favorite team")
        print("2. Show the information for a given team")
        option = input("Please, enter 1 or 2: ")
        TakeOptionNumeric(option, 1, 2)

    if option == "1":
        team = userFavoriteTeam
    else:
        team = input("Please, Enter the team you want to query about: ")

    query = ("select * from club where `Name` = '{}';".format(team))

    res = QueryTheDatabase(query)
    if len(res) == 0:
        print("There is no such team in our database. Please, make sure you type it correctly!")
    else:
        # To remove all the stuff after .com or .uk for better printing
        if ".uk" in res[0][1]:
            res[0] = (res[0][0], res[0][1].split(".uk", 1)[0] + ".uk", res[0][2])
        else:
            res[0]= (res[0][0], res[0][1].split(".com", 1)[0]  + ".com", res[0][2])
        print(tabulate(res, headers=["Team Name", "Website", "Stadium Name"]))
        team = res[0][0]
        query = (
        "select P.FullName, P.Nationaility, P.position from player P INNER JOIN playersinclubs PC ON P.ID = PC.PlayerID "
        "where PC.ClubName = '{}' and PC.Season = '2021/22' order by 3; ".format(team))

        res = QueryTheDatabase(query)
        print("-" * 50)
        print(team, "players in season 2021/22 are :" )
        print(tabulate(res, headers=["Player Name", "Nationality", "Position"]))

        query = (
            "select P.FullName, P.Nationaility, P.position from player P INNER JOIN playersinclubs PC ON P.ID = PC.PlayerID "
            "where PC.ClubName = '{}' and PC.Season = '2020/21' order by 3; ".format(team))

        res = QueryTheDatabase(query)
        print("-" * 50)
        print(team, "players in season 2020/21 are :")
        print(tabulate(res, headers=["Player Name", "Nationality", "Position"]))

        query = (
            "select P.FullName, P.Nationaility, P.position from player P INNER JOIN playersinclubs PC ON P.ID = PC.PlayerID "
            "where PC.ClubName = '{}' and PC.Season = '2019/20' order by 3; ".format(team))

        res = QueryTheDatabase(query)
        print("-" * 50)
        print(team, "players in season 2019/20 are :")
        print(tabulate(res, headers=["Player Name", "Nationality", "Position"]))


        query = (
            "select P.FullName, P.Nationaility, P.position from player P INNER JOIN playersinclubs PC ON P.ID = PC.PlayerID "
            "where PC.ClubName = '{}' and PC.Season = '2018/19' order by 3; ".format(team))

        res = QueryTheDatabase(query)
        print("-" * 50)
        print(team, "players in season 2018/19 are :")
        print(tabulate(res, headers=["Player Name", "Nationality", "Position"]))

# Implements the logic of "View the home team for a given stadium name"
def QueryTeamByStadium():
    stadium = ""
    while len(stadium) == 0:
        stadium  = input("Please, Enter the stadium name: ")
    # using wild cards as the user might not know the full name of the stadium. Usually, you only remember the beginning
    #  Will print all possible results. Just a design choice
    query = (
        "SELECT  `stadiumName`, `Name` from `club` where `stadiumName` like '{}%';".format(stadium)
    )
    res = QueryTheDatabase(query)
    if len(res) == 0:
        print("There is no such stadium in our database. Please, make sure you type it correctly!")
    else:
        print(tabulate(res, headers=["Stadium Name", "Team Name"]))



# Bonus Query: Implements the logic of "View all the teams in a given city in the UK"
def QueryTeamsByCity():
    city = ""
    while len(city) == 0:
        city = input("Plese, Enter the city of the query: ")

     # using wild cards as the user might not know the full name of the stadium. Usually, you only remember the beginning
    #  Will print all possible results. Just a design choice

    query = ("Select `S`.`City`, `C`.`Name` AS `Team Name` from club C INNER JOIN stadium S ON C.stadiumName = `S`.`Name` "
             "where `S`.`City` like '{}%' order by 1;".format(city)
             )
    res = QueryTheDatabase(query)
    if len(res) == 0:
        print("There is no club associated with this city in our database. Please, make sure you type it correctly!")
    else:
        print(tabulate(res, headers=["City" ,"Team Name" ]))

# Implements the logic of "Query and view a given player information by their first and/or last name"
def QueryPlayerbyName():
    first= ""
    while len(first) == 0:
        first = input("Please, enter the first name of the player: ")
    last = input("Please, enter the last name of the player (To leave it empty, just press enter): ")
    query = (
        "SELECT `FullName`, `Nationaility`, `Position`, `BirthDate`, `Height`, `Weight` FROM `player` "
        "where `FullName` like '{}%{}';".format(first, last)
    )
    res = QueryTheDatabase(query)
    if len(res) == 0:
        print("There is no players matching these names in our database. Please, make sure you type them correctly!")
    else:
        print(tabulate(res, headers=["Full Name", "Nationality", "Position", "BirthDate", "Height in cm", "Weight in kg"]))


def QueryPlayersByPosition():
    print("Choose one of the below positions:")
    #Goalkeeper, Defender, Midfielder, Forward
    map_num_to_pos = {"1": "Goalkeeper", "2": "Defender", "3" : "Midfielder", "4" : "Forward"}
    print("1. Goalkeeper")
    print("2. Defender")
    print("3. Midfielder")
    print("4. Forward")
    position = input("Please, Enter a number from 1 to 4: ")
    position = TakeOptionNumeric(position, 1, 4)
    position = map_num_to_pos[position]
    query = (
        "SELECT `FullName`, `Position`, `Nationaility`, `BirthDate`, `Height`, `Weight` FROM `player` "
        "where `Position`='{}';".format(position)
    )
    res = QueryTheDatabase(query)
    print(tabulate(res, headers=["Full Name", "Position", "Nationality", "BirthDate", "Height in cm", "Weight in kg"], showindex='always'))



def QueryPlayersByNationality():
    country = input("Please, Enter the country of nationality of the query: ")
    query = (
        "SELECT `FullName`, `Nationaility`, `Position`, `BirthDate`, `Height`, `Weight`, `clubName`, `Season` "
        "FROM player INNER JOIN playersinclubs ON ID = playerID where Nationaility = '{}';".format(country)
    )

    res = QueryTheDatabase(query)

    if len(res) == 0:
        print("There is no players from that country in our database. Please, make sure you type them correctly!")
    else:
        print(tabulate(res, headers = ["Full Name", "Nationality", "Position", "BirthDate", "Height in cm", "Weight in kg",
                                       "Club Name", "Season"], showindex="always"))

def ViewReviews():
    print("Choose in which season is the match: ")
    print("1. Season 2021/22"); print("2. Season 2020/21"); print("3. Season 2019/20"); print("4. Season 2018/19")
    season_option = input("Please, Enter the number, 1 to 4, of the season: ")
    season_option = TakeOptionNumeric(season_option, 1, 4)

    home_team = input("Please, Enter the home team name in that match: ")
    while CheckClubExists(home_team) == False:
        print("This club does not exist in our database. Please, try again")
        home_team = input("Please, Enter the home team name in that match: ")

    away_team = input("Please, Enter the away team name in that match: ")
    while CheckClubExists(away_team) == False:
        print("This club does not exist in our database. Please, try again")
        away_team = input("Please, Enter the away team name in that match: ")

    map_numer_to_seaon  = {"1":"2021/22", "2" : "2020/21", "3" : "2019/20", "4" : "2018/19"}
    query = (
        "SELECT userEmail, Rating, TextReview FROM matchsreviews where season = '{}' AND HomeTeamName = '{}' AND AwayTeamName = '{}';"
    ).format(map_numer_to_seaon[season_option], home_team, away_team)


    res = QueryTheDatabase(query)
    if len(res) == 0:
        print("There are no reviews for that match. You may add one through option 10 :)")
    else:
        print(tabulate(res, headers = ["Reviewer Email", "Rating", "Text Review"]))


# I assume a user can add single review on a given match
def AddNewReview():
    print("Choose in which season is the match: ")
    print("1. Season 2021/22"); print("2. Season 2020/21"); print("3. Season 2019/20"); print("4. Season 2018/19")
    season_option = input("Please, Enter the number, 1 to 4, of the season: ")
    season_option = TakeOptionNumeric(season_option, 1, 4)

    home_team = input("Please, Enter the home team name in that match: ")
    while CheckClubExists(home_team) == False:
        print("This club does not exist in our database. Please, try again")
        home_team = input("Please, Enter the home team name in that match: ")

    away_team = input("Please, Enter the away team name in that match: ")
    while CheckClubExists(away_team) == False:
        print("This club does not exist in our database. Please, try again")
        away_team = input("Please, Enter the away team name in that match: ")

    map_numer_to_seaon  = {"1":"2021/22", "2" : "2020/21", "3" : "2019/20", "4" : "2018/19"}
    query_review = (
        "SELECT * FROM matchsreviews where season = '{}' AND HomeTeamName = '{}' "
        "AND AwayTeamName = '{}' AND userEmail = '{}';"
    ).format(map_numer_to_seaon[season_option], home_team, away_team, userEmail)


    res = QueryTheDatabase(query_review)
    if len(res) != 0:
        print("You already have a review for this match. Please, review another match!")
    else:
        query_match = (
            "SELECT * FROM `match` where Season = '{}' AND HomeTeamName= '{}' AND AwayTeamName = '{}';"
                       ).format(map_numer_to_seaon[season_option], home_team, away_team)
        res = QueryTheDatabase(query_match)

        if len(res) == 0:
            print('This match has not been played at the time of constructing the database!')
        else:
            insert_review_sql = (
                "INSERT INTO `matchsreviews` values(%s, %s, %s, %s, %s, %s);"
            )
            rating = input("Please, Enter a decimal number between 1 and 10 inclusive as a match rating: ")
            while True:
                try:
                    rating = float(rating)
                    if  rating <1  or rating>10:
                        print("The rating shouls be between 1 and 10 inclusive")
                        rating = input("Please, Enter a decimal number between 1 and 10 inclusive as a match rating: ")
                    else:
                        break
                except ValueError:
                    print("The rating you entered is not decimal")
                    rating = input("Please, Enter a decimal number between 1 and 10 inclusive as a match rating: ")

            text_review = input("Please, Enter a text review for the match if you want (leave blank if you don't want): ")
            val = (userEmail, map_numer_to_seaon[season_option], home_team, away_team, rating, text_review)

            try:
                cursor.execute(insert_review_sql, val)
                db.commit()
                print("Your review has been added successfully!")
            except:
                print("Something wrong happened while connecting to the database. Check your network and restart the program.")
                os.system('pause')
                exit()

def ChooseOption():
    print("-"*50)
    print("Choose an option from the following: ")
    print("A. Teams Section:")
    print("1. Show the top 10 teams by certain criteria")
    print("2. Show teams who won the most games in each season")
    print("3. Query and view a given team information, including team players")
    print("4. View the home team for a given stadium name")
    print("5. View all the teams in a given city in the UK")
    print("B. Players Section:")
    print("6. Query and view a given player information by their first and/or last name")
    print("7. Show all the players who played a certain position")
    print("8. Show all the players from a certain nationality and their home teams history")
    print("C. Match Reviews Section:")
    print("9. View existing reviews on a given match")
    print("10. Add a new review on a match (Not Allowed for guest users).")
    print("D. Other Options: ")
    print("11. I got what I need. Stop the program!")

    option = input("Enter a number from 1 to 11 corresponding to your choice: ")
    while option not in {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"} or (option == "10" and guestMode):
        if option == "10" and guestMode :
            option = input("You can't add a review in guest mode. Please choose another choice: ")
        else:
            option = input("You did not enter a number between 1 and 11. Please enter your choice: ")

    if option == "11":
        return False

    # Calling the appropriate function depending on the choice
    map_option_to_function = {
        "1": "ShowTopTen",
        "2": "ShowTopTeamBySeason",
        "3": "QueryTeamInfo",
        "4": "QueryTeamByStadium",
        "5": "QueryTeamsByCity",
        "6" : "QueryPlayerbyName",
        "7" : "QueryPlayersByPosition",
        "8" : "QueryPlayersByNationality",
        "9": "ViewReviews",
        "10" : "AddNewReview"}
    globals()[map_option_to_function[option]]()

    return True


def main():
    print("Welcome to the English Premier League Database Center for the last four seasons!")
    print("You will be able to access a lot of EPL data easily!")
    LogInOptions()
    CreateAuxilaryViews()
    while ChooseOption():
        continue
    print("Thanks for choosing our application!")
    cursor.close()
    db.close()
    os.system("pause")

if __name__ == "__main__":
    main()