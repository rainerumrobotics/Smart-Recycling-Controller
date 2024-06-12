# Source: https://github.com/openmv/openmv/blob/master/tools/pyopenmv_fb.py

import pyopenmv
import pygame
import serial

DEFAULT_SCRIPT = """
# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time, pyb

led_red = pyb.LED(1); led_green = pyb.LED(2); led_blue = pyb.LED(3)
led_red.on(); led_green.on(); led_blue.on()

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

while(True):
    clock.tick()
    img = sensor.snapshot()         # Take a picture and return the image.
    sensor.flush()
    print("%.2f" % clock.fps(), "fps")
"""

IMAGE_SCALE = 4

def serial_init(serial_port_camera: str, script: str = DEFAULT_SCRIPT):
    print("\nOpenMV firmware camera & LED reset ...")
    try:
        pyopenmv.disconnect()
        pyopenmv.init(serial_port_camera, baudrate=921600, timeout=0.050)
        pyopenmv.set_timeout(1*2) # SD Cards can cause big hicups.
        pyopenmv.stop_script()
        pyopenmv.enable_fb(True)
        pyopenmv.exec_script(script)
    except serial.serialutil.PortNotOpenError:
        pass

_fb = None

def get_image(image_scale: int = IMAGE_SCALE, w: int = 320, h: int = 240) -> tuple[int, int, pygame.Surface]:
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