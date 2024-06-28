from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    records_dict = original_data.to_dict(orient="records")
else:
    records_dict = data.to_dict(orient="records")


def generate_random():
    return random.choice(records_dict)


def french():
    global flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(card_flip, image=card_front)
    canvas.itemconfig(title, text='French', fill='black')
    canvas.itemconfig(words, text=generate_random()['French'], fill='black')
    flip_timer = window.after(3000, english)


def english():
    canvas.itemconfig(card_flip, image=card_back)
    canvas.itemconfig(title, text='English', fill='white')
    canvas.itemconfig(words, text=generate_random()['English'], fill='white')


def is_known():
    records_dict.remove((generate_random()))
    data = pd.DataFrame(records_dict)
    data.to_csv('data/words_to_learn.csv', index=False)
    french()


# UI SETUP-------------------------------------------------------------------
window = Tk()
window.title("FlashCard")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, english)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)

card_front = PhotoImage(file='images/card_front.png')
card_back = PhotoImage(file='images/card_back.png')

card_flip = canvas.create_image(400, 263, image=card_front)
canvas.grid(row=0, column=0, columnspan=2)

title = canvas.create_text(400, 150, text='', font=("Ariel", 40, "italic"))
words = canvas.create_text(400, 263, text='', font=("Ariel", 60, "bold"))

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=french)
wrong_button.grid(row=1, column=0)

generate_random()

window.mainloop()
