# **************************************** NOEVE Jungle Tracker v0.1 alpha ****************************************
import time
import cv2
import numpy as np
from PIL import ImageTk, ImageGrab
import src.sound_generator as sound_generator


def divide_map(x, y):

    # 1.1 Top Lane
    if x <= 140 and y <= (140 - x):
        return 'top lane'

    # 1.2 Bot Lane
    if x >= 114 and y >= (368 - x):
        return 'bot lane'

    # 2.1 Blue Jungle:
    if x <= 194 and y >= (60 + x):

        # 2.1.1 Blue Top Side Jungle
        if x <= 127 and y <= (254 - x):
            return 'blue top jungle'

        # 2.1.2 Blue Bot Side Jungle
        if x < 194 and y > (60 + x):
            return 'blue bot jungle'

    # 2.1 Red Jungle:
    if x >= 60 and y <= (-60 + x):

        # 2.1.1 Red Top Side Jungle
        if x <= 254 and y <= (254 - x):
            return 'red top jungle'

        # 2.1.2 Blue Bot Side Jungle
        if x > 127 and y > (254 - x):
            return 'red bot jungle'

    # 3.1 Baron Area
    if x <= 180 and y <= (180 - x):
        return 'baron'

    # 3.1 Dragon Area
    if x >= 74 and y >= (328 - x):
        return 'dragon'

    # Mid Line by default - all other parts of map will be divided
    return 'mid lane'

    # end of divide_map()


class Tracker:

    def __init__(self, tracker_thread, init_thread):
        self.init_thread = init_thread
        # Containing .init.CHAMPS_ROLES, see below
        # **Champion Roles Keys**    Ally        Enemy
        # Top Lane                    0            1
        # Jungle                      2            3
        # Mid Lane                    4            5
        # Bottom Lane                 6            7
        # Support                     8            9

        # Define variables for later use
        self.frame = ()
        self.frame_grabbed = ()
        self.champion_templates = {}
        self.champion_positions = {}
        self.champion_recognition_thresholds = {}
        self.frame_counter = 0
        self.last_position = ''
        # end of __init__()

    def grab_map_frame(self):
        """ Method to grab frames and save it in Instance of init """
        self.frame_grabbed = ImageGrab.grab(bbox=(1654, 814, 1908, 1068))
        self.frame = cv2.cvtColor(np.array(self.frame_grabbed), cv2.COLOR_RGB2BGR)
        # end of grab_map_frame()

    def generate_jungle_located_signal(self, position):
        print(('Enemy jungle located in ' + position[0]))
        # Sound Output
        sound_generator.position(position[0])
        # Plot map in GUI
        self.init_thread.gui.map_image = ImageTk.PhotoImage(image=self.frame_grabbed)
        self.init_thread.gui.map_image_label.map_image = self.init_thread.gui.map_image
        self.init_thread.gui.map_image_label.config(image=self.init_thread.gui.map_image)
        self.init_thread.gui.position_name.config(text='Last seen position: ' + str(position[0]))
        self.init_thread.gui.position_name.update_idletasks()
        self.last_position = position[0]
        if position[0] == 'top lane':
            self.init_thread.gui.update_ganks_counter('top')
        if position[0] == 'mid lane':
            self.init_thread.gui.update_ganks_counter('mid')
        if position[0] == 'bot lane':
            self.init_thread.gui.update_ganks_counter('bot')
        # end of generate_jungle_located_signal()

    def visualize_jungle_location(self, position):
        self.frame_counter = self.frame_counter + 1
        if self.last_position != position[0]:
            self.generate_jungle_located_signal(position)
            return
        if self.frame_counter > 200:
            self.generate_jungle_located_signal(position)
            self.frame_counter = 0
            return
        # end of visualize_jungle_location()

    def locate_champions(self):
        for i, champion_template in enumerate(self.champion_templates.values()):
            if isinstance(champion_template, list):
                depth, w, h = champion_template[0].shape[::-1]
                # print('Kayn was picked - trying to locate all forms')
                res = cv2.matchTemplate(self.frame, self.champion_templates[i][0], cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                res_sa = cv2.matchTemplate(self.frame, self.champion_templates[i][1], cv2.TM_CCOEFF_NORMED)
                min_val_sa, max_val_sa, min_loc_sa, max_loc_sa = cv2.minMaxLoc(res_sa)
                res_rhaast = cv2.matchTemplate(self.frame, self.champion_templates[i][2], cv2.TM_CCOEFF_NORMED)
                min_val_rhaast, max_val_rhaast, min_loc_rhaast, max_loc_rhaast = cv2.minMaxLoc(res_rhaast)
                if max_val_sa > max_val and max_val_sa > max_val_rhaast:
                    max_loc = max_loc_sa
                    max_val = max_val_sa
                if max_val_rhaast > max_val and max_val_rhaast > max_val_sa:
                    max_loc = max_loc_rhaast
                    max_val = max_val_rhaast
            else:
                depth, w, h = champion_template.shape[::-1]
                res = cv2.matchTemplate(self.frame, self.champion_templates[i], cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            top_left = max_loc
            if max_val > self.champion_recognition_thresholds[i]:
                x = int(top_left[0] + w / 2)
                y = int(top_left[1] + h / 2)
                self.champion_positions[i] = [divide_map(x, y), x, y]
            else:
                self.champion_positions[i] = ['', -1, -1]
        # end of locate_champion()

    def load_champions(self):
        """ Method to load champion images from drive """
        for i, champion in enumerate(self.init_thread.init.CHAMPS_ROLES.values()):
            self.champion_templates[i] = cv2.imread("champions_map_templates/" + champion + ".png")
            if champion == 'Kayn':
                normal_image = self.champion_templates[i]
                sa_image = cv2.imread('champions_map_templates/SAKayn.png')
                rhaast_image = cv2.imread('champions_map_templates/Rhaast.png')
                self.champion_templates[i] = [normal_image, sa_image, rhaast_image]
            if champion == 'Pantheon':
                self.champion_recognition_thresholds[i] = 0.8
            else:
                self.champion_recognition_thresholds[i] = 0.7
        # end of load_champions()

    def loop(self):
        """ Main Loop for Tracking the Enemy Champions  - Grabs Frames and Interprets them """
        # Waits for init flag to be set
        while not self.init_thread.init.ROLES_ASSIGNED_FLAG:
            time.sleep(0.1)
        self.load_champions()
        self.init_thread.gui.update_status_bar("Map locator is running ...")
        while not self.init_thread.gui.STOP:
            try:
                self.grab_map_frame()
            except:
                print('Error I01: Image Grab Failed.')
            if self.frame != ():
                self.locate_champions()
                # for i, champ_name in enumerate(self.init_thread.init.CHAMPS_ROLES.values()):
                #     if self.champion_positions[i][0] != '':
                #         print(champ_name, 'was seen', self.champion_positions[i][0], '[' +
                #               str(self.champion_positions[i][1]) + ', ' + str(self.champion_positions[i][2]) + ']')
                if self.init_thread.gui.PRACTICE_TOOL:
                    if self.champion_positions[2][0] != '':
                        self.visualize_jungle_location(self.champion_positions[2])
                else:
                    if self.champion_positions[3][0] != '':
                        self.visualize_jungle_location(self.champion_positions[3])
        if self.init_thread.gui.STOP:
            self.init_thread.gui.update_status_bar('Tracker stopped. '
                                                   'Press *RUN* to continue or *REININT* to reassign roles.')
        # end of loop()
