# Source: https://github.com/openmv/openmv/blob/master/tools/pyopenmv_fb.py

import pyopenmv
import pygame
import serial

# requires a label.txt & trained.tflite file on virtual USB drive
DEFAULT_OBJECT_DETECTION_SCRIPT = """
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
    labels = [line.rstrip('\\n') for line in open("labels.txt")]
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
            print('x %d\\ty %d' % (center_x, center_y))
            img.draw_circle((center_x, center_y, 12), color=colors[i], thickness=2)

    print("%.2f" % clock.fps(), "fps", end="\\n\\n")

"""

IMAGE_SCALE = 3

def serial_init(serial_port_camera: str, script: str = DEFAULT_OBJECT_DETECTION_SCRIPT):
    print("\nOpenMV firmware camera & LED reset ...")
    try:
        pyopenmv.disconnect()
        # Enters USB debug mode either with 921600 or 12000000 baud 
        pyopenmv.init(serial_port_camera, baudrate=12000000, timeout=0.050)
        pyopenmv.set_timeout(1*2) # SD Cards can cause big hicups.
        pyopenmv.stop_script()
        pyopenmv.enable_fb(True)
        pyopenmv.exec_script(script)
    except serial.serialutil.PortNotOpenError:
        pass

_fb = None

def get_image(image_scale: int = IMAGE_SCALE, w: int = 240, h: int = 240) -> tuple[int, int, pygame.Surface]:
    """
    Retrive last scaled image captured from camera as a tuple: (width, height, image)
    """
    global _fb
    fb = None
    try:
        fb = pyopenmv.fb_dump() # is not always a complete frame
    except serial.serialutil.PortNotOpenError:
        pass
    if fb is None and _fb is None:
        #return 0, 0, pygame.Surface((0, 0)) # equivalent to full screen
        return w * image_scale, h * image_scale, pygame.Surface((w * image_scale, h * image_scale))
    if fb is not None:
        _fb = fb # reuse this framebuffer once a full frame has been captured
    w, h, data = _fb[0], _fb[1], _fb[2]
    # create image from RGB888
    image = pygame.image.frombuffer(data.flat[0:], (w, h), 'RGB')
    width, height = w * image_scale, h * image_scale
    image = pygame.transform.scale(image, (width, height))
    return width, height, image

def get_text() -> str:
    try:
        tx_len = pyopenmv.tx_buf_len()
        if tx_len:
            return pyopenmv.tx_buf(tx_len).decode()
    except serial.serialutil.PortNotOpenError:
        pass
    return ""

def serial_close():
    try:
        pyopenmv.stop_script()
        pyopenmv.disconnect()
    except serial.serialutil.PortNotOpenError:
        pass