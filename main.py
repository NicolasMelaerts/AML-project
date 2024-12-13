from board import ChessBoard
from q_learning import update_q, get_state_index, get_best_move
import time
from chess import Move
import random
from chess_board_generator import ChessBoardGenerator

generator = ChessBoardGenerator()
positions = generator.generate_database(1)
RANDOM_BOARD = positions[0]  # plateau aléatoire

# Initialisation du jeu et des paramètres de Q-learning
board = ChessBoard(RANDOM_BOARD)  # Création du plateau à l'extérieur de la boucle
episodes = 1000
epsilon = 0.1  # Taux d'exploration
alpha = 0.1  # Taux d'apprentissage
gamma = 0.9  # Facteur de discount

def train_q_learning(episodes):
    for episode in range(episodes):
        print(f"\n=== Épisode {episode + 1} ===")
        
        # Réinitialisation du jeu à chaque épisode
        board = ChessBoard(RANDOM_BOARD)  # Réinitialisation du plateau de jeu
        state = get_state_index(board)

        done = False
        while not done:
            print("\nÉtat actuel du plateau:")
            #board.display()  # Afficher le plateau à chaque étape
            possible_actions = list(board.get_possible_moves())
            
            print("Actions possibles:", possible_actions)
            
            # Obtenez le meilleur coup à partir de la Q-table
            best_move = get_best_move(state, possible_actions)
            print(f"Meilleur coup choisi: {best_move}")
            
            # Appliquer le mouvement
            board.apply_move(best_move)
            print(f"Mouvement appliqué: {best_move}")
            
            # Calculer le prochain état et la récompense
            next_state = get_state_index(board)
            reward = -1  # Exemple de récompense, à ajuster selon votre logique
            if board.is_game_over():
                reward = 100  # Récompense lorsque la partie est terminée
                print("La partie est terminée! Récompense obtenue:", reward)
            
            # Mise à jour des Q-values
            update_q(state, best_move, reward, next_state, possible_actions, alpha, gamma)
            print(f"Q-table mise à jour pour l'état {state} et l'action {best_move}")
            
            state = next_state

            # Critère de fin d'épisode (si la partie est terminée)
            done = board.is_game_over()
            
            # Attente avant la prochaine action pour que l'utilisateur puisse observer
            #time.sleep(1)  # Pause de 1 seconde (ajustez selon votre besoin)

        print(f"Fin de l'épisode {episode + 1}")

# Démarrer l'entraînement
train_q_learning(episodes)

# Après l'entraînement, afficher le meilleur coup à jouer (test)
print("---- Après l'entraînement ----")
# Boucle de jeu avec l'agent et l'utilisateur
done = False
while not done:
    print("\nÉtat actuel du plateau:")
    possible_actions = list(board.get_possible_moves())
    
    print(f"Actions possibles: {possible_actions}")
    best_move = get_best_move(get_state_index(board), possible_actions)
    print(f"Meilleur coup de l'agent: {best_move}")
    
    board.display()  # Afficher l'état du plateau

    board.apply_move(best_move)
    possible_actions = list(board.get_possible_moves())

    board.display()

    done = board.is_game_over()
    if not done : 
        user_move_input = random.choices(possible_actions)[0]
        board.apply_move(user_move_input)  # Appliquer le coup de l'utilisateur
        board.display()
    