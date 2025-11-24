"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Bryant Dickerson

AI Usage: [Document any AI assistance used]
# AI USAGE (ChatGPT): Used AI to help me begin/format functions to ensure I had the right formatting
# AI Usage (ChatGPT): I used ChatGPT to reformat these functions below to pass the test cases:
   --> create_character, save_character, load_character, list_saved_characters, delete_character, gain_experience, and validate_character_data. 

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)


# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

# AI USAGE (ChatGPT): Used AI to help me begin/format functions to ensure I had the right formatting

def create_character(name, character_class):


    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    # TODO: Implement character creation
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list

    valid_char_classes = ["Warrior", "Mage", "Rogue", "Cleric"]

    if character_class not in valid_char_classes:
        raise InvalidCharacterClassError(f"{character_class} is not an available class.")
    
    base_stats = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5}, 
        "Mage":    {"health": 80,  "strength": 8,  "magic": 20},
        "Rogue":   {"health": 90,  "strength": 12, "magic": 10},
        "Cleric":  {"health": 100, "strength": 10, "magic": 15}
    }

    stats = base_stats[character_class]

    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0, # experience amount begins at 0.
        "gold": 100, # every character starts with 100 gold.
        "inventory": [], # inventory is empty by default, can be added to later.
        "active_quests": [], # no active quests by default.
        "completed_quests": [] # no completed quests by default (no active quests).
    }



# AI USAGE - I had AI help me format the save function in this format:
def save_character(character, save_directory="data/save_games"):

    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values

# 1. Ensure save directory exists
    os.makedirs(save_directory, exist_ok=True)
    
    character_name = character.get("name", "temp_character") # Ensure we have a name
    file_path = os.path.join(save_directory, f"{character_name}.txt")

    # Prepare data for writing
    lines = []
    
    # Simple stats (non-list, non-dict)
    for key, value in character.items():
        if key in ["level", "xp", "gold", "health", "max_health", "strength", "magic", "name"]:
             lines.append(f"{key.upper()}:{value}")
        elif key == "inventory":
            # Inventory must be converted to a comma-separated string
            inventory_str = ",".join(value)
            lines.append(f"{key.upper()}:{inventory_str}")
        elif key in ["equipped_weapon", "equipped_armor"]:
            # Ensure None is written as the string 'None'
            equipped_str = value if value is not None else "None"
            lines.append(f"{key.upper()}:{equipped_str}")

    try:
        with open(file_path, 'w') as f:
            f.write('\n'.join(lines))
            
    except Exception as e:
        print(f"Error saving character {character_name}: {e}")
        # raise FileSaveError(f"Failed to save file for {character_name}.")
        raise # Re-raise for debugging/testing
    
    return True

def load_character(character_name, save_directory="data/save_games"):

    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists

    file_path = os.path.join(save_directory, f"{character_name}.txt") # Use .txt or similar extension

    if not os.path.exists(file_path):
        # Raise the specific error expected by the test framework
        # raise CharacterNotFoundError(f"Character '{character_name}' not found.")
        raise FileNotFoundError(f"Character '{character_name}' save file not found.")

    character = {}
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or ':' not in line:
                    continue # Skip empty or invalid lines

                key, value_str = line.split(':', 1)
                
                # Clean up key and value
                key = key.strip()
                value_str = value_str.strip()
                
                # --- TYPE CONVERSION ---
                if key in ["LEVEL", "XP", "GOLD", "HEALTH", "MAX_HEALTH", "STRENGTH", "MAGIC"]:
                    character[key.lower()] = int(value_str) # Convert stats to int
                elif key == "INVENTORY":
                    # Inventory is a list, split by comma. Handle empty inventory case.
                    if value_str:
                        character[key.lower()] = value_str.split(',')
                    else:
                        character[key.lower()] = []
                elif key in ["EQUIPPED_WEAPON", "EQUIPPED_ARMOR"]:
                    # Equipped items are strings; use None if value is 'None'
                    character[key.lower()] = None if value_str == "None" else value_str
                else:
                    # Default to string for NAME
                    character[key.lower()] = value_str

    except Exception as e:
        # Catch unexpected errors during reading/parsing
        print(f"Error loading character {character_name}: {e}")
        # raise CorruptedDataError(f"Save file for {character_name} is corrupted.")
        raise # Re-raise for debugging/testing
        
    return character

def delete_character(character_name, save_directory="data/save_games"):


    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion

    # builds the filepath system to retrieve information

    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Character {character_name} was not found.")
    os.remove(filepath)

    return True


# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up

# Dead characters cannot gain experience, so this is checked BEFORE the level-up process
    if character["health"] == 0:
        raise CharacterDeadError("Character is dead, cannot gain experience.")

# The while loop keeps leveling up the character until the experience equals the level * 100
    character["experience"] += xp_amount
    while character["experience"] >= character["level"] * 100:
        level_up_xp = character["level"] * 100
        character["experience"] -= level_up_xp
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]

    

def add_gold(character, amount):

    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold

    # character.get() reads the amount of gold the character has, will return 0 if gold is either nonexistent 
    current_gold = character.get("gold", 0)

    # Checks if the new total would be negative
    total_gold = current_gold + amount
    if total_gold < 0:
        raise ValueError("Stack your bread, you out of gold dawg!")

    # Update the character's gold
    character["gold"] = total_gold

    return total_gold
    

def heal_character(character, amount):

    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    
    if character["health"] <= 0:
        raise CharacterDeadError("Character is dead, heal failed.")
    
    normal_character_health = character["health"]
    character["health"] = min(character["health"] + amount, character["max_health"]) # checks which value between the arguments is the smaller one

    return character["health"] - normal_character_health

def is_character_dead(character):

    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    # TODO: Implement death check

    current_health = character.get("health", 0) # reads character's health

    if current_health <= 0:
        print("Character is currently dead.")
        return True # returns true since the character has no health
    else:
        print("Character is still alive.")
        return False # returns false since the character still has health    




def revive_character(character):

    """
    Revive a dead character with 50% health
    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health

    # Check if character is actually dead
    if not is_character_dead(character):
        return False  # If the character is alive, they obviously cannot be revived
    

    # Characters are revived with half of their max health
    half_health = character["max_health"] // 2  # using floor division for integers

    character["health"] = half_health # assigning result to character's main health attribute

    return True
    

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):

    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    
    # Below are the required fields needed for a full, valid save
def validate_character_data(character):
    """
    Validate character dictionary has all required fields
    """
    required_fields = {
        "name": str,
        "class": str,
        "level": int,
        "health": int,
        "max_health": int,
        "strength": int,
        "magic": int,
        "experience": int,
        "gold": int,
        "inventory": list,
        "active_quests": list,
        "completed_quests": list
    }

    for field, expected_type in required_fields.items():
        if field not in character:
            raise InvalidSaveDataError(f"Missing required field: {field}")
        value = character[field]
        if not isinstance(value, expected_type):
            raise InvalidSaveDataError(f"Field '{field}' must be of type {expected_type.__name__}")

    return True
# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")


