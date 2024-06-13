import serial_port
import serial
import marlin
import openmv
import pygame
import ui

_state_is_busy = False
def state_machine(actuators: serial.Serial, object: str):
    global _state_is_busy
    # objects from labels.txt
    #    "carta.class",
    #    "empty.class",
    #    "metallo.class",
    #    "plastica.class",
    #    "vetro.class"
    # print("State:", _state)
    if _state_is_busy == True:
        # wait until last command has finished
        if marlin.command_is_finished(actuators) == True:
            _state_is_busy = False
        return
    if object == "empty":
        #marlin.move_conveyor(actuators, 0)
        pass
    elif object == "carta":
        marlin.move_conveyor(actuators, 300)
    elif object == "metallo":
        marlin.move_conveyor(actuators, 500)
    elif object == "plastica":
        marlin.move_conveyor(actuators, 800)
    elif object == "vetro":
        marlin.move_conveyor(actuators, 150)
    _state_is_busy = True

if __name__ == "__main__":
    serial_ports = serial_port.find_devices()
    print("\nUsing serial ports", serial_ports)
    serial_port_actuators = serial_ports.get("actuators")
    serial_port_camera = serial_ports.get("camera")
    pygame.init()
    clock = pygame.time.Clock()
    is_running = True
    openmv.serial_init(serial_port_camera)
    with marlin.serial_init(serial_port_actuators) as actuators:
        while is_running:
            # limit the frame rate to 60 FPS
            clock.tick(60)
            width, height, image = openmv.get_image()
            usb_debug_text = openmv.get_text()
            #print(usb_debug_text, end = "")
            screen = ui.draw_screen(width, height, image)
            ui.print_fps(screen, clock)
            object = ui.print_object(screen, usb_debug_text)
            # update display
            pygame.display.flip()
            # TODO: do some processing
            state_machine(actuators, object)
            is_running = ui.event_exit()
        pygame.quit()
        openmv.serial_close()
        """
        marlin.move_conveyor(actuators, 0)
        marlin.move_servo(actuators, 0)
        marlin.idle_servo(actuators)
        # TODO: attendi e poi sposta se necessario
        marlin.move_conveyor(actuators, 180)
        marlin.move_servo(actuators, 180)
        marlin.idle_servo(actuators)
        """
