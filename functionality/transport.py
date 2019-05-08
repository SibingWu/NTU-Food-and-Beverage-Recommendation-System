import xml.etree.ElementTree as ET

# retrieve data from dataset.xml file
tree = ET.parse('dataset/dataset.xml')
root = tree.getroot()

# using networkx package
# overview of networkx package on github: https://networkx.github.io/documentation/stable/
# installation guide: https://networkx.github.io/documentation/stable/install.html
import networkx as nx

shuttle = nx.Graph()
shuttle = nx.read_graphml("dataset/shuttle.graphml")

walk = nx.Graph()
walk = nx.read_graphml("dataset/walk.graphml")

from math import sqrt
from helper.sort import listsort

# helper function to find the nearest canteen / mark
def nearest_place(x, y, type):
    nearest = ""
    nearest_distance = 10000

    for child in root:
        if child.tag == type:
            place = child[0].text
            place_x = int(child[1].text)
            place_y = int(child[2].text)
            place_distance = sqrt((x-place_x)**2+(y-place_y)**2)

            if place_distance<nearest_distance:
                nearest=place
                nearest_distance=place_distance

    return nearest, nearest_distance//50


# helper function to return a list of sorted canteens based on time
def sorted_by_time (x, y, type):

    canteens = []
    for child in root:
        if child.tag == "canteen":
            canteens.append(child[0].text)

    canteen, canteen_time = nearest_place(x, y, "canteen")
    source, source_time= nearest_place(x, y, "mark")

    predecessors, distance = nx.dijkstra_predecessor_and_distance(type, source)

    sorted_transport = []

    for key in distance:
        if key == canteen:
            if (canteen_time<distance[key]+source_time):
                sorted_transport.append([key, canteen_time])
            else:
                sorted_transport.append([key, distance[key] + source_time])
        elif key in canteens:
            sorted_transport.append([key, distance[key]+source_time])

    return listsort(sorted_transport, 1)


# sort the canteens by transportation time
# the type of transportation can be either walk or shuttle
# return a list of lists
# the inner list contains the name of the canteen (the first element) and the transportation time (the second element)
def transport(x, y, type):
    if type == "walk":
        return sorted_by_time(x, y, walk)
    elif type == "shuttle":
        return sorted_by_time(x, y, shuttle)
    else:
        print("Invalid type of transportation")