const io = require("socket.io-client");


const socket = io.connect('http://localhost:5000');
socket.emit('setPTZ', {
  ptz:
    { pan: 100, tilt: 1000 },
  angle: 'center'
});