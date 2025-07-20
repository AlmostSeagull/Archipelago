# from worlds.dk64 import DK64World
from worlds.dk64.randomizer.CompileHints import UpdateSpoilerHintList, getRandomHintLocation, replaceKongNameWithKrusha
from worlds.dk64.randomizer.Lists.WrinklyHints import ClearHintMessages
from worlds.dk64.randomizer.Patching.UpdateHints import UpdateHint


def CompileArchipelagoHints(world, hint_data: list):
    """Insert Archipelago hints."""
    replaceKongNameWithKrusha(world.spoiler)
    ClearHintMessages()
    # All input lists are in the form of [loc]
    # Settings
    woth_count = 10
    major_count = 7
    deep_count = 8

    # Variables
    hints_remaining = 35  # Keep count how many hints we placed
    hints = []  # The hints we compile
    woth_duplicates = []
    kong_locations = hint_data["kong"]
    key_locations = hint_data["key"]
    woth_locations = hint_data["woth"]
    major_locations = hint_data["major"]
    deep_locations = hint_data["deep"]

    # Creating the hints
    # Kong hints
    for kong_loc in kong_locations:
        hints.append(parseKongHint(world, kong_loc))
        hints_remaining -= 1

    # Key hints
    for key_loc in key_locations:
        hints.append(parseKeyHint(world, key_loc))
        hints_remaining -= 1

    # Woth hints
    woth_count = min(min(len(woth_locations), woth_count), hints_remaining)
    woth_locations = world.spoiler.settings.random.sample(woth_locations, woth_count)
    for woth_loc in woth_locations:
        this_hint = parseWothHint(world, woth_loc)
        hints.append(this_hint)
        woth_duplicates.append(this_hint)
        hints_remaining -= 1

    # Major item hints
    major_count = min(min(len(major_locations), major_count), hints_remaining)
    major_locations = world.spoiler.settings.random.sample(major_locations, major_count)
    for major_loc in major_locations:
        hints.append(parseMajorItemHint(world, major_loc))
        hints_remaining -= 1

    # Deep check hints
    deep_count = min(min(len(deep_locations), deep_count), hints_remaining)
    deep_locations = world.spoiler.settings.random.sample(deep_locations, deep_count)
    for deep_loc in deep_locations:
        hints.append(parseDeepHint(world, deep_loc))
        hints_remaining -= 1

    # Woth hint duplicates as needed
    while hints_remaining > 0 and len(woth_duplicates) > 0:
        hints.append(woth_duplicates.pop())
        hints_remaining -= 1

    # Sanity check that 35 hints were placed
    if hints_remaining > 0:
        # This part of the code should not be reached.
        print("Not enough hints. Please wait. stage_generate_output might be crashing.")
        while hints_remaining > 0:
            hints.append("no hint, sorry...".upper())
            hints_remaining -= 1

    for hint in hints:
        hint_location = getRandomHintLocation(random=world.spoiler.settings.random)
        UpdateHint(hint_location, hint)
    UpdateSpoilerHintList(world.spoiler)

def parseKeyHint(world, location):
    """Write a key hint for the given location."""
    text = ""
    if location.player != world.player:
        text = f"\x07{location.item.name[:40]}\x07 is hidden, for {world.multiworld.get_player_name(location.player)} to find in \x0d{location.name[:80]}\x0d.".upper()
    else:
        text = f"\x07{location.item.name[:40]}\x07 is hidden away in \x0d{location.name}\x0d.".upper()
    for letter in text:
        if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?:;'S-()% \x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d":
            text = text.replace(letter, " ")
    return text

def parseKongHint(world, location):
    """Write a kong hint for the given location."""
    text = ""
    if location.player != world.player:
        text = f"\x07{location.item.name[:40]}\x07 is to be found by {world.multiworld.get_player_name(location.player)} in \x0d{location.name[:80]}\x0d.".upper()
    else:
        text = f"\x07{location.item.name[:40]}\x07 is held by your local villain in \x0d{location.name}\x0d.".upper()
    for letter in text:
        if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?:;'S-()% \x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d":
            text = text.replace(letter, " ")
    return text

def parseWothHint(world, location):
    """Write a woth item hint for the given location."""
    text = ""
    if location.player != world.player:
        text = f"Woth item \x07{location.item.name[:40]}\x07 is in {world.multiworld.get_player_name(location.player)} \x0d{location.name[:80]}\x0d.".upper()
    else:
        text = f"Woth item \x07{location.item.name[:40]}\x07 is in your \x0d{location.name}\x0d.".upper()
    for letter in text:
        if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?:;'S-()% \x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d":
            text = text.replace(letter, " ")
    return text

def parseMajorItemHint(world, location):
    """Write a major item hint for the given location."""
    text = ""
    if location.player != world.player:
        text = f"Looking for \x07{location.item.name[:40]}\x07? Ask {world.multiworld.get_player_name(location.player)} to try looking in \x0d{location.name[:80]}\x0d.".upper()
    else:
        text = f"Looking for \x07{location.item.name[:40]}\x07? Try looking in \x0d{location.name}\x0d.".upper()
    for letter in text:
        if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?:;'S-()% \x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d":
            text = text.replace(letter, " ")
    return text

def parseDeepHint(world, location):
    """Write a deep item hint for the given location."""
    text = ""
    if location.item.player != world.player:
        text = f"\x0d{location.name}\x0d has {world.multiworld.get_player_name(location.item.player)}'s \x07{location.item.name[:40]}\x07.".upper()
    else:
        text = f"\x0d{location.name}\x0d has your \x07{location.item.name}\x07".upper()
    for letter in text:
        if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?:;'S-()% \x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d":
            text = text.replace(letter, " ")
    return text