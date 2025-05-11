import math
import time

gesture_active_right = False
gesture_active_left = False

THRESHOLD_HAND_FOREARM = 0.05
THRESHOLD_FOREARM_UPPERARM = 0.18

last_check_time = 0 
CHECK_INTERVAL = 0.25 

def compute_distance(joint1, joint2):
    return math.sqrt((joint2[0] - joint1[0])**2 + (joint2[1] - joint1[1])**2 + (joint2[2] - joint1[2])**2)


def check_right_gesture(hand_r, forearm_r, upperarm_r):
    global gesture_active_right

    distance_hand_forearm_r = compute_distance(hand_r, forearm_r)
    distance_forearm_upperarm_r = compute_distance(forearm_r, upperarm_r)

    if (
        distance_hand_forearm_r > THRESHOLD_HAND_FOREARM and
        distance_forearm_upperarm_r > THRESHOLD_FOREARM_UPPERARM
    ):
        if not gesture_active_right:
            op('image_switch_trigger_right')[0, 0] = '0'
            gesture_active_right = True
    else:
        if gesture_active_right:
            op('image_switch_trigger_right')[0, 0] = '1'
            gesture_active_right = False


def check_left_gesture(hand_l, forearm_l, upperarm_l):
    global gesture_active_left

    distance_hand_forearm_l = compute_distance(hand_l, forearm_l)
    distance_forearm_upperarm_l = compute_distance(forearm_l, upperarm_l)

    if (
        distance_hand_forearm_l > THRESHOLD_HAND_FOREARM and
        distance_forearm_upperarm_l > THRESHOLD_FOREARM_UPPERARM
    ):
        if not gesture_active_left:
            op('image_switch_trigger_left')[0, 0] = '0'
            gesture_active_left = True
    else:
        if gesture_active_left:
            op('image_switch_trigger_left')[0, 0] = '1'
            gesture_active_left = False        


def check_gesture(kinect_data):
    global gesture_active_right, gesture_active_left

    channel_map = {
        "hand_r:tx": "p1/hand_r:tx", "hand_r:ty": "p1/hand_r:ty", "hand_r:tz": "p1/hand_r:tz",
        "forearm_r:tx": "p1/forearm_r:tx", "forearm_r:ty": "p1/forearm_r:ty", "forearm_r:tz": "p1/forearm_r:tz",
        "upperarm_r:tx": "p1/upperarm_r:tx", "upperarm_r:ty": "p1/upperarm_r:ty", "upperarm_r:tz": "p1/upperarm_r:tz",
        "hand_l:tx": "p1/hand_l:tx", "hand_l:ty": "p1/hand_l:ty", "hand_l:tz": "p1/hand_l:tz",
        "forearm_l:tx": "p1/forearm_l:tx", "forearm_l:ty": "p1/forearm_l:ty", "forearm_l:tz": "p1/forearm_l:tz",
        "upperarm_l:tx": "p1/upperarm_l:tx", "upperarm_l:ty": "p1/upperarm_l:ty", "upperarm_l:tz": "p1/upperarm_l:tz"
    }

    try:
        hand_r = (kinect_data[channel_map["hand_r:tx"]], kinect_data[channel_map["hand_r:ty"]], kinect_data[channel_map["hand_r:tz"]])
        forearm_r = (kinect_data[channel_map["forearm_r:tx"]], kinect_data[channel_map["forearm_r:ty"]], kinect_data[channel_map["forearm_r:tz"]])
        upperarm_r = (kinect_data[channel_map["upperarm_r:tx"]], kinect_data[channel_map["upperarm_r:ty"]], kinect_data[channel_map["upperarm_r:tz"]])

        hand_l = (kinect_data[channel_map["hand_l:tx"]], kinect_data[channel_map["hand_l:ty"]], kinect_data[channel_map["hand_l:tz"]])
        forearm_l = (kinect_data[channel_map["forearm_l:tx"]], kinect_data[channel_map["forearm_l:ty"]], kinect_data[channel_map["forearm_l:tz"]])
        upperarm_l = (kinect_data[channel_map["upperarm_l:tx"]], kinect_data[channel_map["upperarm_l:ty"]], kinect_data[channel_map["upperarm_l:tz"]])
    except KeyError as e:
        print(f"Missing channels during gesture check: {e}")
        return

    check_right_gesture(hand_r, forearm_r, upperarm_r)
    check_left_gesture(hand_l, forearm_l, upperarm_l)


def onValueChange(channel, sampleIndex, val, prev):
    global last_check_time
    current_time = time.time()
    if current_time - last_check_time >= CHECK_INTERVAL:
        kinect_data = {chan.name: chan.eval() for chan in op('null_kinect').chans()}
        check_gesture(kinect_data)
        last_check_time = current_time
