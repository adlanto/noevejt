# **************************************** NOEVE Jungle Tracker v0.1 alpha ****************************************

import src.gui as gui
import src.thread_generator as thread_generator

if __name__ == '__main__':

    thread_generator.welcome()
    root = gui.MainGUI()
    root.mainloop()
