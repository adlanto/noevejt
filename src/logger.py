import time


class Logger():

    def __init__(self, logger_thread):
        # logger_thread.gui.update_status_bar("Log file saved")

        # Open Logger file - create Template ...

        self.logger_thread = logger_thread
        self.champion_names = {}
        self.champion_map = {}
        self.positions = {}
        self.STOP = False
        self.lines = []

    def update(self):

        # Define empty dictionary of champions assigned to their roles
        # **Champion Roles Keys**    Ally        Enemy
        # Top Lane                    0            1
        # Jungle                      2            3
        # Mid Lane                    4            5
        # Bottom Lane                 6            7
        # Support                     8            9
        # Champion names are saved as values to the corresponding keys above
        self.champion_names = self.logger_thread.init_thread.init.CHAMPS_ROLES

        # Dictionary of keys (above) and roles (values)
        self.champion_map = self.logger_thread.init_thread.init.ROLE_POSITION_MAP

        # If stop button is pressed
        self.STOP = self.logger_thread.init_thread.gui.STOP

        # Positions of champions [0] Current Position e.g. Top Lane [1] x [2] y (origin: top left corner)
        self.positions = self.logger_thread.tracker_thread.tracker.champion_positions
        # example: self.positions[0] will give you ['Top Lane', 20, 20]
        # if it was not spotted in this tracking loop: ['', -1, -1]


    def loop(self):

        while not self.logger_thread.gui.STOP:
            line = []
            self.update()

            # write information in line as dictionary / as lists / ...
            # example: line.append(champ_info)
            # do something: create new line and append it
            self.lines.append(line)
            time.sleep(0.1)

    def close(self):
        self.logger_thread.gui.top_gank_counter
        self.logger_thread.gui.mid_gank_counter
        self.logger_thread.gui.bot_gank_counter
        # Conversion to dataframe
        # save to .csv
        # Will be opened automatically when window is closed







