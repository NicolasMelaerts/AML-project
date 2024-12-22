import chess
import matplotlib.pyplot as plt
import numpy as np
from chess import Move
import random


class ChessBoard:
    def __init__(self, fen_board):
        self.board = chess.Board(fen_board)
    
    def display(self):
        # Créer un tableau de 8x8 pour le plateau
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Créer une grille (8x8) avec des couleurs alternées (noir et blanc)
        colors = np.array([[[240/255, 217/255, 181/255], [181/255, 136/255, 99/255]] * 4,
                        [[181/255, 136/255, 99/255], [240/255, 217/255, 181/255]] * 4] * 4)
        
        ax.imshow(colors, extent=[0, 8, 0, 8])

        # Placer les pièces sur le plateau
        for square, piece in self.board.piece_map().items():
            row, col = divmod(square, 8)
            piece_symbol = self.piece_to_symbol(piece)
            color = 'black' if piece.color == chess.BLACK else 'white'
            ax.text(col + 0.5, 7.5 - row, piece_symbol, fontsize=25, ha='center', va='center', color=color)

        # Vérifier si la partie est finie par échec et mat
        if self.board.is_game_over():
            ax.text(4, 4, "Échec et mat!", fontsize=30, ha='center', va='center', color='red', fontweight='bold')

        # Retirer les lignes de la grille
        ax.set_xticks([])
        ax.set_yticks([])

        # Afficher l'image
        plt.show()


    def piece_to_symbol(self, piece):
        # Convertir une pièce en son symbole (notation FEN)
        symbol_map = {
            chess.PAWN: 'P', chess.KNIGHT: 'N', chess.BISHOP: 'B', chess.ROOK: 'R', chess.QUEEN: 'Q', chess.KING: 'K'
        }
        symbol = symbol_map.get(piece.piece_type, '')
        return symbol.lower() if piece.color == chess.BLACK else symbol

    def get_possible_moves(self):
        # Retourner les mouvements possibles pour le joueur
        return list(self.board.legal_moves)

    def apply_move(self, move):
        # Appliquer un mouvement sur le plateau
        self.board.push(move)

    def is_game_over(self):
        # Vérifier si la partie est terminée
        return self.board.is_game_over()
    
    def is_check_mate(self):
        # Vérifier si la partie est terminée par échec et mat
        return self.board.is_checkmate()

    def play_move(self, move):
        # Appliquer un mouvement sur le plateau
        self.board.push(Move.from_uci(move))
    
    def play_random_move(self):
        # Jouer un mouvement aléatoire parmis les mouvements possibles
        legal_moves = list(self.board.legal_moves)
        
        if legal_moves:
            move = random.choice(legal_moves)
            self.board.push(move)

    def get_fen(self):
        # Retourner l'état actuel du plateau sous forme de FEN
        return self.board.fen()
    
    def get_total_moves(self):
        # retourne le nombre total de mouvements joués
        return self.board.fullmove_number
    
    def get_halfmove_clock(self):
        # Retourne le nombre de demi-coups (halfmove clock) depuis le dernier mouvement de pion ou capture
        return self.board.halfmove_clock

    def get_is_fifty_moves(self):
        return self.get_halfmove_clock() >= 50
    
    def get_piece_positions(self):
        # Retourner les positions de chaque pièce sur le plateau
        piece_positions = {}
        
        for square, piece in self.board.piece_map().items():
            row, col = divmod(square, 8)
            piece_symbol = self.piece_to_symbol(piece)
            
            # Ajouter la position de la pièce à la liste correspondante
            if piece_symbol not in piece_positions:
                piece_positions[piece_symbol] = []
            piece_positions[piece_symbol].append((row, col))
        
        return piece_positions
