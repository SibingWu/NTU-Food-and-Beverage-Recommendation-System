import tkinter as tk

from functionality import search as rk, display as mp, update as up


# first interface when the program starts
# prompt the user to select either search for some information or update some information
def main_menu():
    global window
    window = mp.window_setup()
    window.title("Main Menu")
    tk.Label(window, text="Welcome to NTU Canteen searching program!\n",
             font=("Calibri", 24)).pack()
    wid = 8
    tk.Button(window, text="Search", command=search_menu, width=wid).pack()
    tk.Button(window, text="Update", command=update_menu, width=wid).pack()
    tk.Button(window, text="Quit", command=mp.quit_action).pack()
    window.mainloop()


# interface after the user have selected search
# prompt the user to choose the way the canteens are searched and displayed
def search_menu():
    global window
    window.destroy()
    wid = 18
    window = mp.window_setup()
    window.title("Search Menu")
    tk.Label(window, text="\n", font=("Calibri", 14)).pack()
    tk.Button(window, text="Sort by Distance", width=wid, command=mp.call_distance).pack()
    tk.Button(window, text="Sort by Rank", width=wid, command=rk.call_rank).pack()
    tk.Button(window, text="Search by Food", width=wid, command=rk.call_food).pack()
    tk.Button(window, text="Search by Price", width=wid, command=rk.call_price).pack()
    tk.Button(window, text="Search by Halal/Veg", width=wid, command=rk.call_search_by_type).pack()
    tk.Button(window, text="Main Menu", command=lambda: back_menu(window)).pack()
    tk.Button(window, text="Quit", command=mp.quit_action).pack()
    window.mainloop()

# interface after the user have selected update
# prompt the user to choose which information to be updated
def update_menu():
    global window
    window.destroy()
    wid = 16
    window = mp.window_setup()
    window.title("Update Menu")
    tk.Label(window, text="\n", font=("Calibri", 14)).pack()
    tk.Button(window, text="Update Price", width=wid, command=up.call_update_price).pack()
    tk.Button(window, text="Update Food Name", width=wid, command=up.call_update_name).pack()
    tk.Button(window, text="Update Halal/Veg", width=wid, command=up.call_update_type).pack()
    tk.Button(window, text="Update Rank", width=wid, command=up.call_update_rank).pack()
    tk.Button(window, text="Main Menu", command=lambda: back_menu(window)).pack()
    tk.Button(window, text="Quit", command=mp.quit_action).pack()
    window.mainloop()

# enable user to return back to the first interface of the program
def back_menu(window):
    window.destroy()
    main_menu()