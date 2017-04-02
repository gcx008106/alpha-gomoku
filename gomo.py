# class represents a state of a tic tac toe game.
# 0 represents an unfilled square
# 1 represents an X
# 2 represents an O
import copy
import random
import pandas as pd
import sys
import logging

   
#handler = logging.StreamHandler()
handler = logging.FileHandler('log.txt',mode='w')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s - %(message)s')
handler.setFormatter(formatter)
#ogger.addHandler(ch)
    
# 'application' code
#    logger.debug('debug message')
#    logger.info('info message')
#    logger.warn('warn message')
#    logger.error('error message')
#    logger.critical('critical message')

               
class ExperimentGenerator:
    boardSize = 8

    
    def __init__(self):
        self.board = self.generateBoard()
        self.history = [copy.deepcopy(self.board)]
        self.log = logging.getLogger(' ExperimentGenerator')
        self.log.setLevel(logging.DEBUG) 
        self.log.addHandler(handler)

    def setBoard(self,board):
        if board == 0:
            print "zero board"
        self.board = board
        self.history.append(copy.deepcopy(self.board))

    def getBoard(self):
        return self.board

    def generateBoard(self):
        board = []
        for y in range(0,self.boardSize):
            row = []
            for x in range(0,self.boardSize):
                row.append(0)
            board.append(row)
        return board

    def getWinner(self, board = 0):
        if board == 0:
            board = self.board

        if self.isDone(board):
            
            possibilities = []
            for row in self.getRows(board):
                possibilities.append(row)
            for column in self.getColumns(board):
                possibilities.append(column)
            for diagonal in self.getDiagonals(board):
                possibilities.append(diagonal)
                    
                        
            for possibility in possibilities:
                lands = self.getLands(possibility)
                for land in lands:
                    if len(land)==5 and land[0]!=0:
                        return land[0]
            return 0

        else:
            print "Game not done, cannot determine winner"

    def isDone(self, board = 0):
        if board == 0:
            board = self.board

        done = 0
                            
        possibilities = []
        for row in self.getRows(board):
            possibilities.append(row)
        for column in self.getColumns(board):
            possibilities.append(column)
        for diagonal in self.getDiagonals(board):
            possibilities.append(diagonal)
            
        for possibility in possibilities:
            lands = self.getLands(possibility)
            #print "isDone()lands" , lands
            for land in lands:
                #print "isDone():" , land
                if len(land)==5 and land[0]!=0:
                    #print "isDone() 5!!!!!!"
                    done = land[0]
                    
                    
        return done

    def getFeatures(self, board = 0):
        if board == 0:
            board = self.board
        
        possibilities = []
        for row in self.getRows(board):
            possibilities.append([row,"row"])
        for column in self.getColumns(board):
            possibilities.append([column,"col"])
        for diagonal in self.getDiagonals(board):
            possibilities.append([diagonal,"dia"])

        landStatus=[]       
        for line in possibilities:
            lineDirection = line[1]
            possibility = line[0]
            lands = self.getLands(possibility)
            #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n",lands
            for i in range(0,len(lands)):
                land = lands[i]
                landMark = land[0]
                if i == 0:
                    leftMark = -1
                else:
                    leftMark = lands[i-1][0]
                if i == len(lands)-1:
                    rightMark = -1
                else:
                    rightMark = lands[i+1][0]
                
                #print "land:",land
                #print "left:{},right:{}".format(leftMark,rightMark)
                if landMark != 0:
                    if rightMark == 0 and leftMark == 0:
                        status = 2   #open
                    elif rightMark !=0 and leftMark == 0:
                        status = 1    #half open
                    elif rightMark ==0 and leftMark != 0:
                        status = 1    #half open
                    else:
                        status = 0
                    landStatus.append([landMark, len(land), status,lineDirection])
        ft=pd.DataFrame.from_records(landStatus,columns=("player","length","status","line"))

        return ft        



    def getRows(self, board = 0):
        if board == 0:
            board = self.board
        return board
    
    def getColumns(self,board = 0):
        if board == 0:
            board = self.board

        columns = []
        for x in range(0,self.boardSize):
            column = []
            for y in range(0,self.boardSize):
                column.append(board[y][x])
            columns.append(column)

        return columns

    def getDiagonals(self,board = 0):
        if board == 0:
            board = self.board

        diagonals = []
        for x in range(0, self.boardSize):
            diagonal = []
            for y in range(0, x+1):
                diagonal.append(self.board[x-y][ y])
                
            #print diagonal
            diagonals.append(diagonal)

        for x in range(1, self.boardSize):
            diagonal = []
            for y in range(0, self.boardSize-x):
                diagonal.append(self.board[self.boardSize-y-1][x+y])
         
            #print diagonal
            diagonals.append(diagonal)

        for x in range(0, self.boardSize):
            diagonal = []
            for y in range(0, x+1):
                diagonal.append(self.board[self.boardSize-y-1][x-y])
        
            #print diagonal
            diagonals.append(diagonal)
            
        for x in range(1, self.boardSize):
            diagonal = []
            for y in range(0, self.boardSize-x):
                diagonal.append(self.board[y][x+y])
        
            #print diagonal
            diagonals.append(diagonal)
    
        return diagonals
        
    
    def getLands(self, line):        
        lands = []
        prev = -1
        for entry in line:
            if prev == entry: 
                land.append(entry)
            else:
                if prev != -1:
                    lands.append(land)
                land=[]
                land.append(entry)
            prev = entry
        lands.append(land)
        return lands
        
        
        
    def getSuccessorsX(self):
        successors = []
        for y in range(0,self.boardSize):
            for x in range(0,self.boardSize):
                if self.board[y][x] == 0:
                    successor = copy.deepcopy(self.board)
                    successor[y][x] = 1
                    successors.append(successor)
        return successors

    def getSuccessorsO(self):
        successors = []
        for y in range(0,self.boardSize):
            for x in range(0,self.boardSize):
                if self.board[y][x] == 0:
                    successor = copy.deepcopy(self.board)
                    successor[y][x] = 2
                    successors.append(successor)
        return successors

    def getHistory(self):
        return self.history

    def setX(self,x,y):
        self.board[y][x] = 1
        self.history.append(copy.deepcopy(self.board))

    def setO(self,x,y):
        self.board[y][x] = 2

    def printBoard(self, board = 0):
        if board == 0:
            board = self.board

        sboard = []
        for row in board:
            srow = []
            for entry in row:
                if entry == 0:
                    srow.append(' ')
                elif entry == 1:
                    srow.append('X')
                elif entry == 2:
                    srow.append('O')
            sboard.append(srow)
        
        header = '-|'
        for x in range(0, self.boardSize):
            header = header + str(x) + '|'
        print header
        for x in range(0, self.boardSize):
            line = str(x) + '|'
            separator = '-|'
            for y in range(0, self.boardSize):
                line = line + sboard[x][y] + '|'
                separator = separator + '-|'
            print separator
            print line
            
                
class PerformanceSystem:
    def __init__(self, game, critic, mode = 1):
        self.game = game
        self.critic = critic
        self.mode = mode
        self.checker = ExperimentGenerator()
        self.log = logging.getLogger(' PerformanceSystem')
        self.log.setLevel(logging.DEBUG) 
        self.log.addHandler(handler)
        
    def setGame(self,game):
        self.game = game

    def chooseRandom(self):
        if self.mode == 1:
            successors = self.game.getSuccessorsX()
        else:
            successors = self.game.getSuccessorsO()
            
        randomBoard = successors[random.randint(0,len(successors)-1)]
        self.game.setBoard(randomBoard)

    def chooseMove(self):
        if self.mode == 1:
            successors = self.game.getSuccessorsX()
        else:
            successors = self.game.getSuccessorsO()

        bestSuccessor = successors[0]
        ft = self.checker.getFeatures(bestSuccessor)
        bestValue = self.critic.evaluateBoard(ft)

        for successor in successors:
            ft = self.checker.getFeatures(successor)
            value = self.critic.evaluateBoard(ft)
            
            ## you can check here how AI think about next move.
            #print "-----successor-----\n", successor
            #print "value:", value
            if value > bestValue:
                bestValue = value
                bestSuccessor = successor

        self.game.setBoard(bestSuccessor)


            

class Critic:
    def __init__(self,hypothesis, updateConstant, mode = 1):
        self.hypothesis = hypothesis
        self.updateConstant = updateConstant
        self.mode = mode
        self.checker = ExperimentGenerator()
        self.log = logging.getLogger(' Critic')
        self.log.setLevel(logging.DEBUG) 
        self.log.addHandler(handler)
        
    def setHypothesis(self,hypothesis):
        self.hypothesis = hypothesis
        
    def getHypothesis(self):
        return self.hypothesis
        
    def setMode(self,mode):
        self.mode = mode

    def getTrainingExamples(self,game):
        trainingExamples = []
        history = game.history
        chk = self.checker
        for i in range(0,len(history)):
            if(self.checker.isDone(history[i])):
                if(self.checker.getWinner(history[i]) == self.mode):
                    trainingExamples.append([chk.getFeatures(history[i]), 100])
                elif(self.checker.getWinner(history[i]) == 0):
                    trainingExamples.append([chk.getFeatures(history[i]), 0])
                else:
                    trainingExamples.append([chk.getFeatures(history[i]), -100])
            else:
                if i+2 >= len(history):
                    if(chk.getWinner(history[len(history)-1]) == 0):
                        trainingExamples.append([chk.getFeatures(history[i]), 0])
                    else:
                        trainingExamples.append([chk.getFeatures(history[i]), -100])
                else:
                    trainingExamples.append([chk.getFeatures(history[i]), self.evaluateBoard(chk.getFeatures(history[i+2]))])
        #t "trainingExamples:", trainingExamples
        return trainingExamples
          
    def evaluateBoard(self, ft):
        eval = 0
        for row in ft.values:
            #print row[0],row[1],row[2]
            #print self.hypothesis[(row[0],row[1],row[2])]
            eval += self.hypothesis[(row[0],row[1],row[2])]
        return eval
    
    
    def updateWeights(self,game):
        eval = 0
        ### seee it!!! len OK?
        trainingExamples = self.getTrainingExamples(game)

        for i in range(0,len(trainingExamples)):
            w = self.hypothesis
            ft = trainingExamples[i][0] # already Feature!
            #print "updateWeights()----------feature---------\n",ft
            #vEst = w0 + w1*x1 + w2*x2 + w3*x3 + w4*x4 + w5*x5 + w6*x6
            # ingored constant w0 
            vEst = self.evaluateBoard(ft)
            vTrain = trainingExamples[i][1]            

            # w0 = w0 + self.updateConstant*(vTrain - vEst)
            # ignored w0
            for row in ft.values:
                self.hypothesis[(row[0],row[1],row[2])] = self.hypothesis[(row[0],row[1],row[2])] + self.updateConstant*(vTrain - vEst)
                        
        #print "hypothesis updated"
        


 
#
#board_test00 =[[1,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0]]
#
#board_test01 =[[1,0,0,0,0,0,0,2],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0]]
#
#board_test02 =[[1,1,0,0,0,0,0,2],
#               [0,0,0,0,0,0,0,2],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0]]     
#
#board_test03 =[[1,1,1,0,0,0,0,2],
#               [1,1,0,0,0,0,0,2],
#               [0,0,0,0,0,0,0,2],
#               [0,0,0,0,0,0,0,2],
#               [0,0,0,0,0,0,0,2],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0]] 
#
#
#
#b = ExperimentGenerator()
#b.setBoard(board_test00)
#b.setBoard(board_test01)
#b.setBoard(board_test02)
#b.setBoard(board_test03)
#ft = b.getFeatures()
#print ft
#hyp1 = w0    
#critic1 = Critic(board,hyp1,.1,1)
#critic1.updateWeights()
#print critic1.getHypothesis()
#sys.exit(0)


             
def main():   

    log = logging.getLogger('main')
    log.setLevel(logging.INFO) 
    for hdlr in log.handlers[:]:  # remove all old handlers
        log.removeHandler(hdlr)
    log.addHandler(handler)
    log.debug('start!!')
        
    w ={}
    player = [1,2]
    length = [1,2,3,4,5,6,7]
    status = [0,1,2]
     
    for p in player:
        for l in length:
            for s in status:
                w[(p,l,s)]=.5

    
    game = ExperimentGenerator()
    hypothesis1 = w   
    hypothesis2 = w
    critic1 = Critic(hypothesis1,.1,1)
    critic2 = Critic(hypothesis1,.3,1)
    player1 = PerformanceSystem(game,critic1,1)
    player2 = PerformanceSystem(game,critic2,2)
    
    
    xwins = 0
    owins = 0
    draws = 0

    log.debug('learning from 100 games')    
    for i in range(0,10):
        if i > 0:
            game = ExperimentGenerator()
            player1.setGame(game)
            player2.setGame(game)
        
        while(not game.isDone()):
             #player1.chooseRandom()
             player1.chooseMove()
             if game.isDone():
                 break
             player2.chooseMove()
             #player2.chooseRandom()
    
        game.printBoard()
        winner = game.getWinner()
        if(winner == 1):
             print "X wins"
             xwins += 1
        elif(winner == 2):
             print "O wins"
             owins += 1
        elif(winner == 0):
             print "game is a draw"
             draws += 1
    
        critic1.updateWeights(game) 
        critic2.updateWeights(game)
    
        log.debug("hypothesis:{}\n".format(critic1.getHypothesis()) )    
    
        
    #log.close()
    print "X won " + str(xwins) + " games."
    print "O won " + str(owins) + " games."
    print "There were " + str(draws) + " draws."
    

    xwins = 0
    owins = 0
    
    while True:
        game = ExperimentGenerator()
        player1.setGame(game)
        while(not game.isDone()):
            #board.printBoard()
            #xval = input("Enter xcoordinate: ")
            #yval = input("Enter ycoordinate: ")
            #board.setX(xval,yval)
    
            #player1.chooseRandom()
            
    
            player1.chooseMove()
            if game.isDone():
                break
    
            game.printBoard()
            #print "First move\n", board.getFeatures()
            xval = input("Enter xcoordinate: ")
            yval = input("Enter ycoordinate: ")
            game.setO(xval,yval)
    
    
            #player2.chooseMove()
            #player2.chooseRandom()
            #board.printBoard()
            #print "Second move\n", board.getFeatures()
        
        winner = game.getWinner()
        if(winner == 1):
            print "X wins"
            xwins += 1
        elif(winner == 2):
            print "O wins"
            owins += 1
        elif(winner == 0):
            print "game is a draw"
            draws += 1
    
        #critic1.setHypothesis(player1.getHypothesis())
        #critic2.setHypothesis(player2.getHypothesis())
    
        critic1.updateWeights(game)
    

    

if __name__ == '__main__':
    main()