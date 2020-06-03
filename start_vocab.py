#importing libraries and modules
import vocabulary_loader
import gamestats_loader
import pygame
import sys
from text_box_class import *
import sendgrid_certificate
# Initialize the screen

pygame.init()
#set screen size
screen_length = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_length,screen_height))

#Caption
pygame.display.set_caption("Vocab Trainer")
#setting button and textbox sizes
general_buttonlength = 200
general_buttonheight = 80
general_buttonfontsize = 30

general_textboxlength = 800
general_textboxheight = 80

font = pygame.font.SysFont('Comic Sans MS', 24)


#Generic function displaying an image on the screen
def show_image(image_name,x,y):
    image = pygame.image.load(image_name)
    screen.blit(image, (x,y))

#Creating and returning a text object
def textObject(text,font,Color=(0,0,0)):
    textArea = font.render(text, True , Color)
    return textArea,textArea.get_rect()
#The main menu of the game
def game_intro():
    intro = True

    #While loop infinitely displaying the buttons
    while intro:
        #Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # RGB - Red, Green, Blue  
        screen.fill((200,230,255))
        #Display logo
        show_image('dictionary.png', screen_length//2-50,screen_height//2-50)

        #Variables for clicks on buttons
        mouse = pygame.mouse.get_pos()
        klick = pygame.mouse.get_pressed()

        #Printing text label
        largeText = pygame.font.Font('freesansbold.ttf',90)
        TextSurf, TextRect = textObject("Vocab Trainer", largeText)
        TextRect.center = (screen_length//2, 200)
        screen.blit(TextSurf, TextRect)

        #Resetting button variable
        button_state = "NONE"

        #Displaying the buttons and checking its value

        button_state = button(mouse,klick,screen_length//2- general_buttonlength//2 - (100 + general_buttonlength),screen_height//2+(general_buttonheight+50),"Practice",general_buttonlength,general_buttonheight,(20,40,200),(90,150,255))

        #Check if the exam is ready
        if button_state == "Practice":
            return button_state

        #Check if the exam is ready
        if vocabulary_loader.check_examprerequisites():
            button_state = button(mouse,klick,screen_length//2- general_buttonlength//2,screen_height//2+ (general_buttonheight+50),"Exam",general_buttonlength,general_buttonheight,(20,40,200),(90,150,255))
        else:
            button(mouse,klick,screen_length//2- general_buttonlength//2,screen_height//2+ (general_buttonheight+50),"Exam",general_buttonlength,general_buttonheight,(190,190,190),(190,190,190))
        if button_state == "Exam":
            return button_state

        button_state = button(mouse,klick,screen_length//2- general_buttonlength//2 + (100 + general_buttonlength),screen_height//2+(general_buttonheight+50),"Stats",general_buttonlength,general_buttonheight,(20,40,200),(90,150,255))

        if button_state == "Stats":
            return button_state

        #Updating screen
        pygame.display.flip()
        pygame.time.wait(200)
        pygame.display.update()
   
#Method that handles button clicks
def button(mouse,klick,bx,by, message, length,height, active_color, passive_color, player_name = "", email = ""):
    #Checking if person clicked on the button
    if mouse[0] > bx and mouse[0] < bx + length and mouse[1] > by and mouse[1] < by + height:
        pygame.draw.rect(screen, active_color, (bx,by,length,height))
        #Waiting to ensure that the previous event isn't active anymore
        pygame.time.wait(50)
        #Check the button value
        if klick[0] == 1:
            if message == "Menu":
                return "Menu"
            if message == "Practice":
                return "Practice"
            if message == "Exam":
                return "Exam"
            if message == "Stats":
                return "Stats"
        
            if message == "Next":
                return "Practice"

            if message == "Continue":
                return "Continue"
            #Advancing the player's rank
            if message == "Advance Rank":
                sendgrid_certificate.send_certificate(gamestats_loader.ranks[gamestats_loader.game_stats[0]['Level']],player_name, email)
                if gamestats_loader.game_stats[0]['Level'] < 9:
                    gamestats_loader.read_data()
                    gamestats_loader.update_stats('Level',gamestats_loader.game_stats[0]['Level']+1)
                    gamestats_loader.write_stats()
                return "Certificate"

            if message == "Back":
                #Updating player data
                gamestats_loader.read_data()
                gamestats_loader.update_stats('Player_Name',player_name)
                gamestats_loader.update_stats('Email',email)
                gamestats_loader.write_stats()
                return "Back"


    else:
        pygame.draw.rect(screen, passive_color, (bx,by,length,height))
        
    pygame.draw.rect(screen,(0,0,0), (bx,by,length,height),1)
    textBackground,textBox = textObject(message,font)
    textBox.center = ((bx+(length//2)),(by+(height//2)))
    screen.blit(textBackground, textBox)
    return "NONE"

#Function that handles practice mode
def Practice_Mode(entry):
    #defining textbox for answer
    text_boxes = []
    text_box = Text_box(screen_length//2 - general_textboxlength//2 ,screen_height//2 ,general_textboxlength,general_textboxheight)
    text_boxes.append(text_box)
    game =  True
    
    #Waiting to ensure that the previous event isn't active anymore
    pygame.time.wait(150)

    #Main loop
    while game:

        mouse = pygame.mouse.get_pos() 
        klick = pygame.mouse.get_pressed()

        #Handling text box events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for box in text_boxes:
                    box.check_click(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                for box in text_boxes:
                    if box.active:
                        box.add_text(event.key)
         # RGB - Red, Green, Blue  
        screen.fill((200,230,255))

        
        #Printing text label
        largeText = pygame.font.Font('freesansbold.ttf',70)

        TextSurf, TextRect = textObject(entry['English'], largeText)
        TextRect.center = (screen_length//2,200)
        screen.blit(TextSurf, TextRect)

        #Drawing text boxes
        text_box.draw(screen)
        
        #Resetting buttons
        button_state = "NONE"

        button_state = button(mouse,klick,screen_length//2- general_buttonlength//2,screen_height//2+ (general_buttonheight+50),"Menu",general_buttonlength,general_buttonheight,(20,40,200),(90,150,255))
        

        if button_state == "Menu":
            return button_state

        button_state = button(mouse,klick,screen_length//2- general_buttonlength//2 + (100 + general_buttonlength),screen_height//2+(general_buttonheight+50),"Next",general_buttonlength,general_buttonheight,(20,40,200),(90,150,255))

        #Updating vocabulary
        if button_state == "Practice":
            vocabulary_loader.update_vocabulary(entry,'New', 0)

            #Storing answer in variable
            answer = text_box.return_value()

            #Checking correctness of answer  and update correct flag
            if vocabulary_loader.check_correctness(entry,answer):
                vocabulary_loader.update_vocabulary(entry,'Correct',1)
                vocabulary_loader.write_vocabulary()
                TextSurfAnswer, TextRectAnswer = textObject("Correct!", largeText, (0,255,0))
                TextRectAnswer.center = (screen_length//2,100)
                screen.blit(TextSurfAnswer, TextRectAnswer)
                pygame.display.flip()
                pygame.time.wait(1000)

            #If answer is incorrect, set correct to false
            else:
                vocabulary_loader.update_vocabulary(entry,'Correct',0)
                TextSurfAnswer, TextRectAnswer = textObject(f"Wrong: {entry['Translation']}", largeText, (255,0,0))
                TextRectAnswer.center = (screen_length//2,100)
                screen.blit(TextSurfAnswer, TextRectAnswer)
                pygame.display.flip()
                pygame.time.wait(1250)
                vocabulary_loader.write_vocabulary()
            return button_state

        pygame.display.flip()

        
        pygame.time.wait(200)
        #Rewrite data in csv file
        vocabulary_loader.write_vocabulary()

#Function that handles the exam mode
def Exam_Mode(entry):
    #defining textbox for answer
    text_boxes = []
    text_box = Text_box(screen_length//2 - general_textboxlength//2 ,screen_height//2 ,general_textboxlength,general_textboxheight)
    text_boxes.append(text_box)
    game =  True
    #Main loop
    pygame.time.wait(150)

    while game:

        mouse = pygame.mouse.get_pos() 
        klick = pygame.mouse.get_pressed()

        #Handling text box events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for box in text_boxes:
                    box.check_click(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                for box in text_boxes:
                    if box.active:
                        box.add_text(event.key)
        # RGB - Red, Green, Blue  
        screen.fill((200,230,255))

        
        #Printing text label
        largeText = pygame.font.Font('freesansbold.ttf',70)
        TextSurf, TextRect = textObject(entry['English'], largeText)
        TextRect.center = (screen_length//2,200)
        screen.blit(TextSurf, TextRect)

      
        text_box.draw(screen)
        

        button_state = "NONE"

        button_state = button(mouse,klick,screen_length//2- general_buttonlength//2 + (100 + general_buttonlength),screen_height//2+(general_buttonheight+50),"Continue",general_buttonlength,general_buttonheight,(20,40,200),(90,150,255))

        #Check if player continues
        if button_state == "Continue":

            #Check Correctness and update vocabulary
            answer = text_box.return_value()
            if vocabulary_loader.check_correctness(entry,answer):
                vocabulary_loader.update_vocabulary(entry,'Correct',1)
                vocabulary_loader.write_vocabulary()
            else:
                vocabulary_loader.update_vocabulary(entry,'Correct',0)
                vocabulary_loader.write_vocabulary()

            #Return if answer was correct
            return vocabulary_loader.check_correctness(entry,answer)

        pygame.display.flip()

        
        pygame.time.wait(200)
        pygame.display.update()
        vocabulary_loader.write_vocabulary()

#Function that displays the Exam results
def show_results(answers,questions):

    # RGB - Red, Green, Blue  
    screen.fill((200,230,255))
    correct = 0
    display = "NONE"
    count = 0

    #Delay to ensure that event handler is reset
    pygame.time.wait(100)
    text = "Your Results"
    largeText = pygame.font.Font('freesansbold.ttf',70)
    TextSurf, TextRect = textObject(f" {text}", largeText)
    TextRect.center = (screen_length//2,80 + count * 50)
    screen.blit(TextSurf, TextRect)

    #Counting number of correct answers
    for answer in answers:
        if answer == True:
            correct = correct + 1
            display = "Correct"
        else:
            display = "False"

        #Displaying the question
        text = questions[count]['English']
        largeText = pygame.font.Font('freesansbold.ttf',40)
        TextSurf, TextRect = textObject(f" {text}: {display}", largeText)
        TextRect.center = (screen_length//2,150 + count * 50)
        screen.blit(TextSurf, TextRect)
        count = count + 1

    #Check if player has passed the exam
    if vocabulary_loader.check_pass(correct):
        text = "Pass"
    else:
        text = "Not pass"

    largeText = pygame.font.Font('freesansbold.ttf',40)

    #Displaying the achieved percentage
    TextSurf, TextRect = textObject(f" {text}: {int(correct/10*100)}% / {gamestats_loader.examconditions[gamestats_loader.game_stats[0]['Level']]}%", largeText)
    TextRect.center = (screen_length//2, 750)
    screen.blit(TextSurf, TextRect)

    pygame.display.flip()
    pygame.display.update()

    showing = True

    #Loop waiting for user input
    while showing:
        mouse = pygame.mouse.get_pos() 
        klick = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        button_state = "NONE"

        #Determinesd what button is to be displayed
        if vocabulary_loader.check_pass(correct):

            button_state = button(mouse,klick,screen_length//2- general_buttonlength//2 + (100 + general_buttonlength),screen_height//2+(general_buttonheight+50) + 100 ,"Advance Rank",general_buttonlength,general_buttonheight,(20,40,200),(90,150,255),gamestats_loader.game_stats[0]['Player_Name'],gamestats_loader.game_stats[0]['Email'])
        else:
            button_state = button(mouse,klick,screen_length//2- general_buttonlength//2 + (100 + general_buttonlength),screen_height//2+(general_buttonheight+50) + 100 ,"Menu",general_buttonlength,general_buttonheight,(20,40,200),(90,150,255))
        
        #Return button value
        if button_state == "Certificate":
            return "Certificate"
        if button_state == "Menu":
            return "Menu"

        pygame.display.flip()
        pygame.time.wait(200)
        pygame.display.update()

#Function that handles statistics
def Stats_Mode():
    vocabulary_loader.analyse_progress()
    gamestats_loader.read_data()
    #defining textbox for player data
    text_boxes = []
    text_box_name = Text_box(screen_length//2 - general_textboxlength//2 ,210,general_textboxlength - 10,general_textboxheight - 10, gamestats_loader.game_stats[0]['Player_Name'])
    text_box_email = Text_box(screen_length//2 - general_textboxlength//2 ,300 ,general_textboxlength - 10,general_textboxheight - 10, gamestats_loader.game_stats[0]['Email'])
    text_boxes.append(text_box_name)
    text_boxes.append(text_box_email)

    # RGB - Red, Green, Blue  
    screen.fill((200,230,255))
    stats = True

    #Calculate completion and correctness
    completion = vocabulary_loader.calculate_completion()
    correctness = vocabulary_loader.calculate_correctness()

    #Loading corrent level
    stats = gamestats_loader.game_stats
    rank = gamestats_loader.ranks[stats[0]['Level']]

    #Displaying the current rank
    largeText = pygame.font.Font('freesansbold.ttf',70)
    TextSurf, TextRect = textObject(rank, largeText)
    TextRect.center = (screen_length//2,150)
    screen.blit(TextSurf, TextRect)
    pygame.display.flip()

    #Displaying completion and correctness
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect = textObject(f"Completion: {completion}% / {gamestats_loader.completness[gamestats_loader.game_stats[0]['Level']]}%", largeText)
    TextRect.center = (screen_length//2, 420)
    screen.blit(TextSurf, TextRect)
    pygame.display.flip()

    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect = textObject(f"Correctness: {correctness}% / {gamestats_loader.correctness[gamestats_loader.game_stats[0]['Level']]}%", largeText)
    TextRect.center = (screen_length//2, 500)
    screen.blit(TextSurf, TextRect)
    pygame.display.flip()

    #Displaying total number of vocabulary
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect = textObject("Total Vocabulary: " + str(len(vocabulary_loader.vocabulary)), largeText)
    TextRect.center = (screen_length//2, 580)
    screen.blit(TextSurf, TextRect)
    pygame.display.flip()

    #Waiting for user input
    while stats:
        #Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for box in text_boxes:
                    box.check_click(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                for box in text_boxes:
                    if box.active:
                        box.add_text(event.key)
        #Drawing text boxes
        for box in text_boxes:
            box.draw(screen)

        button_state = "NONE"
        Stmouse = pygame.mouse.get_pos() 
        Stklick = pygame.mouse.get_pressed()
        button_state = button(Stmouse,Stklick,screen_length//2- general_buttonlength//2 + (100 + general_buttonlength),screen_height//2+(general_buttonheight+50) + 100,"Back",general_buttonlength,general_buttonheight,(20,40,200),(90,150,255),text_boxes[0].return_value(),text_boxes[1].return_value())

        pygame.display.flip()
        pygame.time.wait(200)
        pygame.display.update()

        if button_state == "Back":
            return "Menu" 

#Main function of the game
def main():
    running = True
    game_mode = "Menu"
    while running:
        # RGB - Red, Green, Blue  
       screen.fill((200,230,255))
       pygame.display.flip()
       pygame.display.update()

       #Call the game intro function if the game mode is menu
       if game_mode == "Menu":
            game_mode = game_intro()

       #Call the practice function if the game mode is practice
       if game_mode == "Practice":
            chosenvocabulary = vocabulary_loader.get_randomvocabulary()
            game_mode = Practice_Mode(chosenvocabulary)

       #Call the exam function if the game mode is exam
       if game_mode == "Exam":
            questions = []
            answers = []
            #Select 10 questions for the exam
            for i in range(0,10):
                    examvocabulary = vocabulary_loader.get_exam()

                    #Vocables can be be chosen only once
                    while examvocabulary in questions:
                        examvocabulary = vocabulary_loader.get_exam()
                    questions.append(examvocabulary)

            #Call the game mode function for each question
            for question in questions:   
                game_mode = Exam_Mode(question)
                answers.append(game_mode)
                pygame.time.wait(200)

            #Show the exam results
            show_results(answers,questions)

            game_mode = "Menu"
         
       #Call the stats function if the game mode is stats   
       if game_mode == "Stats":
            pygame.time.wait(200)
            game_mode = Stats_Mode()

#Calling the main function -- starting point for the programme      
main()
#Close game
pygame.quit()





