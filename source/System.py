import json, os

class System:
    "The System class currently is used to handle all the JSON operations."

    def __init__(self) -> None:
        self.json_path = "./_internal/settings.json"
        self.create_json()

    
    # Create the json file used for the options
    def create_json(self):
        # We need to replicate the TemplateManager.read_modes function for the template key for compatibility
        body = {"version": "1.0.3", "template": f"{os.getcwd()}/_internal/lvp_templates/normal_mode/"}

        try:
            # Open the file in exclusive mode to raise FileExistError if the file already exist
            # In this way the file won't be overwritten
            with open(self.json_path, "x") as file:
                json.dump(body, file)   # Write content of the JSON to the file

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