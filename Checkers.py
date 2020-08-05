# Python Class 2169
# Lesson 12 Problem 1
# Author: TheBeast5520 (393519)
from tkinter import *
import random
from tkinter import messagebox

def avg(a,b):
    '''Quick average function'''
    return (a+b)/2

class CheckerCell(Canvas):

    def __init__(self,master,coord,color='tan'):
        '''Initializes all variables and flags-variables in the game'''
        self.length=50 # length of canvas
        self.radius=4/5*self.length/2 # radius of checker piece
        Canvas.__init__(self,master,width=self.length,height=self.length,\
                        bg=color,highlightthickness=0) # intializes canvas
        self.coord=coord # coordinate attribute
        self.bgColor=color # background color attribute
        self.bind("<Button-1>",self.highlight) # binds left-click to the highlight function
        self.cColor='blank' # sets the starting checker color to blank, since it starts off with no checker.
                            # We can add checkers if we want later
        self.color=color # sets the color of its background
        self.hasTile=False # flag for if the tile has a checker of not
        a = self.length  # temp variable, for a quicker implementation
        self.text = self.create_text(a/2,a/2,fill="black",font='Arial',
                        text="") # sets up text (who's turn it is)
        self.circle=self.create_oval(self.length/2-self.radius,self.length/2-self.radius,\
                         self.length/2+self.radius, self.length/2+self.radius,\
                         outline=color,fill=color) # creates a circle, but with the same color as the background
        self.isKing=False # there is no tile on it, so obviously a tile is not a king

    def highlight(self,misc='misc'):
        '''Highlight function; controls the movement'''
        temp=self.master.currentH.coord # a temp variable is set to the previous tile clicked for quicker implementation
        if self.hasTile: # if it has a checker-piece, switch the highlight to this tile
            self.master.cells[temp[0]*8+temp[1]].unhighlight() # unhighlight the previous tile
            self['bg']='lawngreen' # highlight background
            self.master.currentH=self # sets the 'last-tile-variable' to the current tile
        else:
            # if there is no tile there
            if self.master.isPossible:
                # first checkers if a certain flag, isPossible, is true. This happens when a move has already been made
                # and a double jump is possible
                if self.master.currentH==self.master.cells[self.master.onlyJump[0]*8+self.master.onlyJump[1]] and \
                   self.master.isJump(self,self.master.currentH):
                    # if the jump is possible WITH the same tile as before, make it so that that move is the only one possible
                    self['bg']='lawngreen'
                    self.master.cells[8*temp[0]+temp[1]].unhighlight()
                    if self.promotion(self.master.cells[8*temp[0]+temp[1]].cColor\
                                                   ,self.coord):
                        self.addTile(self.master.cells[8*temp[0]+temp[1]].cColor,\
                                 True)
                        # if a promotion is possible, promote it 
                    else:
                        # otherwise just move it
                        self.addTile(self.master.cells[8*temp[0]+temp[1]].cColor,\
                                 self.master.cells[8*temp[0]+temp[1]].isKing)
                    # updateing variables
                    self.master.cells[8*temp[0]+temp[1]].removeTile()
                    self.master.currentH=self
                    if self.master.hasJump1(self.master.currentH):
                        self.master.onlyJump=self.master.currentH.coord
                        self.master.isPossible=True
                        return 0
                    isPossible = False
                    self.master.toggleTurn()
                    
            if self.master.valid_turn(self,self.master.currentH):
                # if it's just another move, check if the move is valid, and continue with the same logic as before
                self['bg']='lawngreen'
                self.master.cells[8*temp[0]+temp[1]].unhighlight()
                if self.promotion(self.master.cells[8*temp[0]+temp[1]].cColor\
                                               ,self.coord):
                    self.addTile(self.master.cells[8*temp[0]+temp[1]].cColor,\
                             True)
                else:
                    self.addTile(self.master.cells[8*temp[0]+temp[1]].cColor,\
                             self.master.cells[8*temp[0]+temp[1]].isKing)
                self.master.cells[8*temp[0]+temp[1]].removeTile()
                self.master.currentH=self
                if self.master.hasJump1(self.master.currentH) and self.master.lastMove=='jump':
                    self.master.onlyJump=self.master.currentH.coord
                    self.master.isPossible=True
                    return 0
                isPossible = False
                self.master.toggleTurn()
    def unhighlight(self,misc='misc'):
        '''simply unhighlight the tile'''
        self['bg']=self.color
    def removeTile(self):
        ''' delete the current circle, whatever color it may be, and create a new circle that is the same color as the background'''
        self.delete(self.circle)
        self.circle=self.create_oval(self.length/2-self.radius,self.length/2-self.radius,\
                         self.length/2+self.radius, self.length/2+self.radius,\
                         outline=self.color,fill=self.color)
        # update variables
        self.hasTile=False
        self.cColor='blank'
        self.isKing=False
        self.delete(self.text)
        a = self.length
        self.text = self.create_text(a/2,a/2,fill="black",font=('Arial',24),
                        text="")
    def addTile(self,ncolor,isKing=False):
        ''' given a parameter of a color, it deletes the current circle and adds another circle'''
        self.delete(self.circle)
        self.circle=self.create_oval(self.length/2-self.radius,self.length/2-self.radius,\
                         self.length/2+self.radius, self.length/2+self.radius,\
                         outline=ncolor,fill=ncolor)
        self.hasTile=True
        a = self.length
        if isKing:
            # if king, add the iconic asterisk
            self.delete(self.text)
            self.text = self.create_text(a/2,a/2,fill="black",font=('Arial',24),
                        text="*")
            self.isKing=True
        self.cColor=ncolor
    def makeKing(self,king):
        '''make the current piece king by updating the variables and adding the \'*\''''
        self.isKing=True
        self.delete(self.text)
        a = self.length
        self.text = self.create_text(a/2,a/2,fill="black",font=('Arial',24),
                        text="*")
    def promotion(self,color,coord):
        ''' check if the piece can be promoted'''
        if (color=='red' and coord[0]==0) or (color=='white' and coord[0]==7):
            return True
        return False
class Checkers(Frame):

    def __init__(self,master,name1,name2):
        # setting up Frame
        Frame.__init__(self,master)
        self.grid()
        self.pTemp=random.randrange(0,2)
        # set up all variables, flags, and give a print the instructions.
        # Also, create all the tiles to start off the game.
        self.names = [name1,name2]
        self.names = [self.names[self.pTemp],self.names[(self.pTemp+1)%2]]
        print(self.names[0]+" goes first. " + self.names[0] + " is red. Please click on a checker to select it, and then click where you want to play it. You may reselect pieces. " + \
              "The game will automatically end when one player has won.")
        self.cells = []
        for i in range(8):
            for j in range(8):
                if (i%2==0 and j%2==1) or (i%2==1 and j%2==0):
                    color='dark green'
                else:
                    color='blanched almond'
                self.cells.append(CheckerCell(self,(i,j),color))
                self.cells[i*8+j].grid(row=i,column=j)
        self.whiteCells = []
        self.redCells = []
        self.colors=['red','white']
        for i in range(5,8):
            for j in range(8):
                if self.cells[i*8+j].color=='dark green':
                    self.cells[i*8+j].addTile('red')
                    self.redCells.append((i,j))
        for i in range(3):
            for j in range(8):
                if self.cells[i*8+j].color=='dark green':
                    self.cells[i*8+j].addTile('white')
                    self.whiteCells.append((i,j))
        self.currentH=self.cells[0]
        self.turn=0
        self.isPossible=False
        self.onlyJump=self.cells[0]
        self.turnLabel=Label(text='Turn: '+self.names[self.turn],font=('Arial',18))
        self.turnLabel.grid(row=1,column=0,columnspan=1)

    def valid_turn(self,cCell,lCell):
        ''' call the 'isJump' and 'isNorm' functions. This helps break each function down into smaller parts'''
        if lCell.cColor != self.colors[self.turn]:
            return False
        if self.hasJump():
            return self.isJump(cCell,lCell)
        return self.isJump(cCell,lCell) or self.isNorm(cCell,lCell)

    def hasJump(self,color='gray'):
        '''Checks if a side has any Jump possible'''
        if color=='gray':
            color=self.colors[self.turn]
        for a in self.cells:
            if self.hasJump1(a,color):
                return True
        return False

    def isJump(self,cCell,lCell,removeCell=True):
        '''based on different scenarios, check whether the there are pieces in between, the color of the piece is right, the piece is going in the correct
           direction, etc.'''
        if lCell.isKing:
            if abs(lCell.coord[0]-cCell.coord[0])==2 and abs(lCell.coord[1]-cCell.coord[1])==2 and not cCell.hasTile:
                temp = self.cells[int(avg(lCell.coord[0],cCell.coord[0])*8+avg(lCell.coord[1],cCell.coord[1]))]
                if temp.hasTile and temp.cColor != lCell.cColor:
                    if removeCell:
                        self.cells[int(avg(lCell.coord[0],cCell.coord[0])*8+avg(lCell.coord[1],cCell.coord[1]))].removeTile()
                        self.lastMove='jump'
                    return True
        elif lCell.cColor=='red':
            if lCell.coord[0]-cCell.coord[0]==2 and abs(lCell.coord[1]-cCell.coord[1])==2 and not cCell.hasTile:
                temp = self.cells[int(avg(lCell.coord[0],cCell.coord[0])*8+avg(lCell.coord[1],cCell.coord[1]))]
                if temp.hasTile and temp.cColor != lCell.cColor:
                    if removeCell:
                        self.cells[int(avg(lCell.coord[0],cCell.coord[0])*8+avg(lCell.coord[1],cCell.coord[1]))].removeTile()
                        self.lastMove='jump'
                    return True
        elif lCell.cColor=='white':
            if lCell.coord[0]-cCell.coord[0]==-2 and abs(lCell.coord[1]-cCell.coord[1])==2 and not cCell.hasTile:
                temp = self.cells[int(avg(lCell.coord[0],cCell.coord[0])*8+avg(lCell.coord[1],cCell.coord[1]))]
                if temp.hasTile and temp.cColor != lCell.cColor:
                    if removeCell:
                        self.cells[int(avg(lCell.coord[0],cCell.coord[0])*8+avg(lCell.coord[1],cCell.coord[1]))].removeTile()
                        self.lastMove='jump'
                    return True
        return False
                   

    def isNorm(self,cCell,lCell,isMove=True):
        '''similar as the isJump function except slightly simpler with the coordinates'''
        if lCell.isKing:
            if abs(lCell.coord[0]-cCell.coord[0])==1 and abs(lCell.coord[1]-cCell.coord[1])==1 and not cCell.hasTile:
                if isMove:
                    self.lastMove='norm'
                return True
        elif lCell.cColor=='red':
            if (lCell.coord[0]-cCell.coord[0])==1 and abs(lCell.coord[1]-cCell.coord[1])==1 and not cCell.hasTile:
                if isMove:
                    self.lastMove='norm'
                return True
        elif lCell.cColor=='white':
            if (lCell.coord[0]-cCell.coord[0])==-1 and abs(lCell.coord[1]-cCell.coord[1])==1 and not cCell.hasTile:
                if isMove:
                    self.lastMove='norm'
                return True
        return False
    def hasJump1(self,a,color='gray'):
        '''checks if a specific piece has a jump'''
        if color=='gray':
            color=self.colors[self.turn]
        if a.hasTile and a.cColor==color:
            if a.isKing:
                for i in range(-2, 3, 4):
                    for j in range(-2,3,4):
                        if a.coord[0]+i >= 0 and a.coord[0]+i < 8 and a.coord[1]+j >= 0 and a.coord[1]+j < 8:
                            if self.isJump(self.cells[(a.coord[0]+i)*8+a.coord[1]+j],self.cells[a.coord[0]*8+a.coord[1]],False):
                                return True
            else:
                if a.cColor=='red':
                    i=-2
                else:
                    i=2
                for j in range(-2,3,4):
                    if a.coord[0]+i >= 0 and a.coord[0]+i < 8 and a.coord[1]+j >= 0 and a.coord[1]+j < 8:
                        if self.isJump(self.cells[(a.coord[0]+i)*8+a.coord[1]+j],self.cells[a.coord[0]*8+a.coord[1]],False):
                            return True
        return False
    def toggleTurn(self):
        self.turn = (self.turn+1)%2
        self.turnLabel['text']='Turn: ' + self.names[self.turn]
        self.win()

    def hasNorm1(self,a,color='gray'):
        '''checks if a specific piece has a normal move'''
        if color=='gray':
            color=self.colors[self.turn]
        if a.hasTile and a.cColor==color:
            if a.isKing:
                for i in range(-1, 2, 2):
                    for j in range(-1,2,2):
                        if a.coord[0]+i >= 0 and a.coord[0]+i < 8 and a.coord[1]+j >= 0 and a.coord[1]+j < 8:
                            if self.isNorm(self.cells[(a.coord[0]+i)*8+a.coord[1]+j],self.cells[a.coord[0]*8+a.coord[1]],False):
                                return True
            else:
                if a.cColor=='red':
                    i=-1
                else:
                    i=1
                for j in range(-1,2,2):
                    if a.coord[0]+i >= 0 and a.coord[0]+i < 8 and a.coord[1]+j >= 0 and a.coord[1]+j < 8:
                        if self.isNorm(self.cells[(a.coord[0]+i)*8+a.coord[1]+j],self.cells[a.coord[0]*8+a.coord[1]],False):
                            return True
    def hasNorm(self,color='gray'):
        '''checks if a side has any possible move'''
        if color=='gray':
            color=self.colors[self.turn]
        for a in self.cells:
            if self.hasNorm1(a,color):
                return True
        return False
    
    def win(self):
        '''if one of the sides doesn't have a move, the other team wins.'''
        self.wHasMove = False
        self.rHasMove = False
        if self.hasJump('red') or self.hasNorm('red'):
            self.rHasMove=True
        if self.hasJump('white') or self.hasNorm('white'):
            self.wHasMove=True
        if self.wHasMove and not self.rHasMove:
            self.winner=self.names[1]
            self.end_game()
        elif self.rHasMove and not self.wHasMove:
            self.winner=self.names[0]
            self.end_game()

    def end_game(self):
        '''Unbinds and finishes up the game'''
        self.turnLabel['text']="GAME OVER"
        for i in self.cells:
            i.unbind("<Button-1>")
        messagebox.showinfo('Checkers','Congratulations, '+self.winner+' -- you won!',parent=self)
        self.endButton=Button(text='Press to continue',command=self.delWindow)
        self.endButton.grid(row=9,column=0)
    def delWindow(self):
        '''closes the tkinter window to start a new game or end the program'''
        self.master.destroy()
def play_checkers(name1,name2):
    '''sets up tkinter to play a checkers game'''
    root = Tk()
    root.title('Checkers')
    game = Checkers(root,name1,name2)
    root.mainloop()
def play_again():
    '''infinite loop unless the player wants to stop playing'''
    name1 = input("Please enter the name of player 1: ")
    name2 = input("Please enter the name of player 2: ")
    play_checkers(name1, name2)
    while True:
        ynPlayAgain=input("Would you like to play again? (y/n) ").lower().strip()
        if ynPlayAgain=='y':
            yn = input("Would you like to use the same names? (y/n) ").lower().strip()
            if yn=='y':
                name1 = input("Please enter the name of player 1: ")
                name2 = input("Please enter the name of player 2: ")
                play_checkers(name1, name2)
            else:
                play_checkers(name1,name2)
        else:
            break
# play_again()

play_checkers("","")

#
