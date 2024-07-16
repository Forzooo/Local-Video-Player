import os, shutil

class TemplateManager:
    "The Template Manager class allows the user to choose between various version of the scripts used by Local Video Player. \n\nIn future it will allow the user to load its custom ones."

    def __init__(self):
        # To avoid redundancy define as constants the path of HTML and CSS/JS directories
        self.HTML_PATH = os.getcwd() + "/_internal/templates/"
        self.STATIC_PATH = os.getcwd() + "/_internal/static/"

        self.mode = None # The current mode used by the server. It's formatted as the absolute path of the directory inside the Local Video Player templates
                         # Thus to get only the name it's requred to use the function get_current_mode
        self.modes = None # Define modes as the dictionary of all the available modes inside Local Video Player templates directory
        self.read_modes() # Read all the modes available

    # Read all the modes available to use: all the files come with the source code, so they won't be written by the script itself.
    # This in future will allow the user to import by himself it's own modes without having to modify the script
    def read_modes(self):
        modes_name = os.listdir("./_internal/lvp_templates/") # Get all the templates available
        self.modes = {mode_name: os.getcwd() + "/_internal/lvp_templates/" + mode_name + "/" for mode_name in modes_name}

    # Return the name of the mode used by the server
    def get_current_mode(self) -> str:
        return os.path.basename(self.mode)
    
    # Update, if new modes have been added, and then return a list providing all the names of the modes available
    def get_modes(self) -> list:
        self.read_modes()
        return list(self.modes.keys())

    # Load the new mode chosen by the user in the options of Local Video Player
    def load_mode(self, user_choice: str):
        self.mode = self.modes[user_choice] # Set the current mode by the one choosed by the user from the options
        self.delete_mode() # Delete the files of the previous mode

        # Iterate through the files inside the template chosen by the user
        for file in os.listdir(self.mode):

            # If the file is the html script then we have to copy it to Flask templates folder;
            # If the file is the css or js script then we have to copy it to Flask static folder;
            # If other files are inside the template, even if there shouldn't be, they are ignored
            if file == "index.html":
                shutil.copyfile(self.mode + file, self.HTML_PATH + file)

            elif file == "styles.css" or file == "script.js":
                shutil.copyfile(self.mode + file, self.STATIC_PATH + file)


    def delete_mode(self):
        # Look for the existing "index.html" file inside the Flask templates folder and delete it
        for file in os.listdir(self.HTML_PATH):
            if file == "index.html":
                os.remove(self.HTML_PATH + file) # The file can be removed without losing anything since it has been copied from the Local Video Player
                                                 # templates folder

        # Look for the existing files "styles.css" and "script.js" inside the Flask static folder and delete them
        for file in os.listdir(self.STATIC_PATH):
            if file == "styles.css" or file == "script.js":
                os.remove(self.STATIC_PATH + file) # The file can be removed without losing anything since it has been copied from the Local Video Player
                                                 # templates folder