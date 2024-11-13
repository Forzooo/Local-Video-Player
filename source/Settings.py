import customtkinter
import CTkMessagebox
import ipaddress
import requests
import os
import shutil
from TemplateManager import TemplateManager
from System import System
from tkinter import filedialog
from werkzeug.serving import make_ssl_devcert


class UserInputDialog(customtkinter.CTkToplevel):
    # In the constructor are required:
    # a title, used for the title of the window
    # the text for the label
    # textbox_data: a list containing the data which is written to the textbox at the creation of the object
    def __init__(self, title: str, label_text: str, textbox_data: list = None):
        super().__init__()

        # Save the following parameters to class attributes to use them in other methods
        self.windowTitle = title 
        self.textbox_data = textbox_data

        # Toplevel window configurations
        self.title(title)
        self.geometry("300x300")
        self.resizable(False, False)  # The window is not meant to be resized as the elements are not dynamically set

        # Configure the rows and columns of the toplevel
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Body of the window
        self.label = customtkinter.CTkLabel(master=self, text=label_text, bg_color="transparent", font=("", 18))
        self.label.grid(row=0, column=0, columnspan=2)  # Use column span to set it at the center

        self.textbox = customtkinter.CTkTextbox(master=self, width=200, height=200)
        self.textbox.grid(row=1, column=0, columnspan=2, sticky="nsew")  # Use column span to use all the space of row 2
        self.textbox_update()  # Update the textbox with the lines given in the parameters

        self.cancel_button = customtkinter.CTkButton(master=self, text="Cancel", command=self.cancel,
                                                     fg_color="transparent", border_width=1,
                                                     text_color=("gray10", "#DCE4EE"))
        self.cancel_button.grid(row=2, column=0)
        
        self.save_button = customtkinter.CTkButton(master=self, text="Save", command=self.save,
                                                   fg_color="transparent", border_width=1,
                                                   text_color=("gray10", "#DCE4EE"))
        self.save_button.grid(row=2, column=1)

    # Destroy the toplevel object if the user has chosen 'Cancel'
    def cancel(self):
        self.destroy()  

    # Save the changes made in the Textbox to the file
    def save(self):
        system = System()  # Create a System object to get the temporary path
        user_input = self.textbox.get("0.0", "end")  # Get all the data written inside the textbox
        # Write the data to a temp file
        with open(system.temp_path+self.windowTitle+".tmp", "x") as file:
            file.write(user_input)

        self.destroy()  # Destroy the object after the data has been saved

    # Add to the textbox the data given from the constructor, only at the creation of the object
    def textbox_update(self):
        if self.textbox_data is not None:
            for data in self.textbox_data:
                self.textbox.insert("0.0", data+"\n")  # Add the data given in the constructor to the textbox


class Settings(customtkinter.CTkToplevel):
    """The Settings class, which is a Toplevel of App, lets the user customize is experience when using the tool."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialization of the objects required by the Settings class
        self.templateManager = TemplateManager()  # Create the Template Manager object 
        self.system = System()  # Create the System object used to handle the file tasks

        # Configure the Settings window
        self.title("Settings")
        self.geometry("800x700")
        self.resizable(False, False)  # The window is not meant to be resized as the elements are not dynamically set

        # Configure the columns and the rows
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Template section
        self.template_option_label = customtkinter.CTkLabel(master=self, text="Choose a template:",
                                                            bg_color="transparent")
        self.template_option_label.grid(row=0, column=0)

        # A string variable used to know which template has been chosen
        self.template_var = customtkinter.StringVar(value=self.templateManager.get_name_current_template())
        self.template_option_menu = customtkinter.CTkOptionMenu(master=self,
                                                                values=self.templateManager.get_updated_templates(),
                                                                command=self.template_chosen,
                                                                variable=self.template_var)
        self.template_option_menu.grid(row=0, column=1)

        # IP section
        self.ip_selection_label = customtkinter.CTkLabel(master=self, text="Enter a new IP address:",
                                                         bg_color="transparent")
        self.ip_selection_label.grid(row=1, column=0)

        self.ip_selection_entry = customtkinter.CTkEntry(master=self, placeholder_text="Default: 0.0.0.0")
        self.ip_selection_entry.grid(row=1, column=1)

        self.ip_selection_button = customtkinter.CTkButton(master=self, text="Save changes",
                                                           command=self.save_ip_changes, fg_color="transparent",
                                                           border_width=1, text_color=("gray10", "#DCE4EE"))
        self.ip_selection_button.grid(row=1, column=2)

        # Port section
        self.port_selection_label = customtkinter.CTkLabel(master=self, text="Enter a new port:",
                                                           bg_color="transparent")
        self.port_selection_label.grid(row=2, column=0)

        self.port_selection_entry = customtkinter.CTkEntry(master=self, placeholder_text="Default: 5000")
        self.port_selection_entry.grid(row=2, column=1)

        self.port_selection_button = customtkinter.CTkButton(master=self, text="Save changes",
                                                             command=self.save_port_changes, fg_color="transparent",
                                                             border_width=1, text_color=("gray10", "#DCE4EE"))
        self.port_selection_button.grid(row=2, column=2)

        # SSL keys section
        self.ssl_keys_label = customtkinter.CTkLabel(master=self, text="Load SSL keys (Optional):",
                                                     bg_color="transparent")
        self.ssl_keys_label.grid(row=3, column=0)
        
        self.ssl_load_keys_button = customtkinter.CTkButton(master=self, text="Load Keys", command=self.load_ssl_keys,
                                                            fg_color="transparent", border_width=1,
                                                            text_color=("gray10", "#DCE4EE"))
        self.ssl_load_keys_button.grid(row=3, column=1)

        self.ssl_generate_keys_button = customtkinter.CTkButton(master=self, text="Generate keys",
                                                                command=self.generate_ssl_keys, fg_color="transparent",
                                                                border_width=1, text_color=("gray10", "#DCE4EE"))
        self.ssl_generate_keys_button.grid(row=3, column=2)

        self.ssl_keys_delete_button = customtkinter.CTkButton(master=self, text="Delete current keys",
                                                              command=self.delete_ssl_keys, fg_color="transparent",
                                                              border_width=1, text_color=("gray10", "#DCE4EE"))
        self.ssl_keys_delete_button.grid(row=3, column=3)

        self.ssl_keys_status_button = customtkinter.CTkButton(master=self, text="", command=self.ssl_keys_set_status,
                                                              fg_color="transparent", border_width=1,
                                                              text_color=("gray10", "#DCE4EE"))
        self.ssl_keys_set_button_text()
        self.ssl_keys_status_button.grid(row=3, column=4)

        # IP whitelist section
        self.whitelist_label = customtkinter.CTkLabel(master=self, text="IP Whitelist:", bg_color="transparent")
        self.whitelist_label.grid(row=4, column=0)

        self.whitelist_status_button = customtkinter.CTkButton(master=self, text="",
                                                               command=self.ip_whitelist_set_status,
                                                               fg_color="transparent", border_width=1,
                                                               text_color=("gray10", "#DCE4EE"))
        self.ip_whitelist_set_button_text()
        self.whitelist_status_button.grid(row=4, column=1)

        self.whitelist_modify_button = customtkinter.CTkButton(master=self, text="Modify whitelist",
                                                               command=self.ip_whitelist_modify, fg_color="transparent",
                                                               border_width=1, text_color=("gray10", "#DCE4EE"))
        self.whitelist_modify_button.grid(row=4, column=2)

        # Tool version section
        self.check_version_button = customtkinter.CTkButton(master=self, text="Check for new versions",
                                                            command=self.check_version, fg_color="transparent",
                                                            border_width=1, text_color=("gray10", "#DCE4EE"))
        self.check_version_button.grid(row=5, column=3)

        # Information about the tool section
        self.infos_label = customtkinter.CTkLabel(master=self, text=f"Version: {self.system.version} \nAuthor: Forzo",
                                                  bg_color="transparent")
        self.infos_label.grid(row=5, column=4)

    # Load the template chosen by the user
    def template_chosen(self, template: str):
        self.templateManager.load_template(template)

    # Update the ip in the json
    def save_ip_changes(self):
        ip = self.ip_selection_entry.get()  # Retrieve the input from the entry

        # Check using the ipaddress library if the given input is an IPv4 address
        try:
            ipaddress.IPv4Address(ip)

        except ipaddress.AddressValueError as e:
            CTkMessagebox.CTkMessagebox(title="Error", message=str(e), icon="cancel")
            return

        self.system.write_settings({"ip": ip})

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
        
        self.system.write_settings({"port": port})  # If the port is valid we can write it to the json

    # Open the file explorer to let the user choose the ssl keys for Flask
    def load_ssl_keys(self):
        
        # First delete the current keys to have only the current ones inside the directory
        # And do not show the messagebox to the user
        self.delete_ssl_keys(False)

        key_path = filedialog.askopenfilenames(
            initialdir="C:",
            title="Select the key file",
            filetypes=(("Key File", "*.pem;*.key;"),)
        )
        
        # The path entered cannot be empty
        if key_path == "":
            return
        
        key_path = key_path[0]  # Get the path as string instead of a list

        cert_path = filedialog.askopenfilenames(
            initialdir="C:",
            title="Select the certification file",
            filetypes=(("Certification File", "*.pem;*.cert;*.crt"),)
        )

        if cert_path == "":
            return
        
        cert_path = cert_path[0]  # Get the path as string instead of a list

        # Copy the two files to the SSL folder of Local Video Player
        try:
            shutil.copyfile(key_path, self.system.ssl_path+os.path.basename(key_path))
            shutil.copyfile(cert_path, self.system.ssl_path+os.path.basename(cert_path))

        except shutil.Error as e:
            CTkMessagebox.CTkMessagebox(title="SSL Keys",
                                        message=f"The following error occurred while trying to copy the file: {e}",
                                        icon="cancel")
            return  # Stop the function

        # Write the two files path to the settings
        self.system.write_settings({"ssl_keys": [True, [self.system.ssl_path+os.path.basename(cert_path),
                                                        self.system.ssl_path+os.path.basename(key_path)]]})

        CTkMessagebox.CTkMessagebox(title="SSL Keys", message="The SSL files have been saved.")
        self.ssl_keys_set_button_text()  # Update the text of the button

    # Generate the SSL keys using Werkzeug
    def generate_ssl_keys(self):
        # First delete the current keys to have only the new ones inside the directory
        # And do not show the messagebox to the user
        self.delete_ssl_keys(False)

        keys = make_ssl_devcert(self.system.ssl_path+"key")  # Generate the two files using Werkzeug and save the paths
        self.system.write_settings({"ssl_keys": [True, list(keys)]})  # Convert the keys to a list and write the paths
        CTkMessagebox.CTkMessagebox(title="SSL Keys", message="The SSL keys have been generated and saved.")
        self.ssl_keys_set_button_text()  # Update the text of the button

    # Remove from the 'settings.json' file the path to the files and delete them
    # Moreover do not show the messagebox only if requested
    def delete_ssl_keys(self, view=True):
        ssl_keys_path = self.system.read_settings_element("ssl_keys")[1]

        # Check if the key exist and delete it
        for key in ssl_keys_path:
            try:
                if os.path.exists(key):
                    os.remove(key)

            # TypeError happens only if the user hasn't saved any SSL file and uses the button to delete them
            except TypeError:
                return

        # Remove the current SSL keys from settings.json
        self.system.write_settings({"ssl_keys": [False, [None, None]]})

        # By default, the messagebox is shown, only in load_ssl_keys and generate_ssl_keys we need to not show it
        if view:
            CTkMessagebox.CTkMessagebox(title="SSL Keys", message="The SSL keys have been deleted.")

    def ssl_keys_set_button_text(self):
        if self.system.read_settings_element("ssl_keys")[0]:
            self.ssl_keys_status_button.configure(text="Disable")

        else:
            self.ssl_keys_status_button.configure(text="Enable")

    def ssl_keys_set_status(self):
        ssl_keys = self.system.read_settings_element("ssl_keys")  # Get the ssl keys from 'settings.json'
        if ssl_keys[0]:  # Check if the whitelist is enabled
            self.system.write_settings({"ssl_keys": [False, ssl_keys[1]]})  # Write the json with the same IP
        
        else:
            if ssl_keys[1][0] is None:
                CTkMessagebox.CTkMessagebox(title="Error",
                                            message="You cannot enable the SSL encryption if you don't have the SSL keys.",
                                            icon="cancel")

                return
            
            self.system.write_settings({"ssl_keys": [True, ssl_keys[1]]})

        self.ssl_keys_set_button_text()  # Update the text of the status button 

    # Change the label of the button self.whitelist_set_button on the current status of 'settings.json'
    def ip_whitelist_set_button_text(self):
        if self.system.read_settings_element("whitelist")[0]:
            self.whitelist_status_button.configure(text="Disable")

        else:
            self.whitelist_status_button.configure(text="Enable")

    # Change whether the whitelist is enabled or not: used by the VideoPlayer class
    def ip_whitelist_set_status(self):
        whitelist_key = self.system.read_settings_element("whitelist")  # Get the whitelist key from 'settings.json'
        if whitelist_key[0]:  # Check if the whitelist is enabled
            self.system.write_settings({"whitelist": [False, whitelist_key[1]]})  # Write the json with the same IP
        
        else:
            if whitelist_key[1] is None:
                CTkMessagebox.CTkMessagebox(title="Error",
                                            message="You cannot enable the whitelist if you don't have at least one IP in it.",
                                            icon="cancel")

                return
            self.system.write_settings({"whitelist": [True, whitelist_key[1]]})

        self.ip_whitelist_set_button_text()  # Update the text of the status button 

    # Modify the whitelist items using the class UserInputDialog
    def ip_whitelist_modify(self):

        # Get the current list of IP in the file to write them in the textbox
        ip_list = self.system.read_settings_element("whitelist")[1]
        title = "Modify Whitelist"  # The tile of the user input dialog

        # Create the dialog used to modify the whitelist
        user_input_whitelist = UserInputDialog(title=title, label_text="Modify Whitelist", textbox_data=ip_list)
        self.withdraw()  # Hide the settings window until the dialog has been closed (destroyed)

        # Wait until the toplevel is destroyed before executing the next lines of code
        self.wait_window(user_input_whitelist)

        # If the user has pressed 'Cancel' then the file won't exist and the function can be stopped
        try:
            with open(self.system.temp_path+title+".tmp", "r") as file:
                ip_list_textbox = file.readlines()

        except FileNotFoundError:
            self.deiconify()  # Show the options window again
            return

        os.remove(self.system.temp_path+title+".tmp")  # Delete the temporary file as it's not used anymore

        # Define IPs as an empty list because all the ip to be set for the whitelist are inside the textbox
        ip_list = []

        for ip in ip_list_textbox:
            ip = ip.strip("\n")  # Remove the '\n' character from the ip

            # If the ip is already in the list do not write it twice
            if ip not in ip_list:

                # Check if the IP is valid, otherwise ignore it
                try:
                    ipaddress.IPv4Address(ip)

                except ipaddress.AddressValueError:
                    continue

                ip_list.append(ip)  # Add the new ip as it's valid and not in the list yet

        # Update the JSON with the new changes
        self.system.write_settings({"whitelist": [self.system.read_settings_element("whitelist")[0], ip_list]})
        self.deiconify()  # Show again the Options window

    # Check if the version of the tool is the latest one available on GitHub
    def check_version(self):
        
        # Obtain the data from the GitHub API of the Local Video Player repository
        repository_data = (requests.get("https://api.github.com/repos/Forzooo/Local-Video-Player/releases")).json() 

        latest_release = repository_data[0]  # Get the latest release from the json

        # Obtain the version of the latest release
        version = latest_release["tag_name"]

        # Check if the current version is the latest
        if self.system.version == version:
            CTkMessagebox.CTkMessagebox(title="Latest Version", message=f"You have the latest version available.")

        else:
            CTkMessagebox.CTkMessagebox(title="New Version",
                                        message=f"The version {version} is now available to be downloaded.")
