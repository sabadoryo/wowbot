import random

class MovementAgent:
    def __init__(self, position=(0, 0)):
        self.position = position
        self.waypoints = []

    def move_up(self, distance=1):
        x, y = self.position
        self.position = (x, y + distance)

    def move_down(self, distance=1):
        x, y = self.position
        self.position = (x, y - distance)

    def move_left(self, distance=1):
        x, y = self.position
        self.position = (x - distance, y)

    def move_right(self, distance=1):
        x, y = self.position
        self.position = (x + distance, y)

    def get_position(self):
        return self.position

    def set_waypoints(self, waypoints):
        self.waypoints = waypoints

    def patrol(self):
        if not self.waypoints:
            raise ValueError("Waypoints not set or empty")
        self.position = random.choice(self.waypoints)
        self.current_waypoint_index = self.waypoints.index(self.position)

    def save_position(self):
        self.saved_position = self.position

    def load_position(self):
        if hasattr(self, 'saved_position'):
            self.position = self.saved_position
            self.current_waypoint_index = self.waypoints.index(self.position)
        else:
            print("No saved position found.")

    def continue_patrol(self):
        if not self.waypoints:
            raise ValueError("Waypoints not set or empty")
        if not hasattr(self, 'current_waypoint_index'):
            self.current_waypoint_index = 0
        next_index = random.choice([i for i in range(len(self.waypoints)) if i != self.current_waypoint_index])
        self.position = self.waypoints[next_index]
        self.current_waypoint_index = next_index