import tkinter, tkinter.messagebox, customtkinter
from tkinter import filedialog
from VideoPlayer import VideoPlayer
from LocalVideo import LocalVideo
from TemplateManager import TemplateManager # Currently not implemented as wanted

# Set the mode and the theme of the Local Video Player GUI
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.videos_list = [] # The video list that will have for every file an object, that contains the path of the video, of the class of it's source (LocalVideo, ...)
        self.videos_label_list = [] # The list where every video label is kept
        self.button_list = [] # The list where every button to delete a specific video is kept

    def add_item(self, item):
        # When multiple sources will be added the add_item function will need to recoded

        local_video = LocalVideo(item)

        video_name_label = customtkinter.CTkLabel(self, text=f"Local: {local_video.get_video_name()}", compound="left", padx=5, anchor="w")
        remove_button = customtkinter.CTkButton(self, text="Delete", width=100, height=24, command=lambda: self.command(item)) # Set the command of the button to App.delete_video

        video_name_label.grid(row=len(self.videos_list), column=0, pady=(0, 10), sticky="w")
        remove_button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)

        self.videos_list.append(local_video)
        self.videos_label_list.append(video_name_label)
        self.button_list.append(remove_button)

    def remove_item(self, item):
        for video in self.videos_list:
            if item == video.video_path:
                index = self.videos_list.index(video) # Get the index used to remove the video, the video_label and the button: is required that those three list are synchronized
                
                self.videos_list[index].delete() # Delete the video from the Flask videos folder
                self.videos_label_list[index].destroy() # Remove the video label from the frame
                self.button_list[index].destroy() # Remove the button from the frame

                # Remove the video from the lists
                self.videos_list.pop(index)
                self.videos_label_list.pop(index)
                self.button_list.pop(index)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.videoPlayer = VideoPlayer() # Create the Video Player object used to manage the webserver
        templateManager = TemplateManager() # Currently not implemented as wanted: it will be in the options
        templateManager.load_mode("normal_mode") # As now the user has to use the normal_mode as the template for the server


        self.title("Local Video Player")
        self.geometry(f"{1200}x{580}")
        self.resizable(False, False) # Currently the elements of the GUI are not dinamically resized thus to avoid this error the size of Local Video Player is fixed

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.video_list_frame = ScrollableLabelButtonFrame(master=self, width=900, command=self.delete_video, corner_radius=0) # Crete the list of the video entered by the user
        self.video_list_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.add_video_button = customtkinter.CTkButton(master=self, text="Add a video", command=self.add_video, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"))
        self.add_video_button.grid(row=1, column=1, padx=(20, 20), pady=(0, 150))

        # The server button is dinamically set to start the server or to stop it based on the current status of the server
        self.server_button = customtkinter.CTkButton(master=self, text="Start server", command=self.server_button_execute, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"))
        self.server_button.grid(row=1, column=1, padx=(20, 20), pady=(0, 50))

        # Currently the options are not developed yet, so the button is disabled
        self.options_button = customtkinter.CTkButton(master=self, text="Options", command=self.show_options, fg_color="transparent", state="disabled", border_width=1, text_color=("gray10", "#DCE4EE"))
        self.options_button.grid(row=1, column=1, padx=(20, 20), pady=(50, 0))

        # This label lets the user know the address of the server when it's being executed
        self.server_address_label = customtkinter.CTkLabel(master=self, text="", bg_color="transparent")
        self.server_address_label.grid(row=2, column=0)

        # A temporary label to display the version and the author of the tool
        self.infos_label = customtkinter.CTkLabel(master=self, text="Version: 1.0.0 \nAuthor: Forzo", bg_color="transparent")
        self.infos_label.grid(row=3, column=1)

    # Add a video to the frame and to the server
    def add_video(self):

        # If the video source is local (The only one supported at the moment)
        video_path = filedialog.askopenfilenames(
        initialdir = "C:",
        title = "Select a video",
        filetypes = (("Video Extensions", "*.mp4;*.mkv;*.avi;*.flv;*.mov;*.wmv;*.vob;*.webm;*.3gp;*.ogv"),))
        
        # The video entered must be a path to a single video file
        if len(video_path) != 1 or video_path == "":
            return

        self.video_list_frame.add_item(str(video_path[0])) # Add the video to the list, which will also copy/move the video to the flask videos folder

    # This function is required as otherwise using only ScrollableLabelButtonFrame.remove_item won't work
    def delete_video(self, item):
        self.video_list_frame.remove_item(item) # item, at least for LocalVideo is the video_path obtained from App.add_video

    def server_button_execute(self):
        if self.videoPlayer.server == None:
            self.process = self.videoPlayer.start_thread() # Start the Flask server
            self.server_button.configure(text="Stop the server") # Set the text of the button as "Stop server"

            # Set a label below the video list to let the user know the address where the server is being executed
            self.server_address_label.configure(text=f"The server is running at the following address: {self.videoPlayer.ip}:{self.videoPlayer.port}") 

        else:
            self.process = self.videoPlayer.stop_thread() # Stop the Flask server
            self.server_button.configure(text="Start the server") # Set the text of the button as "Start server"

            # As the server is not running anymore let the label of the server address be blank
            self.server_address_label.configure(text="")
        
    def show_options(self):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()