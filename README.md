# ♟️ Chess Game with AI (Minimax + Alpha-Beta Pruning)

This is a Python-based chess game featuring a graphical user interface built with Pygame and an AI opponent powered by the **Minimax algorithm with Alpha-Beta pruning**. The project also includes a real-time **move history window** using Tkinter to enhance the game experience.

## 🧠 Features

- Play against an AI opponent with customizable depth
- Smart move selection using Minimax + Alpha-Beta pruning
- Real-time move history window (using Tkinter)
- Interactive graphical interface (Pygame)
- End-game detection: Checkmate and Stalemate

---

## 📁 Project Structure
Chess-Game-in-python/
├── assets/
│   └── images/      (Chess piece images in PNG or SVG format)
├── config.json      (Configuration file with settings for screen size, FPS, etc.)
├── move_history_window.py   (Tkinter code for the move history window)
├── src/
│   ├── main.py              (Entry point and main game loop)
│   ├── game.py              (Game logic, board setup, move generation, and helper functions)
│   ├── ui.py                (Pygame-based user interface code)
│   └── engine.py            (AI engine implementation using the Minimax algorithm with Alpha-Beta pruning)
└── requirements.txt         (List of required Python packages, e.g., pygame)

# Install Dependencies
pip install -r requirements.txt

# How to run 
python src/main.py
