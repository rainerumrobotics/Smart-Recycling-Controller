import serial_port
import openmv
import pygame
import ui

if __name__ == "__main__":
    serial_ports = serial_port.find_devices()
    print("\nUsing serial ports", serial_ports)
    serial_port_camera = serial_ports.get("camera")
    pygame.init()
    clock = pygame.time.Clock()
    is_running = True
    openmv.serial_init(serial_port_camera)
    while is_running:
        # limit the frame rate to 60 FPS
        clock.tick(60)
        width, height, image = openmv.get_image()
        print(openmv.get_text(), end = "")
        screen = ui.draw_screen(width, height, image)
        ui.print_fps(screen, clock)
        # update display
        pygame.display.flip()
        # TODO: do some processing
        #
        is_running = ui.event_exit()
    pygame.quit()
    openmv.serial_close()