import math
import time
import cv2 as cv
import numpy as np
import pyautogui

class FishingAgent:
    def __init__(self, main_agent) -> None:
        self.main_agent = main_agent
        self.fishing_target = cv.imread("C:\\Users\\eabil\\Documents\\code\\wowbot\\fishing\\assets\\image.png")

    def cast_lure(self):
        print("Casting lure...")
        time.sleep(2)
        pyautogui.press('1')
        time.sleep(2)
        self.find_lure()
        

    def find_lure(self):
        print("Waiting for screen update...")
        self.main_agent.screen_ready_event.wait()  # Wait for cur_img to be ready

        lure_location = cv.matchTemplate(
            self.main_agent.cur_img, 
            self.fishing_target,
            cv.TM_CCOEFF_NORMED
            )
        lure_location_array = np.array(lure_location)
        
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(lure_location_array)
        print(max_loc)

        self.move_to_lure(max_loc)


    def move_to_lure(self, max_loc):
        pyautogui.moveTo(max_loc[0], max_loc[1], 0.75, pyautogui.easeOutQuad)
        self.watch_lure(max_loc)

    def watch_lure(self, max_loc):
        watch_time = time.time()
        initial_H, initial_S, initial_V = self.main_agent.cur_imgHSV[max_loc[1], max_loc[0]].astype(int)
    
        while True:
            pixel_H, pixel_S, pixel_V = self.main_agent.cur_imgHSV[max_loc[1], max_loc[0]].astype(int)
            # Check if the difference in any HSV component is greater than 60
            if abs(sum([initial_H, initial_S, initial_V]) - sum([pixel_H, pixel_S, pixel_V])) >= 143 and abs(initial_H - pixel_H >= 4):
                # Logic for detecting the bite

                print("Bite detected!")
                print([initial_H, initial_S, initial_V])
                print([pixel_H, pixel_S, pixel_V])
                print(sum([initial_H, initial_S, initial_V]) - sum([pixel_H, pixel_S, pixel_V]))
                self.pull_line()
                break
            else:
                pass
                # print(sum([initial_H, initial_S, initial_V]) - sum([pixel_H, pixel_S, pixel_V]))
                # print([pixel_H, pixel_S, pixel_V])
            
            if time.time() - watch_time >= 15:
                break

        print("YOY")

    def pull_line(self):
        print("Pulling line!")
        pyautogui.keyDown("shift")
        time.sleep(0.005)
        pyautogui.click(button='right')
        time.sleep(0.010)
        pyautogui.keyUp('shift')

    def run(self):
        while True:
            self.cast_lure()
            time.sleep(5)


if __name__ == "__main__":
    main_agent = None
    fishing_agent = FishingAgent(main_agent)
    fishing_agent.run()