from enum import Enum
from random import shuffle
import os


class State(Enum):
    Empty = 0
    Ghost = 1
    Cherry = 2
    Food_Pallet = 3


stateCount = {
    State.Ghost: 3,
    State.Cherry: 6,
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

    def grid_to_game(self):
        return [[str(stateToEmoji[cell]) for cell in row] for row in self.grid]


class Agent(Environment):
    def __init__(self):
        super().__init__()
        self.row = 0
        self.col = 0
        self.cherry_power_up_cooldown = 0
        self.game = self.grid_to_game()
        self.game[self.row][self.col] = 'ᗧ'

        foodLeft = stateCount[State.Food_Pallet]
        while foodLeft > 0:
            self.show_game()
            options = self.options_to_move()
            options_left = len(options)
            print([row for row in options])
            input("Press any key to continue...\n")
            backtrack = []
            for option in options:

                if self.grid[option[0]][option[1]] == State.Food_Pallet.value:
                    self.move(option)
                    foodLeft -= 1
                    self.cherry_power_up_cooldown -= 1
                    self.grid[option[0]][option[1]] = State.Empty.value
                    break
                elif self.grid[option[0]][option[1]] == State.Cherry.value:
                    if options_left > 0:
                        backtrack = option
                        options_left -= 1
                        continue
                    self.move(option)
                    self.cherry_power_up_cooldown = 3
                    self.grid[option[0]][option[1]] = State.Empty.value

                    break
                elif (self.grid[option[0]][option[1]] == State.Ghost.value) and self.cherry_power_up_cooldown > 0:
                    if options_left > 0:
                        options_left -= 1
                        continue
                    self.move(option)
                    self.cherry_power_up_cooldown -= 1
                    break
                elif self.grid[option[0]][option[1]] == State.Empty.value:
                    if options_left > 0:
                        if not backtrack:
                            # if (self.grid[backtrack[0]][backtrack[1]] != State.Cherry.value
                            #         or self.grid[backtrack[0]][backtrack[1]] != State.Ghost.value):
                            backtrack = option
                        options_left -= 1
                        continue

                    self.move(option)
                    self.cherry_power_up_cooldown -= 1
                    break
                options_left -= 1
            else:
                if backtrack:
                    self.move(backtrack)
                    self.cherry_power_up_cooldown -= 1
                print("No more options")
                quit()

            #os.system('clear')
            self.game = self.grid_to_game()
            self.game[self.row][self.col] = 'ᗧ'

    def options_to_move(self):
        offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        adjacent_coordinates = [(self.row + dr, self.col + dc) for dr, dc in offsets if
                                0 <= self.row + dr <= 3 and 0 <= self.col + dc <= 3]
        # adjacent_coordinates = [
        #     (r, c) for r, c in adjacent_coordinates if 0 <= r <= 3 and 0 <= c <= 3
        # ]
        return adjacent_coordinates

    def move(self, new_pos):
        self.row = new_pos[0]
        self.col = new_pos[1]

    def show_game(self):
        for row in self.game:
            print(row)


os.system('clear')
Agent()
