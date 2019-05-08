from tkinter import messagebox
from math import sqrt

import pygame
import tkinter as tk
import xml.etree.ElementTree as ET

from functionality import main as mm, transport as tp, update as up
from helper.sort import listsort

# window size setting
SIZE_X, SIZE_Y = 1140, 780
win_width, win_height = 800, 700


# helper function to setup the display window
def window_setup():
    global window

    window = tk.Tk()
    # window setup
    window.option_add("*Font", "Calibri 16")
    window.resizable(False, False)
    window.protocol("WM_DELETE_WINDOW", quit_action)
    window.geometry('%dx%d+%d+%d' % (win_width, win_height, (window.winfo_screenwidth() - win_width) / 2,
                                     (window.winfo_screenheight() - win_height) / 2))
    return window


# helper function to setup the display frame
def frame_setup():
    def frame_size(event):
        canvas.configure(scrollregion=canvas.bbox("all"), width=win_width - 25, height=win_height - 5)

    distance_frame = tk.Frame(window, relief=tk.GROOVE, width=50, height=100, bd=1)
    distance_frame.place(x=0, y=0)

    canvas = tk.Canvas(distance_frame)
    frame = tk.Frame(canvas)
    scrollbar = tk.Scrollbar(distance_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left")
    canvas.create_window((0, 0), window=frame, anchor='nw')
    frame.bind("<Configure>", frame_size)
    return frame


# exit from the program after user click quit button
def quit_action():
    quit_msg = "Do you really want to quit?\nIf you quit, the program will be terminated!"
    if messagebox.askokcancel("Quit", quit_msg):
        exit(0)


# set an button to be clickable
def enable_button(b):
    b['state'] = tk.NORMAL


# prompt the user to manually input the coordinate of the location
def enter_coordinate():
    # sample messages and settings
    cor_msg = "Correct!"
    wrong_msg = "Invalid!"
    wid = 50

    def check_x(var, mode, event):
        x_msg.set(cor_msg)
        if not (ex.get().isdigit() and 0 <= int(ex.get()) < SIZE_X):
            x_msg.set(wrong_msg)
            lx["fg"] = "red"
        else:
            lx["fg"] = "green"

    def check_y(var, mode, event):
        y_msg.set(cor_msg)
        if not (ey.get().isdigit() and 0 <= int(ey.get()) < SIZE_Y):
            y_msg.set(wrong_msg)
            ly["fg"] = "red"
        else:
            ly["fg"] = "green"

    def check_button(var, mode, event):
        if ex.get().isdigit() and ey.get().isdigit() and \
                0 <= int(ex.get()) < SIZE_X and 0 <= int(ey.get()) < SIZE_Y:
            b['state'] = tk.NORMAL
            var_x.set(int(ex.get()))
            var_y.set(int(ey.get()))
        else:
            b['state'] = tk.DISABLED

    # main inquiry
    window_setup()
    window.title("Manual Input")
    tk.Label(window, width=wid, text="Please enter the x and y coordinate", font=("Calibri", 20)).pack()
    tk.Label(window, width=wid, text="x: from 0 to " + str(SIZE_X - 1) + "\ty: from 0 to " + str(SIZE_Y - 1),
             font=("Calibri", 16)).pack()

    var_x, var_y = tk.IntVar(), tk.IntVar()  # return value
    ex_var, ey_var = tk.StringVar(), tk.StringVar()  # entry variable
    x_msg, y_msg = tk.StringVar(), tk.StringVar()  # label variable

    ex_var.trace('w', check_x)  # trace ex
    ey_var.trace('w', check_y)  # trace ey
    ex_var.trace('w', check_button)  # trace the button enable/disable
    ey_var.trace('w', check_button)  # same as above

    # input x
    tk.Label(window, width=wid, text="Enter x:").pack()
    ex = tk.Entry(window, textvariable=ex_var)
    ex.pack()
    lx = tk.Label(window, width=wid, textvariable=x_msg)
    lx.pack()

    # input y
    tk.Label(window, width=wid, text="Enter y:").pack()
    ey = tk.Entry(window, textvariable=ey_var)
    ey.pack()
    ly = tk.Label(window, width=wid, textvariable=y_msg)
    ly.pack()

    # confirm
    b = tk.Button(window, state=tk.DISABLED, text="Confirm", command=window.destroy)
    b.pack()

    window.mainloop()

    return var_x.get(), var_y.get()


# prompt the user to click on the map displayed and get the coordinate of the location being clicked
def mouse_click():
    pygame.init()
    screen = pygame.display.set_mode([SIZE_X, SIZE_Y], 0, 32)  # size of window
    map_path = "map/ntu_campus_map.png"
    image = pygame.image.load(map_path)  # image must be in the same folder, else path must be specified
    screen.blit(image, [0, 0])  # position of the image on the window
    while True:
        position = pygame.mouse.get_pos()  # Position of mouse on window
        button = pygame.mouse.get_pressed()  # Ensure which part of the mouse press on the screen
        pygame.display.set_caption("NTU Campus Map [Mouse Position -> " + str(position) + "]")  # title of the window
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONUP and button[0] == 1:  # mouse left click
                pygame.quit()
                return position


# prompt the user to select how to input the current location, either by manually input or clicking on the map
def get_user_location():

    mm.window.destroy()

    ins = up.multiple_choice("Location", "Please enter your location", "Manual Input", "Mouse Click")
    position = 0, 0  # default

    if ins == "Manual Input":
        position = enter_coordinate()
    elif ins == "Mouse Click":
        position = mouse_click()

    return position


# calculate the straight line distance between current location and canteens
def straight_line(location_of_a, location_of_b):
    distance = sqrt((location_of_a[0] - location_of_b[0]) ** 2 + (location_of_a[1] - location_of_b[1]) ** 2)
    return distance


# sort the canteens by distance
# the user can choose from three types of distance
# 1 - straight line distance measured on the map
# 2 - the walking time
# 3 - the traveling time by walking and taking the shuttle bus
def sort_distance(user_location):

    ins = up.multiple_choice("Calculating Method",
                             "User location = "+str(user_location)+"\n"+"Please choose the calculating method",
                             "Straight-line Distance",
                             "Walk",
                             "Shuttle Bus")

    if ins == "Straight-line Distance":

        tree = ET.parse('dataset/dataset.xml')
        root = tree.getroot()

        canteen_data = []
        location_data = []

        for child in root.findall('canteen'):
            canteen_data.append(child.find('name').text)
            location_data.append((int(child.find('location_x').text), int(child.find('location_y').text)))

        distance_list = [straight_line(user_location, each_location) for each_location in location_data]
        canteen_distance = [[canteen_data[i], distance_list[i]] for i in range(len(canteen_data))]

        sort_list = listsort(canteen_distance, 1)

    elif ins == "Walk":
        sort_list = tp.transport(user_location[0], user_location[1], "walk")
    elif ins == "Shuttle Bus":
        sort_list = tp.transport(user_location[0], user_location[1], "shuttle")

    window_setup()
    window.title("Sort by Distance - " + ins)

    def distance_data():
        nonlocal ins
        counter, wid = 0, 35
        tk.Label(frame, text="Canteen", width=wid, font=("Calibri", 20)).grid(row=counter)
        if ins == "Straight-line Distance":
            tk.Label(frame, text="Distance/pixels", font=("Calibri", 20)).grid(row=counter, column=1)
        else:
            tk.Label(frame, text="Time/minutes", font=("Calibri", 20)).grid(row=counter, column=1)

        for i in sort_list:
            counter += 1
            tk.Label(frame, text=i[0], width=wid).grid(row=counter)
            tk.Label(frame, text=("%.2f" % i[1])).grid(row=counter, column=1)

        tk.Button(frame, text="Main Menu", command=lambda: mm.back_menu(window)).grid(row=counter + 1)
        tk.Button(frame, text="Quit", command=quit_action).grid(row=counter + 1, column=1)

    frame = frame_setup()
    distance_data()
    window.mainloop()


# function to be called in module main
# prompt the user to input the current location and recommend canteens based on distance
def call_distance():
    p = get_user_location()
    sort_distance(p)
    window.mainloop()


# enable user to return back to the first interface of the program
def back_menu():
    window.destroy()
    mm.main_menu()
