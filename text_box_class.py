#Importing libraries
import pygame
#Defining vector for the position
vec = pygame.math.Vector2

#Define class text box
class Text_box:

    #Initialize text box
    def __init__(self, x, y, width, height, text=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pos = vec(x,y)
        self.size = vec(width,height)
        self.image = pygame.Surface((width,height))
        self.bg_color = (124,124,124)
        self.active_color = (255,255,255)
        self.active = False
        self.text = text
        self.font = pygame.font.SysFont("Times New Roman",40)
        self.numbers = [48,49,50,51,52,53,54,55,56,57]
        self.special = [8,32,16,46]

    #Function that draws the text box
    def draw(self, window):
        if not self.active:
            self.image.fill((0,0,0))
            pygame.draw.rect(self.image, self.bg_color, (1, 1, self.width-2, self.height-2))

        else:
            self.image.fill((0,0,0))
            pygame.draw.rect(self.image, self.active_color, (1, 1, self.width-2, self.height-2))
        text = self.font.render(self.text,False, (0,0,0))
        text_height = text.get_height()
        text_width = text.get_width()

        if text_width < self.width-2:
            self.image.blit(text,(4,(self.height-text_height)//2))
        else:
            self.image.blit(text,(4+(self.width-text_width-6),(self.height-text_height)//2))

        window.blit(self.image, self.pos)

    #Function that checks if text box is clicked
    def check_click(self,pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                self.active = True
            else:
                self.actice = False
        else:
            self.active = False

    #Returning the text box value
    def return_value(self):
        return self.text

    #Adding text written on the keyboard to the text box
    def add_text(self,key):
        try:
            #Checking if key is a special sign
            if key == 223 and pygame.key.get_mods() &  pygame.KMOD_SHIFT:  
                text = list(self.text)
                text.append('?')
                self.text = ''.join(text)

            elif key == 49 and pygame.key.get_mods() &  pygame.KMOD_SHIFT:  
                text = list(self.text)
                text.append('!')
                self.text = ''.join(text)
            elif chr(key).isalpha() and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                
                text = list(self.text)
                text.append(chr(key).upper())
                self.text = ''.join(text)
            elif pygame.key.get_mods() & pygame.KMOD_ALT and key == 108:
                text = list(self.text)
                text.append('@')
                self.text = ''.join(text)
            #Checking if the key is a letter
            elif chr(key).isalpha():
                text = list(self.text)
                text.append(chr(key))
                self.text = ''.join(text)
            #Deleting text
            elif key == 8:
                text = list(self.text)
                text.pop()
                self.text = ''.join(text)
            #Checking if the key is a space
            elif key == 32:
                text = list(self.text)
                text.append(' ')
                self.text = ''.join(text)
            #Checking if the key is a dot
            elif key == 46:
                 text = list(self.text)
                 text.append('.')
                 self.text = ''.join(text)
            #Checking if the key is a number
            elif key in self.numbers:
                text = list(self.text)
                if key < 100:
                    text.append(str(key-48))
                else:
                    text.append(str(key-256))
                self.text = ''.join(text)
            else: 
                pass
        except:
            pass

