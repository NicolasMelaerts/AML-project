# ♟️ Q-Learning for Chess Endgames  

## 📝 Description  
This project explores the use of **Q-learning** and **Approximate Q-learning** to solve simple chess endgame situations, such as Queen + King vs King. The goal is to evaluate the strengths and limitations of these reinforcement learning techniques and propose improvements for more complex board configurations.

---

## 🚀 Features  
- **Q-learning Implementation:** Traditional Q-learning for chess endgames  
- **Approximate Q-learning:** Enhanced agent with state generalization capabilities  
- **Custom Chess Board Generator:** Create FEN-based board configurations for training and evaluation  
- **Performance Analysis:** Comparative results between Q-learning and Approximate Q-learning  

---

## 📊 Key Insights  
1. Classic Q-learning struggles to generalize and solve complex chess endgames efficiently.  
2. Approximate Q-learning demonstrates better performance by leveraging feature extraction techniques.  
3. Future improvement suggestions include the implementation of **Deep Q-learning** for better generalization in complex environments.

---

## 🧰 Tools & Technologies  
- **Python**  
- `numpy`, `matplotlib`, `python-chess`, `scikit-learn`

---

## 📂 Project Structure  
- `agent_q_learning.py`: Q-learning agent implementation  
- `agent_approx_q_learning.py`: Approximate Q-learning agent  
- `chess_board_generator.py`: Generates FEN-based chess boards  
- `chess_board_loader.py`: Loads predefined chess board configurations  
- `experiences.py`: Generates visual performance analysis  
- `q_learning_test.py`, `approx_q_learning_test.py`: Run games with Q-learning and Approximate Q-learning agents  

---

## 🛠️ How to Run  
1. Clone this repository:  
   git clone https://github.com/NicolasMelaerts/AML-project.git
   cd AML-project

2. Install required packages:
pip install numpy matplotlib python-chess scikit-learn

3. Run an experiment:
python experiences.py


