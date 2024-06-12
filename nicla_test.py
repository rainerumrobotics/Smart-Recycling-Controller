import serial_port
import openmv
import pygame
import ui

OBJECT_DETECTION_SCRIPT = """
# Edge Impulse - OpenMV Object Detection Example

import sensor, image, time, os, tf, math, uos, gc, pyb

led_red = pyb.LED(1); led_green = pyb.LED(2); led_blue = pyb.LED(3)
led_red.on(); led_green.on(); led_blue.on()

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time=2000)          # Let the camera adjust.

net = None
labels = None
min_confidence = 0.5

try:
    # load the model, alloc the model file on the heap if we have at least 64K free after loading
    net = tf.load("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    raise Exception('Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception('Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

colors = [ # Add more colors if you are detecting more than 7 types of classes at once.
    (255,   0,   0),
    (  0, 255,   0),
    (255, 255,   0),
    (  0,   0, 255),
    (255,   0, 255),
    (  0, 255, 255),
    (255, 255, 255),
]

clock = time.clock()
while(True):
    clock.tick()

    img = sensor.snapshot()

    # detect() returns all objects found in the image (splitted out per class already)
    # we skip class index 0, as that is the background, and then draw circles of the center
    # of our objects

    for i, detection_list in enumerate(net.detect(img, thresholds=[(math.ceil(min_confidence * 255), 255)])):
        if (i == 0): continue # background class
        if (len(detection_list) == 0): continue # no detections for this class?

        print("********** %s **********" % labels[i])
        for d in detection_list:
            [x, y, w, h] = d.rect()
            center_x = math.floor(x + (w / 2))
            center_y = math.floor(y + (h / 2))
            print('x %d\ty %d' % (center_x, center_y))
            img.draw_circle((center_x, center_y, 12), color=colors[i], thickness=2)

    print(clock.fps(), "fps", end="\n\n")
"""

if __name__ == "__main__":
    serial_ports = serial_port.find_devices()
    print("\nUsing serial ports", serial_ports)
    serial_port_camera = serial_ports.get("camera")
    pygame.init()
    clock = pygame.time.Clock()
    is_running = True
    openmv.serial_init(serial_port_camera, OBJECT_DETECTION_SCRIPT)
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