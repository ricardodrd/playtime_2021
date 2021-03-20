const sdkProvider = require('./sdkProvider');
const io = require("socket.io-client");
const { ArgumentParser } = require('argparse');

const parser = new ArgumentParser({
  description: 'Multicam SDK client'
});
parser.add_argument('-s', '--serial', { help: 'Camera serial number' });
parser.add_argument('-a', '--angle', { help: 'Camera angle' });
parser.add_argument('-server_ip', { help: 'Server ip adress', default: 'http://localhost' });
parser.add_argument('-server_port', { help: 'Server port', default: '5000' });

const args = parser.parse_args();

const socket = io.connect(`${args.server_ip}:${args.server_port}`);

const sendDetections = (detections) => {
  socket.emit('detections', detections);
}

socket.on('connect', () => {
  socketID = socket.id;
});

// SDK
const sdk = sdkProvider.getSDK(args.serial);
let camManager;

sdk.init();
sdk.on('ATTACH', async (cameraManager) => {
  camManager = cameraManager;
  const detectorOps = {
    objectFilter: ['head'],
    DOWS: true,
  };
  const detector = await cameraManager.getDetector(detectorOps);
  await detector.init();
  detector.on('DETECTIONS', detections => {
    sendDetections(detections);
  });

  process.on('SIGINT', async () => {
    console.log("\nClosing application gracefully");
    if (detector) {
      console.log('Destroying detector');
      await detector.destroy();
    }

    if (cameraManager) {
      console.log('Closing connection with the camera');
      await cameraManager.closeConnection();
    }
    console.log("\nTeardown completed! Application closed");
    process.exit();
  });
});
