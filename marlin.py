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
    # put in relative positioning
    serial.write(bytes("G91\n", "utf-8"))
    return serial

def _transfer_command(serial_actuators: Serial, command: str):
    print("\n" + command, end = "")
    try:
        serial_actuators.write(bytes(command, "utf-8"))
        result = serial_actuators.read_until().decode("utf-8")
        print(result, end = "")
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

_command_finished_is_sent = False
def command_is_finished(serial_actuators: Serial) -> bool:
    """
    Usage: run some command such as: marlin.move_conveyor() and poll with
           marlin.command_is_finished()
           returns True once OK from M400 command is received
    """
    global _command_finished_is_sent
    command = "M400\n"
    old_timeout = serial_actuators.timeout
    if _command_finished_is_sent == False:
        serial_actuators.write(bytes(command, "utf-8"))
        #print("\n" + command, end = "")
        _command_finished_is_sent = True
    serial_actuators.timeout = 0.1
    text = serial_actuators.read_until().decode("utf-8")
    #print(text)
    result = "ok" in text
    if result == True:
        #print(text, end = "")
        _command_finished_is_sent = False
    serial_actuators.timeout = old_timeout
    return result