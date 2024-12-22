#Lit un fichier texte contenant des positions FEN et renvoie les chaînes FEN
def load_positions_from_file(file_name):
    fen_strings = []
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                fen_strings.append(line)  # Ajoute la chaîne FEN à la liste
    return fen_strings
