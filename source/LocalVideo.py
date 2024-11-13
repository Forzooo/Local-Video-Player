import os
import shutil
import pathlib


class LocalVideo:
    """The Local Video class lets the Local Video Player manage all the videos that are already in the user file
     system."""

    # Task is used to tell the constructor whether it needs to copy, move or do nothing about the video
    def __init__(self, video_path: str, task: None | str):
        self.video_path = video_path  # Set the path of the video

        # Get the directory of the tool: used to move the video into the server video directory
        self.server_video_directory = os.getcwd() + "/_internal/static/videos/"

        # Define the path where the video will be after it has been copied or moved
        self.local_video_path = self.server_video_directory + os.path.basename(self.video_path)

        # Check which task the LocalVideo object has to do
        if task == "copy":
            self.copy()

        elif task == "move":
            self.move()

    # Copy the video file to the server video directory.
    def copy(self):
        # Since shutil.copyfile requires as destination another file, and not a directory,
        # we need to get the filename of the video we want to copy
        shutil.copyfile(self.video_path, self.local_video_path)

    # Move the video file to the server video directory
    def move(self):
        shutil.move(self.video_path, self.server_video_directory)

    # When the user chooses to delete the video from the list, the files gets deleted
    def delete(self):
        os.remove(self.local_video_path)

    # Return the filename of the video
    def get_video_name(self) -> str:
        # stem removes only the last extension of the file
        return pathlib.Path(self.video_path).stem
