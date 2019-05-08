import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import messagebox

from functionality import main as mm, display as mp, update as up
from helper.sort import listsort


# prompt the user to get back to the first interface when no valid output
def menu_quit(return_value):
	window.title("No Suggested Food")
	tk.Label(text="You can either go back to the menu or exit the program.\n", font=("Calibri", 24)).pack()
	tk.Button(text="Main Menu", command=back_menu).pack()
	tk.Button(text="Quit", command=mp.quit_action).pack()
	messagebox.showinfo("Sorry", return_value)


# search all canteens and display the canteen which has the wanted food
def search_by_food(foodname):
	tree = ET.parse('dataset/dataset.xml')
	root = tree.getroot()
	stall, price = None, None
	for child in root:
		if child.tag == "stall" and child[1].text == foodname:
			stall = child[0].text
			price = float(child[2].text)
			break
	
	canteens = []
	for child in root:
		if child.tag == "canteen":
			for grandchild in child:
				if grandchild.tag == 'stall' and grandchild.text == stall:
					canteens.append(child[0].text)
	if canteens:
		return_value = (foodname, price, stall, canteens)
	else:
		return_value = "Sorry, there is no such food: " + foodname

	global window
	window = mp.window_setup()
	if isinstance(return_value, tuple):
		window.title("Sort by Food")

		def food_data():
			lb_format = "The food %s is available in %s.\nThe price is %.1f.\nThe following canteens have this stall."
			tk.Label(frame, text=lb_format % (return_value[0], return_value[2], return_value[1]),
					 width=55, font=("Calibri", 20)).grid(row=0, column=0)
			for canteen in return_value[3]:
				tk.Label(frame, text=canteen).grid()
			tk.Button(frame, text="Main Menu", command=back_menu).grid()
			tk.Button(frame, text="Quit", command=mp.quit_action).grid()

		frame = mp.frame_setup()
		food_data()
	else:
		menu_quit(return_value)
	window.mainloop()


# display the canteens by their rankings
def sort_by_rank():
	tree = ET.parse('dataset/dataset.xml')
	root = tree.getroot()
	canteens = []
	for child in root:
		if child.tag == "canteen":
			canteens.append([child.find('name').text, int(child.find('ranking').text)])
	
	canteen_rankings = listsort(canteens, 1)
	for i in range(len(canteen_rankings)):
		canteen_rankings[i][1]=i+1
	
	global window
	
	mm.window.destroy()
	window = mp.window_setup()
	window.title("Sort by Rank")
	
	def rank_data():
		counter, wid = 0, 27
		tk.Label(frame, text="Rank", width=wid, font=("Calibri", 20)).grid(row=counter)
		tk.Label(frame, text="Canteen", font=("Calibri", 20)).grid(row=counter, column=1)
		for k, v in canteen_rankings:
			counter += 1
			tk.Label(frame, text=v, width=wid).grid(row=counter)
			tk.Label(frame, text=k, width=wid).grid(row=counter, column=1)
		
		tk.Button(frame, text="Main Menu", command=back_menu).grid(row=counter + 1)
		tk.Button(frame, text="Quit", command=mp.quit_action).grid(row=counter + 1, column=1)
	
	frame = mp.frame_setup()
	rank_data()


# search all canteens and display the food within the requested price range
def search_by_price(price):
	tree = ET.parse('dataset/dataset.xml')
	root = tree.getroot()

	chosen_food_list = []
	chosen_price_list = []
	chosen_stall_list = []
	chosen_canteen_list = []
	
	for child in root:
		if child.tag == "stall" and price[1] <= float(child.find('price').text) <= price[0]:
			chosen_food_list.append(child.find('signature').text)
			chosen_price_list.append(child.find('price').text)
			chosen_stall_list.append(child.find('name').text)
	
	for i in range(len(chosen_stall_list)):
		canteens = []
		for child in root:
			if child.tag == "canteen":
				for grandchild in child:
					if grandchild.tag == 'stall' and grandchild.text == chosen_stall_list[i]:
						canteens.append(child[0].text)
		chosen_canteen_list.append(canteens)
	
	if len(chosen_food_list) == 0:
		return_value = "Sorry, there are no food within your acceptable range."
	else:
		return_value = (chosen_food_list, chosen_price_list, chosen_stall_list, chosen_canteen_list)
	
	global window
	window = mp.window_setup()
	if isinstance(return_value, tuple):
		window.title("Search by Price")
		
		def price_data():
			def counter_plus():
				nonlocal counter
				counter += 1
			
			wid = 22
			counter = 0
			tk.Label(frame, text="Eligible Food List", font=("Calibri", 20)).grid(row=counter, column=1)
			counter += 1
			
			for i in range(len(return_value[0])):
				tk.Label(frame, text="Food", width=wid).grid(row=counter)
				tk.Label(frame, text="Price", width=wid - 10).grid(row=counter, column=1)
				tk.Label(frame, text="Stall", width=wid).grid(row=counter, column=2)
				counter_plus()
				
				tk.Label(frame, text=return_value[0][i], width=wid).grid(row=counter)
				tk.Label(frame, text="%.1f" % float(return_value[1][i]), width=wid - 10).grid(row=counter, column=1)
				tk.Label(frame, text=return_value[2][i], width=wid).grid(row=counter, column=2)
				
				counter_plus()
				tk.Label(frame, text="Available Canteen List", width=wid).grid(row=counter, column=1)
				for j in range(len(return_value[3][i])):
					counter_plus()
					tk.Label(frame, text=return_value[3][i][j]).grid(row=counter, column=1)
				counter_plus()
				
				for i in range(3):
					tk.Label(frame, text=" ").grid(row=counter, column=i)
				counter_plus()
			
			tk.Button(frame, text="Main Menu", command=back_menu).grid(row=counter + 1, column=0)
			tk.Button(frame, text="Quit", command=mp.quit_action).grid(row=counter + 1, column=2)
		
		frame = mp.frame_setup()
		price_data()
	
	else:
		menu_quit(return_value)
	window.mainloop()


# return a list of the required type (either halal or veg)
def return_type(type):
	tree = ET.parse('dataset/dataset.xml')
	root = tree.getroot()

	type_list = []
	for child in root:
		if child.tag == "canteen" and child.find(type).text == '1':
			type_list.append(child.find('name').text)
	
	return type_list


# return if the canteen is of the specific type (either halal or veg)
def search_by_type(canteen_name, type):
	tree = ET.parse('dataset/dataset.xml')
	root = tree.getroot()

	for child in root:
		if child.tag == "canteen" and child.find('name').text == canteen_name:
			if child.find(type).text == "1":
				return True
			else:
				return False


# prompt the user to select the name of the food
def get_food():
	tree = ET.parse('dataset/dataset.xml')
	root = tree.getroot()

	def manual_input():
		window = mp.window_setup()
		window.title("Manual Input")
		food_var = tk.StringVar()
		tk.Label(window, text="Enter the food you want to look for", font=("Calibri", 20)).pack()
		tk.Entry(window, textvariable=food_var).pack()
		tk.Button(window, text="Confirm", command=window.destroy).pack()
		window.mainloop()
		return food_var.get()

	food_list_format = ""

	food_list = []
	for child in root.findall('stall'):
		food_list.append(child.find("signature").text)
	for food in food_list:
		food_list_format += food + "\n"
	mm.window.destroy()
	ins = up.multiple_choice("Search by Food", "Cuisine Available:",
							 "Select", "Manual Input", _label=food_list_format)
	food = ""  # default

	if ins == "Select":
		food = up.multiple_choice("Select", "Choose your favorite food", food_list)
	elif ins == "Manual Input":
		food = manual_input()

	return food


# prompt the user to input the acceptable price range
def get_price():
	# sample messages
	cor_msg = "Correct!"
	wrong_msg = "Invalid!"
	value_msg = "Lower limit is bigger than upper limit!"
	
	def check_button(var, mode, event):
		def is_pos_float(s):
			try:
				if float(s) >= 0:
					return True
				return False
			except ValueError:
				return False
		
		if is_pos_float(up_var.get()) and is_pos_float(low_var.get()):
			if float(low_var.get()) <= float(up_var.get()):
				up_float.set(up_var.get())
				low_float.set(low_var.get())
				l_msg.set(cor_msg)
				lb["fg"] = "green"
				b["state"] = tk.NORMAL
			else:
				l_msg.set(value_msg)
				lb["fg"] = "red"
				b["state"] = tk.DISABLED
		else:
			b["state"] = tk.DISABLED
			if not (up_var.get() or low_var.get()) or \
					(is_pos_float(up_var.get()) and not low_var.get() or
					 is_pos_float(low_var.get()) and not up_var.get()):
				l_msg.set("")
			else:
				l_msg.set(wrong_msg)
				lb["fg"] = "red"
	
	global window
	# close the menu window
	mm.window.destroy()
	# setup the new window
	window = mp.window_setup()
	window.title("Search by Price")
	
	up_float, low_float = tk.DoubleVar(), tk.DoubleVar()  # return value
	up_var, low_var = tk.StringVar(), tk.StringVar()  # entry variable
	l_msg = tk.StringVar()  # label variable
	
	up_var.trace("w", check_button)
	low_var.trace("w", check_button)
	
	tk.Label(window, text="Enter the upper limit of your acceptable price").pack()
	e_up = tk.Entry(window, textvariable=up_var)
	e_up.pack()
	tk.Label(window, text="Enter the lower limit of your acceptable price").pack()
	e_low = tk.Entry(window, textvariable=low_var)
	e_low.pack()
	
	lb = tk.Label(window, width=50, textvariable=l_msg)
	lb.pack()
	
	# confirm
	b = tk.Button(window, state=tk.DISABLED, text="Confirm", command=window.destroy)
	b.pack()
	window.mainloop()
	# print(up_float.get(), low_float.get())
	return up_float.get(), low_float.get()


# function to be called in module main
# prompt the user to select a food by calling get_food()
# and display the canteens which have that food by calling search_by_food()
def call_food():
	food = get_food()
	search_by_food(food)
	window.mainloop()


# function to be called in module main
# display the canteens by their rankings by calling sorted_by_rank()
def call_rank():
	sort_by_rank()
	window.mainloop()


# function to be called in module main
# prompt the user to input the acceptable price range by calling get_price()
# search all canteens and display the food within the requested price range by calling search_by_price()
def call_price():
	price = get_price()
	search_by_price(price)
	window.mainloop()


# helper function used by call_search_by_halal and call_search_by_veg
# window display the selection between two functionality
# 1 - return a list of the required type (either halal or veg)
# 2 - return if the canteen is of the specific type (either halal or veg)
def call_search_by_type():
	tree = ET.parse('dataset/dataset.xml')
	root = tree.getroot()

	global window
	mm.window.destroy()
	
	def check_certain():

		def check(canteen):
			search = search_by_type(canteen, ins_type.lower())
			if search:
				messagebox.showinfo(ins_type, canteen + " is in the " + ins_type + " list.")
			else:
				messagebox.showinfo("Not " + ins_type, canteen + " is not in the " + ins_type + " list.")

		global window
		window = mp.window_setup()
		window.title("Check a certain canteen")
		var = tk.StringVar()
		var.set(0)
		counter, wid = 1, 44
		tk.Label(window, text="Please tick the button and\nPress the Confirm button to check",
		         width=wid, font=("Calibri", 20)).grid(row=0, column=1)

		canteen_data = []
		for child in root.findall('canteen'):
				canteen_data.append(child[0].text)

		for canteen in canteen_data:
			tk.Radiobutton(window, variable=var, value=canteen, text=canteen,
			               command=lambda: mp.enable_button(b), font=("Calibri", 14)).grid(row=counter, column=1)
			counter += 1
		b = tk.Button(window, state=tk.DISABLED, text="Confirm", command=lambda: check(var.get()))
		b.grid(row=counter, column=1)
		
		tk.Button(text="Main Menu", command=back_menu).grid(row=counter+1, column=0)
		tk.Button(text="Quit", command=mp.quit_action).grid(row=counter+1, column=2)

	def return_all():
		halal_list = return_type(ins_type.lower())
		global window
		window = mp.window_setup()
		window.title("Return all " + ins_type + " canteen list")
		tk.Label(window, text="The " + ins_type + " list is as follows:", font=("Calibri", 24)).pack()
		for canteen in halal_list:
			tk.Label(window, text=canteen, font=("Calibri", 18)).pack()
		tk.Button(text="Main Menu", command=back_menu).pack()
		tk.Button(text="Quit", command=mp.quit_action).pack()
	
	ins_type = up.multiple_choice("Search by Halal/Veg", "Please choose Halal or Veg", "Halal", "Veg")
	ins_method = up.multiple_choice("Search by " + ins_type, "Please proceed", "Check a certain canteen",
	                                "Return all " + ins_type + " canteen list")

	if ins_method == "Check a certain canteen":
		check_certain()
	else:
		return_all()
	window.mainloop()

# enable user to return back to the first interface of the program
def back_menu():
	window.destroy()
	mm.main_menu()
