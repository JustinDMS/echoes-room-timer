import dolphin_memory_engine as dme
from time import sleep

# Addresses
ROOM = 0x803DCD80
PTR_GAMESTATE = 0x803C5C9C
WORLD_OFFSET = 0x4
TIME_OFFSET = 0x48

# Twice per IGT frame (0.016s)
CHECK_INTERVAL = 0.008

# 8 frames / ~0.13 seconds
# Should be short enough to preserve accuracy and long enough to ignore small things like completing a scan
PAUSE_DETECT = 16 

# ID -> Room Name
TEMPLE_GROUNDS = {
     0 : "Landing Site",
     1 : "Service Access",
     2 : "Hive Access Tunnel",
     3 : "Path of Honor",
     4 : "Meeting Grounds",
     5 : "Hive Transport Area",
     6 : "Hive Chamber A",
     7 : "Hall of Honored Dead",
     8 : "Hall of Eyes",
     9 : "Temple Transport C",
    10 : "Industrial Site",
    11 : "Hive Chamber C",
    12 : "Hive Tunnel",
    13 : "Base Access",
    14 : "Path of Eyes",
    15 : "Agon Transport Access",
    16 : "Collapsed Tunnel",
    17 : "Hive Chamber B",
    18 : "Hive Save Station",
    19 : "Command Chamber",
    20 : "War Ritual Grounds",
    21 : "Abandoned Base",
    22 : "Windchamber Gateway",
    23 : "Torvus Transport Access",
    24 : "Transport to Agon Wastes",
    25 : "Temple Assembly Site",
    26 : "Hive Storage",
    27 : "Portal Site",
    28 : "Shrine Access",
    29 : "Grand Windchamber",
    30 : "Transport to Torvus Bog",
    31 : "Dynamo Chamber",
    32 : "Temple Transport B",
    33 : "Storage Cavern B",
    34 : "Plain of Dark Worship",
    35 : "Defiled Shrine",
    36 : "Gateway Access",
    37 : "Windchamber Tunnel",
    38 : "Ing Windchamber",
    39 : "Communication Area",
    40 : "Lake Access",
    41 : "00_scandummy",
    42 : "Sky Temple Gateway",
    43 : "GFMC Compound",
    44 : "Storage Cavern A",
    45 : "Trooper Security Station",
    46 : "Accursed Lake",
    47 : "game_end_part1",
    48 : "Fortress Transport Access",
    49 : "Sacred Bridge",
    50 : "game_end_part2",
    51 : "Transport to Sanctuary Fortress",
    52 : "Sacred Path",
    53 : "game_end_part3",
    54 : "Temple Transport A",
    55 : "Profane Path",
    56 : "game_end_part4",
    57 : "Phazon Pit",
    58 : "game_end_part5",
    59 : "Phazon Grounds",
    60 : "Reliquary Access",
    61 : "Reliquary Grounds",
    62 : "Ing Reliquary"
}
GREAT_TEMPLE = {
     0 : "Temple Transport A",
     1 : "Transport A Access",
     2 : "Temple Sanctuary",
     3 : "Transport C Access",
     4 : "Controller Transport",
     5 : "Transport B Access",
     6 : "Temple Transport C",
     7 : "Main Energy Controller",
     8 : "Temple Transport B",
     9 : "Sky Temple Energy Controller",
    10 : "Sanctum Access",
    11 : "Sanctum"
}
AGON_WASTES = {
     0 : "Transport to Temple Grounds",
     1 : "Plaza Access",
     2 : "Mining Plaza",
     3 : "Agon Map Station",
     4 : "Transit Station",
     5 : "Save Station A",
     6 : "Mining Station Access",
     7 : "Duelling Range",
     8 : "Mining Station B",
     9 : "Transport Center",
    10 : "Mining Station A",
    11 : "Dark Transit Station",
    12 : "Save Station 2",
    13 : "Ing Cache 4",
    14 : "Junction Site",
    15 : "Storage A",
    16 : "Mine Shaft",
    17 : "Trial Grounds",
    18 : "Portal Terminal",
    19 : "Transport to Torvus Bog",
    20 : "Crossroads",
    21 : "Temple Access",
    22 : "Central Station Access",
    23 : "Sand Cache",
    24 : "Portal Access A",
    25 : "Judgment Pit",
    26 : "Agon Temple",
    27 : "Trial Tunnel",
    28 : "Portal Site",
    29 : "Central Mining Station",
    30 : "Dark Agon Temple Access",
    31 : "Warrior's Walk",
    32 : "Save Station 1",
    33 : "Portal Access",
    34 : "Controller Access",
    35 : "Sandcanyon",
    36 : "Dark Agon Temple",
    37 : "Command Center Access",
    38 : "Battleground",
    39 : "Agon Energy Controller",
    40 : "Ventilation Area A",
    41 : "Dark Controller Access",
    42 : "Command Center",
    43 : "Double Path",
    44 : "Main Energy Controller",
    45 : "Transport to Sanctuary Fortress",
    46 : "Main Reactor",
    47 : "Dark Agon Energy Controller",
    48 : "Biostorage Access",
    49 : "Security Station B",
    50 : "Doomed Entry",
    51 : "Sand Processing",
    52 : "Storage D",
    53 : "Dark Oasis",
    54 : "Biostorage Station",
    55 : "Feeding Pit Access",
    56 : "Oasis Access",
    57 : "Save Station C",
    58 : "Hall of Stairs",
    59 : "Ing Cache 3",
    60 : "Security Station A",
    61 : "Storage B",
    62 : "Feeding Pit",
    63 : "Ventilation Area B",
    64 : "Save Station 3",
    65 : "Bioenergy Production",
    66 : "Watering Hole",
    67 : "Ing Cache 1",
    68 : "Bitter Well",
    69 : "Storage C",
    70 : "Phazon Site",
    71 : "Ing Cache 2"
}
TORVUS_BOG = {
     0 : "Transport to Temple Grounds",
     1 : "Temple Transport Access",
     2 : "Torvus Lagoon",
     3 : "Ruined Alcove",
     4 : "Portal Chamber",
     5 : "Path of Roots",
     6 : "Save Station A",
     7 : "Forgotten Bridge",
     8 : "Portal Chamber",
     9 : "Great Bridge",
    10 : "Cache A",
    11 : "Plaza Access",
    12 : "Abandoned Worksite",
    13 : "Dark Forgotten Bridge",
    14 : "Grove Access",
    15 : "Poisoned Bog",
    16 : "Venomous Pond",
    17 : "Temple Access",
    18 : "Torvus Map Station",
    19 : "Torvus Plaza",
    20 : "Dark Arena Tunnel",
    21 : "Putrid Alcove",
    22 : "Brooding Ground",
    23 : "Dark Falls",
    24 : "Torvus Grove",
    25 : "Dark Torvus Temple Access",
    26 : "Save Station 1",
    27 : "Torvus Temple",
    28 : "Dark Torvus Arena",
    29 : "Polluted Mire",
    30 : "Underground Tunnel",
    31 : "Meditation Vista",
    32 : "Dark Torvus Temple",
    33 : "Transport to Agon Wastes",
    34 : "Underground Transport",
    35 : "Controller Access",
    36 : "Gloom Vista",
    37 : "Ammo Station",
    38 : "Cache B",
    39 : "Dark Controller Access",
    40 : "Hydrodynamo Station",
    41 : "Torvus Energy Controller",
    42 : "Undertemple Shaft",
    43 : "Dark Torvus Energy Controller",
    44 : "Gathering Access",
    45 : "Training Access",
    46 : "Catacombs Access",
    47 : "Save Station B",
    48 : "Hydrodynamo Shaft",
    49 : "Main Energy Controller",
    50 : "Crypt Tunnel",
    51 : "Sacrificial Chamber Tunnel",
    52 : "Save Station 2",
    53 : "Undertemple Access",
    54 : "Gathering Hall",
    55 : "Training Chamber",
    56 : "Catacombs",
    57 : "Main Hydrochamber",
    58 : "Crypt",
    59 : "Sacrificial Chamber",
    60 : "Undertemple",
    61 : "Transit Tunnel South",
    62 : "Transit Tunnel West",
    63 : "Transit Tunnel East",
    64 : "Fortress Transport Access",
    65 : "Dungeon",
    66 : "Hydrochamber Storage",
    67 : "Undertransit One",
    68 : "Undertransit Two",
    69 : "Transport to Sanctuary Fortress"
}
SANCTUARY_FORTRESS = {
     0 : "Transport to Temple Grounds",
     1 : "Temple Transport Access",
     2 : "Sanctuary Entrance",
     3 : "Power Junction",
     4 : "Reactor Access",
     5 : "Reactor Core",
     6 : "Save Station A",
     7 : "Minigyro Chamber",
     8 : "Transit Station",
     9 : "Sanctuary Map Station",
    10 : "Hall of Combat Mastery",
    11 : "Main Research",
    12 : "Hive Portal Chamber",
    13 : "Agon Transport Access",
    14 : "Central Area Transport East",
    15 : "Culling Chamber",
    16 : "Central Area Transport West",
    17 : "Torvus Transport Access",
    18 : "Staging Area",
    19 : "Transport to Agon Wastes",
    20 : "Dynamo Works",
    21 : "Hazing Cliff",
    22 : "Central Hive East Transport",
    23 : "Unseen Way",
    24 : "Watch Station",
    25 : "Transport to Torvus Bog",
    26 : "Central Hive West Transport",
    27 : "Dynamo Access",
    28 : "Workers Path",
    29 : "Dynamo Storage",
    30 : "Hive Dynamo Works",
    31 : "Hive Reactor",
    32 : "Sentinel's Path",
    33 : "Watch Station Access",
    34 : "Grand Abyss",
    35 : "Aerial Training Site",
    36 : "Main Gyro Chamber",
    37 : "Sanctuary Temple",
    38 : "Hive Cache 3",
    39 : "Hive Dynamo Access",
    40 : "Hive Save Station 1",
    41 : "Hive Reactor Access",
    42 : "Hive Cache 1",
    43 : "Judgment Drop",
    44 : "Vault",
    45 : "Temple Security Access",
    46 : "Temple Access",
    47 : "Checkpoint Station",
    48 : "Save Station B",
    49 : "Controller Access",
    50 : "Hive Gyro Chamber",
    51 : "Entrance Defense Hall",
    52 : "Vault Attack Portal",
    53 : "Hive Temple",
    54 : "Aerie Transport Station",
    55 : "Sanctuary Energy Controller",
    56 : "Hive Temple Access",
    57 : "Hive Gyro Access",
    58 : "Hive Save Station 2",
    59 : "Hive Entrance",
    60 : "Hive Controller Access",
    61 : "Aerie Access",
    62 : "Main Energy Controller",
    63 : "Hive Ammo Station",
    64 : "Hive Energy Controller",
    65 : "Aerie",
    66 : "Hive Summit"
}

# ID -> Room Map
WORLD_MAP = {
    0x3BFA3EFF : TEMPLE_GROUNDS,
    0x863FCD72 : GREAT_TEMPLE,
    0x42B935E4 : AGON_WASTES,
    0x3DFD2249 : TORVUS_BOG,
    0x1BAA96C2 : SANCTUARY_FORTRESS
}

def get_mode():
    _m = input(
        "Enter 1 to enable pause detection\n"
        "This outputs the time when the in-game timer is paused (text boxes, cutscenes, etc)\n"
        )
    if _m.strip() == "1":
        print("Enabled")
        return 1

    print("Ignoring")
    return 0

def is_equal_approx(a, b, tolerance=0.001):
    if a == b:
        return True

    return abs(a - b) < tolerance

def get_room_name(world_id, room_id):
    return WORLD_MAP[world_id][room_id]

def get_world():
    addr = dme.follow_pointers(PTR_GAMESTATE, [WORLD_OFFSET])
    return dme.read_word(addr)

def get_room():
    return dme.read_word(ROOM)

def get_time():
    addr = dme.follow_pointers(PTR_GAMESTATE, [TIME_OFFSET])
    return dme.read_double(addr)

class MemoryWatcher:
    def __init__(self, read_func, callback):
        self.read_func = read_func
        self.callback = callback
        self.previous_value = None
        self.current_value = None

    # Returns True when value has changed
    def check(self):
        """Read memory and check if value has changed"""
        self.current_value = self.read_func()
        if self.previous_value is None:
            self.previous_value = self.current_value
            return False
        
        if self.current_value != self.previous_value:
            self.callback(self.previous_value, self.current_value)
            self.previous_value = self.current_value
            return True
        return False

def main():
    dme.hook()
    if not dme.is_hooked():
        print("Failed to hook dolphin!")
        return
    
    mode = get_mode()

    current_world = get_world()
    current_room = get_room()
    start_time = get_time()
    current_time = 0
    savestate_room = None

    # Pause detection
    time_check_counter = 0
    paused = False
    paused_room_printed = False
    prev_pause_time = 0

    ## Callbacks for MemoryWatchers

    def room_changed(old_room, new_room):
        nonlocal current_world, current_room, start_time, current_time, paused_room_printed, prev_pause_time, savestate_room
        room_time = get_time() - start_time

        # Load savestate detected
        if room_time < 0:
            savestate_room = get_room()
            paused_room_printed = False
            prev_pause_time = 0
        
        # Don't output if you're leaving the room that you went to after savestating
        # Also don't output if the time is 0 (elevator/portal cutscenes)
        elif not savestate_room == old_room and not is_equal_approx(room_time, 0):
            if mode == 1 and not is_equal_approx(prev_pause_time, 0): # Pause Detection Enabled
                print(f'   | {room_time - prev_pause_time:13.3f}')
            print(f'{room_time:7.3f}: {get_room_name(current_world, old_room)}')
            savestate_room = None
        
        current_world = get_world()
        current_room = get_room()
        start_time = get_time()
        current_time = 0
        paused_room_printed = False
        prev_pause_time = 0
    
    def time_changed(_old_time, new_time):
        nonlocal current_time, time_check_counter, paused
        current_time = new_time - start_time
        time_check_counter = 0
        paused = False

    room_watcher = MemoryWatcher(get_room, room_changed)
    time_watcher = MemoryWatcher(get_time, time_changed)
    
    ## Main loop

    print("\nScanning...")
    while True:
        room_watcher.check()
        if (
            mode == 1 and # Pause Detection Enabled
            room_watcher.current_value != savestate_room and # Player didn't just load a savestate
            not time_watcher.check() and # IGT has not changed
            not paused
            ):
            time_check_counter += 1
            if time_check_counter >= PAUSE_DETECT:
                paused = True

                if not paused_room_printed:
                    print(f'   | {get_room_name(current_world, current_room)}')
                    paused_room_printed = True
                
                # If it's the first pause, current_time == delta
                # Display current time in place of delta
                if is_equal_approx(prev_pause_time, 0):
                    print(f'   | {current_time:13.3f}')
                else:
                    print(f'   | {current_time:6.3f} {current_time - prev_pause_time:6.3f}')
                
                prev_pause_time = current_time
        
        sleep(CHECK_INTERVAL)

        

#=========================

if __name__ == '__main__':
    main()
