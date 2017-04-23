#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 15:56:23 2017

@author: takashi
"""

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

    
    def __init__(self,xdim):
        self.board = self.generateBoard()
        self.history = [copy.deepcopy(self.board)]
        self.log = logging.getLogger(' ExperimentGenerator')
        self.log.setLevel(logging.DEBUG) 
        self.log.addHandler(handler)
        self.xdim = xdim

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

        #print "getWinner\n",board
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
            return 0  #No 5 with game being done means draw.
        else:
            print "Game not done, cannot determine winner"
            return -1
 

    def isDone(self, board = 0):
        if board == 0:
            board = self.board

        done = False

        noMoreSpace = True
        for row in board:
            for cell in row:
                if cell == 0:
                    noMoreSpace = False
                    
        if noMoreSpace == True:
            done = True
        else:
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
                        done = True
                                       
        return done







    def getFeatures(self, board = 0):
        if board == 0:
            board = self.board
        
        possibilities = []
        ls2=[]
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
                    ls2.append((landMark, len(land), status))
        #print "landStatus\n",landStatus
        #print "ls2\n",ls2
                    
        #boardSummary =pd.DataFrame.from_records(landStatus,columns=("player","length","status","line"))
        #ft = boardSummary.groupby(['player','length', 'status']).size()
        
        
        d = {}
        for s in ls2:
            #print "sssss",s
            for j in self.xdim:
                if j == s:      
                    if d.get(s)==None:
                        d[s]=1
                        #print d
                    else:
                        d[s]+=1
                        #print d
        
  
        #bd2 = pd.DataFrame.from_records(ls2,columns=("state"))
        #ft2 = bd2.groupby(["state"]).size()
       

        return d       



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

        boardSize = self.boardSize
        diagonals = []
        for x in range(0, boardSize):
            diagonal = []
            for y in range(0, x+1):
                diagonal.append(board[x-y][y])
                
            #print diagonal
            diagonals.append(diagonal)

        for x in range(1, boardSize):
            diagonal = []
            for y in range(0, boardSize-x):
                diagonal.append(board[boardSize-y-1][x+y])
         
            #print diagonal
            diagonals.append(diagonal)

        for x in range(0, boardSize):
            diagonal = []
            for y in range(0, x+1):
                diagonal.append(board[boardSize-y-1][x-y])
        
            #print diagonal
            diagonals.append(diagonal)
            
        for x in range(1, boardSize):
            diagonal = []
            for y in range(0, boardSize-x):
                diagonal.append(board[y][x+y])
        
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

    def noMoreSpaceO(self):
        if len(self.getSuccessorsO())==0:
            return 1
        return 0
    
    def noMoreSpaceX(self):
        if len(self.getSuccessorsX())==0:
            return 1
        return 0


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
        self.checker = ExperimentGenerator(game.xdim)
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
        bestValue = self.critic.hypof(ft)

        for successor in successors:
            ft = self.checker.getFeatures(successor)
            value = self.critic.hypof(ft)
            
            ## you can check here how AI think about next move.
            #print "-----successor-----\n", successor
            #print "value:", value
            if value > bestValue:
                bestValue = value
                bestSuccessor = successor

        self.game.setBoard(bestSuccessor)


            

class Critic:
    def __init__(self,theta, alpha, xdim, mode = 1):
        self.theta = theta
        self.alpha = alpha
        self.mode = mode
        self.checker = ExperimentGenerator(xdim)
        self.log = logging.getLogger(' Critic')
        self.log.setLevel(logging.DEBUG) 
        self.log.addHandler(handler)
        self.xdim = xdim
        
    def setHypothesis(self,theta):
        self.theta = theta
        
    def getHypothesis(self):
        return self.theta
        
    def setMode(self,mode):
        self.mode = mode

    def getTrainingExamples(self,game):
        te = []
        history = game.history
        c = self.checker
        winner = c.getWinner(history[len(history)-1])

        #print "getTrainingExample():winner:", winner

        for i in range(0,len(history)):
            bi = history[i]
            xi = c.getFeatures(bi)
            #print "Board[i]\n", bi
            #print "feature:", xi

            if i >= len(history)-2:
                if  winner == self.mode:
                    score = 100
                elif winner == 0:
                    score = 0
                else:
                    score = -100
                te.append([xi, score])
                #print "close to the end:", score
            else:
                x2stepsAhead = c.getFeatures(history[i+2])
                score = self.hypof(x2stepsAhead)
                te.append([xi, score])
                #print "2 step ahead:", score
        #print "getTrainingExamples\n", te
        return te
          
    def hypof(self, x):
        eval = 0
        for j,xj in x.items():
            #print 'h[{}]={}'.format(j,self.theta[j])
            eval += self.theta[j]*xj
        return eval
  
        
    
    def updateTheta(self,game):
        a = self.alpha
        eval = 0
        ### seee it!!! len OK?
        trainingExamples = self.getTrainingExamples(game)
        m = len(trainingExamples)
        
        tempTheta = {}
             
        for k in range(0,100): #here starts Gradient Decsent" 100 not so sure.
            for j in self.xdim:
                dJj=0
                tempTheta[j] = self.theta[j]
                for i in range(0,m): # i represents ith training example, means a board state after ith move).
                    xi = trainingExamples[i][0] # xi dictionary object
                    hi = self.hypof(xi)
                    yi = trainingExamples[i][1]  
                    if j == (0,0,0):
                        xij = 1   # for theta0
                    else:
                        if xi.has_key(j):
                            xij = xi[j]
                        else:
                            xij = 0
                    
                    # Prediction = Hypothesis * DataMatrix
                    # DataMatrix = [X(1) X(2) ... X(m)] 
                    #  where X(i)T = (1,xi(i),x2(i),x3(i),...xm(i))T  xij is ith training data of jth dimension
                    # Parameters = (t0,t1,...tn)  belongs to Hypotheses space
                    
                    dJj += (hi-yi)*xij
                tempTheta[j] = tempTheta[j] - a*dJj
                #print "theta[{}]:{}".format(j,tempTheta[j])
            for j in self.xdim:
                self.theta[j] = tempTheta[j] # you need to update once.
        #print "theta updated:", self.theta
             
def main():   

    log = logging.getLogger('main')
    log.setLevel(logging.INFO) 
    for hdlr in log.handlers[:]:  # remove all old handlers
        log.removeHandler(hdlr)
    log.addHandler(handler)
    log.debug('start!!')
        
    w ={}
    player = [1,2]
    #length = [1,2,3,4,5,6,7,8]
    length = [2,3,4]
    status = [0,1,2]
    
    xdim = []
    xdim.append((0,0,0))
    for p in player:
        for l in length:
            for s in status:
                xdim.append((p,l,s))
    #print "Xdim\n", xdim
    
    w[(0,0,0)]=1
    for p in player:
        for l in length:
            for s in status:
                w[(p,l,s)]=1

    
    game = ExperimentGenerator(xdim)
    hypothesis1 = w   
    hypothesis2 = w
    critic1 = Critic(hypothesis1,.0001, xdim, 1)
    critic2 = Critic(hypothesis1,.003, xdim, 2)
    player1 = PerformanceSystem(game,critic1,1)
    player2 = PerformanceSystem(game,critic2,2)
    
    
    xwins = 0
    owins = 0
    draws = 0

    log.debug('learning from 100 games')    
    for i in range(0,1):
        if i > 0:
            game = ExperimentGenerator(xdim)
            player1.setGame(game)
            player2.setGame(game)
        
        while(1):
             #player1.chooseRandom()
             player1.chooseMove()
             if game.isDone():
                 break
             
             player2.chooseRandom()
             # Need a stronger player. Write move scenario.
             if game.isDone():
                 break 

  
    
        game.printBoard()
        #print "main1"
        winner = game.getWinner()
        #print "main2"
        if winner == 1:
             print "X wins"
             xwins += 1
        elif winner == 2:
             print "O wins"
             owins += 1
        elif winner == 0:
             print "game is a draw"
             draws += 1
             
        #print "main3"
        
        critic1.updateTheta(game) 
        #critic2.updateTheta(game)
    
        #log.debug("theta:{}\n".format(critic1.getHypothesis()) )    
    
        
    #log.close()
    print "X won " + str(xwins) + " games."
    print "O won " + str(owins) + " games."
    print "There were " + str(draws) + " draws."
    

    xwins = 0
    owins = 0
    
    while True:
        game = ExperimentGenerator(xdim)
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
    
        critic1.updateTheta(game)
    

    

if __name__ == '__main__':
    main()