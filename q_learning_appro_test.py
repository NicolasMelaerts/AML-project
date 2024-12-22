from chess_board import ChessBoard
from agent_approximate_q_learning import ApproximateQLearningAgent

def make_appro_q_learning_test(all_fen, episodes, nb_episodes):

    nb_fen = len(all_fen)

    # Liste des configurations d'agents
    agent_configurations = [
        {"alpha": 0.3, "gamma": 0.7, "epsilon": 0.5},  # Agent 1 : fort taux d'exploration
        {"alpha": 0.1, "gamma": 0.95, "epsilon": 0.2}, # Agent 2 : équilibre exploration/exploitation
        {"alpha": 0.5, "gamma": 0.8, "epsilon": 0.1},   # Agent 3 : forte exploitation
    ]

    # Créer un dictionnaire d'agents pour chaque position FEN
    agents_per_fen = {}

    for fen_string in all_fen:
        agents_per_fen[fen_string] = [ApproximateQLearningAgent(alpha=config['alpha'], gamma=config['gamma'], epsilon=config['epsilon']) for config in agent_configurations]
        print(f"FEN: {fen_string} - Agents créés: {len(agents_per_fen[fen_string])}")


    # Liste pour stocker le nombre de mats trouvés à chaque nombre d'épisodes pour chaque agent
    mates_found_per_agent = [[0 for f in range(nb_episodes)] for _ in range(len(agent_configurations))]
    games_ended_in_50_moves = [[0 for f in range(nb_episodes)] for _ in range(len(agent_configurations))]

    print(mates_found_per_agent)
    print(games_ended_in_50_moves)

    for _ in range(nb_episodes):
        print(f"\n=== Épisode {_ + 1} ===")
        for fen_idx, (fen_string, agents) in enumerate(agents_per_fen.items()):

            for agent_idx, agent in enumerate(agents):

                # Entraînement de l'agent avec un nombre d'épisodes
                agent.train(episodes, fen_string)

                # Initialisation du plateau de jeu avec la position FEN
                chess_board = ChessBoard(fen_string)
                
                done = False

                while not done:   
                    # L'agent joue son meilleur coup
                    possible_actions = list(chess_board.get_possible_moves())
                    best_move = agent.get_best_move(chess_board.get_fen(), possible_actions)
                    chess_board.apply_move(best_move)

                    # Vérifier si l'agent a gagné
                    if chess_board.is_check_mate() or chess_board.is_game_over():
                        mates_found_per_agent[agent_idx][_] += 1
                        break
                    
                    if chess_board.get_is_fifty_moves():
                        games_ended_in_50_moves[agent_idx][_] += 1
                        break

                    # L'adversaire joue un coup aléatoire
                    chess_board.play_random_move()
                    if chess_board.is_check_mate() or chess_board.is_game_over():
                        mates_found_per_agent[agent_idx][_] += 1
                        break

    print(mates_found_per_agent)
    print(games_ended_in_50_moves)
    return mates_found_per_agent
