import os, shutil
from System import System

class TemplateManager:
    "The Template Manager class allows the user to choose between various version of the scripts used by Local Video Player. \n\nIn future it will allow the user to load its custom ones."

    def __init__(self):
        # To avoid redundancy define as constants the path of HTML and CSS/JS directories
        self.HTML_PATH = os.getcwd() + "/_internal/templates/"
        self.STATIC_PATH = os.getcwd() + "/_internal/static/"

        # To get the first mode selected we read it from the "settings.json" file using the System object
        self.system = System()
        self.mode = self.system.read_json("template")[0]  # The current mode used by the server. 
                                                          # It's formatted as the absolute path of the directory inside the Local Video Player templates
                                                          # Thus to get only the name it's requred to use the function get_current_mode

        self.modes = None  # Define modes as the dictionary of all the available modes inside Local Video Player templates directory
        self.read_modes()  # Read all the modes available

    # Read all the modes available to use: all the files come with the source code, so they won't be written by the script itself.
    # This in future will allow the user to import by himself it's own modes without having to modify the script
    def read_modes(self):
        modes_name = os.listdir("./_internal/lvp_templates/")  # Get all the templates folders available
        self.modes = {mode_name: os.getcwd() + "/_internal/lvp_templates/" + mode_name + "/" for mode_name in modes_name}

    # Return the name of the mode used by the server
    def get_current_mode(self) -> str:
        return self.mode.split("/")[-2]  # The name of the directory is the second last as the last is '' because the path is ".../mode_name/"
    
    # Update, if new modes have been added, and then return a list providing all the names of the modes available
    def get_modes(self) -> list:
        self.read_modes()
        return list(self.modes.keys())

    # Load the new mode chosen by the user in the options of Local Video Player
    def load_mode(self, user_choice: str):
        self.mode = self.modes[user_choice]  # Set the current mode by the one choosed by the user from the options
        self.system.write_json({"template": self.modes[user_choice]})  # Update the json to the new template being used

        self.delete_mode()  # Delete the files of the previous mode

        # Iterate through the files inside the template chosen by the user
        for file in os.listdir(self.mode):

            # Copy every html file inside the chosen template folder to the Flask templates folder
            # Copy every css and javascript file inside the chosen template folder to the Flask static folder
            # Every other file is ignored

            if file.endswith(".html"):
                shutil.copyfile(self.mode + file, self.HTML_PATH + file)

            elif file.endswith((".css", ".js")):
                shutil.copyfile(self.mode + file, self.STATIC_PATH + file)

    # This function looks if any mode is loaded, without knowing which one
    def is_loaded(self) -> bool:
        html_flag = 0  # Counts how many html files are inside the html directory
        static_flag = 0  # Counts how many css and jss files are inside the static directory

        for file in os.listdir(self.HTML_PATH):
            if file.endswith(".html"):
                html_flag += 1

        for file in os.listdir(self.STATIC_PATH):
            if file.endswith(".css") or file.endswith(".jss"):
                static_flag += 1

        # If there is at least one html file and two static files then it's assumed that in the directories there is a template ready to be used
        return True if html_flag > 0 and static_flag > 1 else False


    def delete_mode(self):
        # Look for all the html files inside the Flask templates folder and delete them
        for file in os.listdir(self.HTML_PATH):
            if file.endswith("html"):
                os.remove(self.HTML_PATH + file)  # The file can be removed without losing anything since it has been copied from the Local Video Player
                                                  # templates folder

        # Look for all the css and javascript files inside the Flask static folder and delete them
        for file in os.listdir(self.STATIC_PATH):
            if file.endswith(("css", "js")):
                os.remove(self.STATIC_PATH + file)  # The file can be removed without losing anything since it has been copied from the Local Video Player
                                                    # templates folder