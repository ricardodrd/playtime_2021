const io = require("socket.io")();
const { prototype } = require("@serialport/parser-delimiter/lib");
const SerialPort = require("serialport");

// App setup
const PORT = 5000;

const port = new SerialPort("/dev/ttyACM1", {
  baudRate: 9600,
});

io.on("connection", function (socket) {
  socket.on("detections", function (detections) {
    io.sockets.emit("detections", detections)
    if (detections[0]) {
      // evaluate_detections_duck(detections[0].bbox)
      evaluate_position(detections[0].bbox);
    }
    else{
      console.log("no detections")
    }
  });
});

let index = 0;
function evaluate_position(bbox){
  console.log(index)
  if (index == 0){
    if((bbox.x + bbox.width) > 0.9 || (bbox.x < 0.1)) {
      console.log("ROTATE!")
      let midpoint = bbox.x + (bbox.width/2); 
      let difference = midpoint - 0.5;
      let rotation = calculate_rotation(difference);
      port.write(rotation.toString())
      index = -6
    }
  }
  //wait for the camera to move
  if (index < 0){
    index ++;
  }
}

function calculate_rotation(difference){
  //120 degrees camera
  let dn = difference * 120;
  console.log(dn)
  // converting to percentage of rotation for the stepper motor(100 is 180 degrees of the shield)
  return Math.round((dn * 100) / 180);
}

let idx = 0;
let initial_detecion;
let duck_position = 0.5;
function evaluate_detections_duck(bbox){  
  console.log(idx);
  if (index == 0){
    difference = (bbox.x + (bbox.width/2)) - duck_position
    if(Math.abs(difference) > 0.2) {
      console.log("ROTATE!")
      let rotation = calculate_rotation(difference);
      port.write(rotation.toString())
      index = -7
    }
  }
  //wait for the camera to move
  if (index < 0){
    index ++;
  }
}

io.listen(PORT);
