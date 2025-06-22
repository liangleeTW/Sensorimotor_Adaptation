import tkinter as tk
import tkinter.messagebox as tmsg
import time
import pandas as pd
import numpy as np
pd.set_option("display.precision", 20)
import random
import serial

root = tk.Tk()
#root.geometry("1280x720+0+0") #width x height # initial window size #1920x1080
root.title("task") 
root.attributes('-fullscreen', True) # enables full screen
root.configure(bg = 'black')# background color-black
# root.config(cursor="none") # hide mouse # already moved to after experiment start
def ESC(event):# press esc to quit
    root.destroy()
root.bind('<Escape>', ESC)

##################################################
# variable change 
folder_path = "/Users/leeliang/Desktop/shift/shift_pilot_smallrectangle/" # ex: /Users/leeliang/Desktop/E_project/  , start and end with /
cross_show_duration = 500 # millisecond: 3000 = 3 seconds
circle_show_duration = 3000 # 3000millisecond
wait_for_mouse_click_duration = 2000 # 2000millisecond # wait for mouse click time = circle disappear time
show_circle_feedback_duration = 500 # millisecond 
welcome_label_show_duration = 2000 # millisecond 
circle_diameter = 10
cross_length = 50
# the following variable needs to divide by 3
practice_trial_num = 60 # 60 represent 20 trials
block_13_trial_num = 150 # 150 represent 50 trials
block_2_trial_num = 300 # 300 represent 100 trials

# variable initial
basic_font = 'Helvetica 40 bold'
title_font = 'Helvetica 60 bold'
background_color = 'black'
light_color = "#888888"
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
cell_width = screen_width // 3
cell_height = screen_height // 3
shift = 10
old_nine_circle_dict = {
"circle_1": [cell_width/2 - shift, cell_height/2],                   # Top-left
"circle_2": [cell_width*1.5 - shift, cell_height/2],                 # Top-center
"circle_3": [cell_width*2.5 + shift, cell_height/2],                 # Top-right
"circle_4": [cell_width/2 - shift, cell_height*1.5],                 # Middle-left
"circle_6": [cell_width*2.5 + shift, cell_height*1.5],               # Middle-right
"circle_7": [cell_width/2 - shift, cell_height*2.5],                 # Bottom-left
"circle_8": [cell_width*1.5 + shift, cell_height*2.5],               # Bottom-center
"circle_9": [cell_width*2.5 + shift, cell_height*2.5]  
}


# Calculate red boundary limits
x_min = min(point[0] for point in old_nine_circle_dict.values())
x_max = max(point[0] for point in old_nine_circle_dict.values())
y_min = min(point[1] for point in old_nine_circle_dict.values())
y_max = max(point[1] for point in old_nine_circle_dict.values())

# New cell dimensions for red grid
new_cell_width = (x_max - x_min) / 3
new_cell_height = (y_max - y_min) / 3

# Generate new grid center points (Red circles)
nine_circle_dict = {}
for i in range(3):      # Rows
    for j in range(3):  # Columns
        new_x = x_min + new_cell_width * (j + 0.5)
        new_y = y_min + new_cell_height * (i + 0.5)
        nine_circle_dict[f"circle_{i*3 + j + 1}"] = [new_x, new_y]

circle_set_100trial_block2 = {
    "1_circle_set_100trial": ['circle_4', 'circle_7', 'circle_8', 'circle_9', 'circle_6', 'circle_3', 'circle_2', 'circle_1', 'circle_9', 'circle_4', 'circle_2', 'circle_6', 'circle_1', 'circle_8', 'circle_3', 'circle_7', 'circle_4', 'circle_2', 'circle_7', 'circle_3', 'circle_6', 'circle_9', 'circle_8', 'circle_1', 'circle_6', 'circle_2', 'circle_4', 'circle_1', 'circle_7', 'circle_8', 'circle_9', 'circle_3', 'circle_2', 'circle_8', 'circle_3', 'circle_6', 'circle_7', 'circle_1', 'circle_9', 'circle_4', 'circle_2', 'circle_9', 'circle_6', 'circle_7', 'circle_3', 'circle_8', 'circle_4', 'circle_1', 'circle_7', 'circle_3', 'circle_2', 'circle_6', 'circle_8', 'circle_4', 'circle_9', 'circle_1', 'circle_2', 'circle_9', 'circle_7', 'circle_8', 'circle_6', 'circle_3', 'circle_1', 'circle_4', 'circle_3', 'circle_8', 'circle_9', 'circle_2', 'circle_1', 'circle_4', 'circle_7', 'circle_6', 'circle_9', 'circle_1', 'circle_6', 'circle_2', 'circle_7', 'circle_3', 'circle_8', 'circle_4', 'circle_1', 'circle_2', 'circle_8', 'circle_7', 'circle_3', 'circle_6', 'circle_9', 'circle_4', 'circle_1', 'circle_4', 'circle_7', 'circle_2', 'circle_8', 'circle_6', 'circle_3', 'circle_9', 'circle_3', 'circle_8', 'circle_7', 'circle_3'],
    "2_circle_set_100trial": ['circle_2', 'circle_8', 'circle_7', 'circle_1', 'circle_9', 'circle_6', 'circle_3', 'circle_4', 'circle_9', 'circle_1', 'circle_2', 'circle_6', 'circle_7', 'circle_3', 'circle_8', 'circle_4', 'circle_7', 'circle_2', 'circle_4', 'circle_1', 'circle_3', 'circle_9', 'circle_8', 'circle_6', 'circle_9', 'circle_7', 'circle_2', 'circle_4', 'circle_1', 'circle_6', 'circle_8', 'circle_3', 'circle_3', 'circle_8', 'circle_1', 'circle_4', 'circle_7', 'circle_6', 'circle_2', 'circle_9', 'circle_4', 'circle_3', 'circle_8', 'circle_2', 'circle_6', 'circle_1', 'circle_7', 'circle_9', 'circle_3', 'circle_2', 'circle_8', 'circle_7', 'circle_6', 'circle_9', 'circle_4', 'circle_1', 'circle_2', 'circle_7', 'circle_4', 'circle_8', 'circle_1', 'circle_6', 'circle_3', 'circle_9', 'circle_1', 'circle_9', 'circle_8', 'circle_7', 'circle_6', 'circle_2', 'circle_3', 'circle_4', 'circle_6', 'circle_3', 'circle_2', 'circle_9', 'circle_4', 'circle_1', 'circle_8', 'circle_7', 'circle_2', 'circle_9', 'circle_8', 'circle_6', 'circle_7', 'circle_4', 'circle_3', 'circle_1', 'circle_3', 'circle_4', 'circle_7', 'circle_1', 'circle_6', 'circle_2', 'circle_8', 'circle_9', 'circle_4', 'circle_6', 'circle_7', 'circle_2'],
    "3_circle_set_100trial": ['circle_7', 'circle_2', 'circle_4', 'circle_8', 'circle_1', 'circle_3', 'circle_9', 'circle_6', 'circle_1', 'circle_4', 'circle_6', 'circle_7', 'circle_9', 'circle_3', 'circle_2', 'circle_8', 'circle_4', 'circle_7', 'circle_6', 'circle_2', 'circle_1', 'circle_3', 'circle_8', 'circle_9', 'circle_2', 'circle_8', 'circle_1', 'circle_6', 'circle_7', 'circle_9', 'circle_3', 'circle_4', 'circle_6', 'circle_9', 'circle_4', 'circle_3', 'circle_2', 'circle_8', 'circle_7', 'circle_1', 'circle_3', 'circle_6', 'circle_7', 'circle_1', 'circle_2', 'circle_9', 'circle_4', 'circle_8', 'circle_7', 'circle_2', 'circle_3', 'circle_4', 'circle_8', 'circle_9', 'circle_6', 'circle_1', 'circle_1', 'circle_7', 'circle_8', 'circle_9', 'circle_3', 'circle_2', 'circle_4', 'circle_6', 'circle_7', 'circle_9', 'circle_6', 'circle_3', 'circle_1', 'circle_4', 'circle_2', 'circle_8', 'circle_2', 'circle_7', 'circle_9', 'circle_6', 'circle_3', 'circle_1', 'circle_4', 'circle_8', 'circle_3', 'circle_4', 'circle_1', 'circle_2', 'circle_6', 'circle_9', 'circle_8', 'circle_7', 'circle_2', 'circle_6', 'circle_8', 'circle_7', 'circle_3', 'circle_9', 'circle_4', 'circle_1', 'circle_6', 'circle_8', 'circle_9', 'circle_4'],
    "4_circle_set_100trial": ['circle_1', 'circle_4', 'circle_8', 'circle_6', 'circle_3', 'circle_2', 'circle_9', 'circle_7', 'circle_6', 'circle_9', 'circle_3', 'circle_8', 'circle_7', 'circle_1', 'circle_2', 'circle_4', 'circle_1', 'circle_2', 'circle_8', 'circle_6', 'circle_4', 'circle_9', 'circle_3', 'circle_7', 'circle_8', 'circle_2', 'circle_1', 'circle_3', 'circle_9', 'circle_4', 'circle_6', 'circle_7', 'circle_6', 'circle_3', 'circle_2', 'circle_7', 'circle_9', 'circle_4', 'circle_8', 'circle_1', 'circle_7', 'circle_3', 'circle_6', 'circle_4', 'circle_9', 'circle_1', 'circle_2', 'circle_8', 'circle_3', 'circle_8', 'circle_1', 'circle_2', 'circle_7', 'circle_4', 'circle_6', 'circle_9', 'circle_7', 'circle_2', 'circle_4', 'circle_8', 'circle_9', 'circle_1', 'circle_3', 'circle_6', 'circle_9', 'circle_3', 'circle_8', 'circle_2', 'circle_4', 'circle_1', 'circle_6', 'circle_7', 'circle_3', 'circle_8', 'circle_9', 'circle_7', 'circle_2', 'circle_4', 'circle_6', 'circle_1', 'circle_2', 'circle_4', 'circle_3', 'circle_1', 'circle_8', 'circle_9', 'circle_6', 'circle_7', 'circle_1', 'circle_2', 'circle_7', 'circle_3', 'circle_4', 'circle_8', 'circle_6', 'circle_9', 'circle_6', 'circle_8', 'circle_3', 'circle_9']
    }
circle_set_50trial_block1 = {
    "1_circle_set_50trial": ['circle_8', 'circle_2', 'circle_4', 'circle_3', 'circle_1', 'circle_9', 'circle_6', 'circle_7', 'circle_1', 'circle_8', 'circle_7', 'circle_4', 'circle_2', 'circle_3', 'circle_6', 'circle_9', 'circle_6', 'circle_7', 'circle_8', 'circle_3', 'circle_2', 'circle_9', 'circle_4', 'circle_1', 'circle_9', 'circle_4', 'circle_8', 'circle_2', 'circle_1', 'circle_6', 'circle_7', 'circle_3', 'circle_3', 'circle_2', 'circle_1', 'circle_7', 'circle_4', 'circle_9', 'circle_8', 'circle_6', 'circle_4', 'circle_8', 'circle_9', 'circle_3', 'circle_6', 'circle_1', 'circle_7', 'circle_2', 'circle_3', 'circle_1'],
    "2_circle_set_50trial": ['circle_7', 'circle_8', 'circle_2', 'circle_6', 'circle_4', 'circle_1', 'circle_9', 'circle_3', 'circle_4', 'circle_2', 'circle_3', 'circle_7', 'circle_9', 'circle_8', 'circle_6', 'circle_1', 'circle_3', 'circle_1', 'circle_6', 'circle_9', 'circle_8', 'circle_7', 'circle_4', 'circle_2', 'circle_7', 'circle_6', 'circle_4', 'circle_1', 'circle_9', 'circle_2', 'circle_3', 'circle_8', 'circle_4', 'circle_9', 'circle_3', 'circle_7', 'circle_1', 'circle_8', 'circle_6', 'circle_2', 'circle_1', 'circle_6', 'circle_7', 'circle_4', 'circle_2', 'circle_8', 'circle_9', 'circle_3', 'circle_2', 'circle_6']
    }
circle_set_50trial_block3 = {
    "3_circle_set_50trial": ['circle_8', 'circle_2', 'circle_1', 'circle_3', 'circle_7', 'circle_4', 'circle_9', 'circle_6', 'circle_7', 'circle_2', 'circle_6', 'circle_9', 'circle_8', 'circle_3', 'circle_4', 'circle_1', 'circle_6', 'circle_1', 'circle_3', 'circle_2', 'circle_9', 'circle_7', 'circle_4', 'circle_8', 'circle_3', 'circle_9', 'circle_2', 'circle_4', 'circle_6', 'circle_1', 'circle_7', 'circle_8', 'circle_3', 'circle_1', 'circle_2', 'circle_7', 'circle_9', 'circle_4', 'circle_6', 'circle_8', 'circle_4', 'circle_6', 'circle_1', 'circle_3', 'circle_7', 'circle_8', 'circle_2', 'circle_9', 'circle_6', 'circle_2'],
    "4_circle_set_50trial": ['circle_7', 'circle_2', 'circle_8', 'circle_6', 'circle_3', 'circle_9', 'circle_4', 'circle_1', 'circle_3', 'circle_6', 'circle_4', 'circle_7', 'circle_9', 'circle_2', 'circle_8', 'circle_1', 'circle_7', 'circle_2', 'circle_3', 'circle_1', 'circle_4', 'circle_8', 'circle_9', 'circle_6', 'circle_9', 'circle_2', 'circle_4', 'circle_3', 'circle_8', 'circle_6', 'circle_1', 'circle_7', 'circle_2', 'circle_1', 'circle_7', 'circle_6', 'circle_4', 'circle_3', 'circle_9', 'circle_8', 'circle_6', 'circle_9', 'circle_7', 'circle_3', 'circle_8', 'circle_4', 'circle_2', 'circle_1', 'circle_6', 'circle_8']
    }


login_data = {}
animation_active = False

# beep sound
import pygame
pygame.mixer.init()
def play_beep():
    pygame.mixer.music.load("beep.wav")
    pygame.mixer.music.play(loops = 0)

##################################################
COM_PORT = '/dev/cu.usbmodem143101'    # 指定通訊埠名稱
BAUD_RATES = 9600#115200
ser = serial.Serial(COM_PORT, BAUD_RATES) # Send the current time over the serial connection
##################################################
# condition2 circle animation function
def condition2_circle_animation(login_Block):
    if login_Block == "block_2":
        block_trial_num = block_2_trial_num
        # choose circle set
        chosen_circle_set = random.choices(list(circle_set_100trial_block2), k = 1)[0] # choose 1 circle set
        circle_key_list = circle_set_100trial_block2[chosen_circle_set]
        circle_coor_list = [nine_circle_dict[key] for key in circle_key_list]
        print(chosen_circle_set)
        print("circle_key_list:", circle_key_list)
        # print("circle_coor_list:", circle_coor_list)
        circle_df = pd.concat([pd.DataFrame(circle_key_list), pd.DataFrame(circle_coor_list)], axis = 1)
        circle_df.columns = ["circle_ID", "circle_x", "circle_y"]
        circle_df.to_csv(global_save_file_name + "_" + chosen_circle_set + '_circle_origin.csv')

    elif login_Block == "practice":
        block_trial_num = practice_trial_num
        # choose circle set
        circle_key_list = random.choices(list(nine_circle_dict), k = int(block_trial_num/3))
        circle_coor_list = [nine_circle_dict[key] for key in circle_key_list]
        print("circle_key_list:", circle_key_list)
        circle_df = pd.concat([pd.DataFrame(circle_key_list), pd.DataFrame(circle_coor_list)], axis = 1)
        circle_df.columns = ["circle_ID", "circle_x", "circle_y"]
        circle_df.to_csv(global_save_file_name + "_practicerandom_circle_origin.csv")

    elif login_Block == "block_1":
        block_trial_num = block_13_trial_num
        # choose circle set
        chosen_circle_set = random.choices(list(circle_set_50trial_block1), k = 1)[0] # choose 1 circle set
        circle_key_list = circle_set_50trial_block1[chosen_circle_set]
        circle_coor_list = [nine_circle_dict[key] for key in circle_key_list]
        print(chosen_circle_set)
        print("circle_key_list:", circle_key_list)
        circle_df = pd.concat([pd.DataFrame(circle_key_list), pd.DataFrame(circle_coor_list)], axis = 1)
        circle_df.columns = ["circle_ID", "circle_x", "circle_y"]
        circle_df.to_csv(global_save_file_name + "_" + chosen_circle_set + '_circle_origin.csv')

    elif login_Block == "block_3":
        block_trial_num = block_13_trial_num
        # choose circle set
        chosen_circle_set = random.choices(list(circle_set_50trial_block3), k = 1)[0] # choose 1 circle set
        circle_key_list = circle_set_50trial_block3[chosen_circle_set]
        circle_coor_list = [nine_circle_dict[key] for key in circle_key_list]
        print(chosen_circle_set)
        print("circle_key_list:", circle_key_list)
        circle_df = pd.concat([pd.DataFrame(circle_key_list), pd.DataFrame(circle_coor_list)], axis = 1)
        circle_df.columns = ["circle_ID", "circle_x", "circle_y"]
        circle_df.to_csv(global_save_file_name + "_" + chosen_circle_set + '_circle_origin.csv')

    save_circle_trial = []
    save_circle_time = [] 
    save_circle_x_list = []
    save_circle_y_list = []
    save_circle_type_list = []
    arduino_data_list = []
    def animate_circle(trial): # for loop can't work
        global animation_active, shape_id
        
        if trial < block_trial_num: 
            if trial % 3 == 0:# show cross
                if animation_active: # cross end
                    canvas.delete("all")
                    animation_active = False
                    root.after(0, animate_circle, trial + 1)
                else: # cross show
                    # create_line(x1, y1, x2, y2)
                    # vertical line
                    shape_id = canvas.create_line(screen_width/2, 
                                                  screen_height/2 - cross_length/2, 
                                                  screen_width/2, 
                                                  screen_height/2 + cross_length/2, 
                                                  fill=light_color, width = 8)
                    # horizontal line
                    shape_id1 = canvas.create_line(screen_width/2 - cross_length/2, 
                                                   screen_height/2, 
                                                   screen_width/2 + cross_length/2, 
                                                   screen_height/2, 
                                                   fill=light_color, width = 8)
                    animation_active = True
                    root.after(cross_show_duration, animate_circle, trial)
            if trial % 3 == 1: # show circle, disappear, and wait for click
                if animation_active: # circle end & wait for mouse click time
                    canvas.delete("all")
                    ser.write(b'D\n')# circle disappear signal to arduino
                    # time.sleep(450/1000)
                    play_beep()
                    
                    arduino_time = ser.readline().decode().strip()
                    arduino_data_list.append([int(trial/3)+1, 'D', arduino_time])
                    print(f"Arduino time (D): {arduino_time}")
                    
                    def on_click(event, trial = trial):
                        ser.write(b'S\n') # send signal to arduino: circle show/ScreenClicked
                        arduino_time = ser.readline().decode().strip()# ser.readline().decode()
                        print(f"Arduino time (S): {arduino_time}")
                        arduino_data_list.append([int(trial/3)+1, 'S', arduino_time])
                        pd.DataFrame(arduino_data_list, columns=['trial', 'signal', 'arduino_time']).to_csv(global_save_file_name + '_arduino.csv')
                        
                        x = event.x
                        y = event.y
                        click_trial_list.append(int(trial/3)+1)
                        click_time = time.time()
                        click_time_list.append(click_time)
                        mouse_x_list.append(event.x)
                        mouse_y_list.append(event.y)
                        mouse_coor_dict = {'trial': click_trial_list, 
                                           'click_time': click_time_list,
                                            'mouse_x': mouse_x_list,
                                            'mouse_y': mouse_y_list}
                        pd.DataFrame(mouse_coor_dict).to_csv(global_save_file_name + '_mouse.csv')
                        print("trial:", int(trial/3)+1, "| mouse time:", click_time, "| mouse(x,y):", (x, y))
                        root.unbind("<Button-1>")# Unbind the click handler
                        animate_circle(trial + 1)# Continue with the next trial    
                    
                    
                    animation_active = False
                    root.bind("<Button-1>", lambda event: on_click(event))
                    
                else: # circle show
                    circle_x = circle_coor_list[int(trial/3)][0]
                    circle_y = circle_coor_list[int(trial/3)][1]
                    circle_type = circle_key_list[int(trial/3)]
                    # canvas.create_oval(upper left x, upper left y, lower right x, lower right y) 
                    shape_id = canvas.create_oval(circle_x - circle_diameter, 
                                                  circle_y - circle_diameter, 
                                                  circle_x + circle_diameter, 
                                                  circle_y + circle_diameter, 
                                                  fill=light_color, outline = '') 
                    
                    circle_time =  time.time()
                    print("--------------------------------------------------")
                    print("trial:", int(trial/3)+1, "| circle time:", circle_time, "| circle(x,y):", (circle_x, circle_y))

                    # save circle trial and time
                    save_circle_trial.append(int(trial/3)+1) # trial +1 start with 1
                    save_circle_time.append(circle_time)
                    save_circle_x_list.append(circle_x)
                    save_circle_y_list.append(circle_y)
                    save_circle_type_list.append(circle_type)#!!!!!!!

                    animation_active = True
                    root.after(circle_show_duration, animate_circle, trial) 
            if trial % 3 == 2: # show feedback circle
                if animation_active: # feedback circle end
                    canvas.delete(shape_id)
                    animation_active = False
                    root.after(0, animate_circle, trial + 1)
                else: # feedback circle show
                    play_beep()
                    circle_x = circle_coor_list[int(trial/3)][0]
                    circle_y = circle_coor_list[int(trial/3)][1]
                    circle_type = circle_key_list[int(trial/3)]

                    # canvas.create_oval(upper left x, upper left y, lower right x, lower right y) 
                    shape_id = canvas.create_oval(circle_x - circle_diameter, 
                                                  circle_y - circle_diameter, 
                                                  circle_x + circle_diameter, 
                                                  circle_y + circle_diameter, 
                                                  fill=light_color, outline = '')
                    circle_time =  time.time()
                    
                    print("trial:", int(trial/3)+1, "| feedback circle time:", circle_time, "| feedback circle(x,y):", (circle_x, circle_y))
                    print("--------------------------------------------------")
                    print("**************************************************")
        
                    # save circle trial and time
                    save_circle_trial.append(int(trial/3)+1) # trial +1 start with 1
                    save_circle_time.append(circle_time)
                    save_circle_x_list.append(circle_x)
                    save_circle_y_list.append(circle_y)
                    save_circle_type_list.append(circle_type + "_feedback")
                    
                    animation_active = True
                    root.after(show_circle_feedback_duration, animate_circle, trial)
        else:
            save_circle_coor_dict = {'trial': save_circle_trial, 
                                     'time': save_circle_time, 
                                     'x': save_circle_x_list, 
                                     'y': save_circle_y_list, 
                                     'type': save_circle_type_list}
            circle_df = pd.DataFrame(save_circle_coor_dict)
            circle_df.to_csv(global_save_file_name + '_circle.csv', index=False)

            byebye_label = tk.Label(root, text="此區段測驗結束\n請閉上眼睛", font = title_font, bg=background_color)
            byebye_label.place(relx=0.5, rely=0.5, anchor="center")

            # combine data
            mouse_df = pd.read_csv(global_save_file_name + '_mouse.csv', index_col=0)
            mouse_type_list = ["mouse"]*mouse_df.shape[0]
            mouse_df = pd.concat([mouse_df, pd.DataFrame(mouse_type_list)], axis = 1)
            mouse_df.columns = ['trial', 'time', 'x', 'y', 'type']

            combine_df = pd.concat([mouse_df,circle_df], join='outer').reset_index(drop=True).sort_values('time')
            combine_df = combine_df[['trial', 'time', 'type', 'x', 'y']]
            # combine_df.fillna(method='ffill', inplace=True)
            combine_df.to_csv(global_save_file_name + '_combine.csv')
            print("all data saved!!!!!!!!!")
    
    canvas = tk.Canvas(root, width = screen_width, height = screen_height, bg=background_color, highlightthickness=0)
    canvas.place(relx=0.5, rely=0.5, anchor="center")

    click_trial_list = []
    mouse_x_list = []
    mouse_y_list = []
    click_time_list = []
    animate_circle(0)  # Start the animation

##################################################
##################################################
##################################################

# Save ID to login data dictionary and move to next page
def save_id():
    global global_save_file_name, login_Block
    login_data["ID"] = entry_id.get()
    login_data["Condition"] = var_condition.get()
    login_data["Block"] = var_block.get()
    login_time = time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))
    login_ID = login_data['ID']
    login_Condition = login_data['Condition']
    login_Block = login_data['Block']
    print(f'| {login_ID} | {login_Condition} | {login_Block} |')
    print("===============================")

    #global_save_file_name = f'{folder_path}{login_time}_ID{login_ID}_{login_Condition}_{login_Block}'
    global_save_file_name = f'{folder_path}{login_time}_ID{login_ID}_{login_Block}'
    
    # check entry empty
    if (entry_id.get() == "") or (var_block.get() == ""):
        tmsg.showinfo("Error!","Not complete!")
        print("Error")
    # elif var_condition.get() == "condition_2": # condition_2
    #     root.after(0, Page_condition_2())
    else:
        root.after(0, Page_condition_2(login_Block))

##################################################
def Page_condition_2(login_Block): 
    root.config(cursor="none") # 隱藏mouse
    # clear login page
    frame_ID.destroy()
    frame_block.destroy()
    frame_next.destroy()
    
    # create welcome
    welcome1_label = tk.Label(root, text="實驗即將開始!", font = title_font, bg=background_color)
    welcome1_label.place(relx=0.5, rely=0.5, anchor="center") , 
    root.after(welcome_label_show_duration) # show welcome label for 2 seconds
    welcome1_label.destroy()
    
    welcome2_label = tk.Label(root, text="測驗將於十字出現後開始!", font = title_font, bg=background_color)
    welcome2_label.place(relx=0.5, rely=0.5, anchor="center")
    root.after(welcome_label_show_duration) # show welcome label for 2 seconds
    welcome2_label.destroy()
    
    # if login_Block == "block_2":
    #     condition2_circle_animation(block_2_trial_num)
    # elif login_Block == "practice":
    #     condition2_circle_animation(practice_trial_num)
    # else:
    #     condition2_circle_animation(block_13_trial_num)
    condition2_circle_animation(login_Block)

##################################################
##################################################
##################################################
##################################################

# create login page
# create four frames: frame_ID, frame_block, frame_next
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
frame_ID = tk.Frame(root)
frame_ID.configure(bg = background_color)
frame_ID.grid_columnconfigure(0, weight=1)
frame_block = tk.Frame(root)
frame_block.configure(bg = background_color)
frame_next = tk.Frame(root)
frame_next.configure(bg = background_color)

# frame_ID
## label & entry
label_login = tk.Label(frame_ID,bg = background_color, text="Login Page", font = basic_font)
label_id = tk.Label(frame_ID,bg = background_color, text="Enter ID:", font = basic_font)
entry_id = tk.Entry(frame_ID, insertontime = 0, width=30, font = basic_font, bg = "grey",bd = 2, highlightbackground='red')
entry_id.focus()

# frame_block
## label
label_block = tk.Label(frame_block,bg = background_color, text="Block", font = basic_font)

## button variable
var_condition = tk.StringVar()
var_block = tk.StringVar()

def practice_selected():
    ID = entry_id.get()
    label_block_selected.configure(text = ID + ", practice !!!")
    button_practice.configure(foreground = "white", background = "red")
    button_block1.configure(foreground = "grey", background = "black")
    button_block2.configure(foreground = "grey", background = "black")
    button_block3.configure(foreground = "grey", background = "black")
def block1_selected():#event="<q>"
    ID = entry_id.get()
    label_block_selected.configure(text = ID + ", block 1 !!!")
    button_block1.configure(foreground = "white", background = "red")
    button_block2.configure(foreground = "grey", background = "black")
    button_block3.configure(foreground = "grey", background = "black")
    button_practice.configure(foreground = "grey", background = "black")
def block2_selected():# event="<w>"
    ID = entry_id.get()
    label_block_selected.configure(text = ID + ", block 2 !!!")
    button_block2.configure(foreground = "white", background = "red")
    button_block1.configure(foreground = "grey", background = "black")
    button_block3.configure(foreground = "grey", background = "black")
    button_practice.configure(foreground = "grey", background = "black")
def block3_selected():#event="<e>"
    ID = entry_id.get()
    label_block_selected.configure(text = ID + ", block 3 !!!")
    button_block3.configure(foreground = "white", background = "red")
    button_block2.configure(foreground = "grey", background = "black")
    button_block1.configure(foreground = "grey", background = "black")
    button_practice.configure(foreground = "grey", background = "black")
## create button in frame
## cursor shape:https://docstore.mik.ua/orelly/perl3/tk/ch23_02.htm
button_practice = tk.Radiobutton(frame_block, text = "practice", variable = var_block, value="practice", font = basic_font, indicatoron=False, selectcolor="yellow",cursor="draft_large", command = practice_selected)
button_block1 = tk.Radiobutton(frame_block, text = "Block 1", variable = var_block, value="block_1", font = basic_font, indicatoron=False, selectcolor="yellow",cursor="draft_large", command = block1_selected)
button_block2 = tk.Radiobutton(frame_block, text = "Block 2", variable = var_block, value="block_2", font = basic_font, indicatoron=False, selectcolor="yellow",cursor="draft_large", command = block2_selected)
button_block3 = tk.Radiobutton(frame_block, text = "Block 3", variable = var_block, value="block_3", font = basic_font, indicatoron=False, selectcolor="yellow",cursor="draft_large", command = block3_selected)

# button_block1.bind_all('<q>', block1_selected)
# button_block2.bind_all('<w>', block2_selected)
# button_block3.bind_all('<e>', block3_selected)

label_block_selected = tk.Label(frame_block,bg = "gold", fg = "grey5", text="", font = basic_font)
# frame_next
button_next = tk.Button(frame_next, text="Next", command=save_id, font = basic_font)
#root.bind('<Return>', save_id)

# element position in frame
label_login.pack(pady=30)
label_id.pack(side=tk.TOP, padx=10, pady=10)
entry_id.pack(padx=10, pady=10)
label_block.pack(side=tk.TOP, padx=10, pady=10)
button_practice.pack(side=tk.TOP, padx=10, pady=15)
button_block1.pack(side=tk.TOP, padx=10, pady=15)
button_block2.pack(side=tk.TOP, padx=10, pady=15)
button_block3.pack(side=tk.TOP, padx=10, pady=15)
label_block_selected.pack(side=tk.TOP, padx=10, pady=10)
button_next.pack(side=tk.TOP, padx=10, pady=20)

# frame position
frame_ID.grid(row=0,column=0,columnspan=2,sticky="nsew")# 
frame_block.grid(row=1,column=1,sticky="nw",  padx=80,  pady=30)
frame_next.grid(row=2,column=0,columnspan=2,sticky="nsew")
##################################################
root.mainloop()