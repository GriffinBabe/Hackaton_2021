"""
from IAFactory import *
"""
from src.game.entities import *
from src.game.command import *
import random

class InterfaceGameIA:
    def __init__(self,isTraining, team):
        self.team = team
        self.isTraining = isTraining
        self._setGoodIA(isTraining, team)


    def _setGoodIA(self, isTraining, team):
        self.isTraining = isTraining
        self.team = team
        self.IA = IAFactory.getInstance()
        if self._isMyTeamWhite():
            self.IA.setColorWhite()
        else:
            self.IA.setColorBlack()

        if self.isTraining:
            self.IA.setTraingOn()
        else:
            self.IA.setTrainingOff()


    def play(self, board):
        self.board = board
        self.myState = self._createAState(board)
        self._createFuturState()
        try:
            if len(self.futureState) != 0:
                if len(self.futureState) == 1:
                    return self.lstCommand[0]
                newState = self.IA.play(self.myState, self.futureState)
                indexState = self.futureState.index(newState)
                return self.lstCommand[indexState]
            else:
                return self.randomCommand()
        except:
            return self.randomCommand()



    def randomCommand(self):
        all_moves = self.board.get_legal_moves(self.team)
        tmp = random.choice(all_moves)
        return Command(tmp[0],tmp[1])

    def _createFuturState(self):
        newBoard = self.board.copy_state()
        lstChoixAction = self._getAllMinePositionToPlay()
        lstCommand = []
        lstFutureState = []

        for choix in lstChoixAction:
            command = Command(choix[0],choix[1])
            lstCommand.append(command)

            newBoard.play_command(command)
            lstFutureState.append(self._createAState(newBoard))
            if self.isVicotry(newBoard):
                lstFutureState = []
                lstCommand = []
                lstCommand.append(command)
                lstFutureState.append(self._createAState(newBoard))
                break
            elif self.isDefeat(command):
                lstCommand.pop()
                lstFutureState.pop()

            newBoard = self.board.copy_state()

        self.futureState = lstFutureState
        self.lstCommand = lstCommand

    def isVicotry(self,board):
        rep = False
        if board.get_winner() != None:
            if board.get_winner() == self.team:

                rep = True
        return rep


    def isDefeat(self,Mycommand):
        newBoard = self.board.copy_state()
        newBoard.play_command(Mycommand)
        lstChoixAction = self._getAllEnemiPositionToPlay(newBoard)

        for choix in lstChoixAction:
            command = Command(choix[0], choix[1])
            newBoard.play_command(command)
            if newBoard.get_winner() == self._getOtherTeam():
                return True
            newBoard = self.board.copy_state()
            newBoard.play_command(Mycommand)

        return False

    def _getOtherTeam(self):
        if self._isMyTeamWhite():
            return Team.BLACK
        else:
            return Team.WHITE
            
    def _getAllEnemiPositionToPlay(self,board):
        if self._isMyTeamWhite():
            return board.get_legal_moves(Team.BLACK)
        else:
            return board.get_legal_moves(Team.WHITE)

    def _getAllMinePositionToPlay(self):
        return self.board.get_legal_moves(self.team)


    def _getAllPions(self,board):
        listPion = self._getAllEntities(board)
        blackPion = []
        whitePion = []
        for paw in listPion:
            if paw.is_black():
                self._insertIntoPawList(paw,blackPion)
            else:
                self._insertIntoPawList(paw,whitePion)


        return [whitePion,blackPion]

    def _insertIntoPawList(self,paw,lstPaw):
        if (self._isPawQueen(paw)):
            lstPaw.insert(0, self._getPositionPaw(paw))
        else:
            lstPaw.append(self._getPositionPaw(paw))

    def _getAllEntities(self,board):
        return board.get_entities()

    def _createAState(self,board):
        return self.IA.getState(self._getAllPions(board))

    def _isMyTeamBlack(self):
        return self.team == Team.BLACK

    def _isMyTeamWhite(self):
        return not self._isMyTeamBlack()

    def _getPositionPaw(self,paw):
        return (paw.get_position().x, paw.get_position().y)

    def _isPawQueen(self,paw):
        return paw.is_queen()

    def updateScore(self,winnerTeam):
        if winnerTeam == self.team:
            self.IA.endGame(True)
        else:
            self.IA.endGame(False)

class IAFactory:
    AI = None

    @staticmethod
    def getInstance():
        if IAFactory.AI == None:
            IAFactory.AI = IA()
        return IAFactory.AI

class IA:
    def __init__(self,training = True,colorWhite = True):
        self._win = 100
        self._lose = -50
        self._greedy = 0.2
        self._lstState = []
        self._learningRate = 0.2
        self._gamma = 0.9
        self._reduceReward = 0.9
        self._training = training
        self._colorWhite = colorWhite
        self._actualState = None
        self._futuresStatesFromBoard = None
        self._data = Data()

    def play(self,myState,futureState):
        self._actualState = self._data.getState(myState)
        self._futuresStatesFromBoard = futureState
        if self._training:
            self._lstState.append(myState)  # Etat de l'adversaire
            newState = self._train()



        else:
            newState = self._realPlay()


        self._actualState = None
        self._futuresStatesFromBoard = None
        return newState

    def setTrainingOff(self):
        self._training =  False

    def setTraingOn(self):
        self._training = True

    def setColorWhite(self):
        self._colorWhite = True

    def setColorBlack(self):
        self._colorWhite = False

    def _realPlay(self):
        lstChoiceFututeState = self._getAllFutureState(self._actualState)
        if len(lstChoiceFututeState) != 0:
            newState = self._getBestState(self._actualState)

        else:
            newState = random.choice(self._futuresStatesFromBoard)

        return newState

    def _getBestState(self,aState):
        lstChoiceFututeState = self._getAllFutureState(aState)
        if self._colorWhite:
            actualScore = -1
        else:
            actualScore = 1000

        actualChoice = None
        for state in lstChoiceFututeState:
            score = state.getScore()
            if self._colorWhite and actualScore < score:
                actualScore = score
                actualChoice = state

            elif not self._colorWhite and actualScore > score: #Black => on prend le pire score
                actualScore = score
                actualChoice = state
        return actualChoice


    def _train(self):
        valueToExplore = random.random()

        lstFutureStateFromData = self._getAllFutureState(self._actualState)
        if len(lstFutureStateFromData) == 0:
            self._updateFutureState()

        if valueToExplore >= self._greedy:
            choix = random.choice(lstFutureStateFromData)


        else:
            choix = self._getBestState(self._actualState)

        self._lstState.append(choix)

        return choix

    def endGame(self,victory):
        self._lstState.reverse()
        self._lstState.pop()
        if victory:
            reward = self._win
        else:
            reward = self._lose

        for state in self._lstState:
            if self._data.getState(state) != None:
                self._calculateNewValuesToState(self._data.getState(state), reward)
                reward = self._reduceReward * reward
            else:
                print("hey un NONE")


    def _calculateNewValuesToState(self,state,reward):
        print(state)
        oldScore = state.getScore()
        print(state.index)
        print(state.score)
        bestScore = self._getBestScoreFromAllFutureState(state)
        newScore = oldScore + self._learningRate*(reward + self._gamma * bestScore - oldScore )
        self._setNewScoreToState(state, newScore)

    def _getBestScoreFromAllFutureState(self,actualState):
        return self._getScoreFromState(self._getBestState( self._getAllFutureState(actualState)))

    def getState(self,lstPosPion):
        return self._transformToState(lstPosPion)

    def _getAllFutureState(self,state):

        return self._data.getFuturState(state)

    def _setNewScoreToState(self, state, score):
        self._data.setNewScoreToState(state, score)

    def _transformToState(self,lstPosPion):
        return self._data.createAState(lstPosPion)

    def _getScoreFromState(self,state):
        return self._data.getScoreFromState(self._data.getState(state))

    def _updateFutureState(self):
        for state in self._futuresStatesFromBoard:
            self._data.addState(state)
            self._data.createALinkBetweenState(self._actualState,state)

class Data:
    def __init__(self):
        self._univers = StateUnivers()

    def getState(self, state):
        return self._univers.getState(state)

    def addState(self, stateToADD):
        self._univers.addNewState(stateToADD)

    def setNewScoreToState(self,state,newScore):
        self._univers.updateScore(state,newScore)

    def getScoreFromState(self,state):
        self._univers.getScoreFromState(state)

    def getFuturState(self, state):
        try:
            return state.getNextPossibleState()
        except:
            return []
    def createAState(self, stateToCreate):
        return State(stateToCreate[0],stateToCreate[1],-1)

    def createALinkBetweenState(self,oldState,newState):
        self._univers.createALinkBetweenState(oldState,newState)

class StateUnivers:
    def __init__(self):
        self._stateList = StateList()
        self._hashTableStateOfIndex = HashTable()

    def getState(self, state):
        if self.isExistingState(state):
            listIndex = self._hashTableStateOfIndex.getListIndex(state)
            for index in listIndex:
                stateToTest = self._stateList.getState(index)
                if self._isEqualsState(state, stateToTest):
                    return stateToTest
        else:
            return None

    def isExistingState(self,state):
        listIndex = self._hashTableStateOfIndex.getListIndex(state)
        if listIndex == None:
            return False
        for index  in listIndex:
            stateToTest = self._stateList.getState(index)
            if self._isEqualsState(state, stateToTest):
                return True
        return False

    def _getStateFromIndex(self,index):
        return self._stateList.getState(index)

    def addNewState(self,stateToAdd):
        if not self.isExistingState(stateToAdd):
            indexOfState = self._stateList.getNewIndex()
            stateToAdd.setIndex(indexOfState)
            self._hashTableStateOfIndex.addNewEntry(stateToAdd, indexOfState)
            self._stateList.addNewState(stateToAdd)

    def getScoreFromState(self,state):
        return self.getState(state).getScore()

    def _isEqualsState(self, firstState, secondState):
        for pos in firstState.getWhite():
            if not pos in secondState.getWhite():
                return False
        for pos in firstState.getBlack():
            if not pos in secondState.getBlack():
                return False
        return True

    def updateScore(self,state,newScore):
        self.getState(state).setScore(newScore)

    def createALinkBetweenState(self,oldState,newState):
        trueOldState = self.getState(oldState)
        trueNewState = self.getState(newState)
        if trueNewState == None:
            self.addNewState(trueNewState)
            trueNewState = self.getState(trueNewState)

        trueOldState.addNewLinkedState(trueNewState)

class StateList:
    def __init__(self):
        self._listState =  [State([(3, 0)], [(4, 7)], 0)]

    def getState(self,index):
        return self._listState[index]

    def _isExisting(self,index):
        return len(self._listState)-1 >= index

    def getNewIndex(self):
        return len(self._listState)

    def addNewState(self,state):
        self._listState.append(state)

class HashTable:
    def __init__(self):
        self._hashTable = {42391158275216203514294433255: [0]}

    def addNewEntry(self,state,index):
        listIndex = self.getListIndex(state)
        if listIndex != None :
            if not index in listIndex:
                listIndex.append(index)
        else:
            self._setNewKey(self._hashKey(state),index)

    def _setNewKey(self,key,index):
        self._hashTable[key] = [index]


    def getListIndex(self,state):
        if self.isExistingEntry(state):
            return self._getValueHashTable(self._hashKey(state))
        return None

    def isExistingEntry(self,state):
        try:
            self._getValueHashTable(self._hashKey(state))
            return True
        except KeyError:
            return False

    def _hashKey(self, state):
        pions = []
        for i in range(64):
            pions.append('0')
        for i in state.getWhite():
            pions[i[0] + 8 * i[1]] = '1'
        for i in state.getBlack():
            pions[i[0] + 8 * i[1]] = '2'

        base_3 = ""
        for i in pions:
            base_3 += i
        base_10 = int(base_3, 3)

        return base_10

    def _getValueHashTable(self,key):
        return self._hashTable[key]

class State:
    def __init__(self, lstWhite, lstBlack, index, nextPossibleState=None, score = 0):
        if nextPossibleState is None:
            nextPossibleState = []
        self.lstBlack = lstBlack
        self.lstWhite = lstWhite
        self.index = index
        self.score = score
        self.nextPossibleState = nextPossibleState

    def setScore(self,newScore):
        self.score = newScore

    def getScore(self):
        return self.score

    def getIndex(self):
        return self.index

    def getWhite(self):
        return self.lstWhite

    def getBlack(self):
        return self.lstBlack

    def setBlack(self,newLstBlack):
        self.lstBlack =  newLstBlack

    def setWhite(self,newLstWhite):
        self.lstWhite = newLstWhite

    def setIndex(self,newIndex):
        self.index = newIndex

    def getNextPossibleState(self):
        return self.nextPossibleState

    def setNextPossibleState(self,newLstState):
        self.nextPossibleState = newLstState

    def addNewLinkedState(self,state):
        if not state in self.nextPossibleState:
            self.nextPossibleState.append(state)

class SortList:
    @staticmethod
    def sortList(lstToSort):

        if len(lstToSort) == 1:
            return lstToSort
        else:
            indexToExchange = SortList.findLowestValue(lstToSort)
            SortList.exchange(0,indexToExchange,lstToSort)
            SortList.sortList(lstToSort[1:])


    @staticmethod
    def exchange(indexOne, indexTwo, list):

        list[indexOne], list[indexTwo] = list[indexTwo], list[indexOne]

    @staticmethod
    def findLowestValue(lstToSort):
        bestIndex = 100
        lowestX = 100
        lowestY = 100
        for index in range(len(lstToSort)):
            x = str(lstToSort[0])
            y = str(lstToSort[1])
            if x < lowestX:
                lowestX = x
                lowestY = y
                bestIndex = index
            elif x == lowestX and y < lowestY:
                bestIndex = index
                lowestY = y
        return bestIndex

def make_play(board_copy, current_player, last_move):
    IA = InterfaceGameIA(False,current_player) # TODO True=Entrainement, False=Algo
    command = IA.play(board_copy)
    return (command.get_from(),command.get_to())