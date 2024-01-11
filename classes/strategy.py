import copy
import math
import random
from math import log, sqrt, inf
from random import randrange
import numpy as np
from rich.table import Table
from rich.progress import track
from rich.console import Console
from rich.progress import Progress

import classes.logic as logic

# When implementing a new strategy add it to the `str2strat`
# dictionary at the end of the file


class PlayerStrat:
    def __init__(self, _board_state, player):
        self.root_state = _board_state
        self.player = player

    def start(self):
        """
        This function select a tile from the board.

        @returns    (x, y) A tuple of integer corresponding to a valid
                    and free tile on the board.
        """
        
        raise NotImplementedError
        

class Node(object):
    """
    This class implements the main object that you will manipulate : nodes.
    Nodes include the state of the game (i.e. the 2D board), children (i.e. other children nodes), a list of
    untried moves, etc...
    """
    def __init__(self, board, move=(None, None),
                 wins=0, visits=0, children=None):
        # Save the #wins:#visited ratio
        self.state = board
        self.move = move
        self.wins = wins
        self.visits = visits
        self.children = children or []
        self.parent = None
        self.untried_moves = logic.get_possible_moves(board)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)


class Random(PlayerStrat):
# Build here the class for a random player
    def start(self):
        result = random.choice(logic.get_possible_moves(self.root_state))
        return result
    
class MiniMax(PlayerStrat):
# Build here the class implementing the MiniMax strategy  
    def __init__(self, _board_state, player):
        super().__init__(_board_state, player)
        self.player=player
        self.opponent=3-player

    def max_value(self, node, alpha, beta):
        if logic.is_game_over(self.opponent, node.state):
            return self.utility(node.state), None
        v = -math.inf
        best_move = None
        for action in node.untried_moves:
            new_state = self.result(node.state, action, self.player)
            v2, _ = self.min_value(Node(new_state), alpha, beta)
            if v2 > v:
                v, best_move = v2, action
            if v >= beta:
                return v, best_move  # Beta
            alpha = max(alpha, v)
        return v, best_move 

    def min_value(self, node, alpha, beta):
        if logic.is_game_over(self.player, node.state):
            return self.utility(node.state), None
        v = math.inf
        best_move = None
        for action in node.untried_moves:
            new_state = self.result(node.state, action, self.opponent)
            v2, _ = self.max_value(Node(new_state), alpha, beta)
            if v2 < v:
                v, best_move = v2, action
            if v <= alpha:
                return v, best_move  # Alpha
            beta = min(beta, v)
        return v, best_move
    
    def utility(self, state):
        winner = logic.is_game_over(self.player, state)
        if winner is not None:
            return 1
        else:
            return -1

    def result(self, state, action, player):
    #Create a new state by applying a new action to the current state 
        new_state = copy.deepcopy(state)
        new_state[action] = player
        return new_state

    def start(self):
        _, best_move = self.max_value(Node(self.root_state), -math.inf, math.inf)
        return best_move


class MiniMaxUp(PlayerStrat):
#Upgraded version of the minimax algorithm with evaluation function
    def __init__(self, _board_state, player):
        super().__init__(_board_state, player)
        self.player=player
        self.opponent=3-player

# Build here the class implementing the MiniMax strategy  
        
    def evaluate_board(self, state):

        return 0  #

    def minimax_decision(self, node,depth):
        # if self.player == logic.WHITE_PLAYER:
        #     value, move = self.max_value(node, logic.WHITE_PLAYER, -math.inf, math.inf) 
        # else:
        #     value, move = self.min_value(node, logic.BLACK_PLAYER, -math.inf, math.inf)
        value, move = self.max_value(node, -math.inf, math.inf,depth)
        return value, move

    def max_value(self, node, alpha, beta,depth): #regarde self.opponent(player)
        if depth <= 0 or logic.is_game_over(self.opponent, node.state):
            # print(f"Max pour joueur {player}")
            return self.utility(node.state,depth), None
        v = -math.inf
        best_move = None
        for action in node.untried_moves:
            new_state = self.result(node.state, action, self.player)
            v2, _ = self.min_value(Node(new_state), alpha, beta,depth - 1)
            if v2 > v:
                v, best_move = v2, action
            if v >= beta:
                return v, best_move  # Beta
            alpha = max(alpha, v)
        # print(f"Max renvoyé: {best_move} \n {node.state}")
        return v, best_move 

    def min_value(self, node, alpha, beta, depth):
        if depth <=0 or logic.is_game_over(self.player, node.state):
            return self.utility(node.state, depth), None
        v = math.inf
        best_move = None
        for action in node.untried_moves:
            # print(f"Print des untried {node.untried_moves}")
            new_state = self.result(node.state, action, self.opponent)
            v2, _ = self.max_value(Node(new_state), alpha, beta, depth - 1)
            if v2 < v:
                v, best_move = v2, action
            if v <= alpha:
                return v, best_move  # Alpha
            beta = min(beta, v)
        # print(f"Min renvoyé: {best_move} \n{node.state}")
        return v, best_move
    


    def utility(self, state, depth):
        winner1 = logic.is_game_over(self.player, state)
        winner2 = logic.is_game_over(self.opponent, state)
        if winner1 is not None:
            return 1
        elif winner2 is not None:
            return -1
        else:
            # Use heuristic evaluation for non-terminal states
            return self.evaluate_board(state) * (1 if self.player == 1 else -1)

    def result(self, state, action, player):
        new_state = copy.deepcopy(state)
        new_state[action] = player
        return new_state

    def start(self, depth=4):
        _, best_move = self.minimax_decision(Node(self.root_state), depth)
        return best_move
           

str2strat: dict[str, PlayerStrat] = {
        "human": None,
        "random": Random,
        "minimax": MiniMax,
        "minimaxup": MiniMaxUp
}