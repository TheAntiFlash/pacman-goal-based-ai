from enum import Enum
from random import shuffle


class State(Enum):
    Empty = 0
    Ghost = 1
    Cherry = 2
    Food_Pallet = 3


stateCount = {
    State.Ghost: 4,
    State.Cherry: 5,
    State.Food_Pallet: 6

}

stateToEmoji = {
    State.Ghost.value: '👻',
    State.Cherry.value: '🍒',
    State.Food_Pallet.value: '🍏',
    State.Empty.value: '🕳️'
}


class Environment:
    def __init__(self):
        random_data = ([State.Ghost.value] * stateCount[State.Ghost]
                       + [State.Cherry.value] * stateCount[State.Cherry]
                       + [State.Food_Pallet.value] * stateCount[State.Food_Pallet])
        shuffle(random_data)
        random_data.insert(0, 0)
        self.grid = [random_data[i:i + 4] for i in range(0, len(random_data), 4)]
        self.game = self.grid_to_game()

    def grid_to_game(self):
        return [[str(stateToEmoji[cell]) for cell in row] for row in self.grid]

    def show_game(self):
        for row in self.game:
            print(row)
