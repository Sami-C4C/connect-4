import numpy as np
import pygame
import sys
import math

GRAY = (66, 69, 73)  # Define gray color for the board cells
BLACK = (30, 33, 36)  # Define black color for empty cells and the top bar
GREEN = (63, 255, 0)  # Define green color for Player 1's pieces
BLUE = (0, 191, 255)  # Define blue color for Player 2's pieces

BOARD_ROWS = 7  # Set the number of rows in the game board
BOARD_COLUMNS = 8  # Set the number of columns in the game board


def create_game_board():  # create the game board using NumPy zeros
    board = np.zeros((BOARD_ROWS, BOARD_COLUMNS))
    return board


def drop_piece(board, row, col, piece):  # drop a piece into a specified location
    board[row][col] = piece


def is_valid_location(board, col):  # Function to check if a location is valid for dropping a piece
    return board[BOARD_ROWS - 1][col] == 0


def get_next_open_row(board, col):  # Function to find the next open row in a given column
    for r in range(BOARD_ROWS):
        if board[r][col] == 0:
            return r


def print_board(board):  # Function to print the game board to the console
    print(np.flip(board, 0))


def winning_move(board, piece):  # Function to check if there is a winning move for a given piece

    # Checking the horizontal locations for win
    for c in range(BOARD_COLUMNS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Checking the vertical locations for win
    for c in range(BOARD_COLUMNS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Checking the positively sloped diagonals
    for c in range(BOARD_COLUMNS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Checking the negatively sloped diagonals
    for c in range(BOARD_COLUMNS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def draw_board(board):  # Function to draw the game board using Pygame
    for c in range(BOARD_COLUMNS):
        for r in range(BOARD_ROWS):
            # Draw gray rectangles for the board
            pygame.draw.rect(screen, GRAY, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            # Draw black circles to represent empty cells
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(BOARD_COLUMNS):  # Iterate through all columns
        for r in range(BOARD_ROWS):  # Iterate through all rows
            if board[r][c] == 1:  # If Player 1 has a piece in this position
                pygame.draw.circle(screen, GREEN, (  # Draw a green circle for Player 1's piece
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:  # If Player 2 has a piece in this position
                pygame.draw.circle(screen, BLUE, (  # Draw a blue circle for Player 2's piece
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()  # Update the display


board = create_game_board()  # Create the initial game board
print_board(board)  # Print the initial game board to the console
game_over = False  # Initialize game_over flag as False
turn = 0  # Initialize turn counter

pygame.display.set_caption("Connect-4")  # set the title to "Connect 4"
pygame.init()  # Initialize Pygame

SQUARESIZE = 90  # Set the size of each square in the board

width = BOARD_COLUMNS * SQUARESIZE  # Calculate the width of the game window
height = (BOARD_ROWS + 1) * SQUARESIZE  # Calculate the height of the game window

size = (width, height)  # Set the size of the game window

RADIUS = int(SQUARESIZE / 2 - 5)  # Calculate the radius of the pieces

screen = pygame.display.set_mode(size)  # Create the game window
draw_board(board)  # Draw the initial game board
pygame.display.update()  # Update the display

selected_font = pygame.font.SysFont("Arial", 60)  # Set the font for the game over text

while not game_over:

    for event in pygame.event.get():  # Iterate through Pygame events
        if event.type == pygame.QUIT:  # If the QUIT event is triggered
            sys.exit()  # Exit the game

        if event.type == pygame.MOUSEMOTION:  # If the mouse is moved
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))  # Draw a black rectangle on the top bar
            pos_x = event.pos[0]  # Get the x-coordinate of the mouse position
            if turn == 0:  # If it's Player 1's turn
                pygame.draw.circle(screen, GREEN, (pos_x, int(SQUARESIZE / 2)), RADIUS)  # Draw a green circle
            else:  # If it's Player 2's turn
                pygame.draw.circle(screen, BLUE, (pos_x, int(SQUARESIZE / 2)), RADIUS)  # Draw a blue circle
        pygame.display.update()  # Update the display

        if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse button is clicked
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))  # Draw a black rectangle on the top bar

            # Asking for Player 1 Input
            if turn == 0:
                pos_x = event.pos[0]  # Get the x-coordinate of the mouse position
                col = int(math.floor(pos_x / SQUARESIZE))  # Calculate the column where the piece should be dropped

                if is_valid_location(board, col):  # Checking if the location is valid
                    row = get_next_open_row(board, col)  # Find the next open row
                    drop_piece(board, row, col, 1)  # Drop Player 1's piece

                    if winning_move(board, 1):  # Checking if Player 1 has won
                        label = selected_font.render("1st Player won!!", 1,
                                                     GREEN)  # Create a label to display the win message
                        screen.blit(label, (40, 10))  # Display the win message
                        game_over = True  # Set game_over flag to True


            # Asking for Player 2 Input
            else:
                pos_x = event.pos[0]  # Get the x-coordinate of the mouse position
                col = int(math.floor(pos_x / SQUARESIZE))  # Calculate the column where the piece should be dropped

                if is_valid_location(board, col):  # Checking if the location is valid
                    row = get_next_open_row(board, col)  # Find the next open row
                    drop_piece(board, row, col, 2)  # Drop Player 2's piece

                    if winning_move(board, 2):  # Checking if Player 2 has won
                        label = selected_font.render("2nd Player won!!", 1,
                                                     BLUE)  # Create a label to display the win message
                        screen.blit(label, (40, 10))  # Display the win message
                        game_over = True  # Set game_over flag to True

            print_board(board)  # Print the updated board to the console
            draw_board(board)  # Draw the updated board on the screen

            turn += 1  # Increment the turn counter
            turn = turn % 2  # Alternate between players (0 for Player 1, 1 for Player 2)

            if game_over:  # If the game is over
                pygame.time.wait(4000)  # Wait for 4 seconds before closing the game
