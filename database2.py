from Physics import Database as d
import Physics as p
import math
import sys

def make_table():
    table = p.Table()
    pos = p.Coordinate(p.TABLE_WIDTH / 2.0 - math.sqrt(p.BALL_DIAMETER * p.BALL_DIAMETER / 2.0),\
    p.TABLE_WIDTH / 2.0 - math.sqrt(p.BALL_DIAMETER * p.BALL_DIAMETER / 2.0))
    sb = p.StillBall(1, pos) #create new still ball with a position and number

    pos, vel, acc = p.Coordinate(p.TABLE_WIDTH / 2.0, p.TABLE_LENGTH - p.TABLE_WIDTH / 2.0),\
    p.Coordinate(0.0, -1000.0),\
    p.Coordinate(0.0, 180.0)

    rb = p.RollingBall(0, pos, vel, acc)
    table += sb
    table += rb
    return table

if __name__ == "__main__":
    # table = make_table()
    database = p.Database()
    try:
        table_ID = int(input("Enter the integer table ID: "))
    except ValueError:
            print('invalid')
            sys.exit(1)
    print("Autoincremented TABLEID value is:", table_ID)
    new_table = database.readTable(table_ID)
    if new_table != None:
        # print("increment value: " + str(table_ID)) # the table ID
        print("Table after reading it from database:\n\n" + str(new_table))
        # database.print_database()
    else:
        print(f"readTable returned None for table id {table_ID}")
        sys.exit(1)
    print('Database is:')
    database.print_database()
    # try:
        # print("Physics gives access to: " + str(dir(p)), end="\n\n")
        # my_game = p.Database.Game(gameID=12, database=database)
        # my_game = d.Game(gameID=23, database=database)
        # original_game = d.Game(gameID=None, gameName="gameName", player1Name="Player1", player2Name="Player2", table= new_table, database=database)
        # original_game = d.Game(gameID=1, gameName=None, player1Name=None, player2Name=None, table=None, database=database)
        # original_game.shoot(100, 100)
    # except TypeError:
        # print("Did not use Game class constructor correctly")