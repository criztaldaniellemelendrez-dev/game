# app.py

class GameState:
    def __init__(self):
        # Core Game Settings & Player State
        self.current_day: int = 1
        self.current_season: str = "Spring"  # "Spring", "Summer", "Fall", "Winter"
        self.player_gold: int = 500
        self.player_energy: int = 100
        self.max_energy: int = 100

        # Inventory structure: Grid of item data
        self.inventory: list = []
        self.inventory_size: int = 12

        self.initialize_inventory()
        self.start_new_game()

    def initialize_inventory(self):
        self.inventory.clear()
        for _ in range(self.inventory_size):
            self.inventory.append({"id": "", "count": 0})
        
        # Give starting tools/seeds
        self.add_item("hoe", 1)
        self.add_item("watering_can", 1)
        self.add_item("parsnip_seed", 15)

    def add_item(self, item_id: str, count: int) -> bool:
        # First pass: check for existing stackable item
        for item in self.inventory:
            if item["id"] == item_id:
                item["count"] += count
                print(f"Added {count} {item_id}(s).")
                return True

        # Second pass: find empty slot
        for item in self.inventory:
            if item["id"] == "":
                item["id"] = item_id
                item["count"] = count
                print(f"Added {count} {item_id}(s) to a new slot.")
                return True

        print("Inventory full!")
        return False

    def start_new_game(self):
        print("--- Welcome to Farm Life ---")
        print(f"Season: {self.current_season} | Day: {self.current_day}")
        print(f"Gold: {self.player_gold}g | Energy: {self.player_energy}/{self.max_energy}")
        print("Starting Inventory:", self.inventory)

    def pass_day(self):
        self.current_day += 1
        self.player_energy = self.max_energy  # Restores energy
        
        if self.current_day > 28:
            self.current_day = 1
            self.advance_season()
            
        print(f"You wake up rested. It is now {self.current_season} {self.current_day}.")

    def advance_season(self):
        seasons = ["Spring", "Summer", "Fall", "Winter"]
        current_idx = seasons.index(self.current_season)
        self.current_season = seasons[(current_idx + 1) % 4]

# Run the game loop engine
if __name__ == "__main__":
    game = GameState()
