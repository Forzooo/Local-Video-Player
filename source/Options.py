import customtkinter
from TemplateManager import TemplateManager

class Options(customtkinter.CTkToplevel):
    "The Options class, which is a Toplevel of App, lets the user customize is experience when using the tool."

    def __init__(self, templateManager: TemplateManager, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Options")
        self.geometry("400x500")
        self.resizable(False, False) # The window is not meant to be resized as the elements are not dynamically set

        # Configure the columns and the rows
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Template selection
        self.template_option_label = customtkinter.CTkLabel(master=self, text="Choose a template: ", bg_color="transparent")
        self.template_option_label.grid(row=0, column=0)

        self.templateManager = templateManager # Use the templateManager of the class App as the same object for this class

        self.template_var = customtkinter.StringVar(value=self.templateManager.get_current_mode()) # String variable used to know which template has been chosen
        self.template_option_menu = customtkinter.CTkOptionMenu(master=self, values=self.templateManager.get_modes(), command=self.template_chosen, 
                                                                variable=self.template_var)
        self.template_option_menu.grid(row=0, column=1)

        # Informations about the tool
        self.infos_label = customtkinter.CTkLabel(master=self, text="Version: 1.0.2 \nAuthor: Forzo", bg_color="transparent")
        self.infos_label.grid(row=3, column=1)


    # Load the template chosen by the user
    def template_chosen(self, template: str):
        self.templateManager.load_mode(template)