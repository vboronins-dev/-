class Player:
    def _init_(self, name):
        self.name = name
        self.elixir = 5
        self.towers = [1000, 1000, 1000]
        self.deck = []
        self.hand = []