function changeVideo() {
    var radios = document.getElementsByName('video');
    var selectedVideo = null;
    for (var i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            selectedVideo = radios[i].value;
            break;
        }
    }

    if (selectedVideo !== null) {
        var videoPlayer = document.getElementById('videoPlayer');
        var videoSource = document.getElementById('videoSource');
        videoSource.src = selectedVideo;
        videoPlayer.load();
        videoPlayer.play();
    }
}
