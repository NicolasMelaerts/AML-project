from Board import ChessBoard
from chess_board_generator import ChessBoardGenerator
import chess

def load_positions_from_file(file_name):
    """Lit un fichier texte contenant des positions FEN et renvoie les chaînes FEN."""
    fen_strings = []
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()  # Retire les espaces blancs en début/fin de ligne
            if line:
                fen_strings.append(line)  # Ajoute la chaîne FEN à la liste
    return fen_strings
