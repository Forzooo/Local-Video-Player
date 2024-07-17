import tkinter, tkinter.messagebox, customtkinter, os, CTkMessagebox, pathlib
from tkinter import filedialog
from VideoPlayer import VideoPlayer
from LocalVideo import LocalVideo
from TemplateManager import TemplateManager
from Options import Options

# Set the mode and the theme of the Local Video Player GUI
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.videos_list = [] # The video list that will have for every file an object, that contains the path of the video, of the class of it's source (LocalVideo, ...)
        self.videos_label_list = [] # The list where every video label is kept
        self.button_list = [] # The list where every button to delete a specific video is kept

    def add_video(self, video: str, source: str):
        # sources supported: 
        # 'local': LocalVideo without move/copy operation
        # 'local-copy': LocalVideo with copy operation 
        # 'local-move': LocalVideo with move operation

        if source == "local": # local without any operation currenly is executed only with the function App.retrieve_videos
            local_video = LocalVideo(video, None)

        elif source == "local-copy": # Check if the operation, assuming the video is local, is to execute copy
            local_video = LocalVideo(video, operation="copy")
        
        elif source == "local-move": # Check if the operation, assuming the video is local, is to execute copy 
            local_video = LocalVideo(video, operation="move")


        video_name_label = customtkinter.CTkLabel(self, text=f"Local: {local_video.get_video_name()}", compound="left", padx=5, anchor="w")
        remove_button = customtkinter.CTkButton(self, text="Delete", width=100, height=24, command=lambda: self.command(video)) # Set the command of the button to App.delete_video

        video_name_label.grid(row=len(self.videos_list), column=0, pady=(0, 10), sticky="w")
        remove_button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)

        self.videos_list.append(local_video)
        self.videos_label_list.append(video_name_label)
        self.button_list.append(remove_button)

    def remove_video(self, video: str):
        for video_o in self.videos_list:
            if video == video_o.video_path: # Check if the path of the video is equal to the one of the object (video_o)
                index = self.videos_list.index(video_o) # Get the index used to remove the video, the video_label and the button: is required that those three list are synchronized
                
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

        # The template manager needs to be created here as inside Options it would be destroyed every time: it would lose the current mode selected
        self.templateManager = TemplateManager()
        self.templateManager.load_mode("normal_mode") # The default template chosen is normal_mode which it's loaded at the start of the tool as the server  
                                                      # needs one template to be run. (It can be changed in Options)

        self.title("Local Video Player")
        self.geometry(f"{1200}x{580}")
        self.resizable(False, False) # Currently the elements of the GUI are not dinamically resized thus to avoid this error the size of Local Video Player is fixed

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.video_list_frame = ScrollableLabelButtonFrame(master=self, width=900, command=self.delete_video, corner_radius=0) # Crete the frame of the video entered by the user
        self.video_list_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.retrieve_videos() # Retrieve videos that are already inside the videos folder, and add them to the frame

        self.add_video_button = customtkinter.CTkButton(master=self, text="Add a video", command=self.add_video, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"))
        self.add_video_button.grid(row=1, column=1, padx=(20, 20), pady=(0, 150))

        # The server button is dinamically set to start the server or to stop it based on the current status of the server
        self.server_button = customtkinter.CTkButton(master=self, text="Start server", command=self.server_button_execute, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"))
        self.server_button.grid(row=1, column=1, padx=(20, 20), pady=(0, 50))

        self.options_window = None
        self.options_button = customtkinter.CTkButton(master=self, text="Options", command=self.show_options, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"))
        self.options_button.grid(row=1, column=1, padx=(20, 20), pady=(50, 0))

        # This label lets the user know the address of the server when it's being executed
        self.server_address_label = customtkinter.CTkLabel(master=self, text="", bg_color="transparent")
        self.server_address_label.grid(row=2, column=0)

    # Add a video to the frame and to the server
    def add_video(self):

        # If the video source is local (The only one supported at the moment)
        video_paths = filedialog.askopenfilenames(
        initialdir = "C:",
        title = "Select a video",
        filetypes = (("Video Extensions", "*.mp4;*.mkv;*.avi;*.flv;*.mov;*.wmv;*.vob;*.webm;*.3gp;*.ogv"),))
        
        # The video entered must be a path to one or more files
        if video_paths == "":
            return
    
        else:
            for video_path in video_paths:
                option = CTkMessagebox.CTkMessagebox(title="Choose an option", message="Do you want to copy or move the video: " + pathlib.Path(video_path).stem,
                        icon="question", option_1="Copy", option_2="Move")
                
                self.video_list_frame.add_video(video_path, "local-"+option.get().lower()) # Add the video to the list, which will also copy/move the video to the flask videos folder

    # This function is required as otherwise using only ScrollableLabelButtonFrame.remove_video won't work
    def delete_video(self, video):
        self.video_list_frame.remove_video(video) # video is the path obtained from App.add_video

    # This function is executed only at the start of the execution to retrieve videos that are already in flask videos folder
    def retrieve_videos(self):
        files = os.listdir("./_internal/static/videos/") # Get all the files inside the videos folder

        # Even if there should be only videos inside this folder, look for all the videos
        for file in files:
            if file.endswith((".mp4", ".mkv", ".avi", ".flv", ".mov", "wmv", ".vob", ".webm", ".3gp", ".ogv")):
                self.video_list_frame.add_video(file, "local") # Add the video to the list without copying/moving it

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
        if self.options_window is None or not self.options_window.winfo_exists():

            # The template manager needs to be in the parameters of Options as if it was created inside Options it would be destroyed 
            # every time: it would lose the current mode selected
            self.options_window = Options(self.templateManager) 
            self.options_window.focus()

        else:
            self.options_window.focus() # If the options windows exist and the button is clicked again then it the options window will be focused

if __name__ == "__main__":
    app = App()
    app.mainloop()