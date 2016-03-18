import sys
import time
import oscapi

def swap(cur):
    return (cur[2], cur[0], cur[1])

if __name__ == "__main__":
    import time
    out = oscapi.ColorsOut()
    hue = 0.0
    while True:
        pix = []
        c = 1.0
        x = c * (1.0 - abs(hue % 2.0 - 1.0))
        if hue > 6.0:
            hue = 0.0
        if hue < 1.0:
            pix = oscapi.getFilledPix(1023.0 * c,1023.0 * x,0.0)
        elif hue < 2.0:
            pix = oscapi.getFilledPix(1023.0 * x,1023.0 * c,0.0)
        elif hue < 3.0:
            pix = oscapi.getFilledPix(0.0,1023.0 * c,1023.0 * x)
        elif hue < 4.0:
            pix = oscapi.getFilledPix(0.0,1023.0 * x,1023.0 * c)
        elif hue < 5.0:
            pix = oscapi.getFilledPix(1023.0 * x,0.0,1023.0 * c)
        elif hue < 6.0:
            pix = oscapi.getFilledPix(1023.0 * c,0.0,1023.0 * x)
        out.write(pix)
        hue += 0.02
        print(pix[0])
        time.sleep(0.1)
