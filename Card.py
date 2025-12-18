class Card:
    def _init_(self, name, elixir_cost, damage, health):
        self.name = name
        self.elixir_cost = elixir_cost
        self.damage = damage
        self.health = health
    def _stir_(self):
        return f"{self.name}({self.elixir_cost} элексира )"
