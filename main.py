from PIL import Image, ImageGrab
import mss
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
    with mss.mss() as sct:
        fps_report_delay = 5  # Print FPS every 5 seconds
        fps_report_time = time.time()
        frame_count = 0  # Count frames

        while True:
            agent.screen_ready_event.clear()  # Mark image as "not ready"

            screenshot = sct.grab(sct.monitors[1])  # Capture primary screen
            agent.cur_img = np.array(screenshot)
            agent.cur_img = cv.cvtColor(agent.cur_img, cv.COLOR_BGRA2BGR)
            agent.cur_imgHSV = cv.cvtColor(agent.cur_img, cv.COLOR_BGR2HSV)

            agent.screen_ready_event.set()  # Mark image as "ready"

            # FPS Calculation
            frame_count += 1
            if time.time() - fps_report_time >= fps_report_delay:
                fps = frame_count / fps_report_delay
                print(f"FPS: {fps:.2f}")
                fps_report_time = time.time()
                frame_count = 0  # Reset frame count


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
