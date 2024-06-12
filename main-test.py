import serial_port
import marlin

isProcessing = False

if __name__ == "__main__":
    serial_ports = serial_port.find_devices()
    print("\nUsing serial ports", serial_ports)
    serial_port_actuators = serial_ports.get("actuators")
    serial_port_camera = serial_ports.get("camera")
    while True:

        with marlin.serial_init(serial_port_actuators) as actuators:
            if isProcessing = True
            elif:
            marlin.move_conveyor(actuators, 0)
            marlin.move_servo(actuators, 0)
            marlin.idle_servo(actuators)