import os.path as p
from helper.generater import generate_xml, generate_graphml

# set up the dataset
if not p.exists("dataset/dataset.xml"):
    generate_xml()
if not p.exists("dataset/walk.graphml") or not p.exists("dataset/shuttle.graphml"):
    generate_graphml()

from functionality.main import main_menu

# start the program
main_menu()