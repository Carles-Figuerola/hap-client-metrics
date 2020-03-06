import re
import sys

def c_to_f(c):
    return (c * 9. / 5. ) + 32


def f_to_c(f):
    return 5. / 9. * (f  - 32)


def clean_string_key(string):
    return re.sub('[^A-Za-z0-9]+', '_', string).lower().strip('_')


def clean_value(value):
    if type(value) == str:
        return re.sub('[^A-Za-z0-9]+', '_', value).strip('_')
    else:
        return value


def parse_data(data_blob):
    output = {}
    for accessory in data_blob['accessories']:
        device = {}
        for service in accessory['services']:
            if service['type'].startswith('public.hap.service'):
                service_type = service['type'].split('.')[-1]
                device[service_type] = {}
                for characteristic in service['characteristics']:
                    if characteristic['type'] == "public.hap.characteristic.identify":
                        continue
                    try:
                        device[service_type][clean_string_key(characteristic['description'])] = clean_value(characteristic['value'])
                    except KeyError as e:
                        print(f"Characteristic {characteristic['description']} does not have a value")
        output[device['accessory-information']['name'].lower()] = device
    return output

if __name__ == "__main__":
    import json
    with open(sys.argv[1]) as fd:
        data_blob = json.load(fd)
    data = parse_data(data_blob)
    print(json.dumps(data))
