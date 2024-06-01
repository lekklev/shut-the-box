import numpy as np

class Dice():
    def __init__(self, n_dice=2):
        self.n_dice = n_dice
        self.sides = 6 # Die has 6 sides

    def throw(self):
        """
        Throws number of dice with n sides.

        Credits: https://stackoverflow.com/questions/55546656/how-to-calculate-the-sum-of-dice-rolls-efficiently
        """
        return sum((np.array(range(self.sides))+1)*
                   np.random.multinomial(self.n_dice,[1/float(self.sides)]*self.sides))

class Box():
    """
    This class represents a box in shut the box.
    """
    def __init__(self, n_tiles=9):
        """
        This function initializes the box.

        Attributes:
        :param n_tiles: number of tiles in the box
        :type n_tiles: int
        :param tile_array: array of tiles in the box
        :type tile_array: np.array[int]
        :param status_array: array of status of tiles in the box; either 0 or 1; 0 means unflipped and 1 means flipped
        :type status_array: np.array[int]
        :param n_states: number of states in the box
        :type n_states: int
        :param max_flips: maximum number of tiles that can be flipped in a turn
        :type max_flips: int
        :param reward: reward for the box
        :type reward: int
        """
        self.n_tiles=n_tiles
        self.tile_array = np.arange(1, n_tiles + 1) # Shut the box starts at 1 and ends at n (usually 9)
        self.status_array = np.zeros(n_tiles)
        self.n_states = 2 ** self.n_tiles
        self.max_flips = 2
        # TODO: incorporate reward
        self.reward = -np.sum(self.tile_array)
        #TODO: how to visualise dice combinations?

    def flip(self, tile):
        """
        This function flips a tile in the box.
        
        Attributes:
        :param tile: value of tile to be flipped
        :type tile: int
        :rtype: None
        """ 
        #TODO: what if we want to flip multiple tiles?
        tile_idx = self.tile_array.index(tile)
        self.status_array[tile_idx] = 1
        self.reward += tile

    def reset(self):
        """
        This function resets the box.
        """
        self.status_array = np.zeros(self.n_tiles)

    def terminated(self):
        if np.array_equal(np.status_array, np.ones_like(self.tile_array)):
            return True
            
    def unflipped_tiles(self):
        # Return what the values of tiles are not flipped yet
        return self.tile_array[self.status_array == 0]

    def legal_actions(self, value):
        """
        This function returns the legal actions for a given value.
        
        Attributes:
        :param value: value of dice throw
        :type value: int
        :rtype: list[list[int]]
        """
        unflipped_tiles = unflipped_tiles(self)
        results = []

        def backtrack(start, current_partition, current_sum):
            """
            This backtracking function finds all possible partitions of a given value.

            Attributes:
            :param start: starting index for partition
            :type start: int
            :param current_partition: current partition
            :type current_partition: list[int]
            :param current_sum: current sum of partition
            :type current_sum: int
            :rtype: None
            """
            # Base case: If the partition sum equals n and length is within the limit
            if current_sum == value and len(current_partition) <= self.max_flips:
                results.append(current_partition[:])
                return
            # If the partition sum exceeds n or length exceeds k, stop further exploration
            if current_sum > value or len(current_partition) > self.max_flips:
                return
            
            # Recursively add numbers to the partition
            for i in range(start, len(unflipped_tiles)):
                num = unflipped_tiles[i]
                # Add the number to the current partition and recurse
                current_partition.append(num)
                backtrack(i + 1, current_partition, current_sum + num)
                # Backtrack: Remove the last number added
                current_partition.pop()
        
        backtrack(0, [], 0)
        return results
