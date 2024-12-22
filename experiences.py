import matplotlib.pyplot as plt
import numpy as np
from chess_board_loader import load_positions_from_file
from q_learning_appro_test import make_appro_q_learning_test
from q_learning_test import make_q_learning_test
from agent_q_learning import QLearningAgent

# Fichiers de positions
mate_in_one_positions_3_pieces = 'mate_in_one_positions_3_pieces.txt'
random_positions_3_pieces = 'random_positions_3_pieces.txt'
random_positions_6_pieces = 'random_positions_6_pieces.txt'


def plot_q_learning_results(mates_found_per_agent, episodes, nb_episodes, agents):
    """
    Charge les positions FEN depuis un fichier, exécute les tests de Q-learning et affiche les résultats.
    """
    for idx, mates_found in enumerate(mates_found_per_agent):
        label = f'Agent {idx + 1} (α={agents[idx].alpha}, γ={agents[idx].gamma}, ε={agents[idx].epsilon})'
        plt.plot(range(nb_episodes), mates_found, label=f'{label} - Mats trouvés')

    plt.xlabel(f'Nombre d\'épisodes * {episodes}')
    plt.ylabel('Nombre de mats trouvés')
    plt.title('Nombre de mats trouvés')
    plt.legend()
    plt.show()


def compare_agents_performance(agent_approx_10_10, agent_normaux_10_10):
    """
    Compare les performances des agents approximatifs et normaux et affiche un box plot.
    """
    data = agent_approx_10_10 + agent_normaux_10_10
    labels = ['Agent approx 1', 'Agent approx 2', 'Agent approx 3', 
              'Agent normal 1', 'Agent normal 2', 'Agent normal 3']

    plt.figure(figsize=(10, 6))
    plt.boxplot(data, labels=labels)

    plt.ylabel('Nombre de mats trouvés')
    plt.title('Comparaison des performances des agents approximatifs et normaux')
    plt.grid(True)
    plt.show()

def cumulative_average(data):
    return np.cumsum(data) / (np.arange(len(data)) + 1)

def plot_cumulative_average(agent_approx, agent_normaux):
    """
    Affiche l'évolution de la performance des agents à travers les épisodes sous forme de moyenne cumulative.
    """

    plt.figure(figsize=(10, 6))

    for agent in agent_approx:
        plt.plot(cumulative_average(agent), label=f'Agent approx {agent_approx.index(agent) + 1}')

    for agent in agent_normaux:
        plt.plot(cumulative_average(agent), label=f'Agent normal {agent_normaux.index(agent) + 1}')

    plt.xlabel('Épisodes')
    plt.ylabel('Moyenne cumulative des mats trouvés')
    plt.title('Évolution de la performance des agents à travers les épisodes')
    plt.legend()
    plt.grid(True)
    plt.show()


def extended_compare_agents_performance(agent_approx_10_10, agent_normaux_10_10, agent_normaux_10_100):
    """
    Compare les performances des agents approximatifs et normaux sur plus d'épisodes et affiche un box plot.
    """
    data = agent_approx_10_10 + agent_normaux_10_10 + agent_normaux_10_100
    labels = [
        'Agent approx 1', 'Agent approx 2', 'Agent approx 3', 
        'Agent normal 1 (10-10)', 'Agent normal 2 (10-10)', 'Agent normal 3 (10-10)',
        'Agent normal 1 (10-100)', 'Agent normal 2 (10-100)', 'Agent normal 3 (10-100)'
    ]

    plt.figure(figsize=(12, 7))
    plt.boxplot(data, labels=labels)

    plt.ylabel('Nombre de mats trouvés')
    plt.title('Comparaison des performances des agents approximatifs et normaux')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    agents = [
        QLearningAgent(alpha=0.3, gamma=0.7, epsilon=0.5),  # Agent 1 : fort taux d'exploration
        QLearningAgent(alpha=0.1, gamma=0.95, epsilon=0.2), # Agent 2 : équilibre exploration/exploitation
        QLearningAgent(alpha=0.5, gamma=0.8, epsilon=0.1)   # Agent 3 : forte exploitation
    ]


    # ======= 3 pièces =======

    # Plot Q-learning 3 pièces avec les plateaux pour mettre mat en un coup
    all_fen = load_positions_from_file(mate_in_one_positions_3_pieces)
    mates_found_per_agent = make_q_learning_test(all_fen, 5, 10)
    plot_q_learning_results(mates_found_per_agent, 5, 10, agents)
    
    # Plot Q-learning 3 pièces avec des plateaux aleatoires
    all_fen = load_positions_from_file(random_positions_3_pieces)
    mates_found_per_agent = make_q_learning_test(all_fen, 5, 10)
    plot_q_learning_results(mates_found_per_agent, 5, 10, agents)


    # Compare les performances des agents approximatifs et normaux
    all_fen = load_positions_from_file(random_positions_3_pieces)
    agent_approx_10_10 = make_appro_q_learning_test(all_fen, 10, 10)
    agent_normaux_10_10 = make_q_learning_test(all_fen, 10, 10)
    compare_agents_performance(agent_approx_10_10, agent_normaux_10_10)


    # Plot agent approximatif vs agent normal 10-10
    plot_cumulative_average(agent_approx_10_10, agent_normaux_10_10)

    # Plot agent approximatif vs agent normal 10-100
    agent_normaux_10_100 = make_q_learning_test(all_fen, 100, 10)
    plot_cumulative_average(agent_approx_10_10, agent_normaux_10_100)

    # Plot agent approximatif vs agent normal 10-10 vs agent normal 10-100 
    extended_compare_agents_performance(agent_approx_10_10, agent_normaux_10_10, agent_normaux_10_100)


    # ======= 6 pièces =======
    all_fen = load_positions_from_file(random_positions_6_pieces)
    agent_approx_10_10 = make_appro_q_learning_test(all_fen, 10, 10)
    agent_normaux_10_10 = make_q_learning_test(all_fen, 10, 10)
    agent_normaux_10_100 = make_q_learning_test(all_fen, 100, 10)

    extended_compare_agents_performance(agent_approx_10_10, agent_normaux_10_10, agent_normaux_10_100)

if __name__ == '__main__':
    main()