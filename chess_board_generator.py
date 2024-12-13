import random
import chess

class ChessBoardGenerator:
    def __init__(self):
        pass

    def generate_winnable_position(self):
        """Génère un plateau où un joueur peut gagner en un coup (échec et mat possible)."""
        while True:
            board = chess.Board()
            board.clear()  # Efface toutes les pièces du plateau

            # Placer le roi noir à une position aléatoire
            black_king_pos = random.randint(0, 63)
            board.set_piece_at(black_king_pos, chess.Piece(chess.KING, chess.BLACK))

            # Placer le roi blanc à une position légale (non adjacente au roi noir)
            white_king_pos = random.choice([pos for pos in range(64)
                                            if not self.are_kings_adjacent(pos, black_king_pos)])
            board.set_piece_at(white_king_pos, chess.Piece(chess.KING, chess.WHITE))

            # Placer la dame blanche à une position aléatoire
            white_queen_pos = random.choice([pos for pos in range(64)
                                             if pos != white_king_pos and pos != black_king_pos])
            board.set_piece_at(white_queen_pos, chess.Piece(chess.QUEEN, chess.WHITE))

            # Vérifier si le plateau correspond à une situation de mat en un coup
            if self.is_mate_in_one(board) and not board.is_attacked_by(chess.WHITE, black_king_pos):
                return board

    def are_kings_adjacent(self, pos1, pos2):
        """Vérifie si deux cases sont adjacentes."""
        row1, col1 = divmod(pos1, 8)
        row2, col2 = divmod(pos2, 8)
        return abs(row1 - row2) <= 1 and abs(col1 - col2) <= 1

    def is_mate_in_one(self, board):
        """Vérifie si un échec et mat est possible en un coup."""
        for move in board.legal_moves:
            temp_board = board.copy()
            temp_board.push(move)
            if temp_board.is_checkmate():
                return True
        return False

    def generate_database(self, num_positions):
        """Génère une base de données de plateaux gagnables."""
        positions = []
        for _ in range(num_positions):
            positions.append(self.generate_winnable_position())
        return positions


def main():
    # Générer une base de données de plateaux
    generator = ChessBoardGenerator()
    positions = generator.generate_database(10)

    # Afficher les plateaux générés
    for idx, board in enumerate(positions):
        print(f"Position {idx + 1}:")
        print(board)  # Affiche le plateau en notation FEN
        print(board.board_fen())  # Affiche la position
        print("-" * 30)


if __name__ == '__main__':
    main()