const HuddlyDeviceAPIUVC = require('@huddly/device-api-uvc').default;
const HuddlyDeviceAPIUSB = require('@huddly/device-api-usb').default;
const HuddlySdk = require('@huddly/sdk').default;

const getSDK = (serialNumber) => {
  const usbApi = new HuddlyDeviceAPIUSB({
    alwaysRetry: true,
  });
  const uvcApi = new HuddlyDeviceAPIUVC({
    enforceSupport: false,
  });

  const communicationMethods = ['usb', 'uvc'];

  const communicationApis = communicationMethods.map((cm) => {
    switch (cm) {
      case 'usb':
        return usbApi;
      case 'uvc':
        return uvcApi;
      default:
        throw new Error(`Unknown communication method requested:${cm}`);
    }
  });

  const sdk = new HuddlySdk(uvcApi, communicationApis,
    { serial: serialNumber }
  );

  return sdk;
};


module.exports = {
  getSDK
};