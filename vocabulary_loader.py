#Importing libraries and modules
import csv
import pygame
import gamestats_loader
import random


#Variables and lists for vocabulary
number_new_vocab = 0
number_correct_vocab = 0
number_total_vocab = 0
wrong_vocab = []
new_vocab = []
vocabulary = []

#rewrite the vocabulary file
def write_vocabulary():
    with open('vocabulary.csv', 'w', newline='') as f:
        fieldnames = ['English', 'Translation', 'New', 'Correct']
        writer = csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        for entry in vocabulary:
            writer.writerow({'English' : entry['English'], 'Translation' : entry['Translation'], 'New' : entry['New'], 'Correct' : entry['Correct']})

#Update specific fields
def update_vocabulary(vocab,updatedfieldname,value):
    global vocubalary
    for entry in vocabulary:
        if entry == vocab:
            entry[updatedfieldname] = value
#Assigning values to the global variables above
def analyse_progress():
    global number_new_vocab
    global number_correct_vocab
    global number_total_vocab
    global wrong_vocab
    global new_vocab
    global vocabulary

    #Reset local Vocabulary
    number_new_vocab = 0
    number_correct_vocab = 0
    wrong_vocab = []
    new_vocab = []

    #Read vocabulary
    with open('vocabulary.csv') as f:
        vocabulary = list(csv.DictReader(f))
    for entry in vocabulary:
    
        if entry['Correct'] == '0':
             wrong_vocab.append(entry)
        if entry['Correct'] == '1':
            number_correct_vocab += 1

        if entry['New'] == '1':
              new_vocab.append(entry)
              number_new_vocab += 1
               
        number_total_vocab = len(vocabulary)
        
#Returns the percentage of completion
def calculate_completion():
    return round((1 - (number_new_vocab / number_total_vocab)) * 100,2)

#Returns the percentage of correctness
def calculate_correctness():
    if number_total_vocab - number_new_vocab == 0:
        return 0
    return round((number_correct_vocab / (number_total_vocab - number_new_vocab)) * 100,2)



#Returns a random vocable fulfilling predefined conditions
def get_randomvocabulary():
    analyse_progress()
    if len(new_vocab) > 0 and len(new_vocab) < 15:
        for entry in new_vocab:
            return entry
    elif len(new_vocab) == 0 and len(wrong_vocab) > 0:
        for entry in wrong_vocab:
            return entry
  
    rand = random.randint(0,len(vocabulary)-1)
    return vocabulary[rand]

#Returns a vocable for the exam fulfilling predefined prerequisites
def get_exam():
    analyse_progress()
    category = random.randint(0,2)

    #Chose a wrong vocable
    if (category == 1 or category == 2) and len(wrong_vocab) > 0: #and len(wrong_vocab) != len(new_vocab):
        rand = random.randint(0,len(wrong_vocab)-1)
        #while wrong_vocab[rand] in new_vocab: -For demonstration purposes
            #rand = random.randint(0,len(wrong_vocab)-1)
        return wrong_vocab[rand]
    #Chose a random vocable
    else:
        rand = random.randint(0,len(vocabulary)-1)
        while vocabulary[rand] in new_vocab:
            rand = random.randint(0,len(vocabulary)-1)
        return vocabulary[rand]

#Checking if vocabulary is correct
def check_correctness(vocabulary,answer):
    #Removes trailing spaces
    correctanswer = vocabulary['Translation'].strip()
    ans = answer.strip()

    #Removing special signs
    correctanswer = correctanswer.replace(";","")
    correctanswer = correctanswer.replace(".","")
    correctanswer = correctanswer.replace("!","")
    correctanswer = correctanswer.replace(",","")
    correctanswer = correctanswer.replace("?","")

    ans = ans.replace(";","")
    ans = ans.replace(".","")
    ans = ans.replace("!","")
    ans = ans.replace(",","")
    ans = ans.replace("?","")

    #Capitalizing the answer
    correctanswer = correctanswer.capitalize()
    ans = ans.capitalize()

    return correctanswer == ans
     
#Check if exam prerequisites are fulfilled
def check_examprerequisites():
    analyse_progress()
    correctness = calculate_correctness()
    completness = calculate_completion()
    gamestats_loader.read_data()

    stats = gamestats_loader.game_stats
    currentlevel = stats[0]['Level']
    demandedcompletness = gamestats_loader.completness[currentlevel]
    demandedcorrectness = gamestats_loader.correctness[currentlevel]

    return correctness >= demandedcorrectness and completness >= demandedcompletness

#Checks if the player has passed the exam
def check_pass(correct):
       gamestats_loader.read_data()
       prerequisites = gamestats_loader.examconditions[gamestats_loader.game_stats[0]['Level']]
       return ((correct/10) *100) >= prerequisites

#Analyse progress when module is loaded
analyse_progress()
