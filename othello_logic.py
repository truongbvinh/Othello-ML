# Vinh Truong

import numpy as np

class InvalidMoveError(Exception):
	pass

class GameFinishedError(Exception):
	pass

class InvalidSizeError(Exception):
	pass

class InvalidValueError(Exception):
	pass

class InvalidBoardError(Exception):
	def __str__(self) -> str:
		return "Board has to be even dimensions from 4 to 16"

class Othello:
	"""
	ATTRIBUTES:
	REFER, for program reference
	FULL_OR_SIM, full or simple game
	game, gameboard
	ROWS, number of rows
	COLS, number of cols
	current_player, current player (1 or 2)
	"""

	REFER = {0: ".", 1: "B", 2: "W"}
	FULL_OR_SIM = "FULL"

	#################### INIT FUNCTIONS ###############################
	def __init__(self, rows: int, cols: int, first: str, style: str, board=[]):
		"""
		Initializes the board, first player, win condition based on the imput
		"""
		self._check_row_col(rows, cols)
		self._check_first(first)
		self._check_win_type(style)
		self.game = self._create_board(rows, cols)
		self.ROWS = rows
		self.COLS = cols
		self.current_player = self._first_player(first)
		self.STYLE = style
		if board == []:
			board = self.game
			board[rows//2 -1][cols//2 -1]=1
			board[rows//2][cols//2]=1
			board[rows//2][cols//2 -1]=2
			board[rows//2 -1][cols//2]=2
			# self.print_board()
		self._set_board(board)
	
	def copy(self):
		result = Othello(self.ROWS, self.COLS, Othello.REFER[self.current_player], self.STYLE, self.game)
		return result
	
	def flip_board(self):
		for row in range(self.ROWS):
			for col in range(self.COLS):
				if self.game[row][col] == 1:
					self.game[row][col] = 4
				self.game[row][col] //= 2

	def _create_board(self, rows: int, cols: int) -> [[int]]:
		"""
		Creates a board based on user input. For reference,
		0 is empty, 1 is Black, 2 is White
		"""
		board = []

		if rows < 4 or rows > 16 or cols < 4 or  cols > 16:
			raise InvalidBoardError
		elif rows % 2 == 1 or cols % 2 == 1:
			raise InvalidBoardError

		for _ in range(rows):
			board.append(np.array([0]*cols))

		return np.array(board)

	def _check_row_col(self, row: int, col: int):
		"""
		Checks if the row and column fits acceptable values. Raises error if not
		"""
		if row % 2 == 1 or col % 2 == 1:
			raise InvalidSizeError
		if row < 4 or row > 16 or col < 4 or col > 16:
			raise InvalidSizeError

	def _check_win_type(self, win: str):
		"""
		Checks if the win type fits acceptable values. Raises error if not
		"""
		if win != ">" and win != "<":
			raise InvalidValueError

	def _check_first(self, player: str):
		"""
		Checks if the first player fits acceptable values. Raises error if not
		"""
		if player != "B" and player != "W":
			raise InvalidValueError


	def _first_player(self, first: str) -> str:
		"""
		Returns the first player, "B" will return 1, "W" returns 2
		"""
		if first == "B":
			return 1
		elif first == "W":
			return 2


	def _set_board(self, board: [[str]]) -> None:
		"""
		Sets the object's board based on a string which will represent the
		board
		"""
		# print(board, self.game)
		if len(board) > len(self.game):
			raise InvalidSizeError

		for row in range(len(self.game)):

			if len(board[row]) > len(self.game[row]):
				raise InvalidSizeError

			for col in range(len(self.game[row])):
				if board[row][col] == "." or board[row][col] == 0:
					self.game[row][col] = 0
				elif board[row][col] == "B" or board[row][col] == 1:
					self.game[row][col] = 1
				elif board[row][col] == "W" or board[row][col] == 2:
					self.game[row][col] = 2


	def print_board(self) -> None:
		"""
		Takes in a game board and prints it out to console
		"""
		b = 0
		w = 0
		result = ""
		for row in self.game:
			for col in row:
				if col == 1:
					b += 1
				elif col == 2:
					w += 1
				result += self.REFER[col] + " "
			result = result.strip()
			result += "\n"
		print(result, end = "")


	############################ GET METHODS ###############################
	def get_black_pieces(self) -> int:
		"""
		Returns the number of black pieces
		"""
		total = 0
		for row in self.game:
			for col in row:
				if col == 1:
					total += 1

		return total

	def get_white_pieces(self) -> int:
		"""
		Returns the number of white pieces
		"""
		total = 0
		for row in self.game:
			for col in row:
				if col == 2:
					total += 1

		return total

	def get_rows(self) -> int:
		"""
		Returns the number of rows in the board
		"""
		return self.ROWS

	def get_cols(self) -> int:
		"""
		Returns the number of cols in the board
		"""
		return self.COLS

	def get_current_player(self) -> int:
		"""
		Returns the current player:
		1 is Black
		2 is White
		"""
		if self.current_player == 1:
			return "Black"
		return "White"

	############################# MOVE VALIDATION ##########################

	def _direction_is_valid(self, row, col, dir1, dir2) -> ["tuples of coordinate"]:
		"""
		Returns a list of tuples containing all the tiles to be flipped in
		given direction based on the current player, returns empty list if
		direction is not valid
		"""
		tiles = []
		has_between = False

		row += dir1
		col += dir2

		while (row < self.ROWS and row >= 0) and (col < self.COLS and col >= 0):

			if self.game[row][col] == self.current_player:
				if has_between:
					break
				else:
					return []
			elif self.game[row][col] == 0:
				return []
			else:
				has_between = True
				tiles.append((row, col))

			row += dir1
			col += dir2

		if (row > self.ROWS-1 or row < 0) or (col > self.COLS-1 or col < 0):
			# I need this because there is a case when rows or cols get to 0, appends
			# a piece and thus doesn't break out of the loop UNTIL either rows or
			# cols reach a negative number, which would still be a valid index.
			# This is okay since iif it were a valid move, the while loop would have
			# been broken out of before they would be negative
			return []

		if has_between:
			return tiles
		else:
			return []


	def placement_is_valid(self, row, col) -> ["tuples of coordinates"]:
		"""
		Returns a list of tuples containing the coordinates of the tiles
		to be flipped, returns empty list if the move is not valid
		"""
		if (self.game[row][col] != 0 or 
			(row > self.ROWS - 1 or row < 0) or 
			(col > self.COLS - 1 or col < 0)):
			return []
			# returns empty if the index is invalid

		result = []
		for dir1 in range(-1, 2):
			for dir2 in range(-1, 2):
				if dir1 == 0 and dir2 == 0:
					continue
				try:
					result.extend(self._direction_is_valid(row, col, dir1, dir2))
				except IndexError:
					pass
		return result


	def take_turn(self, move: list) -> None:
		"""
		Places a piece from the current player. If the move is invalid,
		prints INVALID and takes in another coordinate until it is valid, then
		switches players
		"""

		if self.board_is_full():
			raise GameFinishedError

		# Uses 1 based indexing, NOT 0 based indexing
		move[0] = (int)(move[0]) - 1
		move[1] = (int)(move[1]) - 1

		self._make_move(move[0], move[1])

		self.change_player()



	def _make_move(self, row, col) -> bool:
		"""
		Makes a move for the current player, returns true if
		a move was made, false if not
		"""
		try:
			moves = self.placement_is_valid(row, col)
		except IndexError:
			raise InvalidMoveError

		if len(moves) == 0:
			raise InvalidMoveError

		self.game[row][col] = self.current_player

		for move in moves:
			if self.game[move[0]][move[1]] == 1:
				self.game[move[0]][move[1]] = 2
			else:
				self.game[move[0]][move[1]] = 1

		return True



	############################## PLAYING FUNCTIONS ##########################


	def board_is_full(self) -> bool:
		"""
		Method to check if the board is full, returns True if it is, False if not
		"""
		for row in self.game:
			for col in row:
				if col == 0:
					return False
		return True


	def find_winner(self) -> str:
		"""
		Finds the winnder of the game. Returns None if the game is not
		done yet, else it returns a string containing either "B", "W" or
		"NONE"
		"""
		pieces = self._count_pieces()
		b = pieces[0]
		w = pieces[1]

		game_copy = self.copy()
		game_copy.flip_board()

		for spot in range(self.ROWS*self.COLS):
			row, col = spot//self.ROWS, spot%self.COLS
			if len(self.placement_is_valid(row, col)) > 0 or len(game_copy.placement_is_valid(row, col)) > 0:
				return None
				

		if self.STYLE == ">":
			if b > w:
				return "Black"
			elif w > b:
				return "White"
			else:
				return "NONE"
		else:
			if b < w:
				return "Black"
			elif w < b:
				return "Wwhite"
			else:
				return "NONE"

	def _count_pieces(self) -> "tuple of pieces, (black, white)":
		"""
		Helper method to count the pieces in the board
		"""
		b = 0
		w = 0

		for row in self.game:
			for col in row:
				if col == 1:
					b += 1
				elif col == 2:
					w += 1

		return (b, w)


	def change_player(self) -> None:
		"""
		changes to the next player's turn
		"""
		if self.current_player == 1:
			self.current_player = 2
		elif self.current_player == 2:
			self.current_player = 1