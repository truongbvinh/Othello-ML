# Vinh Truong 88812807, lab section 9
"""
I know this code is really long, but I did it so that I could keep the
setup interaction and playing phase in one window without any popups.
I separated the different methods by the phases of the game.
"""

import othello_logic
import tkinter

class othello_GUI:
	def __init__(self):
		"""
		Initializes the board and binds the reconfigure function
		"""
		self._othello_game = None
		self._root_window = tkinter.Tk()

		self._height = 6
		self._width = 6

		full = tkinter.Label(text = "Full Othello Game", font = 24)
		full.grid(row = 0, column = 0,
			pady = 10, sticky = tkinter.W + tkinter.E)

		self._display = tkinter.Canvas(
			master = self._root_window,
			width = 75 * self._width,
			height = 75 * self._height,
			background = "#D8C68A"
			)

		self._display.grid(
			row = 1, column = 0, padx = 30, pady = 0, columnspan = 4,
			sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)

		self.setup_rowcol()

		self._display.bind("<Configure>", self._help_draw)

		self._root_window.rowconfigure(1, weight = 1)
		self._root_window.columnconfigure(0, weight = 1)
		self._root_window.rowconfigure(2, weight = 0)

		self._x_pos = 0
		self._y_pos = 0

	################################# CLICKING FUNCTIONS ##################################

	def run_game(self) -> None:
		"""
		Runs the game
		"""
		self._root_window.mainloop()

	def _on_canvas_resized(self, event: tkinter.Event) -> None:
		"""
		Redraws everything based on fractal values if window is resized
		"""
		self._draw_everything()

	def _on_button_press(self, event: tkinter.Event) -> None:
		"""
		Makes a move in the Othello logic if a button is pressed
		"""
		self._place_tile(self._x_pos, self._y_pos)


	def _mouse_position(self, event: tkinter.Event) -> None:
		"""
		Records the mouse position
		"""
		self._x_pos = event.x
		self._y_pos = event.y

	def _place_tile(self, x: int, y: int) -> None:
		"""
		Places a tile and if it works, then it will redraw the board
		"""
		display_height = self._display.winfo_height()
		display_width = self._display.winfo_width()
		col = int(x/(display_width / self._width)) + 1
		row = int(y/(display_height / self._height)) + 1
		try:
			self._othello_game.take_turn([row, col])
			self._draw_circles(self._othello_game.game)
			self._update_score_and_turn()
			self.switch_players_or_end()
		except:
			pass

	################################ OTHELLO FUNCTIONS #############################

	def has_valid_move(self) -> bool:
		"""
		Returns true if the player has a valid move
		"""
		is_valid_move = False
		for row in range(self._othello_game.get_rows()):
			if is_valid_move:
				break

			for col in range(self._othello_game.get_cols()):

				if len(self._othello_game.placement_is_valid(row, col)) > 0: #if the move is valid
					is_valid_move = True
					break

		return is_valid_move

	def switch_players_or_end(self) -> bool:
		"""
		If there are no valid moves for the player, then switch. If none left for anyone, then end game
		"""
		if not self.has_valid_move():
			self._othello_game.change_player()
			self._update_score_and_turn()

			if not self.has_valid_move():
				self._display.unbind("<Button-1>")
				self._display_winner()

	################################ DRAWING FUNCTIONS #############################
	def _draw_everything(self) -> None:
		"""
		Redraws all the canvas objects
		"""
		self._display.delete(tkinter.ALL)

		self._draw_board()
		self._draw_circles(self._othello_game.game)

	def _draw_board(self) -> None:
		"""
		Draws the grid to place the pieces on
		"""
		display_width = self._display.winfo_width()
		display_height = self._display.winfo_height()
		
		for vertical in range(1, self._width + 1):
			self._display.create_line(
				(vertical / self._width) * display_width, 
				0,
				(vertical / self._width) * display_width, 
				display_height,
				fill = "#000000")

		for horiz in range(1, self._height + 1):
			self._display.create_line(
				0, 
				(horiz / self._height) * display_height, 
				display_width, 
				(horiz / self._height) * display_height,
				fill = "#000000")

	def _draw_circles(self, board: [[int]]) -> None:
		"""
		Draws the pieces on the board
		"""
		for row in range(self._height):
			for col in range(self._width):
				if self._othello_game.game[row][col] != 0:
					self._draw_piece(row, col, self._othello_game.game[row][col])


	def _draw_piece(self, row: int, col: int, color: int) -> None:
		"""
		Draws the peices based on the player's color
		"""
		display_width = self._display.winfo_width()
		display_height = self._display.winfo_height()
		h_padding = (display_height / self._height) / 15
		w_padding = (display_width / self._width) / 15
		row += 1
		col += 1

		if color == 2:
			filler = "white"
		elif color == 1:
			filler = "black"
		self._display.create_oval(
			(col / self._width) * display_width - (1/self._width) * display_width + w_padding,
			(row / self._height) * display_height - (1/self._height) * display_height + h_padding, 
			(col / self._width) * display_width - w_padding,
			(row / self._height) * display_height - h_padding, 
			outline = filler, fill = filler)


	############################# INITIATE PHASE 1 SETUP BOARD SETTINGS ############################

	def setup_rowcol(self) -> None:
		"""
		Creates the dropdown menus to allow the player to choose the
		amount of rows and cols, the player, and the wintpe
		"""
		self._settings_frame = tkinter.Frame(master = self._root_window)
		self._settings_frame.grid(
			row = 2, column = 0, rowspan = 2, columnspan = 5, padx = 10, pady = 10,
			sticky = tkinter.W + tkinter.E)

		self._rows_setter = tkinter.IntVar(self._settings_frame)
		self._rows_setter.set(6) # default value
		self._cols_setter = tkinter.IntVar(self._settings_frame)
		self._cols_setter.set(6)
		self._first_setter = tkinter.StringVar(self._settings_frame)
		self._first_setter.set("Black")
		self._wintype_setter = tkinter.StringVar(self._settings_frame)
		self._wintype_setter.set("Most")
		self._settings_done = tkinter.Button(self._settings_frame, text = "Done", font = 30,
			command = self._create_board)

		tkinter.Label(self._settings_frame, text = "Rows").grid(row = 0, column = 0, padx = 10, sticky = tkinter.S)
		_row_dropdown = tkinter.OptionMenu(self._settings_frame, 
			self._rows_setter, 4, 6, 8, 10, 12, 14, 16)
		_row_dropdown.grid(row = 1, column = 0,
			padx = 10, pady = 10)
		tkinter.Label(self._settings_frame, text = "Columns").grid(row = 0, column = 1, padx = 10, sticky = tkinter.S)
		_col_dropdown = tkinter.OptionMenu(self._settings_frame, 
			self._cols_setter, 4, 6, 8, 10, 12, 14, 16)
		_col_dropdown.grid(row = 1, column = 1,
			padx = 10, pady = 10)
		tkinter.Label(self._settings_frame, text = "First Player").grid(row = 0, column = 2, padx = 10, sticky = tkinter.S)
		_first_dropdown = tkinter.OptionMenu(self._settings_frame,
			self._first_setter, "Black", "White")
		_first_dropdown.grid(row = 1, column = 2,
			padx = 10, pady = 10)
		tkinter.Label(self._settings_frame, text = "Win Condition").grid(row = 0, column = 3, padx = 10, sticky = tkinter.S)
		_wintype_dropdown = tkinter.OptionMenu(self._settings_frame,
			self._wintype_setter, "Most", "Least")
		_wintype_dropdown.grid(row = 1, column = 3,
			padx = 10, pady = 10)
		self._settings_done.grid(row = 1, column = 4,
			padx = 10, pady = 10)
		self._rows_setter.trace("w", self._help_draw)
		self._cols_setter.trace("w", self._help_draw)

		for i in range(5):
			self._settings_frame.columnconfigure(i, weight = 1)

	def _help_draw(self, *args) -> None:
		"""
		Draws only the board without the pieces
		"""
		self._height = self._rows_setter.get()
		self._width = self._cols_setter.get()
		self._display.delete(tkinter.ALL)
		self._draw_board()

	def _set_first(self) -> str:
		"""
		Sets the first player based on the value of the dropdown menu
		"""
		if self._first_setter.get() == "Black":
			return "B"
		return "W"

	def _set_winstyle(self) -> str:
		"""
		Sets the winstyle based on what the user chose on the dropdown menu
		"""
		if self._wintype_setter.get() == "Most":
			return ">"
		return "<"

	def _create_board(self) -> None:
		"""
		Rebinds keys and goes on to next phase which allows player to set peices
		"""
		board = []
		for _ in range(self._height):
			board.append([0] * self._width)

		self._othello_game = othello_logic.Othello(self._rows_setter.get(), 
			self._cols_setter.get(), self._set_first(), self._set_winstyle(),
			board)

		self._display.bind("<Motion>", self._mouse_position)
		self._display.bind("<Button-1>", self._on_button_press_setup)
		self._display.bind("<Configure>", self._on_canvas_resized)
		self._settings_frame.destroy()
		self._setup_pieces()


	###################################### PHASE 2 SETUP PIECES ######################################
	def _black_pressed(self) -> None:
		"""
		Presses the button down and raises the other if user presses Black
		"""
		self._black_setup["relief"] = "sunken"
		self._white_setup["relief"] = "raised"

	def _white_pressed(self) -> None:
		"""
		Pressed the button down and raises the other if user presses White
		"""
		self._white_setup["relief"] = "sunken"
		self._black_setup["relief"] = "raised"

	def _clear_pieces_function(self) -> None:
		"""
		Function for if the user pressed the "Clear" button, clears the pieces and redraws
		"""
		for row in range(self._height):
			for col in range(self._width):
				self._othello_game.game[row][col] = 0
		self._draw_everything()

	def _setup_pieces(self) -> None:
		"""
		Sets up the frame for the user to use to choose chich pieces to set up, to clear
		the board, or to continue on to playing the game
		"""
		self._settings_frame = tkinter.Frame(master = self._root_window)
		self._settings_frame.grid(
			row = 2, column = 0, columnspan = 3, padx = 10, pady = 10,
			sticky = tkinter.W + tkinter.E)
		self._settings_frame.columnconfigure(3, weight = 1)

		self._black_setup = tkinter.Button(self._settings_frame, text = "Black", font = 30, 
			command = self._black_pressed, relief = "sunken")
		self._white_setup = tkinter.Button(self._settings_frame, text = "White", font = 30,
			command = self._white_pressed)
		self._clear_pieces = tkinter.Button(self._settings_frame, text = "Clear", font = 30,
			command = self._clear_pieces_function)
		self._settings_done = tkinter.Button(self._settings_frame, text = "Done", font = 30,
			command = self._start_game)
		self._black_setup.grid(row = 0, column = 0, padx = 10, pady = 10)
		self._white_setup.grid(row = 0, column = 1, padx = 10, pady = 10)
		self._clear_pieces.grid(row = 0, column = 2, padx = 30, pady = 10)
		self._settings_done.grid(row = 0, column = 3, padx = 10, pady = 10, sticky = tkinter.E)

	def _on_button_press_setup(self, event: tkinter.Event) -> None:
		"""
		For when the uses presses the button during the setting phase. Gets which button is
		sunken and places that piece down when mouse is clicked
		"""
		display_height = self._display.winfo_height()
		display_width = self._display.winfo_width()
		col = int(self._x_pos/(display_width / self._width))
		row = int(self._y_pos/(display_height / self._height))

		if self._black_setup["relief"] == "sunken":
			if self._othello_game.game[row][col] == 1:
				self._othello_game.game[row][col] = 0
			else:
				self._othello_game.game[row][col] = 1
		else:
			if self._othello_game.game[row][col] == 2:
				self._othello_game.game[row][col] = 0
			else:
				self._othello_game.game[row][col] = 2
		self._draw_everything()

	def _start_game(self) -> None:
		"""
		Used when the user presses the "Done" button, destroys the frame and goes onto next phase
		"""
		self._settings_frame.destroy()
		self._display.bind("<Button-1>", self._on_button_press)
		self._setup_display()
		self.switch_players_or_end()

	############################### GAME STARTED PHASE 3 #####################################
	def _setup_display(self) -> None:
		"""
		Sets up the display for the score to be displayed
		"""
		self._settings_frame = tkinter.Frame(master = self._root_window)
		self._settings_frame.grid(
			row = 2, column = 0, columnspan = 3, padx = 10, pady = 10, sticky = tkinter.W + tkinter.E)
		self._score_and_turn_display()		

	def _score_and_turn_display(self) -> None:
		"""
		Displays the black and white scores
		"""
		black_pieces, white_pieces = self._othello_game._count_pieces()
		current_player = self._othello_game.get_current_player()

		self.black_label = tkinter.Label(self._settings_frame, text = "Black: {}".format(black_pieces),
			font = 30)
		self.white_label = tkinter.Label(self._settings_frame, text = "White: {}".format(white_pieces),
			font = 30)
		self.turn_label = tkinter.Label(self._settings_frame, text = "Turn: {}".format(current_player),
			font = 30)
		self.black_label.grid(row = 0, column = 0, padx = 10, pady = 10)
		self.white_label.grid(row = 0, column = 1, padx = 10, pady = 10)
		self.turn_label.grid(row = 0, column = 2, padx = 10, pady = 10)

	def _update_score_and_turn(self) -> None:
		"""
		Updates the score when a button is pressed
		"""
		black_pieces, white_pieces = self._othello_game._count_pieces()

		self.black_label["text"] = "Black: {}".format(black_pieces)
		self.white_label["text"] = "White: {}".format(white_pieces)
		self.turn_label["text"] = "Turn: {}".format(self._othello_game.get_current_player())

	############################## WINNING WINDOW WINNERS ONLY ###############################

	def _display_winner(self) -> None:
		"""
		Displays the winner of the game
		"""
		self.turn_label.destroy()
		winner_label = tkinter.Label(self._settings_frame, 
			text = "WINNER: {}!".format(self._othello_game.find_winner()), font = 30)
		winner_label.grid(row = 0, column = 2, padx = 10, pady = 10)



if __name__ == "__main__":
	test = othello_GUI()
	test.run_game()
