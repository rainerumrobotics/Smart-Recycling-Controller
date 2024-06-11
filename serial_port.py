DEVICES = {
    "actuators": "2341:0042", # Arduino Mega with Marlin firmware (Stepper + Servo)
    #"actuators": "1A86:7523", # Arduino Mega clone with Marlin firmware (Stepper + Servo)
    "camera": "2341:045F" # Nicla Vision with OpenMV image recognition (LED + Camera)
}

def find_devices(serial_port_devices: dict = DEVICES) -> dict:
    """
    Search for serial port devices with given { device_name: usb_id } dictionary.
    Returns a dictionary { device: port } with recognized devices.
    """
    from serial.tools.list_ports import grep
    devices = {}
    num_known_devices = 0
    print("\nFound following serial port devices using", serial_port_devices, "...")
    for device, usb_id in serial_port_devices.items():
        for port, desc, hwid in grep(usb_id):
            print(" -", device, "on", port, "as", desc, "with", hwid)
            devices.update({ device: port })
            num_known_devices += 1
    if num_known_devices == 0:
        print(" - None")
    print("Further unkown serial port devices ...")
    num_unknown_devices = 0
    for port, desc, hwid in grep(""):
        if port not in devices.values():
            print(" -", port, "as", desc, "with", hwid)
            num_unknown_devices += 1
    if num_unknown_devices == 0:
        print(" - None")
    return devices