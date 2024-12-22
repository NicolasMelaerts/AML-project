import numpy as np
import random
from sklearn.linear_model import LinearRegression
from chess_board import ChessBoard

class ApproximateQLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        """Initialisation des paramètres du Q-learning approximatif."""
        self.alpha = alpha  # Taux d'apprentissage
        self.gamma = gamma  # Facteur de discount
        self.epsilon = epsilon  # Taux d'exploration
        self.model = LinearRegression()  # Régression linéaire pour l'approximation des valeurs Q
        self.X = []  # Listes pour stocker les caractéristiques des états-action
        self.y = []  # Liste pour stocker les valeurs Q correspondantes

    # Retourne la valeur Q estimée pour un état et une action donnés à l'aide du modèle approximatif
    def get_q_value(self, state, action):
        features = self.extract_features(state, action)
        return self.model.predict([features])[0] if self.X else 0

    # Choisir une action selon une politique d'exploration/exploitation
    def choose_action(self, state, possible_actions):
        if np.random.rand() < self.epsilon:
            return random.choice(possible_actions)  # Exploration
        else:
            q_values = [self.get_q_value(state, action) for action in possible_actions]
            max_q = max(q_values)
            best_actions = [action for action, q in zip(possible_actions, q_values) if q == max_q]
            return random.choice(best_actions)  # Si plusieurs actions ont la même Q-value, on choisit aléatoirement

    # Extraire des caractéristiques simples à partir de l'état et de l'action
    def extract_features(self, state, action):
            board = ChessBoard(state)
            
            # Récupérer les positions de toutes les pièces
            piece_positions = board.get_piece_positions()

            # Extraire quelques caractéristiques intéressantes, par exemple :
            # - Position des rois
            white_king_pos = piece_positions.get('K', [])[0]  # Première position du roi blanc
            black_king_pos = piece_positions.get('k', [])[0]  # Première position du roi noir
            
            # - Nombre de pions sur le plateau
            white_pawns = len(piece_positions.get('P', []))
            black_pawns = len(piece_positions.get('p', []))
            
            # - Distance entre les rois
            king_distance = abs(white_king_pos[0] - black_king_pos[0]) + abs(white_king_pos[1] - black_king_pos[1])

            # Retourner les caractéristiques sous forme de liste
            features = [
                white_king_pos[0], white_king_pos[1],  # Position du roi blanc (x, y)
                black_king_pos[0], black_king_pos[1],  # Position du roi noir (x, y)
                white_pawns, black_pawns,  # Nombre de pions blancs et noirs
                king_distance  # Distance entre les rois
            ]
            return features

    # Met à jour le modèle de Q-learning approximatif
    def update_q(self, state, action, reward, next_state, possible_actions):
        best_next_action = max(possible_actions, key=lambda action: self.get_q_value(next_state, action))
        future_q = reward + self.gamma * self.get_q_value(next_state, best_next_action)
        
        # Calculer la différence entre la Q-value prédite et la nouvelle valeur cible
        features = self.extract_features(state, action)
        self.X.append(features)
        self.y.append(future_q)

        # Recalibrer le modèle (en réajustant les poids à chaque fois)
        if len(self.X) > 0:
            self.model.fit(self.X, self.y)  # Entraînement du modèle avec les données collectées

    # Retourne le meilleur coup en utilisant l'approximation de la Q-table
    def get_best_move(self, state, possible_actions):
        q_values = [self.get_q_value(state, action) for action in possible_actions]
        max_q = max(q_values)
        best_actions = [action for action, q in zip(possible_actions, q_values) if q == max_q]
        return random.choice(best_actions)  # Si plusieurs actions ont la même Q-value, on choisit aléatoirement

    # Entraînement de l'agent avec un certain nombre d'épisodes sur un plateau fen
    def train(self, episodes, fen_string):

        # Si la table Q possède déjà des valeurs pour cet état, jouer le meilleur coup
        test_still_mat_in_Q = ChessBoard(fen_string)
        action = self.get_best_move(fen_string, test_still_mat_in_Q.get_possible_moves())
        test_still_mat_in_Q.apply_move(action)

        if not test_still_mat_in_Q.is_game_over():
            for episode in range(episodes):
                state = fen_string
                board = ChessBoard(fen_string)
                done = False
                position_history = set()

                while not done:
                    possible_actions = [move for move in board.get_possible_moves()]
                    best_move = self.choose_action(state, possible_actions)
                    board.apply_move(best_move)

                    # Vérifier la répétition de positions
                    position_hash = hash(board.get_fen())
                    if position_hash in position_history:
                        reward = -10  # Pénalité pour répétition
                        break  # Sortir de la boucle
                    position_history.add(position_hash)

                    next_state = board.get_fen()
                    reward = -1

                    # Vérifier si la partie est terminée
                    if board.get_is_fifty_moves():
                        reward = -50  # Pénalité pour la règle des 50 coups
                        done = True
                    elif board.is_game_over():
                        reward = 100  # Récompense positive pour la victoire
                        done = True

                    self.update_q(state, best_move, reward, next_state, possible_actions)
                    state = next_state

                # Décrémenter epsilon pour favoriser l'exploitation au fil des épisodes
                self.epsilon = max(0.01, self.epsilon * 0.995)
