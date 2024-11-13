import json
import os
import CTkMessagebox


class System:
    """The System class currently is used to handle all the operations made to files."""

    def __init__(self):
        # The Local Video Player path for settings, json and any other file
        self.lvp_path = os.getcwd()+"/_internal/LocalVideoPlayer/"

        self.settings_path = self.lvp_path+"/settings.json"
        self.templates_path = self.lvp_path+"/templates/"
        self.ssl_path = self.lvp_path+"/ssl/"

        # A temporary folder used to store temporary files, which are deleted every time the tool is launched
        self.temp_path = self.lvp_path+"/temp/"

        self.create_lvp_directories()  # Create the directories used by Local Video Player

        # "settings.json" file elements
        self.json_body = {
            "template": self.lvp_path+"/templates/normal_mode/",
            "ip": "0.0.0.0",
            "port": 5000,
            "ssl_keys": [False, [None, None]],
            "whitelist": [False, None]
        }

        self.version = "1.1.1"  # Define the current version of the tool

        self.create_settings()  # Create the settings file. The creation is skipped if it already exists
        self.update_settings()  # Check if the current settings has elements to be added

        self.clean_temp_dir()  # Clean the temporary folder

    # Create the directories required by Flask webserver
    # (Called by App class and VideoPlayer class instead of the constructor to avoid calling it every time)
    @staticmethod
    def create_flask_directories():
        try:
            # exist_ok = True is used to ignore 'WinError 183: Cannot create a file when that file already exists'
            os.makedirs("./_internal/static", exist_ok=True)
            os.makedirs("./_internal/static/videos", exist_ok=True)
            os.makedirs("./_internal/templates", exist_ok=True)

        except os.error as e:
            CTkMessagebox.CTkMessagebox(title="Error",
                                        message=f"The following error occurred while creating the server folders: {e}",
                                        icon="cancel")
            quit()  # Quit from the tool as these folders are required for the execution of the server            

    # Create the directories used by Local Video Player
    # The method is not defined as static, even if it's going to be called multiple times, because
    # the class itself is designed to handle the operations made inside these directories
    def create_lvp_directories(self):
        try:
            os.makedirs(self.lvp_path, exist_ok=True)
            os.makedirs(self.templates_path, exist_ok=True)
            os.makedirs(self.ssl_path, exist_ok=True)
            os.makedirs(self.temp_path, exist_ok=True)

        except os.error as e:
            CTkMessagebox.CTkMessagebox(title="Error",
                                        message=f"The following error occurred while creating the Local Video Player folders: {e}",
                                        icon="cancel")
            quit()  # Quit from the tool as these folders are required for the execution of the tool

    # Create the 'settings.json' file used for the settings of the tool
    def create_settings(self):
        # Open the file in exclusive mode to raise FileExistError if the file already exist
        # In this way the file won't be overwritten
        try:
            with open(self.settings_path, "x") as file:
                json.dump(self.json_body, file)   # Write content of the JSON to the file

        except FileExistsError:   # If the file already exist ignore the error and stop the function
            return

    # Read the 'settings.json' file and return the entire data (One key per time allowed)
    def read_settings(self) -> dict:

        with open(self.settings_path, "r") as file:
            file_data = json.load(file)

        return file_data

    # Read the 'settings.json' file and return the data requested (One key per call allowed)
    def read_settings_element(self, key: str):
        return self.read_settings()[key]

    # Write in the settings file the new data
    def write_settings(self, data: dict):

        # Read the current data of the file
        file_data = self.read_settings()

        # Update the local data obtained from the file
        for key in data.keys():
            file_data[key] = data[key]

        # Update the data of the settings file
        with open(self.settings_path, "w") as file:
            json.dump(file_data, file)

    # Update the old settings with the new elements added in the latest version
    def update_settings(self):

        # Read the current data of the json
        file_data = self.read_settings()

        # Check if all the elements of self.json_body are in the settings file
        if len(file_data.keys()) != len(self.json_body.keys()):

            # We need to add to the settings the new elements added
            for key in self.json_body.keys():
                if key not in file_data.keys():
                    file_data[key] = self.json_body[key]

        # Update the json with the new changes
        self.write_settings(file_data)

    # Clean the temporary directory every time the tool is launched
    def clean_temp_dir(self):
        files = os.scandir(self.temp_path)
        for file in files:
            os.remove(file)
