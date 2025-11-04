
from rpg_project.src.models.crafting import Recipe


class CraftingService:
    def __init__(self, recipes: list[Recipe]):
        self.recipes = {r.name: r for r in recipes}

    def can_craft(self, player, recipe_name: str) -> bool:
        recipe = self.recipes.get(recipe_name)
        if not recipe:
            return False
        inv = {item["name"]: item["amount"] for item in player.inventory}
        for inp in recipe.inputs:
            if inv.get(inp.name, 0) < inp.amount:
                return False
        return True

    def craft(self, player, recipe_name: str) -> bool:
        recipe = self.recipes.get(recipe_name)
        if not recipe or not self.can_craft(player, recipe_name):
            return False
        # Ressourcen abziehen
        for inp in recipe.inputs:
            for item in player.inventory:
                if item["name"] == inp.name and item["amount"] >= inp.amount:
                    item["amount"] -= inp.amount
        # Entferne leere Items
        player.inventory = [item for item in player.inventory if item["amount"] > 0]
        # Output hinzufügen
        for out in recipe.outputs:
            found = False
            for item in player.inventory:
                if item["name"] == out.name:
                    item["amount"] += out.amount
                    found = True
            if not found:
                player.inventory.append({"name": out.name, "amount": out.amount})
        return True
