'''This module gathers all graphical output possibilities.'''

from typing import Dict, List, Tuple
from collections import defaultdict
from inputparser.MessageMetadata import WorldeGameSource
from WordleStringParser import WordleMetadata
from outputsinks.WordleOutputSink import WordleOutput
import matplotlib.pyplot as plt
import numpy as np

class AverageScore(WordleOutput):
    '''Output that displays a diagram which shows the average number of tries
    for each player.'''

    def __convert_dict_keys_tolist_sample_size(self, theDict: Dict[str, int]) -> List[str]:
        ret = []
        for player in theDict.keys():
            ret.append(f'{player} (N = {theDict[player]})')
        return ret

    def output_results(self, playedWordles: List[WordleMetadata]) -> None:
        data: Dict[str, int] = defaultdict(lambda: 0)
        playerOccurenceCount: Dict[str, int] = defaultdict(lambda: 0)

        # Gather data
        for wordle in playedWordles:
            if not wordle.steps_to_solution == 'X':
                data[wordle.player] = data[wordle.player] + wordle.steps_to_solution
            playerOccurenceCount[wordle.player] = playerOccurenceCount[wordle.player] + 1
        
        # Calculate averages for each player
        averages: List[int] = []
        players: List[str] = list(data.keys())
        for player in players:
            averages.append(float(data[player]) / playerOccurenceCount[player])

        players = self.__convert_dict_keys_tolist_sample_size(playerOccurenceCount)
        print("AverageScore Players:", players)
        print("AverageScore Averages:", averages)

        fig, ax = plt.subplots()
        width = .7
        display_locations = np.arange(len(players))
        bars = ax.barh(display_locations, averages, width)
        ax.bar_label(bars)
        ax.set_yticks(display_locations + width/2)
        ax.set_yticklabels(players, minor=False)

        plt.title('Average number of tries for each person.')
        plt.ylabel('Players')
        plt.xlabel('Average Number of Tries (lower is better)')
        plt.show()

class AverageScoreForEachWordleType(WordleOutput):
    '''Output that displays a diagram which shows the average number of tries
    for each player for each game category.'''

    def __get_wordle_game_types(self, playedWordles: List[WordleMetadata]) -> List[WorldeGameSource]:
        ret = set()
        for wordle in playedWordles:
            ret.add(wordle.wordleGame)
        return list(ret)

    def output_results(self, playedWordles: List[WordleMetadata]) -> None:
        data: Dict[Tuple[str, WorldeGameSource], int] = defaultdict(lambda: 0)
        playerOccurenceCount: Dict[Tuple[str, WorldeGameSource], int] = defaultdict(lambda: 0)

        # Gather data
        for wordle in playedWordles:
            wordleId = (wordle.player, wordle.wordleGame)
            if not wordle.steps_to_solution == 'X':
                data[wordleId] = data[wordleId] + wordle.steps_to_solution
            playerOccurenceCount[wordleId] = playerOccurenceCount[wordleId] + 1
        
        # Calculate averages for each player
        print("AverageScore Players:", players)
        print("AverageScore Averages:", averages)
        
        played_wordle_types = self.__get_wordle_game_types(playedWordles)

        x = np.arange(len(players))  # the label locations
        width = 0.7/len(played_wordle_types)  # the width of the bars

        fig, ax = plt.subplots()
        bars = [] # Holds the diagram's bars

        rects1 = ax.bar(x - width/2, men_means, width, label='Men')
        rects2 = ax.bar(x + width/2, women_means, width, label='Women')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Average Scores')
        ax.set_title('Average Scores by name and game type')
        ax.set_xticks(x, labels)
        ax.legend()

        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)

        fig.tight_layout()

        plt.show()
