// Change current video to user-selected video
function change_video(event) {
    var video_selected = event.target.value; // Retrieve the video path from the video chosen
    var video_player = document.getElementById('video_player'); // Retrieve the video player from the html script
    var video_path = document.getElementById('video_path'); // Retrive the video path of the previous video selected
    video_path.src = video_selected; // Change the path of the video to the one chosen by the user
    video_player.load();

}

// Attach the event listener to the video combobox
document.getElementById('video_combobox').addEventListener('change', change_video);