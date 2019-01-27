import copy
# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions
from game import Agent
from heuristics import *
import random
import math

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class RandomSequenceAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0,10):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        possible = state.getAllPossibleActions();
        for i in range(0,len(self.actionList)):
            self.actionList[i] = possible[random.randint(0,len(possible)-1)];
        tempState = state;
        for i in range(0,len(self.actionList)):
            if tempState.isWin() + tempState.isLose() == 0:
                tempState = tempState.generatePacmanSuccessor(self.actionList[i]);
            else:
                break;
        # returns random action from all the valide actions
        return self.actionList[0];

class HillClimberAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        self.possible = state.getAllPossibleActions()
        for i in range(0,5):
            self.actionList.append(Directions.STOP);
        return;

    def mutate(self, tempList):
        newList = []
        for i in range(0, len(tempList)):
            if random.randint(0,1):
                newList.append(self.possible[random.randint(0, len(self.possible) - 1)])
            else:
                newList.append(tempList[i])
        return newList

    # GetAction Function: Called with every frame
    def getAction(self, state):
        for i in range(0, 5):
            self.actionList[i] = self.possible[random.randint(0, len(self.possible) - 1)]
        bestScore = -100
        # print("New Move")
        stop = False
        while stop is False:
            tempState = state
            tempSequence = self.mutate(self.actionList[:])
            score = -100
            for i in range(0,len(tempSequence)):
                if tempState.isWin() + tempState.isLose() == 0:
                    tempState = tempState.generatePacmanSuccessor(tempSequence[i])
                    if tempState is None:
                        tempState = state
                        stop = True
                        break
                    # tempState = tempState.generatePacmanSuccessor(self.actionList[i]);
                else:
                    tempState = state
                    # self.actionList = bestSequence
                    # print("not considering")
                    break
            if tempState is not state:
                score = gameEvaluation(state,tempState)
            # print(score, bestScore)
            if score >= bestScore:
                bestScore = score
                self.actionList = tempSequence
        # print(self.actionList)
        return self.actionList[0]

class GeneticAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        # self.population = []
        self.possible = state.getAllPossibleActions();
        # for j in range(0,8):
        #     actionList = []
        #     for i in range(0, 5):
        #         actionList.append(Directions.STOP);
        #     self.population.append(actionList)
        return;

    def calcFitness(self,initialState, chromosome):
        tempState = initialState
        for i in chromosome:
            if tempState.isWin() + tempState.isLose() == 0:
                tempState = tempState.generatePacmanSuccessor(i);
            else:
                break
        return gameEvaluation(initialState,tempState)

    def rankSelection(self):
        self.population.sort(key=lambda x: x[1])
        rankSum = 36
        rankProb = []
        for i in range(1, len(self.population)+1):
            rankProb.append(float(i)/float(rankSum))
        randScore = random.uniform(0,sum(rankProb))
        for item in range(len(rankProb)):
            randScore = randScore - rankProb[item]
            if randScore<=0:
                break
        return (self.population[item])[0]

    def crossOver(self, parent1, parent2):
        result = []
        if random.randint(0, 100) <= 70:
            for k in range(2):
                child = []
                for i in range(len(parent1)):
                    if random.randint(0,100) < 50:
                        child.append(parent1[i])
                    else:
                        child.append(parent2[i])
                result.append(child)
        else:
            result.append(parent1)
            result.append(parent2)

        return result[0],result[1]

    def mutate(self,child1, child2):
        # mutationGene = random.randint(0, len(child) - 1)
        # mutatedChild1 = child1
        # mutatedChild1[mutationGene] = self.possible[random.randint(0, len(self.possible) - 1)]
        # mutationGene = random.randint(0, len(child) - 1)
        # mutatedChild2 = child2
        # mutatedChild2[mutationGene] = self.possible[random.randint(0, len(self.possible) - 1)]
        for child in [child1, child2]:
            mutationGene = random.randint(0, len(child)-1)
            child[mutationGene] = self.possible[random.randint(0, len(self.possible) - 1)]
        return child1,child2
        # return mutatedChild1,mutatedChild2

    # GetAction Function: Called with every frame
    def getAction(self, state):
        self.population = []
        for i in range(0, 8):
            actionList = []
            for j in range(0, 5):
                actionList.append(self.possible[random.randint(0, len(self.possible) - 1)])
            self.population.append(actionList)
        self.bestChromosome = [self.possible[0],0]
        try:
            while True:
                new_population = []
                self.population = [(chromosome, self.calcFitness(state, chromosome)) for chromosome in self.population]
                for i in range(len(self.population)/2):
                    child1, child2 = self.crossOver(self.rankSelection(), self.rankSelection())
                    if random.randint(0,100) <= 10:
                        child1, child2 = self.mutate(child1, child2)
                    new_population.append(child1)
                    new_population.append(child2)

                if self.bestChromosome[1] <= (self.population[7])[1]:
                    self.bestChromosome[0] = (self.population[7])[0]
                    self.bestChromosome[1] = (self.population[7])[1]
                self.population = new_population
        except:
            print(self.population[0])[0]
            return (self.population[0])[0]

class MCTSAgent(Agent):
    # Initialization Function: Called one time when the game starts

    def registerInitialState(self, state):
        self.cp = 0.1
        self.stop = False
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        self.stop = False
        # TODO: write MCTS Algorithm instead of returning Directions.STOP
        class node():
            def __init__(self, action=None, possibleChild=None, parent=None):
                self.child = [] #Saving [action, UCT]
                self.parent = parent
                self.action = action
                self.possibleChild = possibleChild
                self.simulationReward = 0
                self.visitCount = 0

            def treePolicy(state, gameState):
                print("We are doing treepolicy")
                while True:
                    if len(state.possibleChild) != 0 and gameState.isLose() + gameState.isWin() == 0:
                        return state.expand(gameState)
                    else:
                        state, gameState = state.bestChild(self.cp, gameState)
                    # else:
                    #     break
                return state, gameState

            def expand(state, gameState):
                print("We are expanding")
                b = random.randint(0, len(state.possibleChild) - 1)
                a = state.possibleChild[b]
                state.possibleChild.pop(b)
                childGameState = gameState.generatePacmanSuccessor(a)
                newChild = node(a, childGameState.getLegalPacmanActions(), state)
                state.child.append(newChild)
                # state.child.append(a)
                return newChild, childGameState

            def bestChild(state, cp, gameState):
                print("We are searching best child")
                bestScore = -25
                bstChild = node()
                bestState = gameState
                for child in state.child:
                    b = (child.simulationReward / child.visitCount) + (cp * (math.sqrt((2 * math.log(state.visitCount)) / child.visitCount)))
                    if b >= bestScore and gameState.isWin() + gameState.isLose() == 0:
                        bstChild = child
                        bestScore = b
                        nextState = gameState.generatePacmanSuccessor(child.action)
                        if nextState is None:
                            self.stop = True
                            break
                        else:
                            bestState = copy.deepcopy(nextState)
                    # else:
                    #     break
                print(bstChild.action, bstChild.visitCount, bstChild.simulationReward,bestScore)
                return bstChild, bestState

            def defaultPolicy(state, gameState):
                print("We are doing rollout")
                s = copy.deepcopy(gameState)
                # steps = ['North', 'South', 'East', 'West']
                steps = gameState.getLegalPacmanActions()
                for i in range(5):
                    if s.isLose() + s.isWin() == 0:
                        s = s.generatePacmanSuccessor(random.choice(steps))
                    else:
                        break
                # print(gameEvaluation(gameState, s))
                return gameEvaluation(gameState, s)

            def backup(state, delta):
                print("We are backingup")
                while state is not None:
                    state.visitCount += 1
                    state.simulationReward += delta
                    state = state.parent

            def mostVisited(state):
                action = 0
                visit = 0
                for i in state.child:
                    if i.visitCount >= visit:
                        visit = i.visitCount
                        action = i.action
                return action

        root = node(None, state.getLegalPacmanActions(), None)
        print("new tree")
        try:
            while True:
                gameState = copy.deepcopy(state)
                for i in root.child:
                    print(i.visitCount,i.simulationReward, i.action)
                print("change")
                v1, gameState = root.treePolicy(gameState)
                delta = v1.defaultPolicy(gameState)
                v1.backup(delta)
        except:
            for i in root.child:
                print(i.visitCount,i.simulationReward, i.action)
            # a1, a2 = root.bestChild(1, state)
            # print("final Action",a1.action)
            # return a1.action
            print("asd",root.mostVisited())
            retAc = root.visitCount
            return root.mostVisited()
