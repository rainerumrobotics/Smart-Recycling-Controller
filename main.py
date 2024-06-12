import serial_port
import marlin

if __name__ == "__main__":
    serial_ports = serial_port.find_devices()
    print("\nUsing serial ports", serial_ports)
    serial_port_actuators = serial_ports.get("actuators")
    serial_port_camera = serial_ports.get("camera")
    with marlin.serial_init(serial_port_actuators) as actuators:
        marlin.move_conveyor(actuators, 0)
        marlin.move_servo(actuators, 0)
        marlin.idle_servo(actuators)
        # TODO: attendi e poi sposta se necessario
        marlin.move_conveyor(actuators, 180)
        marlin.move_servo(actuators, 180)
        marlin.idle_servo(actuators)
