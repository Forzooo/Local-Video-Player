import os
import shutil
from System import System


class TemplateManager:
    """The Template Manager class allows the user to choose between various version of the
     scripts used by Local Video Player."""

    def __init__(self):
        # To avoid redundancy define as constants the path of HTML and CSS/JS directories
        self.HTML_PATH = os.getcwd() + "/_internal/templates/"
        self.STATIC_PATH = os.getcwd() + "/_internal/static/"

        # To get the current selected we read it from the "settings.json" file using the System object
        self.system = System()

        # It's formatted as the absolute path of the directory inside the Local Video Player templates
        # Thus to get only the name it's required to use the method get_current_mode
        self.current_template = self.system.read_settings_element("template")

        # Define templates as the dictionary of all the available templates inside
        # Local Video Player templates directory
        self.templates = None
        self.read_templates()  # Read all the templates available

        # Load the current template
        self.load_template(self.get_name_current_template())

    # Read all the templates available to use: all the files come with the source code,
    # so they won't be written by the script itself.
    def read_templates(self):
        templates = os.listdir(self.system.templates_path)  # Get all the templates folders available
        self.templates = {template: self.system.templates_path + template + "/" for template in templates}

    # Return the name of the template used by the server
    def get_name_current_template(self) -> str:
        # The name of the directory is the second last as the last is '' because the path is ".../mode_name/"
        return self.current_template.split("/")[-2]

    # Check if new templates have been added and then return a list providing all the names of the templates available
    def get_updated_templates(self) -> list:
        self.read_templates()
        return list(self.templates.keys())

    # Load the new template chosen by the user in the Settings class
    def load_template(self, user_choice: str):
        # Set the current template by the one chosen by the user from the Settings class
        self.current_template = self.templates[user_choice]

        # Update the settings file with the new template chosen
        self.system.write_settings({"template": self.current_template})

        self.delete_template()  # Delete the files of the previous mode

        # Iterate through the files, using their relative path, inside the template chosen by the user
        for file in os.listdir(self.current_template):

            # Copy every HTML file to the Flask templates folder
            # Copy every CSS and JavaScript file to the Flask static folder
            # Every other file is ignored

            if file.endswith(".html"):
                shutil.copyfile(self.current_template + file, self.HTML_PATH + file)

            elif file.endswith((".css", ".js")):
                shutil.copyfile(self.current_template + file, self.STATIC_PATH + file)

    # Delete the current template loaded in the Flask directories
    def delete_template(self):
        # The file can be deleted without losing the template as it has been copied instead of being moved
        # Look for all the HTML files and delete them
        for file in os.listdir(self.HTML_PATH):
            if file.endswith("html"):
                os.remove(self.HTML_PATH + file)

        # Look for all the CSS and JavaScript files and delete them
        for file in os.listdir(self.STATIC_PATH):
            if file.endswith(("css", "js")):
                os.remove(self.STATIC_PATH + file)

    # This function looks if a template is already loaded, without knowing which one
    def is_loaded(self) -> bool:
        html_files = 0  # Counts how many html files are inside the html directory
        static_files = 0  # Counts how many css and jss files are inside the static directory

        for file in os.listdir(self.HTML_PATH):
            if file.endswith(".html"):
                html_files += 1

        for file in os.listdir(self.STATIC_PATH):
            if file.endswith(".css") or file.endswith(".jss"):
                static_files += 1

        # If there is at least one html file and two static files
        # then it's assumed that in the directories there is a template ready to be used
        return html_files > 0 and static_files > 1
