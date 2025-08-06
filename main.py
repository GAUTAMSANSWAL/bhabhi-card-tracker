import tkinter as tk
from PIL import Image, ImageTk

CARD_WIDTH = 80
CARD_HEIGHT = 120

class CardTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Tracker")
        
        self.card_images = {}         # card_name -> PhotoImage (original)
        self.card_labels = {}         # card_name -> Label widget
        self.used_cards = set()       # card_names marked used
        self.slashed_images = {}      # card_name -> slashed PhotoImage

        self.suits = ['hearts', 'diamonds', 'clubs', 'spades']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        self.deck = [r + '_of_' + s for s in self.suits for r in self.ranks]

        try:
            self.RESAMPLE = Image.Resampling.LANCZOS
        except AttributeError:
            self.RESAMPLE = Image.ANTIALIAS

        self.slash_img = Image.open("Slashed_image.png").resize((CARD_WIDTH, CARD_HEIGHT), self.RESAMPLE)
        self.slash_tk = ImageTk.PhotoImage(self.slash_img)

        self.create_grid()
        self.create_reset_button()

    def create_grid(self):
        for row_index, suit in enumerate(self.suits):
            suit_label = tk.Label(self.root, text=suit.capitalize(), font=("Arial", 14, "bold"))
            suit_label.grid(row=row_index, column=0, padx=10, pady=5, sticky="w")

            for col_index, rank in enumerate(self.ranks):
                card = f"{rank}_of_{suit}"
                image = Image.open(f"cards/{card}.png").resize((CARD_WIDTH, CARD_HEIGHT), self.RESAMPLE)
                photo = ImageTk.PhotoImage(image)
                self.card_images[card] = photo

                lbl = tk.Label(self.root, image=photo, bd=2, relief="ridge", cursor="hand2")
                lbl.grid(row=row_index, column=col_index + 1, padx=2, pady=2)
                lbl.bind("<Button-1>", lambda e, c=card: self.toggle_card(c))
                self.card_labels[card] = lbl

    def toggle_card(self, card):
        if card in self.used_cards:
            # Restore original image
            self.card_labels[card].configure(image=self.card_images[card])
            self.used_cards.remove(card)
        else:
            # Generate slashed image if not already cached
            if card not in self.slashed_images:
                card_img = Image.open(f"cards/{card}.png").resize((CARD_WIDTH, CARD_HEIGHT), self.RESAMPLE).convert("RGBA")
                slash_img = self.slash_img.convert("RGBA")
                composite = Image.alpha_composite(card_img, slash_img)
                self.slashed_images[card] = ImageTk.PhotoImage(composite)

            self.card_labels[card].configure(image=self.slashed_images[card])
            self.used_cards.add(card)

    def create_reset_button(self):
        reset_btn = tk.Button(self.root, text="Reset", command=self.reset_all, bg="lightblue", font=("Arial", 12, "bold"))
        reset_btn.grid(row=len(self.suits), column=0, columnspan=14, pady=10)

    def reset_all(self):
        for card in self.used_cards.copy():
            self.card_labels[card].configure(image=self.card_images[card])
        self.used_cards.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = CardTrackerApp(root)
    root.mainloop()
