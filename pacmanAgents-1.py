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

class OneStepLookAheadAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(admissibleHeuristic(state), action) for state, action in successors]
        # get best choice
        bestScore = min(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        queue = []
        leafs = []
        # For creating a single node structure.
        class node:
            def __init__(self, state, parent = None, action = None, depth = 0):
                self.state = state
                self.child = []
                self.parent = parent
                self.action = action
                self.depth = depth
            # For returning the actions from parents.
            def solution(find_parent_action):
                while find_parent_action.parent.parent:
                    find_parent_action = find_parent_action.parent
                return find_parent_action.action
            # For getting the leafnodes from the root node.
            def getLeafs(first_node):
                if first_node is not None:
                    if len(first_node.child) == 0:
                        leafs.append(first_node)
                    for n in first_node.child:
                        n.getLeafs()

        root = node(state, None, None, 0)
        queue.append(root)
        #Iterating over the whole queue till its empty.
        while queue:
            current_state = queue.pop(0)
            legal = current_state.state.getLegalPacmanActions()
            successors = [(current_state.state.generatePacmanSuccessor(action), action) for action in legal]
            for child, action in successors:
                new_child = node(child, current_state, action, current_state.depth + 1)
                current_state.child.append(new_child)
                if new_child.state == None:
                    # print "going into max"
                    root.getLeafs()
                    leafNode = leafs
                    scored = [(admissibleHeuristic(leaf.state) + leaf.depth, leaf.solution()) for leaf in leafNode if leaf.state != None]
                    bestScore = min(scored)[0]
                    bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
                    return random.choice(bestActions)
                if new_child.state.isWin():
                    return new_child.solution()
                if new_child.state.isLose():
                    continue
                # Add the child to the queue element.
                queue.append(new_child)


class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        stack = []
        leafs = []

        class node:
            def __init__(self, state, parent=None, action=None, depth = 0):
                self.state = state
                self.child = []
                self.parent = parent
                self.action = action
                self.depth = depth

            def solution(find_parent_action):
                while find_parent_action.parent.parent:
                    find_parent_action = find_parent_action.parent
                return find_parent_action.action

            def getLeafs(first_node):
                if first_node is not None:
                    if len(first_node.child) == 0:
                        leafs.append(first_node)
                    for n in first_node.child:
                        n.getLeafs()

        root = node(state, None, None, 0)
        stack.append(root)
        while stack:
            current_state = stack.pop()
            legal = current_state.state.getLegalPacmanActions()
            successors = [(current_state.state.generatePacmanSuccessor(action), action) for action in legal]
            for child, action in successors:
                new_child = node(child, current_state, action, current_state.depth + 1)
                current_state.child.append(new_child)
                if new_child.state == None:
                    #print "going into max"
                    root.getLeafs()
                    leafNode = leafs
                    scored = [(admissibleHeuristic(leaf.state) + leaf.depth,leaf.solution()) for leaf in leafNode if leaf.state != None]
                    bestScore = min(scored)[0]
                    bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
                    return random.choice(bestActions)
                if new_child.state.isWin():
                    return new_child.solution(new_child)
                if new_child.state.isLose():
                    continue
                stack.append(new_child)

class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        queue = []
        leafs = []

        class node:
            def __init__(self, state, parent=None, action=None,depth = 0, f=None):
                self.state = state
                self.child = []
                self.parent = parent
                self.action = action
                self.depth = depth
                self.f = f

            def solution(find_parent_action):
                while find_parent_action.parent.parent:
                    find_parent_action = find_parent_action.parent
                return find_parent_action.action

            def getLeafs(first_node):
                if first_node is not None:
                    if len(first_node.child) == 0:
                        leafs.append(first_node)
                    for n in first_node.child:
                        n.getLeafs()

        root = node(state, None, None, 0)
        root.f = root.depth + admissibleHeuristic(root.state)
        queue.append(root)
        while queue:
            queue.sort(key=lambda x:x.f)
            current_state = queue.pop(0)
            legal = current_state.state.getLegalPacmanActions()
            successors = [(current_state.state.generatePacmanSuccessor(action), action) for action in legal]
            for child, action in successors:
                new_child = node(child, current_state, action, current_state.depth + 1)
                current_state.child.append(new_child)

                if new_child.state == None:
                    #print "going into max"
                    root.getLeafs()
                    leafNode = leafs
                    scored = [((leaf.f), leaf.solution()) for leaf in leafNode if leaf.state != None]
                    bestScore = min(scored)[0]
                    bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
                    return random.choice(bestActions)

                new_child.f = new_child.depth + admissibleHeuristic(new_child.state)
                if new_child.state.isWin():
                    return new_child.solution(new_child)
                if new_child.state.isLose():
                    continue
                queue.append(new_child)

