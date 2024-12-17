import numpy as np
import random
import chess

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        # Initialisation des paramètres du Q-learning
        self.alpha = alpha  # Taux d'apprentissage
        self.gamma = gamma  # Facteur de discount
        self.epsilon = epsilon  # Taux d'exploration
        self.Q = {}  # Table Q

    def get_q_value(self, state, action):
        """Retourne la valeur Q d'un état et d'une action donnés."""
        return self.Q.get(state, {}).get(action, 0)

    def choose_action(self, state, possible_actions):
        """Choisir une action selon une politique d'exploration/exploitation."""
        if np.random.rand() < self.epsilon:
            return random.choice(possible_actions)  # Exploration
        else:
            if state not in self.Q:
                self.Q[state] = {action: 0 for action in possible_actions}
            return max(possible_actions, key=lambda action: self.Q[state].get(action, 0))

    def update_q(self, state, action, reward, next_state, possible_actions):
        """Met à jour la table Q en utilisant la formule de Q-learning."""
        best_next_action = max(possible_actions, key=lambda action: self.Q.get(next_state, {}).get(action, 0))
        current_q = self.Q.get(state, {}).get(action, 0)
        future_q = reward + self.gamma * self.Q.get(next_state, {}).get(best_next_action, 0)
        self.Q.setdefault(state, {})[action] = current_q + self.alpha * (future_q - current_q)

    def get_best_move(self, state, possible_actions):
        """Retourne le meilleur coup à partir de la Q-table pour un état donné."""
        if state not in self.Q:  # Si l'état n'a pas encore d'entrée dans la Q-table
            self.Q[state] = {action: 0 for action in possible_actions}  # Initialiser la Q-table pour cet état avec des Q-values à 0
        return max(possible_actions, key=lambda action: self.Q[state].get(action, 0))

    def train(self, episodes, fen_string, max_moves=100):
        """Entraînement de l'agent sur un certain nombre d'épisodes."""
        for episode in range(episodes):
            state = fen_string
            board = chess.Board(fen_string)
            done = False
            move_count = 0
            position_history = set()

            while not done and move_count < max_moves:
                move_count += 1
                possible_actions = [move for move in board.legal_moves]
                best_move = self.choose_action(state, possible_actions)
                board.push(best_move)

                # Vérifier la répétition de positions
                position_hash = hash(board.fen())
                if position_hash in position_history:
                    reward = -10  # Pénalité pour répétition
                    break  # Sortir de la boucle
                position_history.add(position_hash)

                next_state = board.fen()
                reward = -1
                if board.is_game_over():
                    reward = 100
                    done = True

                self.update_q(state, best_move, reward, next_state, possible_actions)
                state = next_state

            # Pénaliser si max_moves est atteint sans fin de partie
            if move_count >= max_moves and not board.is_game_over():
                reward = -20


    def clear(self):
        """Réinitialiser la table Q et les autres paramètres si nécessaire."""
        self.Q = {}  # Vider la table Q

    # Getter de Q
    def get_q(self):
        """Retourne l'ensemble complet de la Q-table."""
        return self.Q

    def set_q(self, q):
        """Modifie l'ensemble complet de la Q-table."""
        self.Q = q