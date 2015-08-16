from Tkinter import *
from random import randint
from time import sleep
import unittest
import random
import tkFont
import sys

MARGIN = 25 # Pixels around the board
SIDE = 75 # Width of every board cell.
WIDTH = MARGIN * 2 + SIDE * 4 # Width of the whole board
HEIGHT = WIDTH # height of the whole board

class Kernel(object):
    @staticmethod
    def move_down(myList):
        is_moved = False
        score = 0
        if isinstance(myList, list):
            size = len(myList)
            auxiliarylist = [1] * size
            for i in reversed(xrange(size)):
                for j in reversed(xrange(size-1)):
                    if myList[j+1] == myList[j] and myList[j+1] != 0 and auxiliarylist[j] == 1 and auxiliarylist[j+1] == 1:
                        myList[j+1] *= 2
                        score = score + myList[j+1]
                        auxiliarylist[j+1] = 0
                        myList[j] = 0
                        auxiliarylist[j] = 1
                        is_moved = True
                    if myList[j] != 0 and myList[j+1] == 0 and auxiliarylist[j+1] == 1: 
                        myList[j+1] = myList[j]
                        auxiliarylist[j+1] = auxiliarylist[j]
                        myList[j] = 0
                        auxiliarylist[j] = 1
                        is_moved = True
        else:
            print "is not list"
        return [is_moved, score]
    @staticmethod
    def rotate_listoflist(matrix):
        columns = [[row[col] for row in matrix] for col in range(len(matrix[1]))]
        return columns

class UI2048(Frame):
    def __init__(self, parent):
        Frame.__init__(self,parent)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.parent = parent
        self.row, self.col = -1, -1
        self.initUI()
        
    def initUI(self):
        self.parent.title("2048")
        self.parent.resizable(0,0)
        self.frame = Frame()
        self.label_score = Label(self.frame, text="Score:", font=tkFont.Font(family="Verdina", size=16))
        self.label = Label(self.frame, width=16, text="0", font=tkFont.Font(family="Verdina", size=16))
        self.label_score.pack(side=LEFT)
        self.label.pack(side=LEFT)
        self.canvas = Canvas(
            width=350, height=350,
            highlightthickness=0
        )
        self.canvas.pack(side=BOTTOM,expand=True, fill=BOTH)
        self.frame.pack()
        self.draw_grid(5)
        
    def draw_grid(self, amount):
        for i in xrange(amount):
            self.canvas.create_line(
                MARGIN + i * SIDE, MARGIN,
                MARGIN + i * SIDE, WIDTH - MARGIN,
                fill="blue", tag="grid" 
            )
            self.canvas.create_line(
                MARGIN, MARGIN + i * SIDE,
                WIDTH - MARGIN, MARGIN + i * SIDE,
                fill="blue", tag="grid"
            )

    def get_color(self,value):
        colors = ['#eee4da','#ede0c8','#f2b179','#f59563','#f67c5f','#f65e3b','#edcf72','#edcc61','#edc850','#edc53f','#edc22e','#edb018','#ea6004','#d04500','#c63500','#c03340','#b03060', '#a12a80']
        position = 0
        while True:
            if value != 1:
                value = value/2
                position = position + 1
                if position > len(colors):
                    return '#095aaa'
            else:
                return colors[position-1]
            
    def draw_puzzle(self, x, y, text):
        self.canvas.create_rectangle(
            MARGIN+SIDE*x,
            MARGIN+SIDE*y,
            MARGIN+SIDE*x+SIDE,
            MARGIN+SIDE*y+SIDE,
            width = 3,
            fill=self.get_color(text),
            tag="field"
        )
        self.canvas.create_text(
            MARGIN+37+SIDE*x,
            MARGIN+37+SIDE*y,
            font=("Verdina",14),
            text=text,
            tag="text"
        )
   
class Game2048(object):
    def __init__(self, object):
        self.ui = object
        self.fields = []
        self.is_moving_array = []
        self.score = 0
        for i in xrange(4):
            self.fields.append([0] * 4)
        for i in xrange(4):
            self.is_moving_array.append([0] * 4)
        self.new_random_puzzle(self.fields)
        self.new_random_puzzle(self.fields)
        self.refresh_screen()
        self.press_key()
        
    def refresh_screen(self):
        self.ui.canvas.delete("field")
        self.ui.canvas.delete("text")
        self.ui.label['text'] = self.score
        sizeof = len(self.fields)
        for i in xrange(sizeof):
            for j in xrange(sizeof):
                if self.fields[i][j] != 0:
                    self.ui.draw_puzzle(i, j, self.fields[i][j])
    
    def check_end_of_game(self):
        size = len(self.fields)
        for i in xrange(size):
            for j in xrange(size):
                if self.fields[i][j] == 0:
                    return 0
        for i in xrange(size):
            for j in xrange(size-1):
                if self.fields[i][j] == self.fields[i][j+1]:
                    return 0
        for i in xrange(size-1):
            for j in xrange(size):
                if self.fields[i][j] == self.fields[i+1][j]:
                    return 0             
        return 1
            
    def new_random_puzzle(self, object):
        self.array_puzzle = object
        p = 0.1
        while True:
            rand_field = randint(0,15)
            if self.array_puzzle[rand_field%4][rand_field/4] == 0:
                x = random.random()
                if x < p:
                    self.array_puzzle[rand_field%4][rand_field/4] = 4
                else:
                    self.array_puzzle[rand_field%4][rand_field/4] = 2
                break
    
    def pressed_left(self, event):
        is_moved = False
        self.fields.reverse()
        temp_fields = Kernel.rotate_listoflist(self.fields)
        for i in xrange(4):
            result = Kernel.move_down(temp_fields[i])
            if result[0]:
                is_moved = True
                self.score = self.score + result[1]
            self.fields = Kernel.rotate_listoflist(temp_fields)
            self.fields.reverse()
        if is_moved:
            self.new_random_puzzle(self.fields)
            self.refresh_screen()
            if self.check_end_of_game():
                self.end_game(self.score)

    def pressed_right(self, event):
        is_moved = False
        temp_fields = Kernel.rotate_listoflist(self.fields)
        for i in xrange(4):
            result = Kernel.move_down(temp_fields[i])
            if result[0]:
                is_moved = True
                self.score = self.score + result[1]
            self.fields = Kernel.rotate_listoflist(temp_fields)
        if is_moved:
            self.new_random_puzzle(self.fields)
            self.refresh_screen()
            if self.check_end_of_game():
                self.end_game(self.score)
        
    def pressed_up(self, event):
        is_moved = False
        for i in xrange(4):
            self.fields[i].reverse()
            result = Kernel.move_down(self.fields[i])
            if result[0]:
                is_moved = True
                self.score = self.score + result[1]
            self.fields[i].reverse()
        if is_moved:
            self.new_random_puzzle(self.fields)
            self.refresh_screen()
            if self.check_end_of_game():
                self.end_game(self.score)
        
    def pressed_down(self, event):
        is_moved = False
        for i in xrange(4):
            result = Kernel.move_down(self.fields[i])
            if result[0]:
                is_moved = True
                self.score = self.score + result[1]
        if is_moved:
            self.new_random_puzzle(self.fields)
            self.refresh_screen()
            if self.check_end_of_game():
                self.end_game(self.score)
    
    def press_key(self):
        self.ui.canvas.focus_set()
        self.ui.canvas.bind('<Left>', self.pressed_left)
        self.ui.canvas.bind('<Right>', self.pressed_right)
        self.ui.canvas.bind('<Up>', self.pressed_up)
        self.ui.canvas.bind('<Down>', self.pressed_down)
    
    def end_game(self, score):
        top = Toplevel()
        top.title("Game over")
        msg = Message(top, text="Your score is " + str(self.score))
        msg.pack()
        button = Button(top, text="Exit", command=top.destroy)
        button.pack()
      
root = Tk()
ui = UI2048(root)
game = Game2048(ui)

class tk2048Test(unittest.TestCase):
    list_input = []
    list_result = []
    def setUp(self):
        file_input = open('right_input.txt', 'r')
        file_result = open('right_result.txt', 'r')
        self.list_input = list([int(num) for num in line.split()]  for line in file_input)
        self.list_result = list([int(num) for num in line.split()]  for line in file_result)
     
    def test_down(self):
        is_failed = False
        for j in xrange(len(self.list_input)):
            Kernel.move_down(self.list_input[j])
            if(self.list_input[j] != self.list_result[j]):
                print "ROW: " + str(j+1)+ "  " + str(self.list_input[j]) + " --> " + str(self.list_result[j]) + " WRONG!"
                is_failed = True
        if is_failed == True:        
            self.assertFalse(True)
    
if __name__ == '__main__':
    #unittest.main()  
    root.mainloop()