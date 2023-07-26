import time
from adafruit_circuitplayground import cp

def inRange(value, accepted, error):
    return (value + error >= accepted) and (value - error <= accepted)

forces = []
steps = 0
wait = 0
while True:
    if cp.button_a and cp.button_b:
        cp.pixels.fill((0,0,50))
        time.sleep(1)
        steps = 0
        cp.pixels.fill((0,0,0))
    x,y,z = cp.acceleration
    forces.append((x,y,z)) # Adding steps to force list so that MU Editor plots all the values
    print(steps)
    if len(forces) > 15: # Keep track of the acceleration values in the last 1.5 sec
        del forces[0]
        if wait <= 0:
            localMaxX, localMinX, localMaxY, localMinY, localMaxZ = -100, 100, -100, 100, -100
            for force in forces:
                if force[0] > localMaxX:
                    localMaxX = force[0]
                elif force[0] < localMinX:
                    localMinX = force[0]
                if force[1] > localMaxY:
                    localMaxY = force[1]
                elif force[1] < localMinY:
                    localMinY = force[1]
                if force[2] > localMaxZ:
                    localMaxZ = force[2]
            if (localMaxY > -7) and (localMaxZ < 6): # Don't count if arm is straight down (or almost straight down), because this means they are standing
                if (localMaxX-localMinX > 3) and (localMaxY-localMinY > 3): # If the minimum and maximum values are similar, then there is not much movement
                    if ((localMaxX - localMaxY) < 5): # The x and y values are very similar near the peak of the wave
                        steps+=2  # Each arm swing is two steps
                        # cp.play_tone(256, 1)
                        wait = 15 # If a step has been recorded wait 1.5 second before trying to sense another one
                                # This is to prevent recording the same step multiple times
    if steps < 5000:
        cp.pixels.fill((50,0,0))
    elif steps < 1000:
        cp.pixels.fill((100,20,0))
    else:
        cp.pixels.fill((0,50,0))
    wait -= 1
    time.sleep(0.1)
