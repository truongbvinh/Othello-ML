"""
Author: Vinh Truong
"""

import tensorflow as tf
import numpy as np
import random
import sys
import os
import othello_logic as oth
from math import log2
from tensorflow import keras
# from heap import maxHeap

class Agent(object):
    def __init__(self):
        
        self.generation = 0
        self.gamma = 0.75
        self.board_size = 64
        self.dimension = 8
        self.epsilon = 0.9
        self.learning_rate = 0.2
        self.checkpoint_path = "models/othello_v0.1.h5"
        self.checkpoint_dir = os.path.dirname(self.checkpoint_path)
        self.model = self._create_model()
        self._increment_generation()
    
    def _increment_generation(self):
        if self.epsilon > 0.1:
            self.epsilon = 1/log2(self.generation/2+2)
        self.generation += 1

    def train(self):
        data = self.generate_training_set(100, True)
        print("Generation", self.generation)
        self.model.fit(data[0], data[1], epochs=1)
        self._increment_generation()

    def generate_training_set(self, num_elements, verbose=False):
        percent_done = 0
        result = [[],[]]
        train, target = 0, 1

        temp = (self.generate_training_info(verbose))

        result[train] = temp[train]
        result[target] = temp[target]

        print("Generating... {}%\r".format((percent_done*100)//num_elements))
        for _ in range(num_elements-1):
            percent_done += 1
            temp = self.generate_training_info(verbose)
            result[train].extend(temp[train])
            result[target].extend(temp[target])
            print("Generating... {}%\r".format((percent_done*100)//num_elements))
        
        print("Finished!")

        result[train] = np.array(result[train])
        # result[train] = result[train].reshape(result[train].shape[0], 8, 8)
        result[target] = np.array(result[target])
        # print(result[target])

        return (result[train], result[target])

    def generate_training_info(self, verbose=False):
        game = oth.Othello(self.dimension, self.dimension, "B", ">")
        train = []
        target = []
        scores = []
        score_index = []
        counter = 0

        # game.print_board()
        while game.find_winner() == None and not game.board_is_full():
            game_copy = game.copy()
            if verbose:
                if counter%2 == 0:
                    game.print_board()
                else:
                    game_copy.flip_board()
                    game_copy.print_board()
                    game_copy.flip_board()
            print()
            predictions = self.model.predict(game_copy.game.reshape(1, 8, 8))[0]
            moves = list(zip(predictions, range(self.board_size)))
            moves.sort(key=lambda x: x[0], reverse=True)
            move_index = random.randint(0, int(self.epsilon*self.board_size-1))

            score = None
            if game_copy.get_current_player() == "Black": # Black player
                score = game.get_black_pieces()
            else:
                score = game.get_white_pieces()
            
            attempt = 0
            
            while move_index+attempt > -1:
                try:
                    row, col = moves[move_index+attempt][1]//8, moves[move_index+attempt][1]%8
                    game_copy._make_move(row, col)

                    if game_copy.get_current_player() == "Black":
                        score = game_copy.get_black_pieces() - score
                    else:
                        score = game_copy.get_white_pieces() - score
                    
                    game_copy.flip_board()
                    break

                except oth.InvalidMoveError:
                    predictions[moves[move_index+attempt][1]] = 0
                    # If the move is invalid, then try the next valid move
                    attempt -= 1
            
            if move_index+attempt == -1:
                break
            
            predictions[moves[move_index+attempt][1]] = score / 12
            
            train.append(game.game)
            target.append(predictions)
            game = game_copy
        
        return (train,target)

    def save_model(self):
        self.model.save(self.checkpoint_dir)
        print("Saved!")


    def switch_data(self, current):
        """
        used in generate_training_info to split up data
        by player
        """
        return 1 if current==0 else 0

    def discount(self, r, gamma, normal):
        """
        will discount the moves so that moves that lead
        to good moves will get some extra points
        """
        discount = np.zeros_like(r)
        G = 0.0
        for i in reversed(range(0, len(r))):
            G = G * gamma + r[i]
            discount[i] = G
        # Normalize 
        if normal:
            mean = np.mean(discount)
            std = np.std(discount)
            discount = (discount - mean) / (std)
        return discount

    def customLoss(self, target, pred):
        """
        Returns a mean squared error loss
        """
        loss = (target-pred)**2
        return loss

    def _create_model(self):
        """
        Creates a keras CNN model. Several convolution and maxpooling layers,
        followed by densely connected layers to a softmax output layer
        """

        model = keras.Sequential([
            keras.layers.Flatten(input_shape=(self.dimension, self.dimension)),
            keras.layers.Dense(64, activation=tf.nn.relu),

            keras.layers.Dense(256, activation = tf.nn.relu),
            # keras.layers.Dropout(0.6),

            keras.layers.Dense(512, activation = tf.nn.relu),
            # keras.layers.Dropout(0.6),

            keras.layers.Dense(256, activation = tf.nn.relu),
            # keras.layers.Dropout(0.6),

            keras.layers.Dense(64, activation = tf.nn.softmax)
        ])

        model.compile(optimizer = keras.optimizers.Adam(lr=self.learning_rate),
            loss = self.customLoss)

        return model

if __name__ == "__main__":
    agent = Agent()
    try:
        while True:
            agent.train()
            print("Generation:", agent.generation)
    except KeyboardInterrupt:
        agent.save_model()