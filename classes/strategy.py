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
        #print("Random ")
        #print(result)
        return result
        
class MiniMax(PlayerStrat):
# Build here the class implementing the MiniMax strategy
    def minimax_decision(self, state):
        actions = logic.get_possible_moves(state)
        result = max(actions, key=lambda a: self.max_value(self.result(state, a)))
        #print(result)
        return result

    def max_value(self, state, depth=3):
        if logic.is_game_over(self.player, state) or depth == 0:
            return self.utility(state)
        v = -math.inf
        for a in logic.get_possible_moves(state):
            v = max(v, self.min_value(self.result(state, a)), depth - 1)
        #print(f"Max_value Profondeur : {depth} a la valeur: {a}")
        return v

    def min_value(self, state, depth=3):
        if logic.is_game_over(self.player, state) or depth == 0:
            return self.utility(state)
        v = math.inf
        for a in logic.get_possible_moves(state):
            v = min(v, self.max_value(self.result(state, a)), depth -1 )
        #print(f"Min_value Profondeur : {depth} a la valeur: {v}")
        return v

    def utility(self, state):
        winner = logic.is_game_over(self.player, state)
        if winner == self.player:
            return 1
        elif winner is not None:
            return -1
        else:
            return 0

    def result(self, state, action):
        new_state = copy.deepcopy(state)
        new_state[action] = self.player
        return new_state
    
    def start(self):
        return self.minimax_decision(self.root_state)
    
class MiniMax2(PlayerStrat):
# Build here the class implementing the MiniMax strategy
    def minimax_decision(self, state):
        actions = logic.get_possible_moves(state)
        result = max(actions, key=lambda a: self.max_value(self.result(state, a)))
        #print(result)
        return result

    def max_value(self, state, depth=3):
        if logic.is_game_over(self.player, state) or depth == 0:
            return self.utility(state)
        v = -math.inf
        for a in logic.get_possible_moves(state):
            v = max(v, self.min_value(self.result(state, a)), depth - 1)
        #print(f"Max_value Profondeur : {depth} a la valeur: {a}")
        return v

    def min_value(self, state, depth=3):
        if logic.is_game_over(self.player, state) or depth == 0:
            return self.utility(state)
        v = math.inf
        for a in logic.get_possible_moves(state):
            v = min(v, self.max_value(self.result(state, a)), depth -1 )
        #print(f"Min_value Profondeur : {depth} a la valeur: {v}")
        return v

    def utility(self, state):
        winner = logic.is_game_over(self.player, state)
        if winner == self.player:
            return 1
        elif winner is not None:
            return -1
        else:
            return 0

    def result(self, state, action):
        new_state = copy.deepcopy(state)
        new_state[action] = self.player
        return new_state
    
    def start(self):
        return self.minimax_decision(self.root_state)


str2strat: dict[str, PlayerStrat] = {
        "human": None,
        "random": Random,
        "minimax": MiniMax,
        "test": MiniMax2
}