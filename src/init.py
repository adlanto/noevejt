# **************************************** NOEVE Jungle Tracker v0.1 alpha ****************************************

import cv2
import glob
import operator
import numpy as np
from PIL import ImageGrab
import time
import src.sound_generator as sound_generator


class Init:

    def __init__(self, thread):
        """ Loads all templates from the disk and saves them in Init instance """

        # Add instance of thread to Init instance - thread contains thread.gui
        self.thread = thread
        # Read tab template from disk and save in Init instance
        self.tab_template = cv2.imread('templates/tab_template.png')

        # Read smite image and save in Init instance
        self.smite_template = cv2.imread('templates/smite.png')
        self.smite_template_blue = cv2.imread('templates/smite_blue.png')
        self.smite_template_red = cv2.imread('templates/smite_red.png')
        self.smite_depth, self.smite_width, self.smite_height = self.smite_template.shape[::-1]

        # Read champion templates and save in Init instance as dictionary
        self.champion_templates = {}
        for champ_image_path in glob.glob('champions_tab_templates/*.png'):
            image = cv2.imread(champ_image_path)
            name = (champ_image_path[24:-4])
            self.champion_templates[name] = image

        # Define variables of Init instance
        self.ROLES_ASSIGNED_FLAG = False
        self.TAB_FOUND_FLAG = False
        # Define empty dictionary of champions assigned to their roles
        # **Champion Roles Keys**    Ally        Enemy
        # Top Lane                    0            1
        # Jungle                      2            3
        # Mid Lane                    4            5
        # Bottom Lane                 6            7
        # Support                     8            9
        self.ROLE_POSITION_MAP = {
            0: "Ally Top Lane",
            1: "Enemy Top Lane",
            2: "Ally Jungle",
            3: "Enemy Jungle",
            4: "Ally Mid Lane",
            5: "Enemy Mid Lane",
            6: "Ally Bottom Lane",
            7: "Enemy Bottom Lane",
            8: "Ally Support",
            9: "Enemy Support"
        }
        self.champion_frames = {}
        self.CHAMPS_ROLES = {}
        # Define frame variables
        self.frame = ()
        # Define smite image variables

        # Areas to select in Tab Frame
        self.tab_frame = {}
        self.tab_frame_h = 120
        self.tab_frame_v = 380
        self.tab_frame_v_dis = 135
        self.tab_frame_h_dis = {}
        self.tab_frame_h_dis_blue = -265
        self.tab_frame_h_dis_red = 310
        self.champion_recognition_area_size = (60, 120, 78)
        # end of __init__()

    def grab_frame(self):
        """ Method to grab frames and save it in Instance of init """
        frame_grabbed = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
        self.frame = cv2.cvtColor(np.array(frame_grabbed), cv2.COLOR_RGB2BGR)
        # end of grab_frame()

    def assign_champ_to_role(self, champ_frame):
        """ Assigns a Role to a given Champion Frame """
        probabilities = {}
        for champ_name in self.champion_templates.keys():
            res = cv2.matchTemplate(champ_frame, self.champion_templates[champ_name], cv2.TM_CCOEFF_NORMED)
            probabilities[champ_name] = np.amax(res)
        # print(probabilities)
        return max(probabilities.items(), key=operator.itemgetter(1))[0]
        # end of assign_role_to_champ()

    def validate_jungle(self):
        res = cv2.matchTemplate(self.tab_frame["Enemy"], self.smite_template, cv2.TM_CCOEFF_NORMED)
        res_blue = cv2.matchTemplate(self.tab_frame["Enemy"], self.smite_template_blue, cv2.TM_CCOEFF_NORMED)
        res_red = cv2.matchTemplate(self.tab_frame["Enemy"], self.smite_template_red, cv2.TM_CCOEFF_NORMED)
        res_list = [res, res_blue, res_red]
        max_res_list = [np.amax(res), np.amax(res_blue), np.amax(res_red)]
        highest_res_index = np.argmax(max_res_list)
        res = res_list[highest_res_index]
        if max_res_list[highest_res_index] < 0.8:
            self.thread.gui.update_status_bar("No smite found in enemy team")
            time.sleep(2)
            self.thread.gui.update_status_bar("Assuming smite was just forgot to be picked")
            time.sleep(2)
            return
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + self.smite_width, top_left[1] + self.smite_height)
        if self.thread.gui.DEBUG_PLOTS:
            tab_frame_copy = self.tab_frame["Enemy"].copy()
            cv2.rectangle(tab_frame_copy, top_left, bottom_right, 255, 2)
        if top_left[1] - 50 < self.champion_recognition_area_size[2] < top_left[1] + 50:
            pass
        else:
            tmp = self.tab_frame["Enemy"][top_left[1] - 28:bottom_right[1] + 28, top_left[0] + 50:bottom_right[0] + 90]
            self.CHAMPS_ROLES[3] = self.assign_champ_to_role(tmp)
            text = "Jungler was not on correct position - updated jungle is " + str(self.CHAMPS_ROLES[3])
            self.thread.gui.update_status_bar(text)
        # end of validate_jungle()

    def get_roles_from_tab_frame(self):
        """ Method to assign role to each champion in tab frame """
        # Iterate over parts of the tab frame image from top lane to support
        # Top Lane - Jungle - Mid Lane - Bottom Lane - Support
        for i in range(5):
            x_start = self.champion_recognition_area_size[0]
            x_end = self.champion_recognition_area_size[1]
            y_start = self.champion_recognition_area_size[2] * i
            y_end = self.champion_recognition_area_size[2] * (i + 1)
            # Roles map to be seen in init
            self.champion_frames[i] = self.tab_frame["Enemy"][y_start:y_end, x_start:x_end]
            self.champion_frames[i + 5] = self.tab_frame["Ally"][y_start:y_end, x_start:x_end]
            if self.thread.gui.DEBUG_PLOTS:
                cv2.imshow("self.champion_frames[i]", self.champion_frames[i])
                cv2.imshow("self.champion_frames[i+5]", self.champion_frames[i + 5])
                cv2.waitKey(3000)
        for i, champ_frame in enumerate(self.champion_frames.values()):
            self.CHAMPS_ROLES[i] = self.assign_champ_to_role(champ_frame)
            print(self.ROLE_POSITION_MAP[i], 'is', self.CHAMPS_ROLES[i])
        self.validate_jungle()
        self.ROLES_ASSIGNED_FLAG = True
        # end of get_roles_from_tab_frame()

    def detect_map_side(self):
        """ Method to detect which side ally or enemy team is """
        map_image = self.frame[814:1068, 1654:1908]
        gray_map = cv2.cvtColor(map_image, cv2.COLOR_BGR2GRAY)
        if gray_map[159, 95] <= gray_map[95, 159]:
            self.tab_frame_h_dis["Ally"] = self.tab_frame_h_dis_blue
            self.tab_frame_h_dis["Enemy"] = self.tab_frame_h_dis_red
        else:
            self.tab_frame_h_dis["Enemy"] = self.tab_frame_h_dis_blue
            self.tab_frame_h_dis["Ally"] = self.tab_frame_h_dis_red
        # end of detect_map_side()

    def detect_tab_frame(self):
        """ Method to detect Tab Frame with given template """
        try:
            self.grab_frame()
        except:
            print('Error I01: Image Grab Failed.')
            return
        self.detect_map_side()
        res = cv2.matchTemplate(image=self.frame, templ=self.tab_template, method=cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print(max_val)
        if max_val > 0.8:
            self.TAB_FOUND_FLAG = True
            print("Tab found")
            # Snip Ally Tab Frame out of Tab Image
            top_left = (max_loc[0] + self.tab_frame_h_dis["Ally"], max_loc[1] + self.tab_frame_v_dis)
            bottom_right = (top_left[0] + self.tab_frame_h, top_left[1] + self.tab_frame_v)
            self.tab_frame['Ally'] = self.frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
            # Snip Enemy Tab Frame out of Tab Image
            top_left = (max_loc[0] + self.tab_frame_h_dis["Enemy"], max_loc[1] + self.tab_frame_v_dis)
            bottom_right = (top_left[0] + self.tab_frame_h, top_left[1] + self.tab_frame_v)
            self.tab_frame['Enemy'] = self.frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
            if self.thread.gui.DEBUG_PLOTS:
                frame_edit_copy = self.frame.copy()
                cv2.rectangle(frame_edit_copy, top_left, bottom_right, 255, 2)
                cv2.imshow('TAB_RECOGNIZED.png', frame_edit_copy)
                cv2.waitKey(2000)
        # end of detect_tab_frame()

    def loop(self, thread_queue=None):
        """ Main Loop for Initialization - Grabs Frames and Interprets them """
        # Grab new image and analyze it as long as init is not successful
        self.thread.gui.update_status_bar('Init process started - waiting for tab frame')
        while not self.ROLES_ASSIGNED_FLAG and not self.thread.gui.STOP:
            while not self.TAB_FOUND_FLAG and not self.thread.gui.STOP:
                self.detect_tab_frame()
            self.thread.gui.update_status_bar('Tab frame found - assigning roles')
            self.get_roles_from_tab_frame()
            if self.ROLES_ASSIGNED_FLAG:
                break
        if not self.thread.gui.STOP:
            if self.thread.gui.PRACTICE_TOOL:
                self.thread.gui.update_status_bar('Init successful - tracked jungle is ' + str(self.CHAMPS_ROLES[2]))
                self.thread.gui.champ_name.config(text='Tracked Jungle: ' + str(self.CHAMPS_ROLES[2]))
                image_path = 'champions_original_squares/' + str(self.CHAMPS_ROLES[2]) + 'Square.png'
                self.thread.gui.champ_image.config(file=image_path)
                sound_generator.init_success(str(self.CHAMPS_ROLES[2]))
            else:
                self.thread.gui.update_status_bar('Init successful - tracked jungle is ' + str(self.CHAMPS_ROLES[3]))
                self.thread.gui.champ_name.config(text='Tracked Jungle: ' + str(self.CHAMPS_ROLES[3]))
                image_path = 'champions_original_squares/' + str(self.CHAMPS_ROLES[3]) + 'Square.png'
                self.thread.gui.champ_image.config(file=image_path)
                sound_generator.init_success(str(self.CHAMPS_ROLES[3]))
        else:
            self.thread.gui.update_status_bar("Initialization stopped. Press *RUN* or *REINIT* to start again.")
        # end of loop()
