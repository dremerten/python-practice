"""
Setting Up Our Robot

Let’s begin by creating the class for our robot. We will begin by setting up the instance variables to keep track of important data related to the robot. 
Here are the steps we need to do:

    Create a new class called DriveBot
    Set up a basic constructor (no parameters needed)
    Initialize three instance variables within our constructor which all default to 0: motor_speed, direction, and sensor_range
"""

class DriveBot:
    all_disabled = False
    latitude = float('-inf') # ====> Negative Infinity
    longitude = float('-inf')
    robot_count = 0

    def __init__(self, motor_speed=0, direction=180, sensor_range=10):
        self.motor_speed = motor_speed
        self.direction = direction
        self.sensor_range = sensor_range
        DriveBot.robot_count += 1
        self.id = DriveBot.robot_count
    
    def control_bot(self, new_speed, new_direction):
        self.motor_speed = new_speed
        self.direction = new_direction

    def adjust_sensor(self, new_sensor_range):
        self.sensor_range = new_sensor_range

