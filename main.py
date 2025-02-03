from PIL import Image, ImageGrab
import numpy as np
import cv2 as cv
import time 
from threading import Event, Thread
from fishing.fishing_agent import FishingAgent
import pydirectinput 

class MainAgent:
    def __init__(self):
        self.agents = []
        self.fishing_thread = None
        
        self.cur_img = None
        self.cur_imgHSV = None

        self.zone = "Feralas"
        self.time = "night"

        self.screen_ready_event = Event()

        print("MainAgent setup complete...")



def update_screen(agent):

    t0 = time.time()
    fps_report_delay = 5
    fps_report_time = time.time()

    while True: 
        agent.screen_ready_event.clear()  # Mark image as "not ready"

        agent.cur_img = ImageGrab.grab()
        agent.cur_img= np.array(agent.cur_img)
        agent.cur_img = cv.cvtColor(agent.cur_img, cv.COLOR_RGB2BGR)
        agent.cur_imgHSV = cv.cvtColor(agent.cur_img, cv.COLOR_BGR2HSV)

        agent.screen_ready_event.set()  # Mark image as "ready"
        
        ex_time = time.time() - t0

        if time.time() - fps_report_time >= fps_report_delay:
            print("FPS: " + str(1 / (ex_time)))
            fps_report_time = time.time()


        t0 = time.time()

def print_menu():
    print("Enter a command:")
    print("\tS\tStart the main agent.")
    print("\tZ\tSet zone var.")
    print("\tF\tStart the fishing agent.")
    print("\tQ\tQuit.")

if __name__ == "__main__":
    main_agent = MainAgent()
    
    print_menu()

    while True:
        user_input = input()
        user_input = str.lower(user_input).strip()

        if user_input == "s":
            update_screen_thread = Thread(
                target=update_screen, 
                args=(main_agent,), 
                name="update screen thread",
                daemon=True
            )
            update_screen_thread.start()
            print("Thread started")
        elif user_input == "z":
            pass
        elif user_input == "f":
            fishing_agent = FishingAgent(main_agent)
            fishing_agent.run()

        elif user_input == "q":
            cv.destroyAllWindows()
            break
        elif user_input == "t":
            time.sleep(5)
            pydirectinput.keyDown("w")
        else:
            print("Input error.")
            print_menu()

    print("Done...")
