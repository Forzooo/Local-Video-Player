import os, threading, socket, CTkMessagebox
from flask import Flask, render_template
from werkzeug.serving import make_server
from System import System

class VideoPlayer:
    "The Video Player class allows the creation and execution of a local Flask webserver."

    def __init__(self, static_folder='static', template_folder='templates'):
        self.system = System()   # Create the system object used to retrieve the ip and port chosen by the user

        self.app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
        self.server = None  # Declare the variable of the Flask server
        self.thread = None  # We will use a thread when the server is started to let the GUI still be usable when the server is being executed
        
        self.ip = self.system.read_json("ip")[0]  # The ip of the server chosen by the user
        self.port = self.system.read_json("port")[0]  # The port of the server chosen by the user
        
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            video_folder = os.path.join(self.app.static_folder, 'videos')
            # The extensions of the video file must be synchronized with the ones of App.add_video and App.retrieve_videos
            videos = [f for f in os.listdir(video_folder) if f.endswith((".mp4", ".mkv", ".avi", ".flv", ".mov", "wmv", ".vob", ".webm", ".3gp", ".ogv",))]
            return render_template('index.html', videos=videos)

    def start_thread(self):
        self.server = make_server(self.ip, self.port, self.app)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()

    def stop_thread(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None  # Set the server to None as it's not running anymore

    def get_ip(self):
        # If the ip is assigned by Flask then it needs to be retrieved
        if self.ip == "0.0.0.0":
            return(socket.gethostbyname(socket.gethostname()))

        return self.ip  # Otherwise return the ip chosen