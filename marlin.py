from serial import Serial

def serial_init(serial_port_actuators: str) -> Serial:
    from time import sleep
    print("\nMarlin firmware stepper & servo motors reset ...")
    serial = Serial(serial_port_actuators, 250000, timeout = 1)
    sleep(1) # Attend serial port MCU reset signal
    try:
        print(serial.read_all().decode("utf-8"), end = "")
    except:
        pass
    return serial

def _transfer_command(serial_actuators: Serial, command: str):
    print("\n" + command, end = "")
    try:
        serial_actuators.write(bytes(command, "utf-8"))
        print(serial_actuators.read_until().decode("utf-8"), end = "")
    except:
        pass

def move_conveyor(serial_actuators: Serial, distance_mm: int):
    command = "G0 X" + str(distance_mm) + "\n"
    _transfer_command(serial_actuators, command)

def move_servo(serial_actuators: Serial, angle_deg: int):
    command = "M280 P0 S" + str(angle_deg) + "\n"
    _transfer_command(serial_actuators, command)

def idle_servo(serial_actuators: Serial):
    command = "M282 P0\n"
    _transfer_command(serial_actuators, command)