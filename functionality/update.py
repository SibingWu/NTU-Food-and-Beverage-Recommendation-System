import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import messagebox

from functionality import main as mm, display as mp

tree = ET.parse('dataset/dataset.xml')
root = tree.getroot()


# helper function to display multiple choices on the window
def multiple_choice(title, label, *args, _label=None):
	global window
	window = mp.window_setup()
	window.title(title)
	tk.Label(window, text=label, font=("Calibri", 20)).pack()
	if _label:
		tk.Label(window, text=_label, font=("Calibri", 16)).pack()
	type_name = tk.StringVar()
	type_name.set(-1)
	if isinstance(args[0], tuple) or isinstance(args[0], list):
		for type in args[0]:
			tk.Radiobutton(window, variable=type_name, value=type, text=type, font=("Calibri", 16),
			               command=lambda: mp.enable_button(b)).pack()
	else:
		for type in args:
			tk.Radiobutton(window, variable=type_name, value=type, text=type,
			               command=lambda: mp.enable_button(b)).pack()
	
	b = tk.Button(window, state=tk.DISABLED, text="Confirm", command=window.destroy)
	b.pack()
	window.mainloop()
	return type_name.get()


# display a message box saying that the update is successfully
# prompt the user to either get back to the main menu or quit from the program
def update_success():
	global window
	window = mp.window_setup()
	window.title("Yah!")
	tk.Label(text="Thanks for your updating!\nYou can either go back to menu or exit the program.\n",
	         font=("Calibri", 24)).pack()
	tk.Button(text="Main Menu", command=back_menu).pack()
	tk.Button(text="Quit", command=mp.quit_action).pack()
	messagebox.showinfo("Yah!", "Update Successfully!")
	window.mainloop()


# update the price of a food stored in the dataset
def update_price(food_name, new_price):
	for child in root:
		if child.tag == "stall":
			if child.find("signature").text == food_name:
				child.find("price").text = str(new_price)
	tree.write("dataset/dataset.xml")


# update the name of a food stored in the dataset
def update_name(old_name, new_name):
	for child in root:
		if child.tag == "stall" and child.find("name").text == old_name:
			child.find("signature").text = new_name
	tree.write("dataset/dataset.xml")


# update the type of a canteen stored in the dataset
def update_type(canteen_name, type, new_type):
	for child in root:
		if child.tag == "canteen" and child.find("name").text == canteen_name:
			child.find(type).text = new_type
	tree.write("dataset/dataset.xml")


# update the ranking of a canteen stored in the dataset
def update_ranking(canteen_name, attitude):
	for child in root:
		if child.tag == "canteen" and child.find("name").text == canteen_name:
			ranking = int(child.find('ranking').text)
			child.find('ranking').text = str(ranking + attitude)
	tree.write("dataset/dataset.xml")


# function to be called in module main
# prompt the user to update the price of a food
# modify the record in the dataset.xml by calling update_price(food_name, new_price)
def call_update_price():
	mm.window.destroy()

	food_list = []
	for child in root.findall('stall'):
		food_list.append(child.find("signature").text)

	food = multiple_choice("Update Price", "Please select the food you want to update", food_list)
	
	for child in root:
		if child.tag == "stall":
			if child.find("signature").text == food:
				old_price = child.find("price").text
				
	def check(var, mode, event):
		cor_msg = "Correct!"
		wrong_msg = "Invalid!"

		def is_price(s):
			try:
				if float(s) >= 0:
					return True
				return False
			except:
				return False

		if is_price(price_str.get()):
			lb_msg.set(cor_msg)
			price.set(price_str.get())
			l["fg"] = "green"
			b["state"] = tk.NORMAL
		else:
			lb_msg.set(wrong_msg)
			l["fg"] = "red"
			b["state"] = tk.DISABLED

	window = mp.window_setup()
	window.title("Enter New Price")
	tk.Label(window, text="The original price of " + food + " is $" + old_price + ".").pack()
	tk.Label(window, text="Please enter the new price").pack()
	price_str, price = tk.StringVar(), tk.DoubleVar()
	lb_msg = tk.StringVar()
	price_str.trace("w", check)
	e = tk.Entry(window, textvariable=price_str)
	e.pack()
	l = tk.Label(window, textvariable=lb_msg)
	l.pack()
	b = tk.Button(window, state=tk.DISABLED, text="Confirm", command=window.destroy)
	b.pack()

	window.mainloop()
	update_price(food_name=food, new_price=price.get())
	update_success()


# function to be called in module main
# prompt the user to update the name of a food
# modify the record in the dataset.xml by calling update_name(old_name, new_name)
def call_update_name():
	mm.window.destroy()

	stall_list = []
	for child in root.findall("stall"):
		stall_list.append(child.find("name").text)


	stall_name = multiple_choice("Update Food Name", "Please select the stall you want to update", stall_list)
	for child in root.findall("stall"):
		if child.find("name").text == stall_name:
			food_name = child.find("signature").text
	
	def check(var, mode, event):
		cor_msg = "Correct!"
		wrong_msg = "New stall name cannot be blank!"
		if not new_name.get():
			msg.set(wrong_msg)
			lb["fg"] = "red"
			b["state"] = tk.DISABLED
		else:
			msg.set(cor_msg)
			lb["fg"] = "green"
			b["state"] = tk.NORMAL
			
	window = mp.window_setup()
	window.title("Enter New Stall Name")
	tk.Label(window, text="The original name of the food is \"" + food_name + "\"").pack()
	tk.Label(window, text="Please enter the new food name").pack()
	new_name, msg = tk.StringVar(), tk.StringVar()
	e = tk.Entry(window, textvariable=new_name)
	e.pack()
	new_name.trace("w", check)
	lb = tk.Label(window, textvariable=msg)
	lb.pack()
	b = tk.Button(window, state=tk.DISABLED, text="Confirm", command=window.destroy)
	b.pack()
	window.mainloop()
	new_food_name = new_name.get()
	update_name(old_name=stall_name, new_name=new_food_name)
	update_success()


# function to be called in module main
# prompt the user to update the type of a canteen, either halal or veg
# modify the record in the dataset.xml by calling update_type(canteen_name, type, new_type)
def call_update_type():
	mm.window.destroy()
	type_high = multiple_choice("Choose Type", "Please choose the type you want to update", "Halal", "Veg")
	type = type_high.lower()
	
	canteen_list = []
	for child in root.findall('canteen'):
		canteen_list.append(child.find("name").text)
	canteen = multiple_choice("Update Canteen", "Please select the canteen you want to update", canteen_list)
	
	for child in root:
		if child.tag == "canteen" and child.find("name").text == canteen:
			old_str = child.find(type).text
			if old_str == '1':
				old_type = type_high
			else:
				old_type = ("not " + type).title()
	
	old_format = "Originally: " + canteen + " -> " + old_type
	new_type = multiple_choice("Choose "+type+" or not", "Please update "+type+" information", type_high, ("not "+type).title(), _label=old_format)
	if "Not" in new_type:
		new_type = '0'
	else:
		new_type = '1'

	update_type(canteen, type, new_type)
	update_success()


# function to be called in module main
# prompt the user to update the ranking of a food
# modify the record in the dataset.xml by calling update_ranking(canteen_name, attitude)
# attitude is represented as a integer, -1 stands for good and 1 stands for bad
def call_update_rank():
	mm.window.destroy()

	canteen_list = []
	for child in root.findall('canteen'):
			canteen_list.append(child.find("name").text)
	canteen = multiple_choice("Update Canteen", "Please select the canteen you want to update", canteen_list)
	
	attitude = multiple_choice("Your Attitude", "Please grade on this canteen: "+canteen, "Thumb up", "Thumb down")
	if attitude == "Thumb up":
		grade = -1
	else:
		grade = 1
	update_ranking(canteen, grade)
	update_success()


# enable user to return back to the first interface of the program
def back_menu():
	window.destroy()
	mm.main_menu()
