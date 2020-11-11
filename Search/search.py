# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from util import Stack

    visited = set()                                             # set to keep track of visited nodes
    fringe = Stack()                                            # stack used as fringe for keeping pairs of (node, path-to-node) 
    fringe.push((problem.getStartState(), []))                  # push (Node, [path-from-start-to-node]) pair into the fringe
    curr_node, path_to_node = fringe.pop()

    while(not problem.isGoalState(curr_node)):                  # while not reached a goal state
        
        if curr_node not in visited:                            # if current node is not visited yet
            visited.add(curr_node)              
            successors = problem.getSuccessors(curr_node)       # get the successors of the current node
            for successor in successors:                        # push each successor into the fringe
                child_node = successor[0]
                child_path = successor[1]
                # construct full path to child node
                full_path = path_to_node + [child_path]
                fringe.push((child_node, full_path))
        
        curr_node, path_to_node = fringe.pop()                  # get the next node from fringe

    return path_to_node                                         # return full path to goal node

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue

    visited = set()                                        # set to keep track of visited nodes
    fringe = Queue()                                       # keeping pairs (node, path_to_node) for implementing the BFS
    fringe.push((problem.getStartState(), []))             # push the pair (start_state, []) into the fringe
    curr_node, path_to_node = fringe.pop()                 # get the current node from the fringe (queue)

    while(not problem.isGoalState(curr_node)):             # while not reached a goal state
        
        if curr_node not in visited:
            visited.add(curr_node)
            successors = problem.getSuccessors(curr_node)
            for successor in successors:
                child_node = successor[0]   
                child_path = successor[1]   
                full_path = path_to_node + [child_path]     # assign the full path from start to child
                fringe.push((child_node, full_path))        # push the pair (child_node, [full-path-to-child]) into the fringe
    
        curr_node, path_to_node = fringe.pop()
    
    return path_to_node                                     # return the full path to goal node 

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    
    visited = set()                                             # set to keep track of visited nodes
    fringe = PriorityQueue()                                    # implementing the UCS with a PQ
    fringe.push((problem.getStartState(), [], 0), 0)            # pushing into PQ ((initial_state, path_to-initial-state = null, cost-of-this-path=0), priority of item=0)

    curr_node, path_to_node, cost_to_node = fringe.pop()

    while (not problem.isGoalState(curr_node)):                 # while not reached a goal state
        if curr_node not in visited:                
            visited.add(curr_node)
            successors = problem.getSuccessors(curr_node)   
            for successor in successors:
                child = successor[0]
                child_path = successor[1]
                child_cost = successor[2]
                full_path = path_to_node + [child_path]
                total_cost = cost_to_node + child_cost
                # priority of each node is the total_cost for reaching it
                fringe.push((child, full_path, total_cost), total_cost)
        curr_node, path_to_node, cost_to_node = fringe.pop()

    return path_to_node                                         # return the full path to goal node 

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    visited = set()
    fringe = PriorityQueue()                                                                        # implementing the A* using PQ
    fringe.push((problem.getStartState(), [], 0), 0 + heuristic(problem.getStartState(), problem))  # push((current-node, path-to-current-node, path-cost), g(x)=g(x)+h(x))

    curr_node, path_to_node, cost_to_node = fringe.pop()    
    
    while (not problem.isGoalState(curr_node)):                                                     # while not reached a goal state
        if curr_node not in visited:
            visited.add(curr_node)
            successors = problem.getSuccessors(curr_node)
            for successor in successors:
                child = successor[0]
                child_path = successor[1]
                child_cost = successor[2]
                full_path = path_to_node + [child_path]
                total_cost = cost_to_node + child_cost
                priority = total_cost + heuristic(child, problem)                                    # the priority of each item is the combined total_cost value + the heuristic's value
                fringe.push((child, full_path, total_cost), priority)                                # push the new (successor) node into the fringe
        curr_node, path_to_node, cost_to_node = fringe.pop()

    return path_to_node                                                                              # return the full path to goal node
    

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch