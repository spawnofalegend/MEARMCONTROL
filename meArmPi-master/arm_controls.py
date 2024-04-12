from pynput import keyboard
import pandas as pd
import Calibrate

###############################################################################################################################
# General options settings #
# control set for key mapping
###############################################################################################################################
setkey = 'p'

Baseinc = 'q'
Basedec = 'a'

Sholderinc = 'w'
Sholderdec = 's'

Elbowinc = 'e'
Elbowdec = 'd'

Gripperinc = 'r'
Gripperdec = 'f'

inc = 10
dec = -10

autopoints=[]

# Set values to the middle values of calibration
Currentvals = [1460,1460,1125,1000]


#set values to min and max of servos from calibration, (set first value to smaller regardless)
minmaxvals = [
    # Values for Base
    [500, 2465],

    # Values for Sholder
    [700, 2300],

    # Values for Elbow
    [600, 1425],

    # Values for Gripper
    [400, 1600]
]

###############################################################################################################################
###############################################################################################################################

keymapping = [
    # Format is [ keyassociated/movement , relative index for min/max values, channel, value and direction of change]
    [Baseinc, 0, 0, inc],
    [Basedec, 0, 0, dec],

    [Sholderinc, 1, 1, inc],
    [Sholderdec, 1, 1, dec],

    [Elbowinc, 2, 14, inc],
    [Elbowdec, 2, 14, dec],

    [Gripperinc, 3, 15, dec],
    [Gripperdec, 3, 15, inc]
]



def on_press(key):

    if key == keyboard.Key.esc:
        # Stop listener
        df = pd.DataFrame(autopoints, columns=["base", "shoulder", "elbow", "grip"])
        df.to_csv('autopoints.csv', index=False)
        return False

    if key.char == setkey:
        autopoints.append(Currentvals.copy())
        print ('Currently stored point values', autopoints)

    elif key.char != setkey:
        for i in keymapping: 
            vals = minmaxvals[i[1]]
            x = vals[0]
            y = vals[1]


            #statement for decreasing
            if key.char == i[0] and i[3] == dec and x < Currentvals[i[1]] :
                Calibrate.set_servo_pulse(i[2], Currentvals[i[1]] + i[3] )
                Currentvals[i[1]] = Currentvals[i[1]] + i[3]
                print("Current servo impulse values:",Currentvals)
            
            #statement for increasing
            if key.char == i[0] and i[3] == inc and Currentvals[i[1]] < y:
                Calibrate.set_servo_pulse(i[2], Currentvals[i[1]] + i[3] )
                Currentvals[i[1]] = Currentvals[i[1]] + i[3]
                print("Current servo impulse values:",Currentvals)
    else:
        return True

    pass


def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False


Calibrate.set_servo_pulse(0, Currentvals[0])
Calibrate.set_servo_pulse(1, Currentvals[1])
Calibrate.set_servo_pulse(14, Currentvals[2])
Calibrate.set_servo_pulse(15, Currentvals[3])


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


