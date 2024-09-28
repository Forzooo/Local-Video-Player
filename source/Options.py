import customtkinter
import CTkMessagebox
from TemplateManager import TemplateManager
from System import System
import ipaddress
import requests

class Options(customtkinter.CTkToplevel):
    "The Options class, which is a Toplevel of App, lets the user customize is experience when using the tool."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialization of the objects required by Options class
        self.templateManager = TemplateManager()  # Create the Template Manager object 
        self.system = System()  # Create the System object used to handle the options of the json

        # Configure the window
        self.title("Options")
        self.geometry("500x550")
        self.resizable(False, False)  # The window is not meant to be resized as the elements are not dynamically set

        # Configure the columns and the rows
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Template selection
        self.template_option_label = customtkinter.CTkLabel(master=self, text="Choose a template:", bg_color="transparent")
        self.template_option_label.grid(row=0, column=0)

        self.template_var = customtkinter.StringVar(value=self.templateManager.get_current_mode())  # String variable used to know which template has been chosen
        self.template_option_menu = customtkinter.CTkOptionMenu(master=self, values=self.templateManager.get_modes(), command=self.template_chosen, 
                                                                variable=self.template_var)
        self.template_option_menu.grid(row=0, column=1)

        # IP selection
        self.ip_selection_label = customtkinter.CTkLabel(master=self, text="Enter a new IP address:", bg_color="transparent")
        self.ip_selection_label.grid(row=1, column=0)

        self.ip_selection_entry = customtkinter.CTkEntry(master=self, placeholder_text="Default: 0.0.0.0")
        self.ip_selection_entry.grid(row=1, column=1)

        self.ip_selection_button = customtkinter.CTkButton(master=self, text="Save changes", command=self.save_ip_changes, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"))
        self.ip_selection_button.grid(row=1, column=2)

        # Port selection
        self.port_selection_label = customtkinter.CTkLabel(master=self, text="Enter a new port:", bg_color="transparent")
        self.port_selection_label.grid(row=2, column=0)

        self.port_selection_entry = customtkinter.CTkEntry(master=self, placeholder_text="Default: 5000")
        self.port_selection_entry.grid(row=2, column=1)

        self.port_selection_button = customtkinter.CTkButton(master=self, text="Save changes", command=self.save_port_changes, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"))
        self.port_selection_button.grid(row=2, column=2)

        # Check for new versions
        self.version = "1.0.7"
        self.check_version_button = customtkinter.CTkButton(master=self, text="Check for new versions", command=self.check_version, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"))
        self.check_version_button.grid(row=3, column=1)

        # Information about the tool
        self.infos_label = customtkinter.CTkLabel(master=self, text=f"Version: {self.version} \nAuthor: Forzo", bg_color="transparent")
        self.infos_label.grid(row=3, column=2)


    # Load the template chosen by the user
    def template_chosen(self, template: str):
        self.templateManager.load_mode(template)


    # Update the ip in the json
    def save_ip_changes(self):
        ip = self.ip_selection_entry.get()  # Retrieve the input from the entry

        # Check using the ipaddress library if the given input is an IPv4 address
        try:
            ipaddress.IPv4Address(ip)

        except ipaddress.AddressValueError as e:
            CTkMessagebox.CTkMessagebox(title="Error", message=e, icon="cancel")
            return

        self.system.write_json({"ip": ip})


    # Update the port in the json
    def save_port_changes(self):
        port = self.port_selection_entry.get()  # Retrieve the input from the entry

        # Convert the port to an integer
        try:
            port = int(port)

        except ValueError:
            CTkMessagebox.CTkMessagebox(title="Error", message="The port must be an integer.", icon="cancel")
            return

        if port < 0 or port > 65535:
            CTkMessagebox.CTkMessagebox(title="Error", message="The port must be between 0 and 65535.", icon="cancel")
            return
        
        self.system.write_json({"port": port})  # If the port is valid we can write it to the json

    # Check if the version of the tool is the latest one available on GitHub
    def check_version(self):
        
        # Obtain the data from the GitHub API of the Local Video Player repository
        repository_data = (requests.get("https://api.github.com/repos/Forzooo/Local-Video-Player/releases")).json() 

        latest_release = repository_data[0]  # Get the latest release from the json

        # Obtain the version of the latest release
        version = latest_release["tag_name"]

        # Check if the current version is the latest
        if self.version == version:
            CTkMessagebox.CTkMessagebox(title="Latest Version", message=f"You have the latest version available.")

        else:
            CTkMessagebox.CTkMessagebox(title="New Version", message=f"The version {version} is now available to be downloaded.")