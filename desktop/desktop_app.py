import sys
import os

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, base_dir)

from learn_assistant_gui import LearnAssistantGUI

def main():
    app = LearnAssistantGUI()
    app.run()

if __name__ == "__main__":
    main()
