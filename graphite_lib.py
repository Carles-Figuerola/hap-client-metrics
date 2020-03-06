import graphyte

def get_timestamp():
    return datetime.now().strftime('%s')

def format_for_graphite(data):
    metrics = {}
    for accessory_name, service in data.items():
        for service_name, characteristics in service.items():
            if service_name == 'accessory-information':
                continue
            for characteristic_name, value in characteristics.items():
                if type(value) == str:
                    continue
                if type(value) == bool:
                    value = int(value)
                metrics[".".join([ accessory_name,
                                   service_name,
                                   characteristic_name ])] = value
    return metrics

def send_data(data, host, port, prefix):
    graphyte.init(host, prefix=prefix)
    for metric, value in format_for_graphite(data).items():
        print(f"Sending metric: {metric} with value: {value}")
        graphyte.send(metric, value)
    return True

if __name__ == "__main__":
    import json
    import sys
    if len(sys.argv) < 4:
        print(f"Usage to test this code:\n  {sys.argv[0]} graphite_host graphite_prefix data_file", file=sys.stderr)
        exit(1)
    with open(sys.argv[3]) as fd:
        data = json.load(fd)
    send_to_graphite(sys.argv[1], sys.argv[2], data)
