import itertools
import os
import sys

reach_values = {
    "Marquise de Cat": 10,
    "Lord of the Hundreds": 9,
    "Keepers in Iron": 8,
    "Underground Duchy": 8,
    "Eyrie Dynasties": 7,
    "Vagabond (first)": 5,
    "Riverfolk Company": 5,
    "Woodland Alliance": 3,
    "Corvid Conspiracy": 3,
    "Vagabond (second)": 2,
    "Lizard Cult": 2
}

reach_minimums = {
    2: 17,
    3: 18,
    4: 21,
    5: 25,
    6: 28
}

red_adset_factions = ["Marquise de Cat", "Lord of the Hundreds", "Keepers in Iron", "Underground Duchy", "Eyrie Dynasties"]

min_player_count = 2
max_player_count = 6

# SET UP CSV FILE HEADER (FIRST ROW).
file_output = "Num Players, Total Reach, Recommended Reach, Valid ADSET, " + ", ".join(reach_values) + "\n"

for num_players in range(min_player_count, max_player_count+1):
    player_combinations = list(itertools.combinations(reach_values, num_players))

    for combination in player_combinations:
        # SKIP INVALID COMBINATIONS.
        if "Vagabond (second)" in combination and "Vagabond (first)" not in combination:
            continue

        total_reach = sum(map(lambda faction: reach_values[faction], combination))

        file_output += str(num_players) + ", " + str(total_reach) + ", "

        # IS THIS A RECOMMENDED COMBINATION, AN "ADVENTUROUS" COMBINATION, OR NOT VIABLE?
        if total_reach >= reach_minimums[num_players]:
            file_output += "Yes, "
        elif total_reach >= 17:
            file_output += "Exp., "
        elif total_reach < 17: 
            file_output += "No, "

        # IS THIS A VALID COMBINATION USING ADVANCED SETUP (ADSET)?
        num_red_adset_factions = len(set(combination).intersection(red_adset_factions))
        if (num_players == 2 and num_red_adset_factions == 2) or (num_players >= 3 and num_red_adset_factions >= 1):
            file_output += "Yes, "
        else:
            file_output += "No, "

        faction_list = (", ".join(map(lambda faction: "YES" if (faction in combination) else "-", reach_values)))
        file_output += faction_list + "\n"

# OVERWRITE CSV FILE.
with open(os.path.join(sys.path[0], "combinations.csv"), "w+") as file:
    file.seek(0)
    file.write(file_output)
    file.truncate()

# PRINT FILE CONTENTS TO CONSOLE.
print(file_output)
