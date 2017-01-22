
__license__ = "MIT"
__author__ = "Alexander K."

import threading
import atexit
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    class LED():
        pin = None
        threadstopper = None
        coord = None
        def __init__(self, pin):
            self.pin = pin
            GPIO.setup(self.pin, GPIO.OUT)
            self.threadstopper = threading.Event()
            self.coord = threading.Lock()
        
        def on(self):
            self.threadstopper.set()
            with self.coord:
                GPIO.output(self.pin, GPIO.HIGH)
        
        def off(self):
            self.threadstopper.set()
            with self.coord:
                GPIO.output(self.pin, GPIO.LOW)
        
        def close(self):
            GPIO.cleanup(self.pin)
        
        def blink(self, on_time=1, off_time=1, n=None, background=True):
            self.threadstopper.set()
            if not background:
                self._blink(on_time, off_time, n)
            else:
                threading.Thread(target=self._blink, args=(on_time, off_time, n)).start()
        def _blink(self, on_time, off_time, n):
            self.threadstopper.clear()
            while n is None or n > 0:
                with self.coord:
                    GPIO.output(self.pin, GPIO.HIGH)
                if self.threadstopper.wait(on_time):
                    break
                with self.coord:
                    GPIO.output(self.pin, GPIO.LOW)
                if self.threadstopper.wait(off_time):
                    break
                if n:
                    n -= 1
    atexit.register(GPIO.cleanup)
except ImportError:
    LED = None



