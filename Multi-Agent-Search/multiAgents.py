# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newFood = successorGameState.getFood().asList() # getting the newFood as a list
        minFoodDist = float("inf")   # initialize the minFoodDist as infinity

        # find the closeset food
        for food in newFood:
            minFoodDist = min(minFoodDist, manhattanDistance(newPos, food))
        # avoid ghost if too close
        for ghost in successorGameState.getGhostPositions():
            if (manhattanDistance(newPos, ghost) < 2):
                return -float('inf')    # return -inf, as the proposal pacman's successor is (almost) eaten

        return successorGameState.getScore() + 1/minFoodDist

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # returns the action that maximizes pacman's score
        return self.maxValue(gameState, 0, 0)[0] 

    def miniMax(self, gameState, agentIndex, depth):
        if depth == self.depth * gameState.getNumAgents() \
            or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        # because max/minValue functions return a tuple (best action, best action's value)
        # by [1] below we get the best action's value
        if agentIndex == 0: # maximizing player (pacman)
            return self.maxValue(gameState, agentIndex, depth)[1]
        else:   # minimizing opponent player (a ghost)
            return self.minValue(gameState, agentIndex, depth)[1]

    # both maxValue and minValue work with the same logic. for every legal action of the current state, 
    # they return the best one by the min or max value respectively

    def maxValue(self, gameState, agentIndex, depth):
        bestVal = ("max", -float("inf"))
        for action in gameState.getLegalActions(agentIndex):
            newGameState = gameState.generateSuccessor(agentIndex, action)
            newAgentIndex = (depth+1)%gameState.getNumAgents()
            val = (action, self.miniMax(newGameState, newAgentIndex, depth+1))
            # compare actions using their value (get the one with max value)
            bestVal = max(bestVal, val, key=lambda x:x[1]) 
        return bestVal

    def minValue(self, gameState, agentIndex, depth):
        bestVal = ("min", float("inf"))
        for action in gameState.getLegalActions(agentIndex):
            newGameState = gameState.generateSuccessor(agentIndex, action)
            newAgentIndex = (depth+1)%gameState.getNumAgents()
            val = (action, self.miniMax(newGameState, newAgentIndex, depth+1))
            # compare actions using their value (get the one with min value)
            bestVal = min(bestVal, val, key=lambda x:x[1])
        return bestVal

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # because maxValue function returns a tuple (best action, best action's value)
        # by the [0] below, we get the best action. the one which maximizes pacman's score
        return self.maxValue(gameState, 0, 0, -float("inf"), float("inf"))[0]

    def alphaBeta(self, gameState, agentIndex, depth, alpha, beta):
        if depth == self.depth * gameState.getNumAgents() \
            or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        # because maxValue and minValue functions return a tuple (best action, best action's value)
        # by the [1] below, we get the best action's value
        if agentIndex == 0: # maximizing player (pacman)
            return self.maxValue(gameState, agentIndex, depth, alpha, beta)[1]
        else: # minimizing opponent player (a ghost)
            return self.minValue(gameState, agentIndex, depth, alpha, beta)[1]

    # maxValue and minValue functions are almost same as before 
    # just added two lines of code in each one for checking the alpha-beta values

    def maxValue(self, gameState, agentIndex, depth, alpha, beta):
        bestVal = ("max", -float("inf"))
        for action in gameState.getLegalActions(agentIndex):
            newGameState = gameState.generateSuccessor(agentIndex, action)
            newAgentIndex = (depth+1)%gameState.getNumAgents()
            val = (action, self.alphaBeta(newGameState, newAgentIndex, depth+1, alpha, beta))
            # compare actions using their value (get the one with max value)
            bestVal = max(bestVal, val, key=lambda x:x[1])
            # pruning
            if bestVal[1] > beta: return bestVal
            alpha = max(alpha, bestVal[1])
        return bestVal

    def minValue(self, gameState, agentIndex, depth, alpha, beta):
        bestVal = ("min", float("inf"))
        for action in gameState.getLegalActions(agentIndex):
            newGameState = gameState.generateSuccessor(agentIndex, action)
            newAgentIndex = (depth+1)%gameState.getNumAgents()
            val = (action, self.alphaBeta(newGameState, newAgentIndex, depth+1, alpha, beta))
            # compare actions using their value (get the one with min value)
            bestVal = min(bestVal, val, key=lambda x:x[1])
            # pruning
            if bestVal[1] < alpha: return bestVal
            beta = min(beta, bestVal[1])
        return bestVal

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.maxValue(gameState, 0, 0)[0]    # returns the action that maximizes pacman's score

    def expectiMax(self, gameState, agentIndex, depth):
        if depth == self.depth * gameState.getNumAgents() \
            or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agentIndex == 0: # maximizing player (pacman)
            return self.maxValue(gameState, agentIndex, depth)[1]
        else:   # predicting opponent player (a ghost)
            return self.expValue(gameState, agentIndex, depth)

    def maxValue(self, gameState, agentIndex, depth):
        bestVal = ("max", -float("inf"))
        for action in gameState.getLegalActions(agentIndex):
            newGameState = gameState.generateSuccessor(agentIndex, action)
            newAgentIndex = (depth+1)%gameState.getNumAgents()
            val = (action, self.expectiMax(newGameState, newAgentIndex, depth+1))
            # compare actions using their value (get the one with max value)
            bestVal = max(bestVal, val, key=lambda x:x[1])
        return bestVal

    def expValue(self, gameState, agentIndex, depth):
        bestVal = 0
        for action in gameState.getLegalActions(agentIndex):
            newGameState = gameState.generateSuccessor(agentIndex, action)
            newAgentIndex = (depth+1)%gameState.getNumAgents()
            val = self.expectiMax(newGameState, newAgentIndex, depth+1)
            bestVal += val
        bestVal/=len(gameState.getLegalActions(agentIndex)) # uniform probability
        return bestVal

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    food = currentGameState.getFood().asList()
    ghosts = currentGameState.getGhostStates()
    pacmanPosition = currentGameState.getPacmanPosition()
    activeGhosts = [] # Keep active ghosts (that can eat pacman)
    scaredGhosts = [] # Keep scared ghosts (pacman should eat them for extra points)
    totalCapsules = len(currentGameState.getCapsules()) # Keep total capsules
    totalFood = len(food) # Keep total remaining food
    myEval = 0  # Evaluation value

    for ghost in ghosts:
        if ghost.scaredTimer: # Is scared ghost
            scaredGhosts.append(ghost)
        else:
            activeGhosts.append(ghost)

    # Score weight: 1.5           
    myEval += 1.5 * currentGameState.getScore()
    # Food weight: -10
    myEval += -10 * totalFood
    # Capsules weight: -20
    myEval += -20 * totalCapsules

    # Keep distances from food, active and scared ghosts
    foodDistances = []
    activeGhostsDistances = []
    scaredGhostsDistances = []

    # get the distances for food, active and scared ghosts (manhattan distance used)
    for item in food:
        foodDistances.append(manhattanDistance(pacmanPosition,item))
    for item in activeGhosts:
        scaredGhostsDistances.append(manhattanDistance(pacmanPosition,item.getPosition()))
    for item in scaredGhosts:
        scaredGhostsDistances.append(manhattanDistance(pacmanPosition,item.getPosition()))

    # Close food weight: -1                   
    # Quite close food weight: -0.5           
    # Far away food weight: -0.2              
    for item in foodDistances:
        if item < 3:
            myEval += -1 * item
        if item < 7:
            myEval += -0.5 * item
        else:
            myEval += -0.2 * item

    # Close scared ghosts weight: -20                  
    # Quite close scared ghosts weight: -10            
    for item in scaredGhostsDistances:
        if item < 3:
            myEval += -20 * item
        else:
            myEval += -10 * item

    # Close ghost weight: 3                             
    # Quite close ghost weight: 2                       
    # Far away ghosts weight: 0.5                       
    for item in activeGhostsDistances:
        if item < 3:
            myEval += 3 * item
        elif item < 7:
            myEval += 2 * item
        else:
            myEval += 0.5 * item

    return myEval


# Abbreviation
better = betterEvaluationFunction
