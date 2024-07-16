from flask import Flask, render_template
import os, threading, socket, CTkMessagebox
from werkzeug.serving import make_server

class VideoPlayer:
    "The Video Player class allows the creation and execution of a local Flask webserver."

    def __init__(self, static_folder='static', template_folder='templates'):
        self.createDirectories() # Create the directories required by the webserver

        self.app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
        self.server = None # Declare the variable of the Flask server
        self.thread = None # We will use a thread when the server is started to let the GUI still be usable when the server is being executed
        self.ip = None # The ip of the server, retrived after the server is being executed
        self.port = 5000 # The default port of the server
        self.setup_routes()

    # Create the directories required by Flask
    def createDirectories(self) -> None:
        try:
            os.makedirs("./_internal/static", exist_ok=True) # Ignore WinError 183: Cannot create a file when that file already exists
            os.makedirs("./_internal/static/videos", exist_ok=True)
            os.makedirs("./_internal/templates", exist_ok=True)

        except os.error as e: 
            CTkMessagebox(title="Error", message=f"The following error occured while creating the videos folder: {e}", icon="cancel")
            quit() # Quit as these folders are required for the execution of the server            
        
    def setup_routes(self):
        @self.app.route('/')
        def index():
            video_folder = os.path.join(self.app.static_folder, 'videos')
            videos = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]
            return render_template('index.html', videos=videos)
        
    def run(self):
        self.server = make_server('0.0.0.0', self.port, self.app)
        self.server.serve_forever()

    def start_thread(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
        self.get_ip() # Set the ip variable to the ip of the server

    def stop_thread(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None # Set the server to None as it's not running anymore
            self.ip = None # Set the ip to None as the server it's not running anymore

    def get_ip(self):
        self.ip = socket.gethostbyname(socket.gethostname())
