from player import Player
from board import HexBoard
import random as random
import time as time
import heapq as heapq

# An action is a tuple (row,col,player_id). For example (1,4,1) or (2,1,2).

# Smart Player is a MonteCarloTreeSearch based player.
class SmartPlayer(Player):
    # Time limit of five seconds
    time_limit = 4.8

    def play(self, board: HexBoard) -> tuple:
        return self.mcts(board)

    def mcts(self,board: HexBoard):
        startTime = time.time()

        actions = self.GetCandidateActions(board,self.player_id)
        other_player = self.AlternatePlayer(self.player_id)

        utility = {}
        for action in actions:
            utility[action] = 0

        playouts = 0
        
        while time.time() - startTime < self.time_limit:
            action = random.choice(actions)
            winner = self.Simulate(self.MakeNewBoard(action,board),other_player)
            if winner == self.player_id:
                utility[action] = utility[action] + 1
            playouts = playouts + 1

        return self.GetBestAction(actions,utility,playouts)

    
    def GetBestAction(self,actions,utility,playouts):
        """Returns the action of higest average utility. Ties are broke randomly."""
        bestAction = []
        bestAverageUtility = -1
        for action in actions:
            averageUtility = utility[action] / playouts

            if fabs(averageUtility - bestAverageUtility) < 0.000001:
                bestAction.append(action)
                continue

            if averageUtility > bestAverageUtility:
                bestAction = [ action ]
                bestAverageUtility = averageUtility

        return random.choice(bestAction)


    # Returns the wining player. Simulates alternating plays, following a playout policy, until it reaches a terminal state. 
    def Simulate(self,board: HexBoard, player):
        """ board: A copy of the current board. player: the current player"""
        while not self.IsTerminal(board):
            actions = self.GetCandidateActions(board,player) # Playout policy
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

    # Even-r adyacency logic. For moving in the board-graph.
    adyacents_for_odd_rows = [(-1,0),(0,1),(1,0),(1,-1),(0,-1),(-1,-1)]
    adyacents_for_even_rows = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(0,-1)]
    def Adyacent(self,row,col,size):
        a = []
        adj = 0
        if row % 2 == 0:
            adj = self.adyacents_for_even_rows
        else:
            adj = self.adyacents_for_odd_rows
        for i,j in adj:
            nrow = row + i
            ncol = col + j
            if nrow < 0 or nrow >= size or ncol < 0 or ncol >= size:
                continue
            a.append((nrow,ncol))
        return a

    # Apply policy of nodes on minimum cost paths
    def GetCandidateActions(self,board: HexBoard, player_id):
        # dont modify the board
        # each cell in the board is a node in the graph
        inf = 100000000
        minimumCost = [ [inf for _ in range(board.size)] for _ in range(board.size) ]
        parents = [ [ [] for _ in range(board.size)] for _ in range(board.size) ]
        isExamined = [ [False for _ in range(board.size)] for _ in range(board.size) ]

        # Dijkstra Algorithm
        pq = [] # Priority queue
        
        # Get first column cells that are empty or belong to you
        if player_id == 1:
            for row in range(board.size):
                if board.board[row][0] == 0 or board.board[row][0] == 1:
                    heapq.heappush(pq,(1 - board.board[row][0],row,0,(-1,-1)) )

        # Get first row cells that are empty or belong to you
        if player_id == 2:
            for col in range(board.size):
                if board.board[0][col] == 0:
                    heapq.heappush(pq,(1,0,col,(-1,-1)))
                if board.board[0][col] == 2:
                    heapq.heappush(pq,(0,0,col,(-1,-1)))

        while len(pq) > 0:
            cost,row,col,parent = heapq.heappop(pq)

            # Revisiting, ignore
            if cost > minimumCost[row][col]:
                continue

            # Another path, different from previous one
            if cost == minimumCost[row][col]:
                parents[row][col].append(parent)
                continue
            
            # Visited for first time
            if cost < minimumCost[row][col]:
                minimumCost[row][col] = cost
                parents[row][col].append(parent)
                for newrow,newcol in self.Adyacent(row,col,board.size):
                    weight = 0 # If you played on this cell the edge has weight 0

                    # if this cell is empty the edge has weight 1
                    if board.board[newrow][newcol] == 0:
                        weight = 1
                    
                    # You cant move to other player cells
                    if board.board[newrow][newcol] != 0 and board.board[newrow][newcol] != player_id:
                        continue
                    
                    heapq.heappush(pq,(cost + weight,newrow,newcol,(row,col)))

        # Compute Nodes that belong to minimun cost paths

        selected = []
        if player_id == 1:
            lastCol = board.size - 1
            # Get the last column cells whose cost is equal to the minimum cost, they can be unocupied or ocupied
            min = inf
            for row in range(board.size):
                if board.board[row][lastCol] == 2:
                    continue
                cost = minimumCost[row][lastCol]
                if cost == min:
                    selected.append((row,lastCol))
                if cost < min:
                    min = cost
                    selected = [ (row,lastCol) ]
                
        if player_id == 2:
            lastRow = board.size - 1
            # Get the last row cells whose cost is equal to the minimum cost, they can be unocupied or ocupied by you
            min = inf
            for col in range(board.size):
                if board.board[lastRow][col] == 1:
                    continue
                cost = minimumCost[lastRow][col]
                if cost == min:
                    selected.append((lastRow,col))
                if cost < min:
                    min = cost
                    selected = [ (lastRow,col) ]

        candidates = []
        while len(selected) > 0:
            row,col = selected.pop()
            # que puede pasar sean 0 o mias, no pueden ser del otro
            # sea -1 -1 que no se juega
            if row == -1 or col == -1:
                continue

            if isExamined[row][col]:
                continue

            isExamined[row][col] = True
            if board.board[row][col] == 0:
                candidates.append((row,col,player_id))

            selected = selected + parents[row][col]

        return candidates


    def ApplyAction(self,action,board: HexBoard):
        """Given an action and a board, modify the board by appliying the action."""
        row, col, player_id = action
        if not board.place_piece(row,col,player_id):
            raise RuntimeError(f"Cannot apply action. Row {action[0]}, col {action[1]} , player {action[2]}")

    def MakeNewBoard(self,action,board):
        """Given an action and a board returns a new board, the result of appliying the action on the old board."""
        newBoard = board.clone()
        self.ApplyAction(action,newBoard)
        return newBoard

    # A state is terminal if either player has connected its sides
    def IsTerminal(self,board):
        return board.check_connection(1) or board.check_connection(2)

    def AlternatePlayer(self,player):
        if player == 1:
            return 2
        if player == 2:
            return 1
        raise RuntimeError(f"Invalid player. Expected 1 or 2 but received {player}")

