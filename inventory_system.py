"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Bryant Dickerson

AI Usage: [Document any AI assistance used]
# AI Usage: Used AI (ChatGPT) to help structure/finish functions if I had errors or if I didn't have the correct formatting


This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

# AI Usage: Used AI (ChatGPT) to help structure/finish functions if I had errors or if I didn't have the correct formatting
# AI Usage: GitHub's AI (Copilot??) suggested that I add a few functions to fix the error in my test cases

# new helper to add near the top of inventory_system.py (**SUGGESTED BY GITHUB AI**)
def _resolve_item(item_data, item_id):
    """
    Accept either:
    - item_data as a mapping {item_id: item_dict} -> returns item_dict
    - item_data as a single item dict (with a 'type' key) -> returns item_data
    Raise KeyError if item_id not found in mapping.
    """
    if isinstance(item_data, dict):
        # case 1: full mapping
        if item_id in item_data:
            return item_data[item_id]
        # case 2: single item dict passed as item_data
        if "type" in item_data and "effect" in item_data:
            return item_data
    raise KeyError(f"Item '{item_id}' not found in provided item_data")


def add_item_to_inventory(character, item_id):

    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list

    inventory = character.get("inventory", []) # checks character inventory

    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Character inventory at maximum capacity. Unable to add more items")
    
    inventory.append(item_id)

    character["inventory"] = inventory
    

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list

    inventory = character.get("inventory", [])

    # Check if item exists
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")

    # Remove it
    inventory.remove(item_id)
    character["inventory"] = inventory

    return True

    

def has_item(character, item_id):

    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check

    if item_id in character["inventory"]:
        return True
    
    else:
        return False
    
    

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method

    return character["inventory"].count(item_id)

    

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    current_size = len(character["inventory"])
    return MAX_INVENTORY_SIZE - current_size

    # TODO: Implement space calculation
    

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """

    removed_items = character["inventory"][:]  # copy so we don’t lose items
    character["inventory"].clear()            # empty inventory
    return removed_items

    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list
    

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data): # (**FIXES SUGGESTED BY GITHUB'S AI**)
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory

    
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory")

    item = _resolve_item(item_data, item_id)

    # Item must be consumable
    if item.get("type") != "consumable":
        raise InvalidItemTypeError(f"Item '{item_id}' is not consumable")

    # use the parse helper
    stat, value = parse_item_effect(item["effect"])
    apply_stat_effect(character, stat, value)

    # Remove item from inventory
    character["inventory"].remove(item_id)

    return f"Used {item_id}, {stat} increased by {value}"
    

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """

     if item_id not in character.get("inventory", []):
        raise ItemNotFoundError(f"Weapon '{item_id}' not found in inventory")

    item = _resolve_item(item_data, item_id)
    if item.get("type") != "weapon":
        raise InvalidItemTypeError(f"Item '{item_id}' is not a weapon")

    # Unequip existing weapon if present
    old_weapon = character.get("equipped_weapon")
    if old_weapon:
        try:
            old_data = _resolve_item(item_data, old_weapon)
            old_stat, old_val = parse_item_effect(old_data["effect"])
            apply_stat_effect(character, old_stat, -old_val)
        except KeyError:
            # old weapon data not available: skip stat removal but still return to inventory
            pass

        character.setdefault("inventory", []).append(old_weapon)

    # Apply new weapon effect
    stat, value = parse_item_effect(item["effect"])
    apply_stat_effect(character, stat, value)

    # Equip and remove from inventory
    character["equipped_weapon"] = item_id
    character["inventory"].remove(item_id)

    return f"Equipped {item_id}, {stat} increased by {value}"

    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    # Handle unequipping current weapon if exists
    # Parse effect and apply to character stats
    # Store equipped_weapon in character dictionary
    # Remove item from inventory
    

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """

    if item_id not in character.get("inventory", []):
        raise ItemNotFoundError(f"Armor '{item_id}' not found in inventory")

    item = _resolve_item(item_data, item_id)
    if item.get("type") != "armor":
        raise InvalidItemTypeError(f"Item '{item_id}' is not armor")

    # Unequip existing armor if present
    old_armor = character.get("equipped_armor")
    if old_armor:
        try:
            old_data = _resolve_item(item_data, old_armor)
            old_stat, old_val = parse_item_effect(old_data["effect"])
            apply_stat_effect(character, old_stat, -old_val)
        except KeyError:
            pass

        character.setdefault("inventory", []).append(old_armor)

    # Apply new armor effect
    stat, value = parse_item_effect(item["effect"])
    apply_stat_effect(character, stat, value)

    character["equipped_armor"] = item_id
    character["inventory"].remove(item_id)

    return f"Equipped {item_id}, {stat} increased by {value}"
    
    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor
    

def unequip_weapon(character, item_data):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """

    equipped = character.get("equipped_weapon")
    if not equipped:
        return None

    # Ensure inventory space
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Inventory is full")

    try:
        weapon_data = _resolve_item(item_data, equipped)
        stat, value = parse_item_effect(weapon_data["effect"])
        apply_stat_effect(character, stat, -value)
    except KeyError:
        # If the item info isn't available, just remove equip status and return to inventory
        pass

    character.setdefault("inventory", []).append(equipped)
    character["equipped_weapon"] = None
    return equipped
    
    # TODO: Implement weapon unequipping
    # Check if weapon is equipped
    # Remove stat bonuses
    # Add weapon back to inventory
    # Clear equipped_weapon from character
    

def unequip_armor(character, item_data):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """

    equipped = character.get("equipped_armor")
    if not equipped:
        return None

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Inventory is full")

    try:
        armor_data = _resolve_item(item_data, equipped)
        stat, value = parse_item_effect(armor_data["effect"])
        apply_stat_effect(character, stat, -value)
    except KeyError:
        pass

    character.setdefault("inventory", []).append(equipped)
    character["equipped_armor"] = None
    return equipped
    
    # TODO: Implement armor unequipping
    

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data): # (**FIXES SUGGESTED BY GITHUB'S AI**)
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    
    item = _resolve_item(item_data, item_id)

    # Check gold
    if character.get("gold", 0) < item.get("cost", 0):
        raise InsufficientResourcesError("Not enough gold to purchase this item.")

    # Check inventory space
    if len(character.get("inventory", [])) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")

    character["gold"] -= item["cost"]
    character.setdefault("inventory", []).append(item_id)

    return True
    
    # TODO: Implement purchasing
    # Check if character has enough gold
    # Check if inventory has space
    # Subtract gold from character
    # Add item to inventory
    

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """

    if item_id not in character.get("inventory", []):
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")

    item = _resolve_item(item_data, item_id)
    sell_price = item.get("cost", 0) // 2

    # Remove one instance and add gold
    character["inventory"].remove(item_id)
    character["gold"] = character.get("gold", 0) + sell_price
    return sell_price

    # TODO: Implement selling
    # Check if character has item
    # Calculate sell price (cost // 2)
    # Remove item from inventory
    # Add gold to character
    

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    parts = effect_string.split(":", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid effect format: {effect_string}")
    stat = parts[0].strip()
    value = int(parts[1].strip())
    return stat, value
    
    # TODO: Implement effect parsing
    # Split on ":"
    # Convert value to integer
    

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """

# Ensure stat exists (default 0)
    character.setdefault(stat_name, 0)
    character[stat_name] += value

    # If adjusting health, clamp to max_health (if present)
    if stat_name == "health":
        max_h = character.get("max_health")
        if isinstance(max_h, int) and character["health"] > max_h:
            character["health"] = max_h
            
    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health
    

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """

    inventory = character.get("inventory", [])

    if not inventory:
        print("\nInventory is empty.")
        return

    print("\n=== INVENTORY ===")
    item_counts = {}
    for item_id in inventory:
        item_counts[item_id] = item_counts.get(item_id, 0) + 1

    for item_id, count in item_counts.items():
        # Try to resolve item info; if not available, print item_id
        try:
            item_info = _resolve_item(item_data_dict, item_id)
            name = item_info.get("name", item_id)
            item_type = item_info.get("type", "unknown")
        except KeyError:
            name = item_id
            item_type = "unknown"

        print(f"{name} ({item_type}) x{count}")

    print("=================\n")

    # TODO: Implement inventory display
    # Count items (some may appear multiple times)
    # Display with item names from item_data_dict
    

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")

