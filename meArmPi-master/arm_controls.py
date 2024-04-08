from pynput import keyboard
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

Changeamount = 10

autopoints=[]

# Set vals to the middle values
Currentvals = [1460,1460,1125,1600]

minmaxvals = [
    # Values for Base
    [500, 2465],

    # Values for Sholder
    [700, 2300],

    # Values for Elbow
    [1425, 600],

    # Values for Gripper
    [400, 1600]
]

###############################################################################################################################
###############################################################################################################################

keymapping = [
    # Format is [ keyassociated/movement , relative index for min/max values, channel, value and direction of change]
    [Baseinc, 0, 0, Changeamount],
    [Basedec, 0, 0, -Changeamount],

    [Sholderinc, 1, 1, Changeamount],
    [Sholderdec, 1, 1, -Changeamount],

    [Elbowinc, 2, 14, Changeamount],
    [Elbowdec, 2, 14, -Changeamount],

    [Gripperinc, 3, 15, -Changeamount],
    [Gripperdec, 3, 15, Changeamount]
]



def on_press(key):
    if key.char == setkey:
        autopoints.append(Currentvals)

    elif key.char != setkey:
        for i in keymapping: 
            vals = minmaxvals[i]
            x = vals[0]
            y = vals[1]

            if key.char == i[0] and x < Currentvals[i[1]] < y:
                Calibrate.set_servo_pulse(i[2], Currentvals[i[1]] + i[3] )
                Currentvals[i[1]] = Currentvals[i[1]] + i[3]
    else:
        return True

    pass


def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

