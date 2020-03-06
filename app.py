#!/usr/local/bin/python
from optparse import OptionParser
from hap_init import write_pairing_data, read_json_file, load_config, pair_homekit
from parse_lib import parse_data
from graphite_lib import send_data
import json
import logging as log

def parse_options():
    parser = OptionParser()
    parser.add_option("-d", "--device-id", dest="device_id", help="Device ID of the HomeKit server (looks like A1:B2:C3:D4:E5:F6)", default='')
    parser.add_option("-a", "--address", dest="address", help="Address of the HomeKit server", default='')
    parser.add_option("-p", "--port", dest="port", help="Port of the HomeKit server", default='')
    parser.add_option("-n", "--pin", dest="pin", help="PIN to pair with HomeKit", default='')
    parser.add_option("-u", "--autodiscover", dest="autodiscover", help="Try to detect the HomeKit server and connect automatically (needs the PIN)", default=False, action="store_true")
    parser.add_option("--config-folder", dest="config_folder", help="Folder to read config.json and store pairing_data.json, config/ by default", default="config/")
    parser.add_option("--graphite-enabled", dest="graphite_enabled", help="Enable graphite output, it needs --graphite-hostname to have a value", default=False, action="store_true")
    parser.add_option("--graphite-hostname", dest="graphite_hostname", help="Graphite hostname to send metrics", default='')
    parser.add_option("--graphite-port", dest="graphite_port", help="Graphite port to send metrics, default: 2003", default='2003')
    parser.add_option("--graphite-prefix", dest="graphite_prefix", help="Graphite prefix to add to all metrics, default: homekit", default='homekit')
    return parser.parse_args()


if __name__ == "__main__":
    (options, args) = parse_options()
    config_file = f"{options.config_folder}/config.json"
    config = load_config(config_file, options)

    pairing_data_file = f"{options.config_folder}/pairing_data.json"
    pairing_data = read_json_file(pairing_data_file)
    client = pair_homekit(config, pairing_data)

    data_blob = client.get_accessories()
    data = parse_data(data_blob)

    if options.graphite_enabled:
        if options.graphite_hostname == '':
            log.error("A hostname is needed if graphite sending is enabled")
            sys.exit(1) 
        send_data(data, options.graphite_hostname, options.graphite_port, options.graphite_prefix)
        log.info(f"Successfully sent metrics to graphite")

    # ToDo: add prometheus metrics, run a flask server to publish them
