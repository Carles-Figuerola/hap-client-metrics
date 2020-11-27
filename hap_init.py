#!/usr/bin/python
import os
from hapclient.client import HapClient
import json
import logging as log
import sys

def read_json_file(file):
    with open(file) as fd:
        try:
            content = json.load(fd)
        except json.decoder.JSONDecodeError as e:
            content = {}
    return content

def write_pairing_data(pairing_data, pairing_data_file):
    with open(pairing_data_file, 'w') as fd:
        json.dump(pairing_data, fd)

def wipe_pairing_data(pairing_data_file):
    with open(pairing_data_file, 'w') as fd:
        fd.write("")


def load_config(config_file, options):
    config = read_json_file(config_file)

    if options.device_id:
        config['device_id'] = options.device_id
    if options.address:
        config['address'] = options.address
    if options.port:
        config['port'] = options.port
    if options.pin:
        config['pin'] = options.pin
    if options.autodiscover:
        config['autodiscover'] = True
    else:
        config['autodiscover'] = False

    if options.autodiscover:
        if not 'pin' in config:
            log.error('pin is needed for autodiscovery')
            #sys.exit(1)
    else:
        if not all(x in config for x in ['device_id', 'address', 'port', 'pin']):
            log.error("Config file or flags do not have all required fields: [device_id, address, port, pin]")
            #sys.exit(1)

    return config


def pair_homekit(config, pairing_data, pairing_data_file):

    if pairing_data:
        client = HapClient(device_id=config['device_id'], pairing_data=pairing_data)
        log.info("Successfully paired with the device")
    else:
        if config['autodiscover']:
            devices = HapClient.discover()
            if len(devices) > 1:
                log.warn(f"Found more than one devices, choosing the first one: {devices[0]['id']}")
            log.info(f"Found Server: {devices[0]['id']}")
            client = HapClient(devices[0]['id'], address=devices[0]['address'], port=devices[0]['port'])
        else:
            client = HapClient(config['device_id'], address=config['address'], port=config['port'])

        pair_result = client.pair(config['pin'])
        if pair_result:
            log.info("Successfully paired with the device")
            write_pairing_data(client.pairing_data, pairing_data_file)
            log.info("Saved pairing data")
        else:
            log.error("Failed to pair with the device")

    return client

def unpair_homekit(client):
    client.unpair()
    return True
