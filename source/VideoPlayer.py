import os
import threading
import socket
from flask import Flask, render_template, request, abort
from werkzeug.serving import make_server
from System import System
from TemplateManager import TemplateManager


class VideoPlayer:
    """The Video Player class allows the creation and execution of a local Flask webserver."""

    def __init__(self, static_folder='static', template_folder='templates'):
        self.system = System()   # Create the system object used to retrieve the settings of the server

        self.app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
        self.server = None  # Set the attribute of the server to None as it's not running yet

        # We are using a thread to handle the server to let the GUI still be usable when the server is being executed
        self.thread = None
        
        self.ip = self.system.read_settings_element("ip")  # The ip of the server chosen by the user
        self.port = self.system.read_settings_element("port")  # The port of the server chosen by the user

        # Get either a list[Str] if whitelist is enabled, otherwise None
        self.whitelist = self.system.read_settings_element("whitelist")

        # Load, if a template is not loaded yet, the one defined inside settings.json
        template_manager = TemplateManager()
        del template_manager  # Delete the object as it's not used anymore

        # Define the routes of the server
        self.setup_routes()

    # It's required to have this function as otherwise the class attributes can't be called
    def setup_routes(self):

        # If the user has enabled a whitelist of IP addresses then check if the ip is inside it
        @self.app.before_request
        def check_whitelist():
            if self.whitelist[0]:  # Check if the whitelist is enabled
                if request.remote_addr not in self.whitelist[1]:  # Look for the IPs in the whitelist
                    abort(403)  # Raise error 403 and handle it

        # If the IP is not in the whitelist load the error 403 html file to let the client know
        @self.app.errorhandler(403)
        def not_in_whitelist(e):
            return render_template('error_403.html', error_code=403, client_ip=request.remote_addr), 403

        # Default app route 
        @self.app.route('/')
        def index():
            video_folder = os.path.join(self.app.static_folder, 'videos')

            # The extensions of the video file must be synchronized with the ones
            # of App.add_video and App.retrieve_videos

            videos = [video for video in os.listdir(video_folder) if video.endswith((".mp4", ".mkv", ".avi", ".flv",
                                                                                     ".mov", "wmv", ".vob", ".webm",
                                                                                     ".3gp", ".ogv",))]
            return render_template('index.html', videos=videos, version=self.system.version)

    def run(self):
        # If the SSL keys are entered by the user, then start the Flask server with it, otherwise use HTTP
        ssl_keys_path = self.system.read_settings_element("ssl_keys")

        if ssl_keys_path[0]:
            # Start the Flask server using HTTPS
            self.server = make_server(self.ip, self.port, self.app, ssl_context=(ssl_keys_path[1][0],
                                                                                 ssl_keys_path[1][1]))

        else:
            self.server = make_server(self.ip, self.port, self.app)  # Start the Flask server with HTTP
        
        self.server.serve_forever()

    def start_thread(self):
        self.thread = threading.Thread(target=self.run)
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
            return socket.gethostbyname(socket.gethostname())

        # Otherwise return the ip chosen
        return self.ip
