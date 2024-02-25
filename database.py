from Physics import Database as d
import Physics as p
import math

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


def make_table_3():
    table = p.Table()
    pos = p.Coordinate(250, 365)
    sb = p.StillBall(6, pos) #create new still ball with a position and number

    pos, vel, acc = p.Coordinate(520, 25.3),\
    p.Coordinate(0.0, 255.0),\
    p.Coordinate(0.0, 500.0)

    rb = p.RollingBall(7, pos, vel, acc)
    table += sb
    table += rb
    table.time = 230.978
    return table

def make_table_2():
    table = p.Table()
    pos = p.Coordinate(157.36, 1221.36)
    sb = p.StillBall(3, pos) #create new still ball with a position and number

    pos, vel, acc = p.Coordinate(287.36, 580.3),\
    p.Coordinate(0.0, 512.14),\
    p.Coordinate(0.0, 1000.52)

    rb = p.RollingBall(4, pos, vel, acc)
    table += sb
    table += rb
    table.time = 127.38
    return table

if __name__ == "__main__":
        database = p.Database(reset=True)
        try:
            game_1 = d.Game(gameID=None, gameName="myGame1", player1Name="Player1", player2Name="Player2", table=make_table(), database=database)
            # print("First insert")
            # database.print_database()
            game_2 = d.Game(gameID=None, gameName="myGame2", player1Name="Player1_2", player2Name="Player2_2", table=make_table_2(), database=database)
            # print("second insert")
            # database.print_database()
            game_3 = d.Game(gameID=None, gameName="myGame3", player1Name="Player1_3", player2Name="Player2_3", table=make_table_3(), database=database)
            # print("third insert")
            # database.print_database()
            table = d.Game(gameID=3, database=database).table # fetch the third game
            database.print_database()
            game_1.shoot(30, 20)
            database.print_database()
            # print(table)
        except TypeError:
            print("Did not use Game class constructor correctly")