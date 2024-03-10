from enum import Enum
from random import shuffle


# State for each cell in game grid.
class State(Enum):
    Empty = 0
    Ghost = 1
    Cherry = 2
    Food_Pallet = 3


# number of such states for each randomly generated game environment.
stateCount = {
    State.Ghost: 4,
    State.Cherry: 5,
    State.Food_Pallet: 6

}

# Converting State to emoji to display in game.
stateToEmoji = {
    State.Ghost.value: '👻',
    State.Cherry.value: '🍒',
    State.Food_Pallet.value: '🍏',
    State.Empty.value: '🕳️'
}


class Environment:
    def __init__(self):
        # Generates a list of each state * how many of each state should be in any game
        random_data = ([State.Ghost.value] * stateCount[State.Ghost]
                       + [State.Cherry.value] * stateCount[State.Cherry]
                       + [State.Food_Pallet.value] * stateCount[State.Food_Pallet])

        # Shuffles the random data to set the environment for the game.
        shuffle(random_data)

        # Inserts the empty state at index 0 for where pacman will be placed
        random_data.insert(0, State.Empty.value)
        # Converts 16 length array to 4x4 array
        self.grid = [random_data[i:i + 4] for i in range(0, len(random_data), 4)]
        # Converts the grid of values 0-3 to their emoji counterparts to display.
        self.game = self.grid_to_game()

    # Converts the grid to game view
    def grid_to_game(self):
        return [[str(stateToEmoji[cell]) for cell in row] for row in self.grid]

    # Displays the game to console.
    def show_game(self):
        for row in self.game:
            print(row)
