from Environment import Environment, State, stateCount
from os import system, name


# Function that uses os to clear screen.
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


class Agent(Environment):
    def __init__(self):
        super().__init__()

        # Initial values of pacman agent.
        self.row = 0
        self.col = 0

        # value of how many moves till cherry power up is over. Initially zero until cherry is picked up.
        self.cherry_power_up_cooldown = 0
        # Placing pacman emoji on (0,0)
        self.game[self.row][self.col] = 'ᗧ'

        # Goal is to eat all food_pallet. this will get the current count of food that will be
        # tracked throughout the session.
        foodLeft = stateCount[State.Food_Pallet]
        # This is the previous state pacman was at. initialized to current state for now. Keep track of this to avoid
        # being stuck in a loop
        prev = (0, 0)

        # Session will run until all food_pallets are eaten.
        while foodLeft > 0:
            clear()
            if self.cherry_power_up_cooldown > 0:
                print("Cherry Power Up!!!", self.cherry_power_up_cooldown, "s LEFT!")
            self.show_game()

            # Get all positions pacman can move to.
            options = self.options_to_move()

            # initialize a dictionary for all options, setting default priority to 0.
            # 4 for food, 3 for cherry, 2 for when there is ghost and
            # cherry is eaten. 1 for empty. 0 for ghost.
            priority = {option: 0 for option in options}

            input("Press any key to continue...\n")
            # Loops through all options and assigns it a priority based on its state.
            for option in options:

                if self.grid[option[0]][option[1]] == State.Food_Pallet.value:
                    priority[option] = 4

                elif self.grid[option[0]][option[1]] == State.Cherry.value:
                    priority[option] = 3

                elif (self.grid[option[0]][option[1]] == State.Ghost.value) and self.cherry_power_up_cooldown > 0:
                    priority[option] = 2

                elif self.grid[option[0]][option[1]] == State.Empty.value:
                    priority[option] = 1

            # Gets the current max priority available amongst the options to move.
            maxPriority = max(priority.values())

            # Ensuring the max priority isn't 0 (in case of ghost and no powerup)
            if maxPriority > 0:

                # checks if we ignore the option with max priority which was the previous state,
                # do we have any other options?
                # if the if condition is true we move to the previous state.
                # else move to the second state with max priority
                if next((key for key, value in priority.items() if value == maxPriority and key != prev), None) is None:
                    option = next((key for key, value in priority.items() if value == maxPriority), None)
                else:
                    option = next((key for key, value in priority.items() if value == maxPriority and key != prev),
                                  None)
                prev = (self.row, self.col)

                # Moving to state with max priority keeping in mind previous state as well.
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
        clear()
        self.show_game()
        print("Mission Accomplished!!!")

    # Returns the coordinates adjacent to pacman.
    def options_to_move(self):
        offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        adjacent_coordinates = [(self.row + dr, self.col + dc) for dr, dc in offsets if
                                0 <= self.row + dr <= 3 and 0 <= self.col + dc <= 3]

        return adjacent_coordinates

    # Moves pacman

    def move(self, new_pos):
        self.row = new_pos[0]
        self.col = new_pos[1]
