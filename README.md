# hap-client-metrics

Run this application to pull data from a HomeKit server (tested with homebridge.io) and publish available metrics to several metrics systems (only graphite implemented so far)

## Usage:

```
Usage: app.py [options]

Options:
  -h, --help            show this help message and exit
  -d DEVICE_ID, --device-id=DEVICE_ID
                        Device ID of the HomeKit server (looks like
                        A1:B2:C3:D4:E5:F6)
  -a ADDRESS, --address=ADDRESS
                        Address of the HomeKit server
  -p PORT, --port=PORT  Port of the HomeKit server
  -n PIN, --pin=PIN     PIN to pair with HomeKit
  -u, --autodiscover    Try to detect the HomeKit server and connect
                        automatically (needs the PIN)
  --config-folder=CONFIG_FOLDER
                        Folder to read config.json and store
                        pairing_data.json, config/ by default
  --graphite-enabled    Enable graphite output, it needs --graphite-hostname
                        to have a value
  --graphite-hostname=GRAPHITE_HOSTNAME
                        Graphite hostname to send metrics
  --graphite-port=GRAPHITE_PORT
                        Graphite port to send metrics, default: 2003
  --graphite-prefix=GRAPHITE_PREFIX
                        Graphite prefix to add to all metrics, default:
                        homekit
```

### Config folder

The config folder can be used to provide the HomeKit server configs without using the command line arguments. By default the config folder is `config/`

The `config.json` file looks like this:

```
{
    "device_id": "A1:B2:C3:D4:E5:F6",
    "address": "127.0.0.1",
    "port": 51826,
    "pin": "111-22-333"
}
```

the hap-client-metrics application will save another file named `pairingdata.json` to repair with the HomeKit server on subsequent runs. Do not delete this file or the application won't be able to talk to your HomeKit server.

### Running with docker

This is an example command t run as a docker container (recommended):

```
docker run -ti -v $HOME/.hap-client-metrics:/app/config cfiguerola/hap-client-metrics --graphite-enabled --graphite-hostname 192.168.11.102 --graphite-prefix homekit
```
