# GameInitializer.gd
# Attach this script to your main Scene Tree / Node2D setup.

extends Node2D

# Core Game Settings & Player State
var current_day: int = 1
var current_season: String = "Spring" # "Spring", "Summer", "Fall", "Winter"
var player_gold: int = 500
var player_energy: int = 100
var max_energy: int = 100

# Inventory structure: Grid of item data
var inventory: Array = []
const INVENTORY_SIZE: int = 12

func _ready() -> void:
	initialize_inventory()
	start_new_game()

func initialize_inventory() -> void:
	inventory.clear()
	for i in range(INVENTORY_SIZE):
		inventory.append({"id": "", "count": 0})
	
	# Give starting tools/seeds
	add_item("hoe", 1)
	add_item("watering_can", 1)
	add_item("parsnip_seed", 15)

func add_item(item_id: String, count: int) -> bool:
	# First pass: check for existing stackable item
	for item in inventory:
		if item["id"] == item_id:
			item["count"] += count
			print("Added " + str(count) + " " + item_id + "(s).")
			return true

	# Second pass: find empty slot
	for item in inventory:
		if item["id"] == "":
			item["id"] = item_id
			item["count"] = count
			print("Added " + str(count) + " " + item_id + "(s) to a new slot.")
			return true

	print("Inventory full!")
	return false

func start_new_game() -> void:
	print("--- Welcome to Farm Life ---")
	print("Season: " + current_season + " | Day: " + str(current_day))
	print("Gold: " + str(player_gold) + "g | Energy: " + str(player_energy) + "/" + str(max_energy))
	print("Starting Inventory: ", inventory)

# Call this when player sleeps
func pass_day() -> void:
	current_day += 1
	player_energy = max_energy # Restores energy
	
	if current_day > 28:
		current_day = 1
		advance_season()
		
	print("You wake up rested. It is now " + current_season + " " + str(current_day) + ".")

func advance_season() -> void:
	match current_season:
		"Spring": current_season = "Summer"
		"Summer": current_season = "Fall"
		"Fall": current_season = "Winter"
		"Winter": current_season = "Spring"
