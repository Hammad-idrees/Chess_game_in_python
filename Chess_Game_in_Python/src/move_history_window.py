import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# Global move history list (shared with main.py)
move_history = []

def start_move_history_window():
    """Starts a Tkinter window that continuously updates with the move history."""
    # Create the main window for move history
    root = tk.Tk()
    root.title("Move History")
    root.geometry("300x400")  # You can adjust the width/height as needed

    # Create a scrolled text widget for displaying moves
    text_area = ScrolledText(root, wrap=tk.WORD, width=40, height=20, font=("Courier New", 12))
    text_area.pack(expand=True, fill="both")

    def update_text():
        """Clear and update the move history text area with extra spacing for black moves."""
        text_area.delete("1.0", tk.END)
        # Insert a header
        text_area.insert(tk.END, "No.   White Move                Black Move\n")
        # Display moves in pairs (white and black)
        for idx in range(0, len(move_history), 2):
            move_no = (idx // 2) + 1
            white_move = move_history[idx]
            black_move = move_history[idx + 1] if idx + 1 < len(move_history) else ""
            # Increase spacing between the white and black move columns
            line = f"{move_no:2}.   {white_move:12}                  {black_move:12}\n"
            text_area.insert(tk.END, line)
        # Schedule next update after 500 milliseconds.
        root.after(500, update_text)

    update_text()
    root.mainloop()
