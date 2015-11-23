import pyaudio
import numpy
import audioop
import sys
import math
import struct
from oscapi import ColorsOut
from animations import FadeAnimation

'''
Sources

http://www.swharden.com/blog/2010-03-05-realtime-fft-graph-of-audio-wav-file-or-microphone-input-with-python-scipy-and-wckgraph/
http://macdevcenter.com/pub/a/python/2001/01/31/numerically.html?page=2

'''

chunk      = 2**11 # Change if too fast/slow, never less than 2**11
scale      = 15    # Change if too dim/bright
exponent   = 9     # Change if too little/too much difference between loud and quiet sounds
samplerate = 44100 
cutoff = 0

MAX = 48
out = FadeAnimation()
out.FADEINRATE = 2.0 #optional
out.FADEOUTRATE = 8.0 #optional, makes things 'trail off'
out.start()

RGBMIN = 0
RGBMAX = 255

def list_devices():
    # List all audio input devices
    p = pyaudio.PyAudio()
    i = 0
    n = p.get_device_count()
    while i < n:
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
            print str(i)+'. '+dev['name']
        i += 1

def music_visuals(): 
    # CHANGE THIS TO CORRECT INPUT DEVICE
    # Enable stereo mixing in your sound card
    # to make you sound output an input
    # Use list_devices() to list all your input devices
    device   = 5  
    
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
                    channels = 1,
                    rate = 44100,
                    input = True,
                    frames_per_buffer = chunk,
                    input_device_index = device)

    hue = 0.0
    colors = [(0,0,0), (0, 0, 255), (255, 0, 0)]
    # colors = [(0,0,0), (0, 0, 255), (0, 255, 255), (0, 255, 0),  (255, 255, 0), (255, 0, 0) ]
    
    # colors = [(0, 0, 0), (2, 0, 90), (20, 0, 123), (55, 0, 143), (84, 0, 152), (115, 0, 157), (146, 0, 156), (171, 0, 153), (188, 5, 147), (201, 17, 135), (212, 33, 111), (223, 53, 66), (231, 72, 20), (237, 90, 7), (241, 106, 2), (245, 125, 0), (249, 142, 0), (253, 163, 0), (254, 184, 0), (254, 202, 1), (255, 219, 15), (255, 232, 63), (255, 242, 134), (255, 249, 203)] 
    try:
        while True:
            try:
                data = stream.read(chunk)
            except IOError, e:
                if e.args[1] == pyaudio.paInputOverflowed:
                    data = '\x00'*chunk
                else:
                    raise

            # Do FFT
            levels = calculate_levels(data, chunk, samplerate)

            for i in range(0,len(levels)):
                levels[i] = max(min(levels[i] / scale, 1.0), 0.0)
                levels[i] = levels[i]**exponent 
                levels[i] = int(levels[i] * 255)
                if levels[i] < cutoff:
                    levels[i] = 0

            print levels

            cols = (1.0, 1.0, 1.0)
            c = 1.0
            x = c * (1.0 - abs(hue % 2.0 - 1.0))
            if hue > 6.0:
                hue = 0.0
            if hue < 1.0:
                cols = (1.0 * c, 1.0 * x, 0.0)
            elif hue < 2.0:
                cols = (1.0 * x, 1.0 * c, 0.0)
            elif hue < 3.0:
                cols = (0.0, 1.0 * c, 1.0 * x)
            elif hue < 4.0:
                cols = (0.0, 1.0 * x, 1.0 * c)
            elif hue < 5.0:
                cols = (1.0 * x, 0.0, 1.0 * c)
            elif hue < 6.0:
                cols = (1.0 * c, 0.0, 1.0 * x)

            # s = ser.read(6)
            r = 4.0 * cols[0]
            g = 4.0 * cols[1]
            b = 4.0 * cols[2]
            pix = [convert_to_rgb(level, colors) for level in levels]
            hue += 0.02
            out.write(pix)

    except KeyboardInterrupt:
        print "\nStopping"
        stream.close()
        p.terminate()
        quit()

def calculate_levels(data, chunk, samplerate):
    # Use FFT to calculate volume for each frequency
    global MAX

    fmt = "%dH"%(len(data)/2)
    data2 = struct.unpack(fmt, data)
    data2 = numpy.array(data2, dtype='h')
    # Convert raw sound data to Numpy array
    # Apply FFT
    fourier = numpy.fft.fft(data2)
    ffty = numpy.abs(fourier[0:len(fourier)/2])/1000
    ffty1=ffty[:len(ffty)/2]
    ffty2=ffty[len(ffty)/2::]+2
    ffty2=ffty2[::-1]
    ffty=ffty1+ffty2
    ffty=numpy.log(ffty)-2
    
    fourier = list(ffty)[4:-4]
    fourier = fourier[:len(fourier)/2]
    
    size = max(MAX,len(fourier))

    # Add up for MAX lights
    levels = [sum(fourier[i:(i+size/MAX)]) for i in xrange(0, size, size/MAX)][:MAX]
    
    return levels

def convert_to_rgb(val, colors):
    global RGBMIN
    global RGBMAX
    minval, maxval = float(RGBMIN), float(RGBMAX)
    max_index = len(colors)-1
    v = float(val-minval) / float(maxval-minval) * max_index
    i1, i2 = int(v), min(int(v)+1, max_index)
    (r1, g1, b1), (r2, g2, b2) = colors[i1], colors[i2]
    f = v - i1
    return int(r1 + f*(r2-r1))*4, int(g1 + f*(g2-g1))*4, int(b1 + f*(b2-b1))*4

if __name__ == '__main__':
    list_devices()
    music_visuals()
