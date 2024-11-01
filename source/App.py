import customtkinter
import os
import CTkMessagebox
import pathlib
from tkinter import filedialog
from VideoPlayer import VideoPlayer
from LocalVideo import LocalVideo
from Settings import Settings
from System import System

# Set the mode and the theme of the Local Video Player GUI
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class VideoListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command  # Set the command of the frame to delete the video from the frame

        # The video list that will have for every file an object, that contains the path of the video
        # of the class of it's source (LocalVideo, ...)
        self.videos_list = []

        self.videos_label_list = []  # The list where every video label is kept
        self.button_list = []  # The list where every button to delete a specific video is kept

    def add_video(self, video: str, source: str):
        # sources supported: 
        # 'local': LocalVideo without move/copy operation
        # 'local-copy': LocalVideo with copy operation 
        # 'local-move': LocalVideo with move operation

        # 'local' without any operation currently is executed only with the function App.retrieve_videos
        if source == "local":
            local_video = LocalVideo(video)

        elif source == "local-copy":  # Check if the task, assuming the video is local, is to execute copy
            local_video = LocalVideo(video, task="copy")

        elif source == "local-move":  # Check if the task, assuming the video is local, is to execute copy
            local_video = LocalVideo(video, task="move")

        video_name_label = customtkinter.CTkLabel(self, text=f"Local: {local_video.get_video_name()}", compound="left",
                                                  padx=5, anchor="w")

        # Set the command of the button to App.delete_video
        remove_button = customtkinter.CTkButton(self, text="Delete", width=100, height=24,
                                                command=lambda: self.command(video))

        video_name_label.grid(row=len(self.videos_list), column=0, pady=(0, 10), sticky="w")
        remove_button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)

        self.videos_list.append(local_video)
        self.videos_label_list.append(video_name_label)
        self.button_list.append(remove_button)

    def remove_video(self, video: str):
        for video_o in self.videos_list:
            # Check if the path of the video is equal to the one of the object (video_o)
            if video == video_o.video_path:
                # Get the index used to remove the video, the video_label and the button: is required that
                # those three list are synchronized
                index = self.videos_list.index(video_o)

                self.videos_list[index].delete()  # Delete the video from the Flask videos folder
                self.videos_label_list[index].destroy()  # Remove the video label from the frame
                self.button_list[index].destroy()  # Remove the button from the frame

                # Remove the video from the lists
                self.videos_list.pop(index)
                self.videos_label_list.pop(index)
                self.button_list.pop(index)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Local Video Player")
        self.geometry(f"{1200}x{580}")

        # Create the flask directories here to prevent an issue involving: 'App.retrieve_videos'
        System.create_flask_directories()

        # Currently the elements of the GUI are not dynamically resized thus to avoid this error
        # the size of Local Video Player is fixed
        self.resizable(False, False)

        # Row and columns configure
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Create the frame of the video entered by the user
        self.video_list_frame = VideoListFrame(master=self, width=900, command=self.delete_video, corner_radius=0)
        self.video_list_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.retrieve_videos()  # Retrieve videos that are already inside the videos folder and add them to the frame

        self.add_video_button = customtkinter.CTkButton(master=self, text="Add a video", command=self.add_video,
                                                        fg_color="transparent", border_width=1,
                                                        text_color=("gray10", "#DCE4EE"))
        self.add_video_button.grid(row=1, column=1, padx=(20, 20), pady=(0, 150))

        # The server button is dynamically set to start the server or to stop it based
        # on the current status of the server
        self.videoPlayer = None  # Set the video player attribute to None as it's not created yet
        self.server_button = customtkinter.CTkButton(master=self, text="Start server",
                                                     command=self.server_button_execute, fg_color="transparent",
                                                     border_width=1, text_color=("gray10", "#DCE4EE"))
        self.server_button.grid(row=1, column=1, padx=(20, 20), pady=(0, 50))

        self.settings_button = customtkinter.CTkButton(master=self, text="Settings",
                                                       command=self.show_settings, fg_color="transparent",
                                                       border_width=1, text_color=("gray10", "#DCE4EE"))

        self.settings_button.grid(row=1, column=1, padx=(20, 20), pady=(50, 0))

        # This label lets the user know the address of the server when it's being executed
        self.server_address_label = customtkinter.CTkLabel(master=self, text="", bg_color="transparent")
        self.server_address_label.grid(row=2, column=0)

    # Add a video to the frame and to the server
    def add_video(self):

        # If the video source is local (The only one supported at the moment)
        video_paths = filedialog.askopenfilenames(
            initialdir="C:",
            title="Select a video",
            filetypes=(("Video Extensions", "*.mp4;*.mkv;*.avi;*.flv;*.mov;*.wmv;*.vob;*.webm;*.3gp;*.ogv;"),)
        )

        # The video entered must be a path to one or more files
        if video_paths == "":
            return

        else:
            for video_path in video_paths:
                option = CTkMessagebox.CTkMessagebox(title="Choose an option",
                                                     message="Do you want to copy or move the video: " + pathlib.Path(
                                                         video_path).stem,
                                                     icon="question", option_1="Copy", option_2="Move")

                # Add the video to the list, which will also copy/move the video to the flask videos folder
                self.video_list_frame.add_video(video_path, "local-" + option.get().lower())

    # This function is required as otherwise using only VideoListFrame.remove_video won't work
    def delete_video(self, video):
        self.video_list_frame.remove_video(video)  # video is the path obtained from App.add_video

    # This function is executed only at the start of the execution to retrieve videos
    # that are already in flask videos folder
    def retrieve_videos(self):
        files = os.listdir("./_internal/static/videos/")  # Get all the files inside the videos folder

        # Even if there should be only videos inside this folder, look for all the videos
        for file in files:
            if file.endswith((".mp4", ".mkv", ".avi", ".flv", ".mov", "wmv", ".vob", ".webm", ".3gp", ".ogv",)):
                self.video_list_frame.add_video(file, "local")  # Add the video to the list without copying/moving it

    def server_button_execute(self):

        if self.videoPlayer is None:
            self.videoPlayer = VideoPlayer()

            self.videoPlayer.start_thread()  # Start the Flask server
            self.server_button.configure(text="Stop the server")  # Set the text of the button as "Stop server"

            # Set a label below the video list to let the user know the address where the server is being executed
            system = System()

            # Check whether the SSL Keys are imported
            if system.read_settings_element("ssl_keys")[0]:
                self.server_address_label.configure(
                    text=f"The server is running at the following address: https://{self.videoPlayer.get_ip()}:{self.videoPlayer.port}")

            else:
                self.server_address_label.configure(
                    text=f"The server is running at the following address: http://{self.videoPlayer.get_ip()}:{self.videoPlayer.port}")

            del system  # Delete the System object as it's not used anymore

        else:
            self.videoPlayer.stop_thread()  # Stop the Flask server
            self.server_button.configure(text="Start the server")  # Set the text of the button as "Start server"

            # As the server is not running anymore set the label of the server address to be blank
            self.server_address_label.configure(text="")
            del self.videoPlayer
            self.videoPlayer = None

    def show_settings(self):
        settings_window = Settings()
        self.withdraw()  # Hide the App window until the Settings toplevel is destroyed

        # Wait until the toplevel is destroyed before redrawing the App again
        self.wait_window(settings_window)
        self.deiconify()


if __name__ == "__main__":
    app = App()
    app.mainloop()
