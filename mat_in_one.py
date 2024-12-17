import matplotlib.pyplot as plt
from Board import ChessBoard
from q_learning import QLearningAgent
from chess_board_generator import ChessBoardGenerator
from chess_board_loader import load_positions_from_file
import random
import chess

# Générateur de positions de mat en un
generator = ChessBoardGenerator()
# generator.generate_database(50, 'mate_in_two_positions.txt', mode="mate_in_two")
all_fen = load_positions_from_file('random_positions.txt')

# Liste des différentes configurations d'agents
# Définition des trois agents avec différents paramètres de Q-learning
agents = [
    QLearningAgent(alpha=0.3, gamma=0.7, epsilon=0.5),  # Agent 1 : fort taux d'exploration
    QLearningAgent(alpha=0.1, gamma=0.95, epsilon=0.2), # Agent 2 : équilibre exploration/exploitation
    QLearningAgent(alpha=0.5, gamma=0.8, epsilon=0.1)   # Agent 3 : forte exploitation
]

# Liste pour stocker le nombre de mats trouvés à chaque nombre d'épisodes pour chaque agent
mates_found_per_agent = [[] for _ in agents]

# Dictionnaire pour stocker les Q-tables de chaque agent par position FEN
q_tables_per_agent = [{} for _ in range(len(agents))]

# Effectuer l'entraînement sur différentes valeurs d'épisodes
episodes = 2
nb_episodes = 20

for i in range(nb_episodes):
    print(f"\n=== Épisode {i + 1} ===")
    for agent_idx, agent in enumerate(agents):
        num_mates_found = 0

        for fen_string in all_fen:
            if fen_string in q_tables_per_agent[agent_idx]:
                agent.set_q(q_tables_per_agent[agent_idx][fen_string])
            
            else:
                q_tables_per_agent[agent_idx][fen_string] = None

            agent.train(episodes, fen_string)

            board = chess.Board(fen_string)
            chess_board = ChessBoard(board)

            # Après l'entraînement, jouer le meilleur coup de l'agent
            possible_actions = list(chess_board.get_possible_moves())
            best_move = agent.get_best_move(board.fen(), possible_actions)  # Utilisation de board.fen() pour obtenir la FEN

            # Appliquer le meilleur coup choisi par l'agent
            chess_board.apply_move(best_move)

            # Vérifier si le coup mène à un mat
            if chess_board.board.is_checkmate() or chess_board.is_game_over():
                num_mates_found += 1

            q_tables_per_agent[agent_idx][fen_string] = agent.get_q()
            agent.clear()

        mates_found_per_agent[agent_idx].append(num_mates_found)



# Affichage des résultats
for idx, mates_found in enumerate(mates_found_per_agent):
    label = f'Agent {idx + 1} (α={agents[idx].alpha}, γ={agents[idx].gamma}, ε={agents[idx].epsilon})'
    plt.plot(range(nb_episodes), mates_found, label=label)

plt.xlabel(f'Nombre d\'épisodes * {episodes}')
plt.ylabel('Mats trouvés')
plt.title('Nombre de mats trouvés selon le nombre d\'épisodes')
plt.legend()
plt.show()


