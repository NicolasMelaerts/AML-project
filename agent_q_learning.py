import numpy as np
import random
from chess_board import ChessBoard

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.alpha = alpha  # Taux d'apprentissage
        self.gamma = gamma  # Facteur de discount
        self.epsilon = epsilon  # Taux d'exploration
        self.Q = {}  # Table Q

    # Retourne la valeur Q d'un état et d'une action donnés
    def get_q_value(self, state, action):
        return self.Q.get(state, {}).get(action, 0)

    # Choisir une action selon une politique d'exploration/exploitation
    def choose_action(self, state, possible_actions):
        if np.random.rand() < self.epsilon:
            return random.choice(possible_actions)  # Exploration
        else:
            if state not in self.Q:
                self.Q[state] = {action: 0 for action in possible_actions}
            return max(possible_actions, key=lambda action: self.Q[state].get(action, 0))

    # Met à jour la table Q en utilisant la formule de Q-learning
    def update_q(self, state, action, reward, next_state, possible_actions):
        best_next_action = max(possible_actions, key=lambda action: self.Q.get(next_state, {}).get(action, 0))
        current_q = self.Q.get(state, {}).get(action, 0)
        future_q = reward + self.gamma * self.Q.get(next_state, {}).get(best_next_action, 0)
        self.Q.setdefault(state, {})[action] = current_q + self.alpha * (future_q - current_q)

    # Retourne le meilleur coup à partir de la Q-table pour un état donné
    def get_best_move(self, state, possible_actions):
        if state not in self.Q:  # Si l'état n'a pas encore d'entrée dans la Q-table
            self.Q[state] = {action: 0 for action in possible_actions}  # Initialiser la Q-table pour cet état avec des Q-values à 0
        return max(possible_actions, key=lambda action: self.Q[state].get(action, 0))
    
    # Entraînement de l'agent sur un certain nombre d'épisodes sur un plateau fen
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