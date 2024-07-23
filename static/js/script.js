document.addEventListener("DOMContentLoaded", function() {  
    const video = document.getElementById('video');
    const display = document.getElementById('display');
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({  
            video: true, audio: true
        }).then(function(stream) {
            console.log(stream,'444');  
            video.srcObject = stream;
            video.play();
            // Handle the video stream  
        }).catch(function(error) {  
            console.error("Error accessing media devices.", error);  
        });
    }
    const socket = io.connect('http://localhost:5000/');  
    socket.onopen = () => {
        console.log('WebSocket connection established');
    };
    socket.on('connect', () => {  
        console.log('WebSocket connection established');
        socket.send('Hello from client!'); // Optional: Send a message to the server on connect  
    });
    socket.on('message', (data) => {
        // If data is an image string, set it to the img element  
        if (data.startsWith('data:image/jpeg;base64,' )) {  
            console.log(data,'3333333');
            display.src = data;
            // display.play();
            // display.src = data; // Set the source of the img to the incoming data  
        }  
    });  

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    function sendFrame() {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataURL = canvas.toDataURL('image/jpeg');
        socket.send(dataURL);
        requestAnimationFrame(sendFrame);
    }
    
    video.addEventListener('play', () => {
        console.log(33333333333333333333);
        requestAnimationFrame(sendFrame);
    });
})
