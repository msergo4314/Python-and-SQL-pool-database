import phylib
#import os

################################################################################
# header and footer for svg function

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />"""

FOOTER = """</svg>\n"""

################################################################################
# import constants from phylib to global varaibles (some new constants)

FRAME_RATE    = 0.01 # constant frame rate for database operations
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS   = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH  = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH   = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE      = phylib.PHYLIB_SIM_RATE
VEL_EPSILON   = phylib.PHYLIB_VEL_EPSILON
DRAG          = phylib.PHYLIB_DRAG
MAX_TIME      = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS   = phylib.PHYLIB_MAX_OBJECTS

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ]

################################################################################
class Coordinate(phylib.phylib_coord):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass

################################################################################
class StillBall(phylib.phylib_object):
    """
    Python StillBall class.
    """
    def __init__(self, number, pos):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """
        # this creates a generic phylib_object
        phylib.phylib_object.__init__(self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0)
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall


    # add an svg method here
    def svg(self):
        # print('type stillball is : ', (self.type))
        return""" <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x,self.obj.still_ball.pos.y,\
        BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])

################################################################################
class RollingBall(phylib.phylib_object):
    """
    Python RollingBall class.
    """

    def __init__(self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number, position, velocity, and acceleration
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__(self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0)
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall

    # add an svg method here
    def svg(self):
        # print('type is : ', (self.type))
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x,self.obj.rolling_ball.pos.y,\
        BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])

################################################################################
class Hole(phylib.phylib_object):
    """
    Python Hole class.
    """

    def __init__(self, pos):
        """
        Constructor function. Requires hole position
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__(self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0)
      
        # this converts the phylib_object into a Hole class
        self.__class__ = Hole

    # add an svg method here
    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" %\
        (self.obj.hole.pos.x,self.obj.hole.pos.y, HOLE_RADIUS)

################################################################################
class HCushion(phylib.phylib_object):
    """
    Python HCushion class.
    """

    def __init__(self, y):
        """
        Constructor function. Requires y position only
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__(self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, y)
      
        # this converts the phylib_object into a HCushion class
        self.__class__ = HCushion

    # add an svg method here
    
    def svg(self):
        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" \
        % (-25 if self.obj.hcushion.y == 0.0 else 2700)

################################################################################
class VCushion(phylib.phylib_object):
    """
    Python VCushion class.
    """

    def __init__(self, x):
        """
        Constructor function. Requires x position as only argument
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__(self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       0, 
                                       None, None, None, 
                                       x, 0.0)
      
        # this converts the phylib_object into a VCushion class
        self.__class__ = VCushion

    # add an svg method here
    def svg(self):
        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (-25 if self.obj.vcushion.x == 0.0 else 1350)

################################################################################

class Table(phylib.phylib_table):
    """
    Pool table class.
    """

    def __init__(self):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__(self)
        self.current = -1

    def __iadd__(self, other):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object(other)
        return self

    def __iter__(self):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self

    def __next__(self):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ] # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1    # reset the index counter
        raise StopIteration  # raise StopIteration to tell for loop to stop

    def __getitem__(self, index):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object(index) 
        if result==None:
            return None
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion
        return result

    def __str__(self):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = ""    # create empty string
        result += "time = %6.1f\n" % self.time    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj)  # append object description
        return result  # return the string

    def segment(self):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment(self)
        if result:
            result.__class__ = Table
            result.current = -1
        return result

    # add svg method here

    def svg(self):
        svg_strings = ''
        for i in self:
            # print(type(i))
            if i:
                svg_strings += i.svg() # call SVG method for each object in table
        # print("exiting", end="\n\n")
        return HEADER + svg_strings + FOOTER

class Database:
    """
    Database class.
    """
    import sqlite3 # for database operations
    database_name = "phylib.db"
    
    def __init__(self, reset=False):
        import os
        if reset and os.path.exists(self.database_name):
            os.remove(self.database_name)
        self.current_database_connection = self.sqlite3.connect(self.database_name)
        self.current_cursor = self.current_database_connection.cursor()
        self.createDB()
        self.current_database_connection.commit()
        return

    def createDB(self):
        # need to create each table
        table_names = ("Ball", "Table", "BallTable", "Shot", "TableShot", "Game", "Player")

        for current_table in table_names:
            # make sure table exists. If not, create it
            self.current_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{current_table}';")
            current_data = self.current_cursor.fetchone()
            if current_data is None:
                # print(f"Missing for {current_table}") # MUST remove later
                self.create_DB_table(current_table)
        return

    def create_DB_table(self, table_name_to_create):
        # creates the table that is passed in as name_to_create
        table_names = ("Ball", "Table", "BallTable", "Shot", "TableShot", "Game", "Player")
        if not table_name_to_create in table_names:
            print("error") # this shouldn't ever happen anyway
            return
        table_dictionary = {'Ball'      : "BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, BALLNO INTEGER NOT NULL, \
                                           XPOS FLOAT NOT NULL, YPOS FLOAT NOT NULL, XVEL FLOAT, YVEL FLOAT",
                            'Table'     : "TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, TIME FLOAT NOT NULL",
                            'BallTable' : "BALLID INTEGER NOT NULL, TABLEID FLOAT NOT NULL, FOREIGN KEY (BALLID) REFERENCES Ball(BALLID), \
                                           FOREIGN KEY (TABLEID) REFERENCES 'Table'(TABLEID)",
                            'Shot'      : "SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, PLAYERID INTEGER NOT NULL, \
                                           GAMEID INTEGER NOT NULL, FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID), \
                                           FOREIGN KEY (SHOTID) REFERENCES 'TableShot'(SHOTID), FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID) ",
                            'TableShot' : "TABLEID INTEGER NOT NULL, SHOTID INTEGER NOT NULL, FOREIGN KEY (TABLEID) REFERENCES 'Table'(TABLEID), \
                                           FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID)",
                            'Game'      : "GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, GAMENAME VARCHAR(64) NOT NULL", #  FOREIGN KEY (GAMENAME) REFERENCES Game(GAMEID)",
                            'Player'    : "PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, GAMEID INTEGER NOT NULL, PLAYERNAME VARCHAR(64) NOT NULL, \
                                           FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)"}
        self.current_cursor.execute(f"CREATE TABLE '{table_name_to_create}' (\
                                     {table_dictionary.get(table_name_to_create)}\
                                     );")
        # self.current_cursor.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{table_name_to_create}';")
        # current_data = self.current_cursor.fetchone()
        # if current_data is None:
        #     print(f"failed for {current_table}") # MUST remove later
        # else:
        #     print("succesfully made table: " + table_name_to_create)
        #     self.current_cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND NAME != 'sqlite_sequence'")
        #     print(self.current_cursor.fetchall())
        self.current_database_connection.commit()
        return

    def readTable(self, tableID):
        # assume TableID is a float
        if not (isinstance(tableID, float) or isinstance(tableID, int)):
            return None
        self.current_cursor.execute(f"SELECT (BALLID) FROM BallTable WHERE BallTable.TABLEID = {tableID};")
        ball_ID_list = tuple(tup[0] for tup in self.current_cursor.fetchall())
        if not (ball_ID_list):
            # self.print_database()
            print(f"No entries in BallTable have a matching ID: {tableID}")
            return None
        table_to_return = Table() # create a new table object
        table_to_return.time = self.current_cursor.execute(f'SELECT TIME FROM "Table" WHERE "Table".TABLEID = {tableID}').fetchone()[0]

        for current_ball_ID in ball_ID_list:
            # print(current_ball_ID)
            self.current_cursor.execute(f"SELECT * FROM Ball WHERE Ball.BALLID = {current_ball_ID};") # we want every column so use wildcard (*)
            ball_data = self.current_cursor.fetchall()[0][1:] # from list of one tuple to tuple
            # remove ball ID from tuple (not needed to insert a ball into a table)
            # len(ball_data) should always be 5 due to Ball columns
            if ball_data[3] is None and ball_data[4] is None:
                # print("still ball")
                new_ball = StillBall(ball_data[0], Coordinate(ball_data[1], ball_data[2]))
            else:
                # print("rolling ball")
                new_ball = RollingBall(ball_data[0], Coordinate(ball_data[1], ball_data[2]), Coordinate(ball_data[3], ball_data[4]),\
                self.getAccelerationCoordinates(ball_data[3], ball_data[4]))
            table_to_return += new_ball
        return table_to_return
        
    def getAccelerationCoordinates(self, rolling_ball_dx, rolling_ball_dy):
        import math
        if type(rolling_ball_dx) != float or type(rolling_ball_dy) != float:
            # print("fatal error with acceleration values")
            return Coordinate(0.0, 0.0)
        rolling_ball_a_x = 0.0
        rolling_ball_a_y = 0.0
        rolling_ball_speed = math.hypot(rolling_ball_dx, rolling_ball_dy)
        if (rolling_ball_speed > VEL_EPSILON):
            rolling_ball_a_x = -rolling_ball_dx * DRAG / rolling_ball_speed
            rolling_ball_a_y = -rolling_ball_dy * DRAG / rolling_ball_speed
        return Coordinate(rolling_ball_a_x, rolling_ball_a_y)

    def writeTable(self, table):
        if not isinstance(table, Table):
            print("Must pass in table to write to database")
            return
        self.current_cursor.execute("SELECT MAX(TABLEID) FROM 'Table' WHERE 'Table'.TABLEID >= 1")
        table_ID_tuple = self.current_cursor.fetchone()
        if table_ID_tuple[0] is None:
            table_ID = 1 # returns one because autoincrement will start at 1
        else:
            table_ID = int(table_ID_tuple[0]) + 1
        for item in table:
            if isinstance(item, RollingBall) or isinstance(item, StillBall):
                if isinstance(item, RollingBall):
                    current_ball = item.obj.rolling_ball
                    self.current_cursor.execute(f"INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (\
                    {current_ball.number}, {current_ball.pos.x}, {current_ball.pos.y}, {current_ball.vel.x}, {current_ball.vel.y})")
                elif isinstance(item, StillBall):
                    current_ball = item.obj.still_ball
                    self.current_cursor.execute(f"INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (\
                    {current_ball.number}, {current_ball.pos.x}, {current_ball.pos.y}, NULL, NULL)") # no velocity for still balls
        self.current_cursor.execute(f"INSERT INTO 'Table'(TABLEID, TIME) VALUES ({table_ID}, {table.time}); ")
        # only insert into Balltable if the combo of BALLID AND TABLEID is not already present (like a primary key)
        self.current_cursor.execute("""
                                    INSERT INTO BallTable (BALLID, TABLEID) SELECT BALLID, TABLEID
                                    FROM Ball, 'Table' WHERE (BALLID IS NOT NULL AND TABLEID IS NOT NULL
                                    AND NOT EXISTS (
                                        SELECT 1
                                        FROM BallTable
                                        WHERE (BallTable.BALLID = Ball.BALLID
                                        OR BallTable.TABLEID = "Table".TABLEID)
                                    ));
                                    """)
        # self.current_cursor.execute("INSERT INTO BallTable (BALLID, TABLEID) SELECT BALLID, TABLEID FROM Ball, 'Table' WHERE BALLID IS NOT NULL AND TABLEID IS NOT NULL;")

        self.current_database_connection.commit()
        return table_ID

    def print_database(self):
        # helper for printing entire database to console
        table_names = ("Ball", "Table", "BallTable", "Shot", "TableShot", "Game", "Player")
        nameColumns = {
            "Ball": ("BALLID", "BALLNO", "XPOS", "YPOS", "XVEL", "YVEL"),
            "Table": ("TABLEID", "TIME"),
            "BallTable": ("BALLID", "TABLEID"),
            "Shot": ("SHOTID", "PLAYERID", "GAMEID"),
            "TableShot": ("TABLEID", "SHOTID"),
            "Game": ("GAMEID", "GAMENAME"),
            "Player": ("PLAYERID", "GAMEID", "PLAYERNAME")
            }
        for name in table_names:
            print("Table %s data is:" % name, end='\n\n')
            # if name == 'BallTable':
                # self.print_single_table(self.current_cursor.execute(f"SELECT * FROM '{name}' ORDER BY BALLID;").fetchall(), nameColumns.get(name))
            # else:
            self.print_single_table(self.current_cursor.execute(f"SELECT * FROM '{name}';").fetchall(), nameColumns.get(name))
            print()
        return

    def print_single_table(self, listoftuples, nameColumns):
        if not listoftuples:
            return
        widths_data = [max(len(str(item[col])) for item in listoftuples) for col in range(len(nameColumns))]
        name_widths = tuple(len(i) for i in nameColumns)
        widths = tuple(max(pair) for pair in zip(widths_data, name_widths))        
        # print("Total max widths: " + str(widths))
        # Print table columns
        left_side = '| '
        right_side = left_side[::-1]
        column_strings = [("%-" + str(width) + "s") % name.center(width) for width, name in zip(widths, nameColumns)]
        column_line = " | ".join(column_strings)
        print(left_side + column_line + right_side)

        # Print separator line
        separator = "+".join(["-" * ((width + 1) if i < 1 else (width + 2)) for i, width in enumerate(widths)])
        chars_removed = len(left_side) - len(left_side.strip())
        print(left_side.strip() +'-'*chars_removed + separator[:len(separator)-1] +'-'*chars_removed + right_side.strip())
        fmt = " | ".join(["%%-%ds" % width for width in widths])
        for row in listoftuples:
            centered_row = [str(data).center(width) for data, width in zip(row, widths)]
            print(left_side +  fmt % tuple(centered_row) + right_side)
            # print('|' + separator[:len(separator)-1] + '|')
        return

    def __del__(self):
        self.current_cursor.close()
        self.current_database_connection.commit()
        self.current_database_connection.close()

    class Game():
        import time

        def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None, table=None, database=None): # MUST take database param (for now)
            self.game_ID = gameID
            self.game_Name = gameName
            self.player1_Name = player1Name
            self.player2_Name = player2Name
            self.current_cursor = None
            self.database = database
            arguments = (gameID, gameName, player1Name, player2Name, table)
            # print('Types:',  *(str(type(i)) for i in arguments))
            if isinstance(arguments[0], int) and all(obj is None for obj in arguments[1:]):
                self.current_cursor = database.current_cursor
                self.gameID = gameID
                # get gameName, player1Name, player2Name from JOIN. Order by PLAYERID to make sure the first entry (player one) comes first
                data = self.current_cursor.execute(f"SELECT p.PLAYERNAME, g.GAMENAME FROM Game AS g\
                                                     INNER JOIN Player AS p ON g.GAMEID = ? AND p.GAMEID = ? ORDER BY p.PLAYERID;", (gameID, gameID)).fetchall()
                if not data:
                    print("No players and games in database matching the value of %d" % gameID)
                    return
                # print("Join data is (PLAYERNAME, GAMENAME): ", *(str(i) for i in data), sep='\n')
                # player_1_name, player_2_name, game_name = data[0][0], data[1][0], data[0][1]
                # print("Player one name is:", player_1_name)
                # print("Player two name is:", player_2_name)
                # print("Table name is: '%s'" % game_name)
                self.table = database.readTable(gameID)
                
            elif (gameID is None and all((type(i) == str and i) for i in arguments[1:-1]) and isinstance(arguments[-1], Table)):
                self.table = table
                self.current_cursor = database.current_cursor
                self.current_cursor.execute("SELECT MAX (GAMEID) FROM Game;")
                data = self.current_cursor.fetchone()[0]
                # print("Biggest GAMEID in database is: " + str(data))
                if data is None: # this is the case where there are no GAMEIDs stored in the database
                    self.game_ID = 1 # from autoincrement
                else:
                    self.game_ID = int(data) + 1
                # print(f"Game ID set to {game_ID}")
                self.current_cursor.execute("INSERT INTO Game (GAMEID, GAMENAME) VALUES (?, ?);", (self.game_ID, gameName))
                # GAMEID autoincrements so do not actually need to insert it directly
                # data = self.current_cursor.execute(f"SELECT * FROM Game WHERE Game.GAMEID = {game_ID};").fetchall()
                # print("Game Table is: ", *(row for row in data), sep='\n')
                self.current_cursor.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?);", (self.game_ID, player1Name)) # need to do player one first
                self.current_cursor.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?);", (self.game_ID, player2Name))
                # self.current_cursor.execute(f"SELECT * FROM Player WHERE Player.GAMEID = {game_ID};")
                # data = self.current_cursor.fetchall()
                # print("Player Table is: ", *(row for row in data), sep='\n')
                player1_ID = self.current_cursor.execute("SELECT (PLAYERID) FROM Player WHERE Player.PLAYERNAME = ?;", (player1Name,)).fetchone()[0]
                # should be safe to index since Player was just updated
                # add the first player's shot into the table
                self.current_cursor.execute("INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?);", (player1_ID, self.game_ID))
                # data = self.current_cursor.execute("SELECT * FROM Shot").fetchall()
                # print("Shot table data: ", *(row for row in data), sep='\n')
                # write table to database now
                table_ID = database.writeTable(table)
                shot_ID = self.current_cursor.execute("SELECT MAX(SHOTID) FROM Shot;").fetchone()
                # print("SHOT ID is: ", *(value for value in shot_ID))
                self.current_cursor.execute(f"INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?);", (table_ID, shot_ID[0]))
                # data = self.current_cursor.execute("SELECT * FROM TableShot").fetchall()
                # print("TableShot is: ", *(row for row in data), sep='\n')
                # data = self.current_cursor.execute("SELECT * FROM Shot").fetchall()
                # print("Shot is: ", *(row for row in data), sep='\n')
            else:
                raise TypeError # throw an exception
            return
        
        def shoot(self, xvel, yvel):
            if not ((type(xvel) in (int, float)) or (type(yvel) in (int, float))):
                return
            shot_ID = self.current_cursor.execute(f"SELECT MAX(SHOTID) FROM Shot WHERE Shot.GAMEID = {self.game_ID}").fetchone()[0]
            if shot_ID is None:
                print("No shots made for current game") # should not occur
                return
            table_ID = self.current_cursor.execute(f"SELECT MAX(TABLEID) FROM TableShot WHERE TableShot.ShotID = {shot_ID}").fetchone()[0]
            if table_ID is None:
                print(f"No TableID from TableShot with an ID of {shot_ID}")
                return
            self.current_cursor.execute("""UPDATE Ball SET XVEL = ?, YVEL = ? WHERE Ball.BALLID = (
                                            SELECT b.BALLID FROM Ball as b INNER JOIN BallTable AS bt 
                                        ON b.BALLID = bt.BALLID WHERE b.BALLNO = 0 AND bt.TABLEID = ?)""", (xvel, yvel, table_ID,))
            
            self.table = self.database.readTable(table_ID) # update the table by rereading data
            segment_time = self.table.segment().time - self.table.time
            print("Segment time is: "+ str(segment_time))

            start_time = self.time.time()
            while True:
                # For demonstration, let's print something
                print("Running...")
                # Check elapsed time
                elapsed_time = self.time.time() - start_time
                # If elapsed time exceeds the specified duration, break the loop
                if elapsed_time >= SIM_RATE:
                    break
            return
