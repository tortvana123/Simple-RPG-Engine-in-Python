# Cell-Based Text-Adventure Engine
# A text game engine, with a simple GUI interface, 
# made with the intent of making these games as easy as possible to make.
# Author: Alex Vreimann
# Licence: MIT


# --------
# Imports
# --------

from appJar import gui # Current version 0.90.0
import ruamel.yaml as yaml # Current version 0.15.35

# --------
# Dictionary pointing to the config file filenames.
# --------

files = {"general_data" : "general_data.yaml"}
character = {}

# -------
# Functions
# -------

# --------
# YAML de-/serializing, compatible with older and newer versions of ruamel.yaml (Works with 0.15.35)
# --------

def yaml_io(action, istream):  # ser_type - "serialize" data into YAML or "deserialize" data from YAML; istream - input data
    ostream = ""
    yml = yaml.YAML(typ='safe', pure=True) # Using the new syntax.
    if action == "deserialize":
        ostream = yml.load(istream)
        return ostream
    elif action == "serialize":
        yml.dump(istream, ostream)
        return ostream


# --------
# Setup
# --------

def setup():
    # ----
    # Loading data from config files
    # ----

    # Enable access to the files variable
    global files
    
    # Set title
    app.setTitle("Loading...")
    app.addLabel("current", " ")
    
    # Open and load data from files
    app.setLabel("current", "Loading general data...")
    global general_data
    with open(files["general_data"]) as yaml_data:
        general_data = yaml_io("deserialize", yaml_data)

    # ----
    # Setting up neccesary variables
    # ----
    app.setLabel("current", "Setting up variables...")
    global stat_points
    stat_points = general_data["stat_points_default"]
    
# ----
# Title screen
# ----
def title_screen():
    app.removeAllWidgets()
    app.setTitle(general_data["game_title"])
    app.addLabel("title_label", general_data["title_label"])
    app.addLabel("title_description", general_data["title_description"])
    app.addButton("Start Game", title_btn)
    app.addButton("Quit", title_btn)

def title_btn(button):
    if button == "Start Game": # TBD: Implement save system
        character_name()
    elif button == "Quit":
        raise SystemExit

# ----
# Character Creation
# ----

def character_name():
    app.removeAllWidgets()
    app.addLabel("entry_label", "What is your name?")
    app.addEntry("Name")
    app.addButton("Continue", character_stats)
    app.enableEnter(character_stats)
    
def stats_button(btn):
    current_stat = app.getSpinBox("Current stat: ")
    global stat_points
    if stat_points != 0: # If stat point pool isn't empty
        if character[current_stat] == 0:  # If the current stat is empty
            if btn == "+":
                app.setLabel(current_stat, current_stat + " {}".format(character[current_stat] + 1))
                character[current_stat] += 1
                app.setLabel("Points", "Available points: {}".format(stat_points - 1))
                stat_points -= 1
            else:
                pass
        elif character[current_stat] == 10:
            if btn == "-":
                app.setLabel(current_stat, current_stat + " {}".format(character[current_stat] - 1))
                character[current_stat] -= 1
                app.setLabel("Points", "Available points: {}".format(stat_points + 1))
                stat_points += 1
            else:
                pass
        else: 
            if btn == "+":
                app.setLabel(current_stat, current_stat + " {}".format(character[current_stat] + 1))
                character[current_stat] += 1
                app.setLabel("Points", "Available points: {}".format(stat_points - 1))
                stat_points -= 1
            elif btn == "-":
                app.setLabel(current_stat, current_stat + " {}".format(character[current_stat] - 1))
                character[current_stat] -= 1
                app.setLabel("Points", "Available points: {}".format(stat_points + 1))
                stat_points += 1
    else: # If the stat points pool is empty
        if character[current_stat] == 10:
            if btn == "-":
                app.setLabel(current_stat, current_stat + " {}".format(character[current_stat] - 1))
                character[current_stat] -= 1
                app.setLabel("Points", "Available points: {}".format(stat_points + 1))
                stat_points += 1
            else:
                pass
        else: 
            pass 
            
def character_stats():
    character["Name"] = app.getEntry("Name") # Saves the name from the last function
    app.removeAllWidgets()
    app.addLabel("Choose your stats:")
    app.addLabelSpinBox("Current stat: ", general_data["stats"])
    app.addButton("+", stats_button)
    app.addButton("-", stats_button)
    for i in general_data["stats"]:
        app.addLabel(i, i + " {}".format(0))
        character[i] = 0
    app.addLabel("Points", "Available points: {}".format(stat_points))
    app.addButton("Print character data", test)

def test(btn):
    print(character)

# --------
# Compatibility for importing this script as a module.
# --------

if __name__ == "__main__":
    with gui() as app:
        setup()
        title_screen()

