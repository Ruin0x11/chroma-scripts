import sys
import time
import oscapi

def swap(cur):
    return (cur[2], cur[0], cur[1])

if __name__ == "__main__":
    out = oscapi.ColorsOut()
    hue = 0.0

    current_color = (512.0,0.0,0.0)
    next_color = current_color
    began = False
    advancement = 1
    
    while True:
        pix = oscapi.getFilledPix((0.0, 0.0, 0.0))
        if advancement > oscapi.WIDTH + oscapi.HEIGHT:
            current_color = next_color
            began = False
        if began == False:
            began = True
            pix = oscapi.getFilledPix(current_color)
            next_color = swap(current_color)
            advancement = 1
            out.write(pix)
            time.sleep(2)
        else:
            for i in range(0, oscapi.WIDTH):
                for j in range(0, oscapi.HEIGHT):
                    if (i < advancement) and (j < advancement - i):
                        oscapi.setPix(pix, i, j, next_color)
                    else:
                        oscapi.setPix(pix, i, j, current_color)
            advancement += 1
            out.write(pix)
            time.sleep(0.05)
