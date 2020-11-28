# **************************************** NOEVE Jungle Tracker v0.1 alpha ****************************************

import tkinter as tk
import tkinter.messagebox as tkmb
# import old_init
# import old_map_locator
# import queue
# import threading
# import old_sound_generator
import time
import sys
import src.sound_generator as sound_generator
import src.thread_generator as thread_generator


class MainGUI(tk.Tk):
    """ Class to generate MainGUI of NOEVE Jungle Tracker """

    def __init__(self):

        # ** Settings for runtime
        self.DEBUG_PLOTS = False
        self.PRACTICE_TOOL = False

        # ** Variables for runtime
        self.STOP = False
        self.top_gank_counter = 0
        self.mid_gank_counter = 0
        self.bot_gank_counter = 0
        self.init_thread = ()

        # ** Set basic GUI Parameters
        super(MainGUI, self).__init__()
        self.geometry("400x350")
        self.iconbitmap('dist/icon.ico')
        self.winfo_toplevel().title("NOEVE Jungle Tracker")

        # ** Create Drop-Down-Menu **
        self.drop_down_menu = tk.Menu(self)
        self.config(menu=self.drop_down_menu)
        self.file_menu = tk.Menu(self.drop_down_menu, tearoff=0)
        self.drop_down_menu.add_cascade(label='File', menu=self.file_menu)
        # self.file_menu.add_command(label='Placeholder Settings', command=self.open_settings)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.callback_quit)

        # ** Create Toolbar **
        self.toolbar = tk.Frame(self)
        self.run_all_button = tk.Button(self.toolbar, text='Run', command=self.run_button)
        self.run_all_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.init_button = tk.Button(self.toolbar, text='Reinit', command=self.reinit_button)
        self.init_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.practice_tool_var = tk.IntVar()
        self.practice_tool_cb = tk.Checkbutton(self.toolbar, text='Practice Tool', variable=self.practice_tool_var)
        self.practice_tool_cb.pack(side=tk.LEFT, padx=10, pady=2)
        self.stop_button = tk.Button(self.toolbar, text='Stop', command=self.stop_button)
        self.stop_button.pack(side=tk.RIGHT, padx=2, pady=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # ** Create Status-Bar **
        self.status_text = 'Ready'
        self.status_bar = tk.Label(self, bd=2, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.config(text=self.status_text)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # ** Frame for recognized Champion Information **
        self.champ_frame = tk.Frame(self)
        self.champ_name = tk.Label(self.champ_frame)
        self.champ_name.config(text='Press *Run* to track')
        self.champ_name.pack(side=tk.TOP)
        self.champ_image = tk.PhotoImage(file='images/noevejt.png')
        self.champ_image_label = tk.Label(self.champ_frame, image=self.champ_image)
        self.champ_image_label.pack(side=tk.TOP)
        self.bot_ganks_label = tk.Label(self.champ_frame)
        self.bot_ganks_label.pack(side=tk.BOTTOM)
        self.mid_ganks_label = tk.Label(self.champ_frame)
        self.mid_ganks_label.pack(side=tk.BOTTOM)
        self.top_ganks_label = tk.Label(self.champ_frame)
        self.top_ganks_label.pack(side=tk.BOTTOM)
        self.champ_frame.pack(side=tk.LEFT)

        # ** Status frame of Map Locator **
        self.map_frame = tk.Frame(self)
        self.position_name = tk.Label(self.map_frame)
        self.position_name.config(text='Jungler must be afk or was not seen yet ...')
        self.position_name.pack(side=tk.TOP)
        self.map_image_label = tk.Label(self.map_frame)
        self.map_image_label.pack(side=tk.TOP)
        self.map_frame.pack(side=tk.LEFT)

        # ** Protocol if Window is closed **
        self.protocol("WM_DELETE_WINDOW", self.callback_quit)

    # ********************************************** UTILITY FUNCTIONS **********************************************

    def update_status_bar(self, text):
        """ Updates the text of the status bar to the given Argument text """
        self.status_bar.config(text=text)
        self.status_bar.update_idletasks()

    def update_ganks_counter(self, lane):
        if lane == 'top':
            self.top_gank_counter =  self.top_gank_counter + 1
            text = 'Top Lane Ganks: ' + str(self.top_gank_counter)
            self.top_ganks_label.config(text=text)
            self.top_ganks_label.update_idletasks()
        if lane == 'mid':
            self.mid_gank_counter =  self.mid_gank_counter + 1
            text = 'Mid Lane Ganks: ' + str(self.mid_gank_counter)
            self.mid_ganks_label.config(text=text)
            self.mid_ganks_label.update_idletasks()
        if lane == 'bot':
            self.bot_gank_counter =  self.bot_gank_counter + 1
            text = 'Bot Lane Ganks: ' + str(self.bot_gank_counter)
            self.bot_ganks_label.config(text=text)
            self.bot_ganks_label.update_idletasks()

    def callback_quit(self):
        """ Defines what happens if the program is quit """
        if tkmb.askokcancel("Quit", "Do you really wish to quit?"):
            try:
                self.logger_thread.logger.close()
            except:
                print("Error L11: Could not close Logger File")
            sound_generator.quit()
            self.destroy()
            sys.exit()

    # *********************************************** DROP-DOWN-MENU ************************************************

    def open_settings(self):

        pass

    # *********************************************** TOOLBAR BUTTONS **********************************************

    def run_button(self):
        """ Starts with Initialization and then runs Jungle Tracking Loop - Resets Stop """
        self.STOP = False
        self.PRACTICE_TOOL = self.practice_tool_var.get()
        self.update_status_bar("Running ...")
        try:
            if self.init_thread.init.ROLES_ASSIGNED_FLAG:
                tracker_thread = thread_generator.TrackerThread(self.init_thread)
        except:
            self.init_thread = thread_generator.InitThread(self)
            tracker_thread = thread_generator.TrackerThread(self.init_thread)
        self.logger_thread = thread_generator.LoggerThread(self, self.init_thread, tracker_thread)
        # end of run_button()

    def reinit_button(self):
        """ Resets Champion Assignments - Continues with new Init and Jungle Tracking Loop """
        self.top_gank_counter = 0
        self.mid_gank_counter = 0
        self.bot_gank_counter = 0
        self.STOP = True
        self.update_status_bar("Reinitialization ...")
        # Sleep for 1 second to assure that all threads got the STOP signal
        time.sleep(1)
        self.init_thread = ()
        self.run_button()
        # end of reinit_button()

    def stop_button(self):
        """ Stops current Jungle Tracking Loop until the Loop is Run again or Reinited """
        self.STOP = True
        # end of stop_button()

