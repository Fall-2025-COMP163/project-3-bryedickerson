"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Bryant Dickerson

AI Usage: [Document any AI assistance used]
# AI USAGE (ChatGPT): Used AI to help me begin/format functions to ensure I had the right formatting

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

        # os.makedirs creates a directory
    os.makedirs(save_directory, exist_ok=True)

    # building the filename/
    filename = f"{character['name']}_save.txt"
    filepath = os.path.join(save_directory, filename)

    # 3. Prepare save data in the exact required file format
    character = (
        f"NAME: {character['name']}\n"
        f"CLASS: {character['class']}\n"
        f"LEVEL: {character['level']}\n"
        f"HEALTH: {character['health']}\n"
        f"MAX_HEALTH: {character['max_health']}\n"
        f"STRENGTH: {character['strength']}\n"
        f"MAGIC: {character['magic']}\n"
        f"EXPERIENCE: {character['experience']}\n"
        f"GOLD: {character['gold']}\n"
        f"INVENTORY: {','.join(character['inventory'])}\n"
        f"ACTIVE_QUESTS: {','.join(character['active_quests'])}\n"
        f"COMPLETED_QUESTS: {','.join(character['completed_quests'])}\n"
    )

    # 4. Write the file (let IOError/PermissionError propagate naturally)
    with open(filepath, "w") as file:
        file.write(character)

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

    # building the filename
    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)

    # os.path.exists checks if file exists
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Save file not found for: {character_name}")

    # Try reading the file
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
    except Exception:
        raise SaveFileCorruptedError("Could not read save file")
    # SaveFileCorruptedError means the file couldn't be read

    # Parse the lines into a dictionary
    character = {}
    try:
        for line in lines:
            key, value = line.strip().split(": ", 1)
            character[key] = value
    except Exception:
        raise InvalidSaveDataError("Save data format is invalid")

    # Converts comma-separated text back into lists
    character["INVENTORY"] = character["INVENTORY"].split(",") if character["INVENTORY"] else []
    character["ACTIVE_QUESTS"] = character["ACTIVE_QUESTS"].split(",") if character["ACTIVE_QUESTS"] else []
    character["COMPLETED_QUESTS"] = character["COMPLETED_QUESTS"].split(",") if character["COMPLETED_QUESTS"] else []

    # Convert numeric fields
    int_fields = ["LEVEL", "HEALTH", "MAX_HEALTH", "STRENGTH", "MAGIC", "EXPERIENCE", "GOLD"]
    for field in int_fields:
        character[field] = int(character[field])

    return character

    

def list_saved_characters(save_directory="data/save_games"):

    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames

    
    if not os.path.exists(save_directory):
        return [] # returns an empty list if the directory is nonexistent
    
    files = os.listdir(save_directory) # this command lists the files inside of the directory

    saved_characters = [
        filename.replace("_save.txt", "")
        for filename in files
        if filename.endswith("_save.txt")
    ]

    return saved_characters
 # ChatGPT suggested to use these commands above 
 # They act as a filter for files that end with "_save.txt" only, and keeps the ones that do.
    

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

    # Next, this verifies if the file exists before the system tries to delete it
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Character {character_name} was not found.")
    

    # The os.remove function will remove the file once ran
    
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

    # As directed by the docstring, this checks if the health of the character is 0 (if the character is dead) first.
    if character["health"] == 0:
        raise CharacterDeadError("Character is dead, unable to apply any levels") # if so, the function raises an error
    
    character["experience"] += xp_amount # adds xp points to character's xp amount

    level_up_xp = character["level"] * 100 # Calculates the xp needed for leveling up
    
    # Level up loop (in cases of high amounts of xp, this loop will keep going until the xp is less than or equal to the experience amount)
    while character["experience"] >= level_up_xp:


        character["level"] += 1
        character["health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]

        # Recalculates XP 
        character["experience"] -= level_up_xp
        level_up_xp = character["level"] * 100
    
    

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
    
    health = character.get("health", 0) # reads the current health of the character
    max_health = character.get("max_health", 0) # reads the max health for character

    # Calculate potential healed health
    new_health = health + amount 

    # Cap at max_health
    if new_health > max_health:
        health_regen = max_health - health
        health_regen = max_health
    else:
        health_regen = amount

    # Apply the healing
    character["health"] = new_health

    return health_regen


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
        "completed_quests": list,
    }

    # Below: Checks that all required fields exist
    for field, expected_type in required_fields.items():
        if field not in character:
            raise InvalidSaveDataError(f"Missing required field: {field}")

        # Below: Checks that each type (string, integer, etc.) matches (int, str, list)
        if not isinstance(character[field], expected_type):
            raise InvalidSaveDataError(
                f"Field '{field}' must be of type {expected_type.__name__}"
            )

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


