import random
import chess

class ChessBoardGenerator:
    def __init__(self, allowed_pieces=None):
        self.allowed_pieces = allowed_pieces or [
            (chess.KING, chess.WHITE), (chess.KING, chess.BLACK),
            (chess.QUEEN, chess.WHITE)
        ]

    #Génère un plateau permettant un mat en un coup (mate_in_one)
    def generate_winnable_position(self, mate_in_one=True):
        while True:
            board = chess.Board()
            board.clear()

            # Placer le roi noir à une position aléatoire
            black_king_pos = random.randint(0, 63)
            board.set_piece_at(black_king_pos, chess.Piece(chess.KING, chess.BLACK))

            # Placer le roi blanc à une position légale (non adjacente au roi noir)
            white_king_pos = random.choice([pos for pos in range(64) if not self.are_kings_adjacent(pos, black_king_pos)])
            board.set_piece_at(white_king_pos, chess.Piece(chess.KING, chess.WHITE))

            # Placer la dame blanche sur une position aléatoire (ni sur le roi blanc ni sur le roi noir)
            white_queen_pos = random.choice([pos for pos in range(64) if pos not in {black_king_pos, white_king_pos}])
            board.set_piece_at(white_queen_pos, chess.Piece(chess.QUEEN, chess.WHITE))

            # Vérifier si la position est valide (aucun roi en échec ou illégal)
            if not board.is_valid():
                continue

            # Vérifier si les conditions de mat sont remplies pour ce plateau
            if mate_in_one and self.is_mate_in_one(board):
                return board

    # Génère un plateau aléatoire avec les pièces autorisées
    def generate_random_position(self):
        board = chess.Board()
        board.clear()

        # Parcours de toutes les pièces autorisées et placement sur des cases vides
        for piece_type, color in self.allowed_pieces:
            square = random.choice([sq for sq in range(64) if board.piece_at(sq) is None])
            board.set_piece_at(square, chess.Piece(piece_type, color))

        # Valider qu'il n'y a pas déjà un mat ou que la partie ne soit pas déjà terminée
        if not board.is_valid() or board.is_checkmate() or board.is_game_over():
            return self.generate_random_position()  # Recommence si le plateau initial est invalide

        return board

    # Vérifie si deux cases sont adjacentes
    def are_kings_adjacent(self, pos1, pos2):
        row1, col1 = divmod(pos1, 8)
        row2, col2 = divmod(pos2, 8)
        return abs(row1 - row2) <= 1 and abs(col1 - col2) <= 1

    # Vérifie si un échec et mat est possible en un coup
    def is_mate_in_one(self, board):
        # si le plateau est déjà un échec et mat
        if board.is_checkmate():
            return False
        
        # Parcours de tous les mouvements et voir si un échec et mat est possible
        for move in board.legal_moves:
            temp_board = board.copy()
            temp_board.push(move)
            if temp_board.is_checkmate():
                return True
            
        return False

    # Vérifie si un mouvement donné mène à un échec et mat
    def is_checkmate_after_one_move(self, board, move):
        temp_board = board.copy()
        temp_board.push(move)
        return temp_board.is_checkmate()

    # Génère une base de données de plateaux et les enregistre dans un fichier texte
    def generate_database(self, num_positions, file_name, mode="mate_in_one"):
        with open(file_name, 'w') as file:
            for _ in range(num_positions):
                if mode == "mate_in_one":
                    board = self.generate_winnable_position(mate_in_one=True)
                elif mode == "random":
                    board = self.generate_random_position()
                else:
                    raise ValueError("Mode invalide. Utilisez 'mate_in_one' ou 'random'.")
                board_fen = board.board_fen() + " w - - 0 1"  # Ajouter la partie manquante du FEN
                file.write(board_fen + '\n')  # Sauvegarde les positions en FEN


def main():
    # Génération des plateaux pour les parties simple avec 3 pièces 
    allowed_pieces = [
        (chess.KING, chess.WHITE), (chess.KING, chess.BLACK),
        (chess.QUEEN, chess.WHITE)
    ]
    generator_simple = ChessBoardGenerator(allowed_pieces=allowed_pieces)

    generator_simple.generate_database(20, 'mate_in_one_positions_3_pieces.txt', mode="mate_in_one")
    generator_simple.generate_database(20, 'random_positions_3_pieces.txt', mode="random")


    allowed_pieces = [
        (chess.KING, chess.WHITE), (chess.KING, chess.BLACK),
        (chess.QUEEN, chess.WHITE), (chess.PAWN, chess.BLACK), (chess.PAWN, chess.BLACK), (chess.PAWN, chess.BLACK)
    ]
    generator_6_pieces = ChessBoardGenerator(allowed_pieces=allowed_pieces)

    generator_6_pieces.generate_database(20, 'random_positions_6_pieces.txt', mode="random")


if __name__ == '__main__':
    main()