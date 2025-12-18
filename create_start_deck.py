class Card:
    def __init__(self, name, elixir_cost, damage, health):
        self.name = name
        self.elixir_cost = elixir_cost
        self.damage = damage
        self.health = health
    def __str__(self):
        return f"{self.name}({self.elixir_cost} элексира )"

class Player:
    def _init_(self, name):
        self.name = name
        self.elixir = 5
        self.towers = [1000, 1000, 1000]
        self.deck = []
        self.hand = []

    def create_start_deck(self):
        cards = [
            Card("Рыцарь", 3, 150, 1000),
            Card("Лучники", 3, 100, 300),
            Card("Гигант", 5, 200, 2000),
            Card("Огненный шар", 4, 400, 0),
            Card("Снайпер", 7, 500, 500),
            Card("Тыква", 2, 150, 400),
            Card("Паучек", 1, 50, 400),
            Card("Дракончик", 3, 200, 600)
        ]
        return cards