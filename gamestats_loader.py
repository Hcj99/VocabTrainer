#Importing json
import json

#Variable to store dictionary
game_stats = []

#Lists containing information about current level
ranks = ['Elementary School', 'Junior High', 'High School', 'Undergraduate Student', 'Graduate Student', 'PhD student', 'Teaching Assistant', 'Associate Professor','Full Professor','Nobel Prize Laureate']
completness = [10,15,20,30,40,50,60,70,80,100]
correctness = [25,35,40,50,60,70,80,90,97,100]
examconditions = [50,50,50,60,60,60,70,80,90,100]

#Reading data from file and storing it into a list
def read_data():
    global game_stats
    with open('game_stats.json') as f:
        game_stats = json.load(f)


#Update a specific value  
def update_stats(fieldname,value):
    global game_stats
    game_stats[0][fieldname] = value

#Write new data to file
def write_stats():
    with open('game_stats.json', 'w') as f:
        json.dump(game_stats,f)




