import device


def dev_list():
    device_list = [k[0] for v, k in enumerate(device.getDeviceList())]
    return device_list
