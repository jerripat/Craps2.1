import random
import sqlite3
from tkinter import *
from tkinter import messagebox, Label
import tkinter as tk

# Initialize the main Tkinter window
root = Tk()
root.title("Simple Dice Roller")
root.geometry("500x500")
root.configure(background="lightblue")

# Global variables
game_Id = 0
comeout = False
die1 = 0
die2 = 0
point = 0
wager = IntVar()
# Placeholder labels for dice images and game point
dice1_label = Label(root, bg="lightblue")
dice2_label = Label(root, bg="lightblue")
dice1_label.pack(pady=10)
dice2_label.pack(pady=10)

game_point_label = Label(root, text="Game Point: None", bg="lightblue", font=("Arial", 11))
game_point_label.place(x=350, y=25)

image = PhotoImage(file="images/dice_W_gold.png")
image_label = Label(root, image=image, bg="lightblue")
image_label.place(x=25, y=100)

game_Id_label = Label(root, text="Game ID: None", bg="lightblue", font=("Arial", 11))
game_Id_label.place(x=25, y=25)

wager_label = Label(root, text="Wager", bg="lightblue", font=("Arial", 11))
wager_label.place(x=225, y=425)

bet_label = Label(root, text="Win/Lose", bg="lightblue", font=("Arial", 11))
bet_label.place(x=375, y=425)

bet_results = Label(root, text="Win/Lose", bg="lightblue", font=("Arial", 11))
bet_results.place(x=375, y=440)

wager_display = Label(root, text="Win/Lose", bg="lightblue", font=("Arial", 11))
wager_display.place(x=375, y=55)


def set_wager():
    rad = wager.get()
    if rad == 5:
        wager_display = Label(root, text=f"Wager is ${rad}", bg="lightblue", font=("Arial", 11))
        wager_display.place(x=375, y=55)
    elif rad == 10:
        wager_display = Label(root, text=f"Wager is ${rad}", bg="lightblue", font=("Arial", 11))
        wager_display.place(x=375, y=55)
    elif rad == 25:
        wager_display = Label(root, text=f"Wager is ${rad}", bg="lightblue", font=("Arial", 11))
        wager_display.place(x=375, y=55)
    else:
        messagebox.showerror("Invalid Wager", "Please select a valid wager.")
        return

    print(f"Wager: {rad}")


# Wager Radio Buttons

r1 = Radiobutton(root, text="5", variable=wager, value=5, bg="lightgreen", fg="black", command=set_wager)
r1.place(x=170, y=450)
wager_display = Label(root, text="0", bg="lightblue", font=("Arial", 11))
r2 = Radiobutton(root, text="10", variable=wager, value=10, bg="lightgreen", fg="black", command=set_wager)
r2.place(x=215, y=450)
r3 = Radiobutton(root, text="25", variable=wager, value=25, bg="lightgreen", fg="black", command=set_wager)
r3.place(x=270, y=450)


def start_game():
    """Start a new game and initialize the database."""
    global game_Id, comeout
    comeout = False

    try:
        # Connect to the database
        conn = sqlite3.connect("Main.db")
        c = conn.cursor()

        # Ensure the game_ID table exists
        c.execute("""
            CREATE TABLE IF NOT EXISTS game_ID (
                gameID INTEGER PRIMARY KEY AUTOINCREMENT
            )
        """)

        # Increment or initialize game ID
        c.execute("INSERT INTO game_ID (gameID) VALUES ((SELECT IFNULL(MAX(gameID), 0) + 1 FROM game_ID))")
        conn.commit()

        # Fetch the latest game ID
        game_Id = c.execute("SELECT MAX(gameID) FROM game_ID").fetchone()[0]
        conn.close()

        # Update game ID label
        game_Id_label.config(text=f"Game ID: {game_Id}")

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")


def set_dice():
    """Roll the dice and update the game state."""
    global comeout, die1, die2, game_Id
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    score = die1 + die2

    # Update dice images
    update_dice_images(die1, die2)

    if not comeout:  # Come-out roll
        if is_craps(score):
            messagebox.showinfo("Result", "Craps! You lose!")
        elif is_comeout_winner(score):
            messagebox.showinfo("Result", "Come Out Winner! You win!")
        else:
            comeout = True
            game_Id = score
            update_game_point_label(game_Id)
            messagebox.showinfo("Result", f"Game Point set to {score}. Roll again!")
    else:  # Point roll
        if score == 7:
            messagebox.showinfo("Result", "Seven-out! You lose!")
            comeout = False
            update_game_point_label(None)  # Clear the game point
        elif score == game_Id:
            messagebox.showinfo("Result", "You hit the point! You win!")
            comeout = False
            update_game_point_label(None)  # Clear the game point


def update_dice_images(die1, die2):
    """Update the dice images based on the roll."""
    try:
        dice1_img = PhotoImage(file=f"images/dice-{die1}.png")
        dice2_img = PhotoImage(file=f"images/dice-{die2}.png")

        # Set the images for dice labels
        dice1_label.config(image=dice1_img)
        dice2_label.config(image=dice2_img)

        # Keep a reference to prevent garbage collection
        dice1_label.image = dice1_img
        dice2_label.image = dice2_img

    except Exception as e:
        messagebox.showerror("Error", f"Could not load dice images: {e}")


def update_game_point_label(game_point):
    """Update the game point label."""
    if game_point:
        game_point_label.config(text=f"Game Point: {game_point}")
    else:
        game_point_label.config(text="Game Point: None")


def is_craps(score):
    """Check if the score is a losing craps roll."""
    return score in [2, 3, 12]


def is_comeout_winner(score):
    """Check if the score is a winning come-out roll."""
    return score in [7, 11]


def set_widgets():
    """Set up the UI widgets."""
    roll_button = Button(root, text="Roll Dice", command=set_dice, bg="lightgreen", fg="black")
    roll_button.pack(pady=20)


def pass_line():
    pass_label = Label(root, text="Pass Line", bg="lightblue", font=("Arial", 11))
    pass_label.pack(pady=20)
    pass_label.place(x=225, y=425)
pass_line()



def set_up_odds():
    """Set up the odds for the game."""

    # List to store Checkbuttons and their associated IntVars
    odds = []

    # Create Checkbuttons with state variables
    odd4_var = tk.IntVar()
    odd4 = Checkbutton(root, text="4", bg="lightblue", font=("Arial", 11), variable=odd4_var)
    odd4.place(x=100, y=400)
    odds.append(("odd4", odd4_var))  # Add to list with a label

    odd5_var = tk.IntVar()
    odd5 = Checkbutton(root, text="5", bg="lightblue", font=("Arial", 11), variable=odd5_var)
    odd5.place(x=145, y=400)
    odds.append(("odd5", odd5_var))

    odd6_var = tk.IntVar()
    odd6 = Checkbutton(root, text="6", bg="lightblue", font=("Arial", 11), variable=odd6_var)
    odd6.place(x=190, y=400)
    odds.append(("odd6", odd6_var))

    odd8_var = tk.IntVar()
    odd8 = Checkbutton(root, text="8", bg="lightblue", font=("Arial", 11), variable=odd8_var)
    odd8.place(x=235, y=400)
    odds.append(("odd8", odd8_var))

    odd9_var = tk.IntVar()
    odd9 = Checkbutton(root, text="9", bg="lightblue", font=("Arial", 11), variable=odd9_var)
    odd9.place(x=280, y=400)
    odds.append(("odd9", odd9_var))

    odd10_var = tk.IntVar()
    odd10 = Checkbutton(root, text="10", bg="lightblue", font=("Arial", 11), variable=odd10_var)
    odd10.place(x=325, y=400)
    odds.append(("odd10", odd10_var))

    # Function to check which Checkbuttons are selected
    def check_selected_odds():
        for label, var in odds:
            if var.get() == 1:  # If the Checkbutton is selected
                print(f"{label} is selected")
            else:
                print(f"{label} is not selected")

    # Add a button to trigger the check function
    check_button = tk.Button(root, text="Check Odds", command=check_selected_odds)
    check_button.place(x=50, y=450)


# Call the function to set up the odds
set_up_odds()

if __name__ == "__main__":
    start_game()
    set_widgets()
    set_up_odds()
    root.mainloop()
