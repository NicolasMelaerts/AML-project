import numpy as np
from board import ChessBoard

# Initialisation de la table Q
Q = {}

def get_q_value(state, action):
    return Q.get(state, {}).get(action, 0)

# Fonction pour obtenir un indice d'état à partir du plateau (simplification)
def get_state_index(board: ChessBoard):
    # Utiliser la FEN (notation échiquéenne) comme index d'état
    return board.board.fen()

# Choisir une action basée sur l'exploration ou l'exploitation
def choose_action(state, possible_actions, epsilon=0.1):
    if np.random.rand() < epsilon:
        return np.random.choice(possible_actions)  # Exploration
    else:
        # Exploitation : choisir l'action avec la meilleure valeur dans la table Q
        if state not in Q:
            Q[state] = {action: 0 for action in possible_actions}
        return max(possible_actions, key=lambda action: Q[state].get(action, 0))

# Exemple de mise à jour de la Q-table avec des clés appropriées
def update_q(state, action, reward, next_state, possible_actions, alpha, gamma):
    best_next_action = max(possible_actions, key=lambda action: Q.get(next_state, {}).get(action, 0))
    
    # Utiliser une clé pour action (par exemple, une chaîne ou un indice)
    current_q = Q.get(state, {}).get(action, 0)
    future_q = reward + gamma * Q.get(next_state, {}).get(best_next_action, 0)
    
    Q.setdefault(state, {})[action] = current_q + alpha * (future_q - current_q)

def get_best_move(state, possible_actions):
    """Retourne le meilleur coup à partir de la Q-table pour un état donné."""
    if state not in Q:  # Si l'état n'a pas encore d'entrée dans la Q-table
        Q[state] = {action: 0 for action in possible_actions}  # Initialiser la Q-table pour cet état avec des Q-values à 0

    # Choisir l'action avec la plus haute Q-value pour l'état donné
    best_action = max(possible_actions, key=lambda action: Q[state].get(action, 0))
    
    return best_action

