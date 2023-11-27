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
    def minimax_decision(self, state, player):
        actions = logic.get_possible_moves(state)
        result = max(actions, key=lambda a: self.min_value(self.result(state, a), player))
        # print(f"Print de state {result}")
        return result

    def max_value(self, state, player):
        if logic.is_game_over(player, state):
            # print(f"Dans max_value, print {self.utility(state)}")
            return self.utility(state, player)
        v = -math.inf
        for a in logic.get_possible_moves(state):
            v = max(v, self.min_value(self.result(state, a), player))
        # print(f"MAX_VALUE Je maximise le joueur {player}")
        return v

    def min_value(self, state, player):
        if logic.is_game_over(player, state):
            return self.utility(state, player)
        v = math.inf
        for a in logic.get_possible_moves(state):
            v = min(v, self.max_value(self.result(state, a), player))
        # print(f"MIN_VALUE je minimise le joueur {player}")
        return v

    def utility(self, state, player):
        winner = logic.is_game_over(player, state)
        if winner == player:
            return 1
        else:
            return -1

    def result(self, state, action):
        new_state = copy.deepcopy(state)
        new_state[action] = self.player
        return new_state
    
    def start(self):
        return self.minimax_decision(self.root_state, self.player)
    
class MiniMax(PlayerStrat):
# Build here the class implementing the MiniMax strategy        
    def minimax_decision(self, state, player):
        actions = logic.get_possible_moves(state)
        result = max(actions, key=lambda a: self.min_value(self.result(state, a), player))
        # print(f"Print de state {result}")
        return result

    def max_value(self, state, player):
        if logic.is_game_over(player, state):
            # print(f"Dans max_value, print {self.utility(state)}")
            return self.utility(state, player)
        v = -math.inf
        for a in logic.get_possible_moves(state):
            v = max(v, self.min_value(self.result(state, a), player))
        # print(f"MAX_VALUE Je maximise le joueur {player}")
        return v

    def min_value(self, state, player):
        if logic.is_game_over(player, state):
            return self.utility(state, player)
        v = math.inf
        for a in logic.get_possible_moves(state):
            v = min(v, self.max_value(self.result(state, a), player))
        # print(f"MIN_VALUE je minimise le joueur {player}")
        return v

    def utility(self, state, player):
        winner = logic.is_game_over(player, state)
        if winner == player:
            return 1
        else:
            return -1

    def result(self, state, action):
        new_state = copy.deepcopy(state)
        new_state[action] = self.player
        return new_state
    
    def start(self):
        return self.minimax_decision(self.root_state, self.player)
    
class test(PlayerStrat):
# Build here the class implementing the MiniMax strategy  
    def minimax_decision(self, node):
        if self.player == logic.WHITE_PLAYER:
            value, move = self.min_value(node)
        else:
            value, move = self.min_value(node)
        return value, move

    def max_value(self, node):
        if logic.is_game_over(self.player, node.state):
            return self.utility(node.state, self.player), None
        v = -math.inf
        best_move = None
        for action in node.untried_moves:
            child_node = Node(self.result(node.state, action))
            v2, _ = self.min_value(child_node)
            if v2 > v:
                v, best_move = v2, action
        return v, best_move

    def min_value(self, node):
        if logic.is_game_over(self.player, node.state):
            return self.utility(node.state, self.player), None
        v = v = math.inf
        best_move = None
        for action in node.untried_moves:
            child_node = Node(self.result(node.state, action))
            v2, _ = self.max_value(child_node)
            if v2 < v:
                v, best_move = v2, action
        return v, best_move

    def utility(self, state, player):
        winner = logic.is_game_over(player, state)
        if winner == player:
            return 1
        else:
            return -1

    def result(self, state, action):
        new_state = copy.deepcopy(state)
        new_state[action] = self.player
        return new_state

    def start(self):
        _, best_move = self.minimax_decision(Node(self.root_state))
        return best_move

str2strat: dict[str, PlayerStrat] = {
        "human": None,
        "random": Random,
        "minimax": MiniMax,
        "test": test
}