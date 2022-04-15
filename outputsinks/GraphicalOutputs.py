from typing import Dict, List
from collections import defaultdict
from WordleStringParser import WordleMetadata
from outputsinks.WordleOutputSink import WordleOutput
import matplotlib.pyplot as plt
import numpy as np

class AverageScore(WordleOutput):
    
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

        print("AverageScore Players:", players, end='\n')
        print("AverageScore Averages:", averages, end='\n')

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
