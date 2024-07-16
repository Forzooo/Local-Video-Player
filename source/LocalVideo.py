import os, shutil

class LocalVideo:
    "The Local Video class lets the Local Video Player manage all the videos that are already in the user file system."

    # Operation is required to tell the constructor whether it needs to copy/move the video
    def __init__(self, video_path: str, operation: bool):
        self.video_path = video_path # Set the path of the video

        self.player_directory = os.getcwd() # Get the directory of the script: used to copy/move the video into the server video directory
        self.server_video_directory = self.player_directory + "/_internal/static/videos/"
        
        # Define the path where the video will be after it has been copied or moved
        self.local_video_path = self.server_video_directory + os.path.basename(self.video_path) 

        if operation:
            # As of now the user can only get the video copied. In future versions the user will choose if he wants to copy it or move it.
            # self.move()
            self.copy()

    def copy(self):
        # Copy the video file to the server video directory. Since shutil.copyfile requires as destination another file, and not a directory,
        # we need to get the filename of the video we want to copy
        shutil.copyfile(self.video_path, self.local_video_path) 

    def move(self):
        # Move the video file to the server video directory
        shutil.move(self.video_path, self.server_video_directory)

    # When the user chooses to delete the video from the list, the files gets deleted
    def delete(self):
        os.remove(self.local_video_path)

    # Return the basename of the video
    def get_video_name(self) -> str:
        # Get the basename of the video file, remove the file extension, look for other dots in the name: if there are rewrite them in the final name
        return ".".join(os.path.basename(self.video_path).split(".")[:-1])