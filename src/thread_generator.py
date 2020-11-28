# **************************************** NOEVE Jungle Tracker v0.1 alpha ****************************************

import threading
import queue
import src.sound_generator as sound_generator
from src.init import Init
from src.tracker import Tracker
from src.logger import Logger


def create_and_start_thread(target, thread_queue=False):
    """ Creates a new thread and starts it """
    if thread_queue:
        thread_queue = queue.Queue()
        thread = threading.Thread(target=target, kwargs={'thread_queue': thread_queue})
        thread.start()
        return thread, thread_queue
    else:
        thread = threading.Thread(target=target)
        thread.start()
        return thread


def welcome():
    """ Creates Welcome Sound Thread and runs Sound """
    thread_welcome = create_and_start_thread(sound_generator.welcome)


class InitThread:
    """ Creates an Init Thread and Loops until Init is successful or Application is stopped """

    def __init__(self, gui):
        self.INIT_SUCCESS_FLAG = False
        self.gui = gui
        self.init = Init(self)
        self.thread = create_and_start_thread(self.init.loop)


class TrackerThread:
    """ Creates a Tracker Thread and Loops until Application is stopped """

    def __init__(self, init_thread):
        self.tracker = Tracker(self, init_thread)
        self.thread = create_and_start_thread(self.tracker.loop)


class LoggerThread:
    """ """

    def __init__(self, gui, init_thread, tracker_thread):
        self.gui = gui
        self.init_thread = init_thread
        self.tracker_thread = tracker_thread
        self.logger = Logger(self)
        self.thread = create_and_start_thread(self.logger.loop)
