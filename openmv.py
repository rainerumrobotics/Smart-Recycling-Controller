from serial import Serial

def serial_init(serial_port_actuators: str) -> Serial:
    from time import sleep
    print("\nOpenMV firmware camera & LED reset ...")
    serial = Serial(serial_port_actuators, 921600, timeout = 1)
    sleep(1) # Attend serial port MCU reset signal
    try:
        print(serial.read_all().decode("utf-8"), end = "")
    except:
        pass
    return serial

def stop_script():
    # TODO: https://github.com/openmv/openmv/blob/master/tools/pyopenmv.py
    pass # __serial.write(struct.pack("<BBI", __USBDBG_CMD, __USBDBG_SCRIPT_STOP, 0))