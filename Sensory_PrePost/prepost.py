import tkinter as tk
from tkinter import messagebox
import random
import pandas as pd
import os
import datetime
import time
from PIL import Image, ImageTk
import serial  # for arduino
import pygame  # for playing beep sound
pygame.mixer.init()# Initialize pygame mixer for sound

# Initialize Arduino serial connection
arduino_connected = False
ser = None
try:
    COM_PORT = '/dev/cu.usbmodem143101'  # Change to match your Arduino's port
    BAUD_RATES = 9600
    ser = serial.Serial(COM_PORT, BAUD_RATES, timeout=3)
    arduino_connected = True
    print(f"Connected to Arduino on {COM_PORT}")
    
    # Wait for Arduino to initialize and send ready message
    arduino_ready = False
    timeout = time.time() + 5  # 5 second timeout
    
    while time.time() < timeout and not arduino_ready:
        if ser.in_waiting:
            response = ser.readline().decode().strip()
            print(f"Arduino init message: {response}")
            if "ARDUINO_READY" in response:
                arduino_ready = True
        time.sleep(0.1)
    
    if not arduino_ready:
        print("Warning: Arduino ready message not received, continuing anyway...")
    
    # Flush any remaining data
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    time.sleep(0.5)
    
    # Synchronize time with Arduino using a single command with the timestamp
    # Send with full precision including milliseconds
    current_unix_time = time.time()  # Get timestamp with milliseconds
    time_cmd = f"T:{current_unix_time}\n"
    print(f"Sending time sync command: {time_cmd.strip()}")
    
    # Send the combined command
    ser.write(time_cmd.encode())
    
    # Wait for sync confirmation with timeout
    sync_timeout = time.time() + 5  # 5 second timeout
    sync_received = False
    
    while time.time() < sync_timeout and not sync_received:
        if ser.in_waiting:
            response = ser.readline().decode().strip()
            print(f"Arduino response: {response}")
            
            if response.startswith("SYNC_OK:"):
                arduino_time_str = response.split(":")[1]
                arduino_time = float(arduino_time_str)  # Convert to float to preserve decimals
                time_diff = abs(current_unix_time - arduino_time)
                print(f"Arduino time synchronized successfully!")
                print(f"Python time: {current_unix_time}, Arduino time: {arduino_time}")
                print(f"Time difference: {time_diff} seconds")
                sync_received = True
            elif response.startswith("SYNC_ERROR:"):
                print(f"Error synchronizing: {response}")
                # Try again with a short delay
                time.sleep(0.5)
                current_unix_time = time.time()  # Get fresh timestamp with milliseconds
                time_cmd = f"T:{current_unix_time}\n"
                print(f"Retrying with: {time_cmd.strip()}")
                ser.write(time_cmd.encode())
        time.sleep(0.1)  # Short delay to prevent CPU hogging
    
    if not sync_received:
        print("Warning: Arduino time synchronization failed after multiple attempts")
        # Continue anyway, but with a warning
        
except Exception as e:
    arduino_connected = False
    print(f"Failed to connect to Arduino: {e}")
    
# Function to play beep sound
def play_beep():
    try:
        pygame.mixer.music.load("beep.wav")
        pygame.mixer.music.play(loops=0)
    except Exception as e:
        print(f"Error playing sound: {e}")

# Global variables for participant ID and block type
participant_id = None
block_type = None
start_timestamp = None

# Configurable trial numbers
VISUAL_TRIAL_COUNT = 40 
PROPRIOCEPTIVE_TRIAL_COUNT = 40 
OPENLOOP_TRIAL_COUNT = 40

# Global styling variables
basic_font = 'Helvetica 40 bold'
title_font = 'Helvetica 60 bold'
background_color = 'black'
light_color = "#888888"

# Predefined circle sequences
circle_set_100trial = {
    "1_circle_set_100trial": ['circle_4', 'circle_7', 'circle_8', 'circle_9', 'circle_6', 'circle_3', 'circle_2', 'circle_1', 'circle_9', 'circle_4', 'circle_2', 'circle_6', 'circle_1', 'circle_8', 'circle_3', 'circle_7', 'circle_4', 'circle_2', 'circle_7', 'circle_3', 'circle_6', 'circle_9', 'circle_8', 'circle_1', 'circle_6', 'circle_2', 'circle_4', 'circle_1', 'circle_7', 'circle_8', 'circle_9', 'circle_3', 'circle_2', 'circle_8', 'circle_3', 'circle_6', 'circle_7', 'circle_1', 'circle_9', 'circle_4', 'circle_2', 'circle_9', 'circle_6', 'circle_7', 'circle_3', 'circle_8', 'circle_4', 'circle_1', 'circle_7', 'circle_3', 'circle_2', 'circle_6', 'circle_8', 'circle_4', 'circle_9', 'circle_1', 'circle_2', 'circle_9', 'circle_7', 'circle_8', 'circle_6', 'circle_3', 'circle_1', 'circle_4', 'circle_3', 'circle_8', 'circle_9', 'circle_2', 'circle_1', 'circle_4', 'circle_7', 'circle_6', 'circle_9', 'circle_1', 'circle_6', 'circle_2', 'circle_7', 'circle_3', 'circle_8', 'circle_4', 'circle_1', 'circle_2', 'circle_8', 'circle_7', 'circle_3', 'circle_6', 'circle_9', 'circle_4', 'circle_1', 'circle_4', 'circle_7', 'circle_2', 'circle_8', 'circle_6', 'circle_3', 'circle_9', 'circle_3', 'circle_8', 'circle_7', 'circle_3'],
    "2_circle_set_100trial": ['circle_3', 'circle_8', 'circle_4', 'circle_1', 'circle_7', 'circle_9', 'circle_2', 'circle_6', 'circle_2', 'circle_8', 'circle_3', 'circle_7', 'circle_4', 'circle_6', 'circle_1', 'circle_9', 'circle_4', 'circle_7', 'circle_3', 'circle_1', 'circle_8', 'circle_2', 'circle_6', 'circle_9', 'circle_1', 'circle_8', 'circle_9', 'circle_6', 'circle_7', 'circle_3', 'circle_4', 'circle_2', 'circle_1', 'circle_6', 'circle_7', 'circle_3', 'circle_8', 'circle_4', 'circle_9', 'circle_2', 'circle_7', 'circle_1', 'circle_8', 'circle_6', 'circle_9', 'circle_4', 'circle_2', 'circle_3', 'circle_9', 'circle_6', 'circle_2', 'circle_4', 'circle_8', 'circle_7', 'circle_3', 'circle_1', 'circle_9', 'circle_4', 'circle_2', 'circle_7', 'circle_8', 'circle_1', 'circle_6', 'circle_3', 'circle_6', 'circle_9', 'circle_1', 'circle_7', 'circle_4', 'circle_2', 'circle_8', 'circle_3', 'circle_4', 'circle_8', 'circle_1', 'circle_2', 'circle_9', 'circle_3', 'circle_6', 'circle_7', 'circle_1', 'circle_2', 'circle_8', 'circle_3', 'circle_4', 'circle_9', 'circle_6', 'circle_7', 'circle_6', 'circle_2', 'circle_3', 'circle_8', 'circle_9', 'circle_1', 'circle_4', 'circle_7', 'circle_1', 'circle_9', 'circle_7', 'circle_1'],
    "3_circle_set_100trial": ['circle_7', 'circle_1', 'circle_6', 'circle_3', 'circle_9', 'circle_8', 'circle_2', 'circle_4', 'circle_8', 'circle_4', 'circle_9', 'circle_3', 'circle_2', 'circle_6', 'circle_7', 'circle_1', 'circle_3', 'circle_6', 'circle_8', 'circle_9', 'circle_4', 'circle_2', 'circle_7', 'circle_1', 'circle_8', 'circle_3', 'circle_7', 'circle_4', 'circle_6', 'circle_9', 'circle_1', 'circle_2', 'circle_3', 'circle_4', 'circle_9', 'circle_8', 'circle_6', 'circle_1', 'circle_2', 'circle_7', 'circle_1', 'circle_9', 'circle_2', 'circle_3', 'circle_4', 'circle_6', 'circle_8', 'circle_7', 'circle_3', 'circle_2', 'circle_4', 'circle_8', 'circle_1', 'circle_6', 'circle_9', 'circle_7', 'circle_3', 'circle_8', 'circle_6', 'circle_4', 'circle_7', 'circle_9', 'circle_2', 'circle_1', 'circle_4', 'circle_9', 'circle_6', 'circle_2', 'circle_8', 'circle_1', 'circle_7', 'circle_3', 'circle_6', 'circle_2', 'circle_8', 'circle_9', 'circle_3', 'circle_7', 'circle_1', 'circle_4', 'circle_3', 'circle_9', 'circle_7', 'circle_2', 'circle_8', 'circle_1', 'circle_6', 'circle_4', 'circle_7', 'circle_3', 'circle_9', 'circle_6', 'circle_2', 'circle_4', 'circle_8', 'circle_1', 'circle_4', 'circle_4', 'circle_6', 'circle_1'],
    "4_circle_set_100trial": ['circle_3', 'circle_4', 'circle_8', 'circle_9', 'circle_7', 'circle_2', 'circle_6', 'circle_1', 'circle_2', 'circle_8', 'circle_3', 'circle_4', 'circle_7', 'circle_6', 'circle_9', 'circle_1', 'circle_2', 'circle_7', 'circle_4', 'circle_1', 'circle_6', 'circle_8', 'circle_9', 'circle_3', 'circle_4', 'circle_2', 'circle_7', 'circle_1', 'circle_3', 'circle_6', 'circle_9', 'circle_8', 'circle_3', 'circle_8', 'circle_4', 'circle_6', 'circle_7', 'circle_9', 'circle_1', 'circle_2', 'circle_1', 'circle_9', 'circle_2', 'circle_6', 'circle_3', 'circle_7', 'circle_8', 'circle_4', 'circle_9', 'circle_7', 'circle_4', 'circle_3', 'circle_1', 'circle_6', 'circle_2', 'circle_8', 'circle_4', 'circle_2', 'circle_3', 'circle_8', 'circle_7', 'circle_9', 'circle_6', 'circle_1', 'circle_6', 'circle_7', 'circle_2', 'circle_1', 'circle_3', 'circle_9', 'circle_8', 'circle_4', 'circle_4', 'circle_2', 'circle_1', 'circle_7', 'circle_9', 'circle_3', 'circle_8', 'circle_6', 'circle_7', 'circle_6', 'circle_9', 'circle_3', 'circle_4', 'circle_2', 'circle_8', 'circle_1', 'circle_9', 'circle_3', 'circle_7', 'circle_2', 'circle_4', 'circle_1', 'circle_6', 'circle_8', 'circle_3', 'circle_1', 'circle_2', 'circle_1']
}

class BaseExperiment:
    """Base class for all experiments to inherit from"""
    def __init__(self, app, canvas, screen_width, screen_height):
        self.app = app
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_width = screen_width // 3
        self.cell_height = screen_height // 3
        self.circle_radius = 10
        self.trial_count = 0
        self.circle_sequence = []
        self.nine_circle_dict = self.create_nine_circle_dict()
        
        # Select a random circle sequence at initialization
        self.select_random_circle_sequence()
        
    def create_nine_circle_dict(self):
        """Create a dictionary mapping circle IDs to screen coordinates"""
        # Calculate center points for each cell in the 3x3 grid
        return {
            # Top row
            "circle_1": [self.cell_width/2, self.cell_height/2],                   # Top-left
            "circle_2": [self.cell_width*1.5, self.cell_height/2],                 # Top-center
            "circle_3": [self.cell_width*2.5, self.cell_height/2],                 # Top-right
            
            # Middle row
            "circle_4": [self.cell_width/2, self.cell_height*1.5],                 # Middle-left
            "circle_5": [self.cell_width*1.5, self.cell_height*1.5],               # Middle-center
            "circle_6": [self.cell_width*2.5, self.cell_height*1.5],               # Middle-right
            
            # Bottom row
            "circle_7": [self.cell_width/2, self.cell_height*2.5],                 # Bottom-left
            "circle_8": [self.cell_width*1.5, self.cell_height*2.5],               # Bottom-center
            "circle_9": [self.cell_width*2.5, self.cell_height*2.5]                # Bottom-right
        }
        
    def select_random_circle_sequence(self):
        """Select a random circle sequence from the predefined set"""
        sequence_key = random.choice(list(circle_set_100trial.keys()))
        self.circle_sequence = circle_set_100trial[sequence_key]
        print(f"Selected circle sequence: {sequence_key}")
        
    def get_circle_position(self, trial_idx):
        """Get circle coordinates for a given trial index"""
        # Make sure we don't go out of bounds of the sequence
        if trial_idx < len(self.circle_sequence):
            circle_id = self.circle_sequence[trial_idx]
            return self.nine_circle_dict[circle_id]
        else:
            # Fallback to a random position if we somehow exceed sequence length
            return self.nine_circle_dict[random.choice(list(self.nine_circle_dict.keys()))]
        
    def setup(self):
        """Initialize experiment-specific settings"""
        raise NotImplementedError("Subclasses must implement setup()")
    
    def start(self):
        """Start the experiment"""
        raise NotImplementedError("Subclasses must implement start()")
    
    def cleanup(self):
        """Clean up resources and unbind events"""
        raise NotImplementedError("Subclasses must implement cleanup()")
    
    def show_welcome_screen(self, text1, text2=None):
        """Display a welcome screen with instructions"""
        self.canvas.delete("all")
        
        block_name = block_type.title() if block_type else "Unknown"
        
        self.canvas.create_text(
            self.screen_width // 2, 
            self.screen_height // 3, 
            text=f"Welcome to the {block_name} experiment", 
            fill=light_color, 
            font=title_font
        )
        
        self.canvas.create_text(
            self.screen_width // 2, 
            self.screen_height // 2, 
            text=text1, 
            fill=light_color, 
            font=basic_font
        )
        
        if text2:
            self.canvas.create_text(
                self.screen_width // 2, 
                self.screen_height // 2 + 60, 
                text=text2, 
                fill=light_color, 
                font=basic_font
            )
    
    def show_cross(self, duration, next_step):
        """Display a centered cross"""
        self.canvas.delete("all")
        cross_size = 25
        self.canvas.create_line(
            self.screen_width//2 - cross_size, self.screen_height//2, 
            self.screen_width//2 + cross_size, self.screen_height//2, 
            fill=light_color, width=5
        )
        self.canvas.create_line(
            self.screen_width//2, self.screen_height//2 - cross_size, 
            self.screen_width//2, self.screen_height//2 + cross_size, 
            fill=light_color, width=5
        )
        self.app.root.after(duration, next_step)
    
    def grid_to_coords(self, pos):
        """Convert grid position (1-9) to x,y coordinates."""
        pos -= 1  # Convert to 0-based
        row = pos // 3
        col = pos % 3
        x = col * self.cell_width + self.cell_width // 2
        y = row * self.cell_height + self.cell_height // 2
        return x, y
    
    def save_data(self, filename=None):
        """Save experiment data to CSV"""
        global participant_id, block_type, start_timestamp
        
        if not self.data.empty and participant_id and block_type and start_timestamp:
            timestamp_str = start_timestamp.strftime('%Y%m%d_%H%M%S')
            
            if not filename:
                filename = f"{timestamp_str}_ID{participant_id}_{block_type}_results.csv"
                
            self.data.to_csv(filename, index=False)
            return True
        return False
    
    def show_completion_screen(self):
        """Show experiment completion screen and return to login"""
        self.canvas.delete("all")
        self.canvas.create_text(
            self.screen_width//2, 
            self.screen_height//2, 
            text="Experiment Finished", 
            fill=light_color, 
            font=title_font
        )
        self.app.root.after(2000, self.app.return_to_login)


class VisualExperiment(BaseExperiment):
    """Visual experiment implementation"""
    def setup(self):
        """Initialize visual experiment settings"""
        self.total_trials = VISUAL_TRIAL_COUNT  # Use the configurable trial count
        self.data = pd.DataFrame(columns=["Trial", "Circle_X", "Circle_Y", "Stop_X", "Stop_Y", 
                                          "Circle_ID", "Circle_Speed", "Start_X_Pos"])
        self.trial_count = 0
        self.current_circle = None
        self.circle_x = None
        self.circle_y = None
        self.x_pos = None
        self.y_pos = None
        self.x_end = None
        self.selected_pos = None
        self.circle_speed = None  # Will be randomly chosen for each trial
        self.possible_speeds = [round(7 + i * 0.2, 1) for i in range(int((9 - 7) / 0.2) + 1)]
        self.noise_frames = None
        self.noise_frame_index = 0
        self.noise_image_id = None
        self.current_circle_id = None
        
        # Try to load the noise GIF
        try:
            # Open the GIF file
            self.noise_gif = Image.open("noise.gif")
            # Get number of frames
            self.noise_frames = self.noise_gif.n_frames
        except Exception as e:
            print(f"Error loading noise.gif: {e}")
            self.noise_frames = None
        
        # Bind space bar for stopping the circle
        self.app.root.bind("<KP_Enter>", self.stop_circle)
    
    def start(self):
        """Start the visual experiment"""
        welcome_text = "press 'Enter' to stop the moving circle"
        self.show_welcome_screen(welcome_text)
        self.app.root.after(2000, self.start_trial)
    
    def start_trial(self):
        """Start a new trial"""
        if self.trial_count >= self.total_trials:
            self.show_completion_screen()
            return
            
        self.trial_count += 1
        print(self.trial_count)
        self.show_cross(500, self.show_static_circle) # Show cross for 0.5 seconds
    
    def show_static_circle(self):
        """Show a stationary circle based on the predefined sequence"""
        self.canvas.delete("all")
        
        # Get circle position from the sequence
        self.current_circle_id = self.circle_sequence[self.trial_count - 1]
        self.circle_x, self.circle_y = self.nine_circle_dict[self.current_circle_id]
        
        # Extract position number (used later for moving the circle)
        # Position is the number at the end of the circle ID (e.g., "circle_3" -> 3)
        self.selected_pos = int(self.current_circle_id.split('_')[1])
        
        # Draw the circle
        self.canvas.create_oval(
            self.circle_x - self.circle_radius, 
            self.circle_y - self.circle_radius,
            self.circle_x + self.circle_radius, 
            self.circle_y + self.circle_radius,
            fill=light_color, outline=""
        )
        
        # Show circle for 3 seconds
        self.app.root.after(500, self.show_noise) 
        
    def show_noise(self):
        """Display the noise GIF for 2 seconds."""
        self.canvas.delete("all")
        self.noise_start_time = time.time()
        
        self.show_noise_frame(0)
        self.app.root.after(200, self.start_moving_circle)
    
    def show_noise_frame(self, frame_idx):
        """Show a specific frame of the noise GIF."""
        if not self.noise_frames:
            return
            
        self.noise_gif.seek(frame_idx) # Seek to the specified frame
        noise_photo = ImageTk.PhotoImage(self.noise_gif) # Convert the current frame to a PhotoImage
        self.noise_photo = noise_photo # Keep a reference to avoid garbage collection
        # Display the frame
        self.noise_image_id = self.canvas.create_image(
            self.screen_width // 2, 
            self.screen_height // 2,
            image=noise_photo
        )
        
        frame_duration = min(100, 200 // self.noise_frames) # Calculate time for next frame (to complete all frames in 2 seconds)
        
        
        next_frame = (frame_idx + 1) % self.noise_frames
        
        # If we still want to show noise (haven't reached 2 seconds)
        if time.time() - self.noise_start_time < 0.2:
            self.app.root.after(frame_duration, lambda: self.show_noise_frame(next_frame))
       
    def start_moving_circle(self):
        """Start moving the circle from right to left in the same grid."""
        self.canvas.delete("all")
        
        # Select a random speed for this trial
        self.circle_speed = random.choice(self.possible_speeds)
        
        
        col = (self.selected_pos - 1) % 3 # Calculate position based on the sequence
        right_edge = (col + 1) * self.cell_width # Calculate right edge of the cell
        right_quarter_start = right_edge - (self.cell_width / 4) # Calculate left edge of the right 1/4 of the cell
        segment_width = (self.cell_width / 4) / 20 # Split the right 1/4 into 20 possible starting points
        random_segment = random.randint(0, 19) # Pick one of the 20 points randomly
        self.x_pos = right_quarter_start + (random_segment * segment_width)
        self.x_end = col * self.cell_width + 10 # End position remains at left edge of cell + 10px
        
        # Create the circle at the randomly chosen position
        self.current_circle = self.canvas.create_oval(
            self.x_pos - self.circle_radius, 
            self.circle_y - self.circle_radius,
            self.x_pos + self.circle_radius, 
            self.circle_y + self.circle_radius,
            fill=light_color, outline=""
        )
        self.move_circle()
    
    def move_circle(self):
        """Move the circle smoothly from right to left."""
        if self.current_circle is None:
            return  # Prevent movement if circle is missing
            
        coords = self.canvas.coords(self.current_circle)
        if len(coords) < 4:
            return  # Ensure coordinates exist before accessing
            
        if self.x_pos > self.x_end:
            self.x_pos = (coords[0] + coords[2]) / 2
            self.canvas.move(self.current_circle, -self.circle_speed, 0)
            self.app.root.after(50, self.move_circle)
        else:
            self.app.root.after(500, self.start_trial)
    
    def stop_circle(self, event=None):
        """Stop the circle and save coordinates."""
        if self.current_circle:
            coords = self.canvas.coords(self.current_circle)
            if len(coords) < 4:
                return  # Prevent errors if circle is missing
                
            stop_x = (coords[0] + coords[2]) // 2
            stop_y = (coords[1] + coords[3]) // 2
            
            new_data = pd.DataFrame([[self.trial_count, self.circle_x, self.circle_y, stop_x, stop_y, 
                                     self.current_circle_id, self.circle_speed, self.x_pos]], 
                                  columns=["Trial", "Circle_X", "Circle_Y", "Stop_X", "Stop_Y", 
                                           "Circle_ID", "Circle_Speed", "Start_X_Pos"])
            
            self.data = pd.concat([self.data, new_data], ignore_index=True)
            self.save_data()
            
            self.current_circle = None  # Clear the current circle reference
            self.app.root.after(1, self.start_trial)
    
    def cleanup(self):
        """Clean up resources and unbind events"""
        self.app.root.unbind("<KP_Enter>")
        self.save_data()

class ProprioceptiveExperiment(BaseExperiment):
    """Proprioceptive experiment implementation"""
    def setup(self):
        """Initialize proprioceptive experiment settings"""
        self.total_trials = PROPRIOCEPTIVE_TRIAL_COUNT  # Use the configurable trial count
        self.data = pd.DataFrame(columns=["Trial", "Circle_Time", "Circle_X", "Circle_Y", 
                                         "Click_Time", "Click_X", "Click_Y", "Circle_ID",
                                         "Arduino_Disappear_Time", "Arduino_Click_Time"])
        self.trial_count = 0
        self.circle_position = None
        self.circle_timestamp = None
        self.current_circle_id = None
        self.click_enabled = False  # Flag to track when clicks are enabled
        self.arduino_disappear_time = None  # Store Arduino timestamp for disappear event
        self.arduino_click_time = None  # Store Arduino timestamp for click event
            
    def start(self):
        """Start the proprioceptive experiment"""
        welcome_text = "The circle will show after cross and disappear,"
        additional_text = "CLOSE YOUR EYES, and point the circle position after the it disappears."
        self.show_welcome_screen(welcome_text, additional_text)
        self.app.root.after(3000, self.start_trial)
    
    def start_trial(self):
        """Start a new trial"""
        # Check if we've completed all trials
        if self.trial_count >= self.total_trials:
            self.show_completion_screen()
            return
            
        self.show_cross(500, self.show_circle)
    
    def show_circle(self):
        """Show a circle based on the predefined sequence"""
        self.canvas.delete("all")
        
        # Increment trial count
        self.trial_count += 1
        print(self.trial_count)
        # Record timestamp when circle is shown
        self.circle_timestamp = time.time()
        
        # Get circle position from the sequence
        self.current_circle_id = self.circle_sequence[self.trial_count - 1]
        circle_x, circle_y = self.nine_circle_dict[self.current_circle_id]
        
        # Draw the circle
        self.canvas.create_oval(
            circle_x - self.circle_radius, 
            circle_y - self.circle_radius,
            circle_x + self.circle_radius, 
            circle_y + self.circle_radius,
            fill=light_color, outline=""
        )
        
        # Save circle position for data collection
        self.circle_position = (circle_x, circle_y)
        
        # Show circle for 3 seconds then hide it
        self.app.root.after(3000, self.wait_for_click)
    
    def wait_for_click(self):
        """Hide the circle and wait for mouse click"""
        self.canvas.delete("all")
        
        # Play beep sound to indicate participant should click
        play_beep()
        
        # Send signal to Arduino to indicate circle disappeared
        if arduino_connected and ser:
            try:
                ser.write(b'D\n')
                # Read Arduino's response
                response = ser.readline().decode().strip()
                if response.startswith("D:"):
                    self.arduino_disappear_time = float(response.split(":")[1])
                    # print(f"Arduino disappear time: {self.arduino_disappear_time}")
            except Exception as e:
                print(f"Error sending to Arduino or reading response: {e}")
                
        # Enable click detection
        self.click_enabled = True
        self.canvas.bind("<Button-1>", self.record_mouse_click)
    
    def record_mouse_click(self, event):
        """Record the mouse click coordinates and proceed to next trial"""
        # Check if clicks are enabled
        if not self.click_enabled:
            return
            
        # Disable clicking immediately to prevent double-clicks
        self.click_enabled = False
        self.canvas.unbind("<Button-1>")
        
        # Get mouse click coordinates and timestamp
        click_x, click_y = event.x, event.y
        click_timestamp = time.time()
        
        # Send signal to Arduino to indicate click was made
        if arduino_connected and ser:
            try:
                ser.write(b'S\n')
                # Read Arduino's response
                response = ser.readline().decode().strip()
                if response.startswith("S:"):
                    self.arduino_click_time = float(response.split(":")[1])
                    # print(f"Arduino click time: {self.arduino_click_time}")
            except Exception as e:
                print(f"Error sending to Arduino or reading response: {e}")
        
        if self.circle_position and self.circle_timestamp:
            # Save data for this trial with timestamps including Arduino timestamps
            new_data = pd.DataFrame(
                [[self.trial_count, self.circle_timestamp, self.circle_position[0], self.circle_position[1], 
                  click_timestamp, click_x, click_y, self.current_circle_id,
                  self.arduino_disappear_time, self.arduino_click_time]], 
                columns=["Trial", "Circle_Time", "Circle_X", "Circle_Y", 
                         "Click_Time", "Click_X", "Click_Y", "Circle_ID",
                         "Arduino_Disappear_Time", "Arduino_Click_Time"]
            )
            
            self.data = pd.concat([self.data, new_data], ignore_index=True)
            self.save_data()
            
            # Reset Arduino time values for next trial
            self.arduino_disappear_time = None
            self.arduino_click_time = None
            
            # Continue to next trial
            self.start_trial()
                
    def cleanup(self):
        """Clean up resources and unbind events"""
        self.canvas.unbind("<Button-1>")
        self.save_data()


class OpenloopExperiment(BaseExperiment):
    """Openloop experiment implementation"""
    def setup(self):
        """Initialize Openloop experiment settings"""
        self.total_trials = OPENLOOP_TRIAL_COUNT  # Use the configurable trial count
        self.data = pd.DataFrame(columns=["Trial", "Circle_Time", "Circle_X", "Circle_Y", 
                                         "Click_Time", "Click_X", "Click_Y", "Circle_ID",
                                         "Arduino_Disappear_Time", "Arduino_Click_Time"])
        self.trial_count = 0
        self.circle_position = None
        self.circle_timestamp = None
        self.current_circle_id = None
        self.click_enabled = False  # Flag to track when clicks are enabled
        self.arduino_disappear_time = None  # Store Arduino timestamp for disappear event
        self.arduino_click_time = None  # Store Arduino timestamp for click event
            
    def start(self):
        """Start the proprioceptive experiment"""
        welcome_text = "The circle will show after cross and disappear,"
        additional_text = "you have to point the circle position after the circle disappears."
        self.show_welcome_screen(welcome_text, additional_text)
        self.app.root.after(3000, self.start_trial)
    
    def start_trial(self):
        """Start a new trial"""
        # Check if we've completed all trials
        if self.trial_count >= self.total_trials:
            self.show_completion_screen()
            return
            
        self.show_cross(500, self.show_circle)
    
    def show_circle(self):
        """Show a circle based on the predefined sequence"""
        self.canvas.delete("all")
        
        # Increment trial count
        self.trial_count += 1
        print(self.trial_count)
        # Record timestamp when circle is shown
        self.circle_timestamp = time.time()
        
        # Get circle position from the sequence
        self.current_circle_id = self.circle_sequence[self.trial_count - 1]
        circle_x, circle_y = self.nine_circle_dict[self.current_circle_id]
        
        # Draw the circle
        self.canvas.create_oval(
            circle_x - self.circle_radius, 
            circle_y - self.circle_radius,
            circle_x + self.circle_radius, 
            circle_y + self.circle_radius,
            fill=light_color, outline=""
        )
        
        # Save circle position for data collection
        self.circle_position = (circle_x, circle_y)
        
        # Show circle for 3 seconds then hide it
        self.app.root.after(3000, self.wait_for_click)
    
    def wait_for_click(self):
        """Hide the circle and wait for mouse click"""
        self.canvas.delete("all")
        
        play_beep() # Play beep sound
        
        # Send signal to Arduino to indicate circle disappeared
        if arduino_connected and ser:
            try:
                ser.write(b'D\n')
                # Read Arduino's response
                response = ser.readline().decode().strip()
                if response.startswith("D:"):
                    self.arduino_disappear_time = float(response.split(":")[1])
                    # print(f"Arduino disappear time: {self.arduino_disappear_time}")
            except Exception as e:
                print(f"Error sending to Arduino or reading response: {e}")
                
        # Enable click detection
        self.click_enabled = True
        self.canvas.bind("<Button-1>", self.record_mouse_click)
    
    def record_mouse_click(self, event):
        """Record the mouse click coordinates and proceed to next trial"""
        # Check if clicks are enabled
        if not self.click_enabled:
            return
            
        # Disable clicking immediately to prevent double-clicks
        self.click_enabled = False
        self.canvas.unbind("<Button-1>")
        
        # Get mouse click coordinates and timestamp
        click_x, click_y = event.x, event.y
        click_timestamp = time.time()
        
        # Send signal to Arduino to indicate click was made
        if arduino_connected and ser:
            try:
                ser.write(b'S\n')
                # Read Arduino's response
                response = ser.readline().decode().strip()
                if response.startswith("S:"):
                    self.arduino_click_time = float(response.split(":")[1])
                    # print(f"Arduino click time: {self.arduino_click_time}")
            except Exception as e:
                print(f"Error sending to Arduino or reading response: {e}")
        
        if self.circle_position and self.circle_timestamp:
            # Save data for this trial with timestamps including Arduino timestamps
            new_data = pd.DataFrame(
                [[self.trial_count, self.circle_timestamp, self.circle_position[0], self.circle_position[1], 
                  click_timestamp, click_x, click_y, self.current_circle_id,
                  self.arduino_disappear_time, self.arduino_click_time]], 
                columns=["Trial", "Circle_Time", "Circle_X", "Circle_Y", 
                         "Click_Time", "Click_X", "Click_Y", "Circle_ID",
                         "Arduino_Disappear_Time", "Arduino_Click_Time"]
            )
            
            self.data = pd.concat([self.data, new_data], ignore_index=True)
            self.save_data()
            
            # Reset Arduino time values for next trial
            self.arduino_disappear_time = None
            self.arduino_click_time = None
            
            # Continue to next trial
            self.start_trial()
                
    def cleanup(self):
        """Clean up resources and unbind events"""
        self.canvas.unbind("<Button-1>")
        self.save_data()


class ExperimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Experiment Login")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg=background_color)
        
        # Store all frames
        self.frames = {}
        
        # Create login frame
        self.login_frame = tk.Frame(root, bg=background_color)
        self.frames['login'] = self.login_frame
        
        # Create experiment frame
        self.experiment_frame = tk.Frame(root, bg=background_color)
        self.frames['experiment'] = self.experiment_frame
        
        # Setup login frame
        self.setup_login_frame()
        
        # Initially show the login frame
        self.show_frame('login')
        
        # Screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Current active experiment
        self.current_experiment = None
        
        # ESC key to exit
        self.root.bind("<Escape>", lambda event: self.root.destroy())
    
    def setup_login_frame(self):
        """Set up the login interface"""
        # Login page title
        title_label = tk.Label(self.login_frame, text="Login Page", font=title_font, bg=background_color, fg=light_color)
        title_label.grid(row=0, column=0, pady=(0, 60))
        
        # ID label and entry
        id_label = tk.Label(self.login_frame, text="Enter ID:", font=basic_font, bg=background_color, fg=light_color)
        id_label.grid(row=1, column=0, pady=(0, 20))
        
        self.id_entry = tk.Entry(self.login_frame, font=basic_font, width=15, bg=light_color, fg="black", bd=3, relief=tk.RIDGE)
        self.id_entry.grid(row=2, column=0, pady=(0, 60))
        
        # Experiment type label
        experiment_label = tk.Label(self.login_frame, text="Experiment", font=basic_font, bg=background_color, fg=light_color)
        experiment_label.grid(row=3, column=0, pady=(0, 30))
        
        # visual shift button
        visual_shift_button = tk.Button(
            self.login_frame, 
            text="visual", 
            font=basic_font, 
            width=10,
            bd=3,
            relief=tk.RIDGE,
            padx=10,
            pady=5,
            bg=light_color,
            fg="black",
            command=lambda: self.start_selected_block("visual")
        )
        visual_shift_button.grid(row=4, column=0, pady=10)
        
        # proprioceptive shift button
        proprioceptive_shift_button = tk.Button(
            self.login_frame, 
            text="proprioceptive", 
            font=basic_font, 
            width=10,
            bd=3,
            relief=tk.RIDGE,
            padx=10,
            pady=5,
            bg=light_color,
            fg="black",
            command=lambda: self.start_selected_block("proprioceptive")
        )
        proprioceptive_shift_button.grid(row=5, column=0, pady=10)
        
        # open loop pointing button
        open_loop_pointing_button = tk.Button(
            self.login_frame, 
            text="openloop", 
            font=basic_font, 
            width=10,
            bd=3,
            relief=tk.RIDGE,
            padx=10,
            pady=5,
            bg=light_color,
            fg="black",
            command=lambda: self.start_selected_block("openloop")
        )
        open_loop_pointing_button.grid(row=6, column=0, pady=10)
        
        # Space for confirmation label (will be created dynamically)
        self.confirmation_space = tk.Frame(self.login_frame, bg=background_color, height=40)
        self.confirmation_space.grid(row=8, column=0, pady=15)
        
        # Next button (inactive until block is selected)
        self.next_button = tk.Button(
            self.login_frame, 
            text="Next", 
            font=basic_font, 
            width=10,
            bd=3,
            relief=tk.RIDGE,
            padx=10,
            pady=5,
            bg=light_color,
            fg="black",
            command=lambda: messagebox.showinfo("Info", "Select a block first")
        )
        self.next_button.grid(row=9, column=0, pady=10)
        
        # Center the frame
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def show_frame(self, frame_name):
        """Show the specified frame and hide others"""
        for name, frame in self.frames.items():
            frame.place_forget()
        
        if frame_name == 'experiment':
            self.setup_experiment_frame()
            self.frames[frame_name].place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.frames[frame_name].place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def setup_experiment_frame(self):
        """Set up the experiment interface"""
        # Clear any existing widgets
        for widget in self.experiment_frame.winfo_children():
            widget.destroy()
        
        # Create canvas
        self.canvas = tk.Canvas(self.experiment_frame, width=self.screen_width, height=self.screen_height,
                              bg=background_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
    
    def start_selected_block(self, selected_block):
        """Start the selected experiment block"""
        global participant_id, block_type
        
        entered_id = self.id_entry.get().strip()
        
        if not entered_id:
            messagebox.showerror("Error", "Please enter an ID")
            return
            
        participant_id = entered_id
        block_type = selected_block
        
        # Show confirmation label
        if hasattr(self, 'confirmation_label'):
            self.confirmation_label.destroy()
            
        if hasattr(self, 'next_button_active'):
            self.next_button_active.destroy()
            
        # Create confirmation label with yellow background
        self.confirmation_label = tk.Label(
            self.login_frame,
            text=f"ID: {participant_id}, Block: {block_type}",
            font=basic_font,
            bg="yellow",
            fg="black",
            relief=tk.RIDGE,
            padx=15,
            pady=8
        )
        self.confirmation_label.grid(row=8, column=0, pady=15)
        
        # Replace the default Next button with an active one
        self.next_button_active = tk.Button(
            self.login_frame, 
            text="Next", 
            font=basic_font, 
            width=10,
            bd=3,
            relief=tk.RIDGE,
            bg="yellow",
            fg="black",
            padx=10,
            pady=5,
            command=lambda: self.start_experiment_with_timestamp()
        )
        self.next_button_active.grid(row=9, column=0, pady=10)
        
    def start_experiment_with_timestamp(self):
        """Record timestamp and start the experiment"""
        global start_timestamp
        self.root.config(cursor="none")
        # Record the timestamp when Next is pressed
        start_timestamp = datetime.datetime.now()
        # Switch to experiment frame
        self.show_frame('experiment')
        
        # Create and start the appropriate experiment based on block_type
        if block_type == "visual":
            self.current_experiment = VisualExperiment(self, self.canvas, self.screen_width, self.screen_height)
        elif block_type == "proprioceptive":
            self.current_experiment = ProprioceptiveExperiment(self, self.canvas, self.screen_width, self.screen_height)
        elif block_type == "openloop":
            self.current_experiment = OpenloopExperiment(self, self.canvas, self.screen_width, self.screen_height)
        # else:
        #     self.current_experiment = OpenloopExperiment(self, self.canvas, self.screen_width, self.screen_height)
        
        # Setup and start the experiment
        self.current_experiment.setup()
        self.current_experiment.start()
    
    def return_to_login(self, event=None):
        """Return to the login screen after saving data."""
        global participant_id, block_type, start_timestamp
        self.root.config(cursor="")
        # Clean up the current experiment if it exists
        if self.current_experiment:
            self.current_experiment.cleanup()
            self.current_experiment = None
        
        # Reset global variables
        participant_id = None
        block_type = None
        start_timestamp = None
        
        # Show login frame again
        self.show_frame('login')


# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ExperimentApp(root)
    root.mainloop()