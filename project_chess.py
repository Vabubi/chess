# This program simulates a simplified chess scenario.
# It allows the user to place a white 'king' or 'queen' on the board,
# add black pieces, and then determines which black pieces the white piece can capture.

while True:
    # Prompt the user to choose a white piece and its position
    print("You can choose between 'king' or 'queen' for the white piece.")

    # Loop until the user provides valid input for the white piece
    while True:
        white_piece_input = input("Enter the white piece and its position (e.g., 'king e3'): ")
        split_input = white_piece_input.split(maxsplit=1)

        if len(split_input) != 2:
            print("Invalid input. Please enter the piece and coordinates in the format 'Piece LetterNumber'.")
            continue

        white_piece, white_position = split_input
        white_piece = white_piece.lower()
        white_position = white_position.lower()

        if white_piece not in ['king', 'queen']:
            print("Invalid white piece. Please choose from 'king' or 'queen'.")
            continue

        if (
            len(white_position) == 2 and
            white_position[0] in 'abcdefgh' and
            white_position[1] in '12345678'
        ):
            print("Input confirmed.")
            break
        else:
            print("Invalid position format. Please enter a valid position (e.g., 'e3').")

    # Initialize an empty 8x8 chess board represented as a 2D list
    board = [[' ' for _ in range(8)] for _ in range(8)]

    # Function to add a piece to the board
    def add_piece_to_board(piece, position, board, color):
        row = 8 - int(position[1])
        col = ord(position[0]) - ord('a')

        if board[row][col] == ' ':
            board[row][col] = color + piece[0].upper()
            print(f"Successfully added the {color} {piece.capitalize()} at position {position.upper()} to the board.")
        else:
            print(f"Cannot add the {color} {piece.capitalize()} at position {position.upper()}. Square is already occupied.")

    # Add the white piece to the board
    add_piece_to_board(white_piece, white_position, board, 'W')

    # Function to print the current state of the board
    def print_board(board):
        print("   A   B   C   D   E   F   G   H")
        print("  ---------------------------------")
        for i, row in enumerate(board, 1):
            row_str = ' | '.join(row)
            print(f"{9 - i} | {row_str} | {9 - i}")
            print("  ---------------------------------")
        print("   A   B   C   D   E   F   G   H")

    # Print the board after adding the white piece
    print_board(board)

    # Define the allowed quantities of each black piece type
    black_piece_quantities = {
        'pawn': 8,
        'bishop': 2,
        'knight': 2,
        'rook': 2,
        'queen': 1,
        'king': 1
    }

    # Counter to keep track of how many black pieces have been added
    black_pieces_added = 0

    # Loop to allow the user to add black pieces
    while black_pieces_added < 16:
        black_piece_input = input("Enter the black piece and its position (e.g., 'pawn e4', or type 'done' to finish): ")

        if black_piece_input.lower() == 'done':
            if black_pieces_added == 0:
                print("No black pieces added. Please add at least one black piece before finishing.")
                continue
            else:
                break

        split_input = black_piece_input.split(maxsplit=1)
        if len(split_input) != 2:
            print("Invalid input. Please enter the piece and coordinates in the format 'Piece LetterNumber'.")
            continue

        black_piece, black_position = split_input
        black_piece = black_piece.lower()
        black_position = black_position.lower()

        if black_piece not in black_piece_quantities:
            print("Invalid black piece. Please choose from: 'pawn', 'bishop', 'knight', 'rook', 'queen', 'king'.")
            continue

        if (
            len(black_position) == 2 and
            black_position[0] in 'abcdefgh' and
            black_position[1] in '12345678'
        ):
            add_piece_to_board(black_piece, black_position, board, 'B')
            black_pieces_added += 1
            print_board(board)
        else:
            print("Invalid position format. Please enter a valid position (e.g., 'e3').")

    # Function to determine which black pieces the white piece can capture
    def get_piece_captures(white_piece, white_position, board):
        captures = []
        row = 8 - int(white_position[1])
        col = ord(white_position[0]) - ord('a')

        if white_piece == 'king':
            directions = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1),          (0, 1),
                (1, -1),  (1, 0),  (1, 1)
            ]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8 and board[r][c].startswith('B'):
                    capture_position = chr(c + ord('a')) + str(8 - r)
                    captures.append((board[r][c], capture_position))

        elif white_piece == 'queen':
            directions = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1),          (0, 1),
                (1, -1),  (1, 0),  (1, 1)
            ]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                while 0 <= r < 8 and 0 <= c < 8:
                    if board[r][c] != ' ':
                        if board[r][c].startswith('B'):
                            capture_position = chr(c + ord('a')) + str(8 - r)
                            captures.append((board[r][c], capture_position))
                        break
                    r += dr
                    c += dc

        return captures

    # Get the list of black pieces that the white piece can capture
    captures = get_piece_captures(white_piece, white_position, board)

    # Print out the result
    if captures:
        print(f"The W {white_piece.capitalize()} can capture the following pieces:")
        for captured_piece, capture_position in captures:
            print(f"- {captured_piece} at {capture_position.upper()}")
    else:
        print(f"The W {white_piece.capitalize()} cannot capture any black pieces.")

    # Ask if the user wants to run the simulation again
    again = input("\nRun simulation again? (y/n): ").lower()
    if again not in ('y', 'yes'):
        print("Goodbye!")
        break
