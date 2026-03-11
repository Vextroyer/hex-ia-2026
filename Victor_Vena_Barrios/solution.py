from player import Player
from board import HexBoard
import random as random
import time as time

# Smart Player is a MonteCarloTreeSearch based player.
class SmartPlayer(Player):
    # Time limit of five seconds
    time_limit = 4.9

    def play(self, board: HexBoard) -> tuple:
        return self.mcts(board)

    def mcts(self,board: HexBoard):
        startTime = time.time()
        actions = self.GetCandidateActions(board,self.player_id)
        
        utility = {}
        for action in actions:
            utility[action] = 0

        playouts = 0
        
        while time.time() - startTime < self.time_limit:
            action = random.choice(actions)
            simulationBoard = board.clone()
            self.ApplyAction(action,simulationBoard)
            winner = self.Simulate(simulationBoard,self.AlternatePlayer(self.player_id))
            if winner == self.player_id:
                utility[action] = utility[action] + 1
            playouts = playouts + 1

        bestAction = (0,0,0)
        bestAverageUtility = -1
        for action in actions:
            averageUtility = utility[action] / playouts
            if averageUtility > bestAverageUtility:
                bestAction = action
                bestAverageUtility = averageUtility 

        return bestAction

    # Helper functions and classes

    # Returns the wining player. Simulates alternating random plays until it reaches a terminal state.
    def Simulate(self,board: HexBoard, player):
        """ board: A COPY of the current board. player: the current player"""
        while not self.IsTerminal(board):
            actions = self.GetCandidateActions(board,player)
            action = random.choice(actions)
            self.ApplyAction(action,board)
            player = self.AlternatePlayer(player)

        player1Wins = board.check_connection(1)
        player2Wins = board.check_connection(2)
        
        if (player1Wins and player2Wins) or (not player1Wins and not player2Wins):
            raise RuntimeError("Inconsistent simulation")
        
        if player1Wins:
            return 1
        else:
            return 2


    # Just return empty cells
    def GetCandidateActions(self,board: HexBoard, player_id):
        actions = []
        for row in range(board.size):
            for col in range(board.size):
                if board.board[row][col] == 0:
                    actions.append((row,col,player_id))
        return actions

    # Modify state of a board
    def ApplyAction(self,action,board: HexBoard):
        row, col, player_id = action
        if not board.place_piece(row,col,player_id):
            raise RuntimeError("Cannot apply action. This should not happen.")

    # A state is terminal if either player has connected its sides
    def IsTerminal(self,board):
        return board.check_connection(1) or board.check_connection(2)

    def AlternatePlayer(self,player):
        if player == 1:
            return 2
        if player == 2:
            return 1
        raise RuntimeError("Invalid player")



# What is game state: A hex grid with some moves done.
# What is an action: a tuple (row,column,player_id)
# Approach on simulate: alternating random play, its nedded to know the sate of the board