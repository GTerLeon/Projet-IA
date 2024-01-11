import os
import pickle
import logging
import csv
import seaborn as sns
import matplotlib.pyplot as plt
from rich import print
from rich.logging import RichHandler

# Hide Pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import pandas as pd

from classes.logic import player2str
from classes.game import Game

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler()]
)


class Tournament:
    def __init__(self, args: list):
        """
        Initialises a tournament with:
           * the size of the board,
           * the players strategies, eg., ("human", "random"),
           * the game counter,
           * the number of games to play.
        """
        self.args = args
        (self.BOARD_SIZE, self.STRAT, self.GAME_COUNT,
         self.N_GAMES, self.USE_UI) = args

        if self.USE_UI:
            pygame.init()
            pygame.display.set_caption("Polyline")

    def single_game(self, black_starts: bool=True) -> int:
        """
        Runs a single game between two opponents.

        @return   The number of the winner, either 1 or 2, for black
                  and white respectively.
        """

        game = Game(board_size=self.BOARD_SIZE,
                    black_starts=black_starts, 
                    strat=self.STRAT,
                    use_ui=self.USE_UI)
        game.print_game_info(
            [self.BOARD_SIZE, self.STRAT, self.GAME_COUNT]
        )
        while game.winner is None:
            game.play()

        print(f"{player2str[game.winner]} player ({self.STRAT[game.winner-1]}) wins!")

        return game.winner

    def championship(self):
        """
        Runs a number of games between the same two opponents.
        """
        scores = [0, 0]

        for _ in range(self.N_GAMES):
            self.GAME_COUNT = _

            # First half of the tournament started by one player.
            # Remaining half started by other player (see "no pie
            #  rule")
            winner = self.single_game(
                black_starts=self.GAME_COUNT < self.N_GAMES / 2
            )
            scores[winner-1] += 1

        log = logging.getLogger("rich")

        # TODO Design your own evaluation measure!
        # https://pyformat.info/
        log.info("Design your own evaluation measure!")
        #Writes in score.csv the outcome of the tournament and display heatmap of all scores 
        percentWin = (scores[0] / self.N_GAMES) * 100

        # Write to CSV
        with open('score.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.STRAT[0], self.STRAT[1], self.N_GAMES, percentWin])

        # Read the CSV into a DataFrame
        df_load = pd.read_csv('score.csv', header=None, names=['strategy1', 'strategy2', 'n_games', 'win_percentage'])

        # Group by strategy1, strategy2 and calculate the mean of the win percentages
        df = df_load.groupby(['strategy1', 'strategy2']).apply(lambda x: (x['win_percentage'] * x['n_games']).sum() / x['n_games'].sum()).reset_index(name='win_percentage')

        pivot_df = df.pivot('strategy1', 'strategy2', 'win_percentage')

        # Create the heatmap using seaborn
        plt.figure(figsize=(10, 8))
        sns.heatmap(pivot_df, annot=True, fmt=".1f", cmap='viridis')
        plt.title("Heatmap of all scores")
        plt.show()

        print(scores)
        