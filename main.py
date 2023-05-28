import tkinter as tk
import time
import math

victory = False

def start_timer():
    global start_time
    start_time = time.time()

def show_elapsed_time():
    global minutes, seconds

    elapsed_time = time.time() - start_time
    minutes = int(math.floor(elapsed_time/60))
    seconds = int(elapsed_time%60)
    elapsed_str = "Time passed: {}:{:0>2}".format(minutes,seconds)
    label2.config(text=elapsed_str)
    label2.after(1000, show_elapsed_time)  # Atualiza a cada segundo


    #label2.pack(pady=1)
    label2.config(text=elapsed_str)

guide = """Enter numbers from 1 to 9 in the grid.
Your goal is to make the sum of all lines equal to 15,\nwhether it's in the diagonal, horizontal, or vertical.
Press "Enter" to lock a number in!
"""

def print_grid(grid):
    for row in grid:
        print(" | ".join(map(str, row)))
        print("-" * 11)

def check_sum(grid):
    target_sum = 15

    # Check rows
    for row in grid:
        if sum(row) != target_sum:
            return False

    # Check columns
    for col in range(3):
        if sum(grid[row][col] for row in range(3)) != target_sum:
            return False

    # Check diagonals
    if (grid[0][0] + grid[1][1] + grid[2][2] != target_sum) or (grid[0][2] + grid[1][1] + grid[2][0] != target_sum):
        return False

    return True

def on_cell_click(row, col):
    global grid, numbers_remaining, number_entries, result_label

    if grid[row][col] == 0:
        selected_number = number_entries[row][col].get()

        if selected_number.isdigit():
            number = int(selected_number)

            if number in numbers_remaining:
                grid[row][col] = number
                numbers_remaining.remove(number)
                number_entries[row][col].config(state="disabled", disabledforeground="black")
                number_entries[row][col].delete(0, tk.END)
                number_entries[row][col].insert(0, str(number))

                if len(numbers_remaining) == 0:
                    if check_sum(grid):
                        result_label.config(text="Congratulations! You completed the grid.\nYou took: {}:{:0>2}".format(minutes,seconds))
                    else:
                        result_label.config(text="Sorry, the grid is incorrect.")
            else:
                result_label.config(text="Invalid number. Choose another number.")
        else:
            result_label.config(text="Invalid input. Please enter a valid number.")
    else:
        result_label.config(text="Cell already filled. Choose another cell.")

def restart_game(guide=guide):
    global grid, numbers_remaining, number_entries, result_label

    grid = [[0, 0, 0] for _ in range(3)]
    numbers_remaining = set(range(1, 10))

    for row in range(3):
        for col in range(3):
            number_entries[row][col].config(state="normal", disabledforeground="black")
            number_entries[row][col].delete(0, tk.END)

    result_label.config(text=guide)

def create_gui(guide=guide):
    global grid, numbers_remaining, number_entries, result_label, label2

    root = tk.Tk()
    root.title("Sum it to 15")
    #root.geometry("500x300")

    grid = [[0, 0, 0] for _ in range(3)]
    numbers_remaining = set(range(1, 10))

    number_entries = [[None, None, None] for _ in range(3)]

    for row in range(3):
        for col in range(3):
            button_var = tk.StringVar()
            number_entries[row][col] = tk.Entry(root, textvariable=button_var, width=5)
            number_entries[row][col].grid(row=row, column=col)
            number_entries[row][col].bind("<Return>", lambda event, r=row, c=col: on_cell_click(r, c))

    result_label = tk.Label(root, text=guide, font=("Arial", 10))
    result_label.grid(row=3, columnspan=3)
    

    label2 = tk.Label(root, font=("Arial", 10))
    label2.grid(row=5, columnspan=3)
    # label2.config(text="Deu certo") 

    restart_button = tk.Button(root, text="Restart", command=restart_game)
    restart_button.grid(row=4, column=1, pady=10)

    start_timer()
    show_elapsed_time()

    root.mainloop()

if __name__ == "__main__":
    number_buttons = [[None, None, None] for _ in range(3)]
    create_gui()

