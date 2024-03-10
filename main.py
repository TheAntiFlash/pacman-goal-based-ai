from enum import Enum
from random import shuffle
import os


class State(Enum):
    Empty = 0
    Ghost = 1
    Cherry = 2
    Food_Pallet = 3


stateCount = {
    State.Ghost: 4,
    State.Cherry: 5
    ,
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
            os.system('clear')
            if self.cherry_power_up_cooldown > 0:
                print("Cherry Power Up!!!", self.cherry_power_up_cooldown, "s LEFT!")
            self.show_game()
            options = self.options_to_move()
            priority = {option: 0 for option in options} # 4 for food, 3 for cherry, 2 for when there is ghost and cherry is eaten. 1 for empty. 0 for ghost.
            options_left = len(options)
            input("Press any key to continue...\n")
            for option in options:

                if self.grid[option[0]][option[1]] == State.Food_Pallet.value:
                    priority[option] = 4

                elif self.grid[option[0]][option[1]] == State.Cherry.value:
                    priority[option] = 3

                elif (self.grid[option[0]][option[1]] == State.Ghost.value) and self.cherry_power_up_cooldown > 0:
                    priority[option] = 2

                elif self.grid[option[0]][option[1]] == State.Empty.value:
                    priority[option] = 1
                options_left -= 1


            maxPriority = max(priority.values())
            if maxPriority > 0:
                option = next((key for key, value in priority.items() if value == maxPriority), None)
                if maxPriority == 4:
                    self.move(option)
                    foodLeft -= 1
                    self.cherry_power_up_cooldown -= 1
                    self.grid[option[0]][option[1]] = State.Empty.value
                elif maxPriority == 3:
                    self.move(option)
                    self.cherry_power_up_cooldown = 3
                    self.grid[option[0]][option[1]] = State.Empty.value
                elif maxPriority == 2:
                    self.move(option)
                    self.cherry_power_up_cooldown -= 1
                elif maxPriority == 1:
                    self.move(option)
                    self.cherry_power_up_cooldown -= 1
            else:
                print("No more moves!!!")
                quit()

            self.game = self.grid_to_game()
            self.game[self.row][self.col] = 'ᗧ'
        os.system('clear')
        self.show_game()

    def options_to_move(self):
        offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        adjacent_coordinates = [(self.row + dr, self.col + dc) for dr, dc in offsets if
                                0 <= self.row + dr <= 3 and 0 <= self.col + dc <= 3]

        return adjacent_coordinates

    def move(self, new_pos):
        self.row = new_pos[0]
        self.col = new_pos[1]

    def show_game(self):
        for row in self.game:
            print(row)


os.system('clear')
Agent()
