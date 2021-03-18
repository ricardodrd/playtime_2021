// Import dependencies
const SerialPort = require("serialport");
const Readline = require("@serialport/parser-readline");

var readline = require('readline');
var log = console.log;

var rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const port = new SerialPort("/dev/ttyACM0", {
    baudRate: 9600,
});

var recursiveAsyncReadLine = function () {
  rl.question('Command: ', function (answer) {
    if (answer == 'exit') //we need some base case, for recursion
      return rl.close(); //closing RL and returning from function.
    log('Got it! Your answer was: "', answer, '"');
    if (answer == 'a'){
        port.write("20");
    }
    if (answer == 'd'){
        port.write("-20");
    }
    recursiveAsyncReadLine(); //Calling this function again to ask new question
  });
};

recursiveAsyncReadLine(); //we have to actually start our recursion somehow


// // Defining the serial port

// // The Serial port parser
// const parser = new Readline();
// port.pipe(parser);

// // Read the data from the serial port
// parser.on("data", (line) => console.log(line));

// // Write the data to the serial port
// port.write("ROBOT POWER ON");
// port.write("ROBOT POWER ON");