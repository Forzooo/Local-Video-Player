import json
import os
import CTkMessagebox

class System:
    "The System class currently is used to handle all the JSON operations."

    def __init__(self) -> None:
        self.json_path = "./_internal/settings.json"

        self.create_flask_directories()  # Create the Flask directories used by the webserver
        self.create_json()  # Create the json file. The creation is skipped if it already exist
        self.update_json()  # Check if the current json has elements to be added


    # Create the directories required by Flask
    def create_flask_directories(self) -> None:
        try:
            # exist_ok = True is used to ignore 'WinError 183: Cannot create a file when that file already exists'
            os.makedirs("./_internal/static", exist_ok=True)
            os.makedirs("./_internal/static/videos", exist_ok=True)
            os.makedirs("./_internal/templates", exist_ok=True)

        except os.error as e: 
            CTkMessagebox.CTkMessagebox(title="Error", message=f"The following error occured while creating the server folders: {e}", icon="cancel")
            quit()  # Quit from the tool as these folders are required for the execution of the server            
        
    
    # Create the json file used for the options
    def create_json(self):
        # We need to replicate the TemplateManager.read_modes function for the template key for compatibility
        # body is a class variable because is used to update the json
        self.body = {"template": f"{os.getcwd()}/_internal/lvp_templates/normal_mode/", "ip": "0.0.0.0", "port": 5000}

        try:
            # Open the file in exclusive mode to raise FileExistError if the file already exist
            # In this way the file won't be overwritten
            with open(self.json_path, "x") as file:
                json.dump(self.body, file)   # Write content of the JSON to the file

        except FileExistsError:   # If the file already exist ignore the error and stop the function
            return
        
    
    # Read the json and return a tuple containing the data requested
    def read_json(self, keys: tuple) -> tuple:

        if type(keys) == str:  # We need to check if the keys are only one, and thus it is a string, to avoid KeyError
            keys = (keys, )   # Set the string at the index 0 of a tuple for compatibility

        with open(self.json_path, "r") as file:
            file_data = json.load(file)

        return tuple(file_data[key] for key in tuple(keys))  # Convert the generator to a tuple
    

    # Write in the json the new data
    def write_json(self, data: dict):

        # Read the current data of the json
        with open(self.json_path, "r") as file:
            file_data = json.load(file)

        # Update the local data obtained from the json
        for key in data.keys():
            file_data[key] = data[key]

        # Update the data of json file
        with open(self.json_path, "w") as file:
            json.dump(file_data, file)


    # Update the old json with the new elements added in the current version
    def update_json(self):

        # Read the current data of the json
        with open(self.json_path, "r") as file:
            file_data = json.load(file)

        # Check if all the elements of self.body are in the json file
        if len(file_data.keys()) != len(self.body.keys()):

            # We need to add to the json the new elements added
            for key in self.body.keys():

                if key not in file_data.keys():
                    file_data[key] = self.body[key]

        # Update the json with the new changes
        self.write_json(file_data)