import math
import time

gesture_active = False 
last_trigger_time = 0  
CHECK_DELAY = 0.25  

THRESHOLD_HAND_FOREARM = 0.05
THRESHOLD_FOREARM_UPPERARM = 0.18

last_check_time = 0

def compute_distance(joint1, joint2):
    return math.sqrt((joint2[0] - joint1[0])**2 + (joint2[1] - joint1[1])**2 + (joint2[2] - joint1[2])**2)

def check_gesture(kinect_data):
    global gesture_active, last_trigger_time

    channel_map = {
        "hand_r:tx": "p1/hand_r:tx", "hand_r:ty": "p1/hand_r:ty", "hand_r:tz": "p1/hand_r:tz",
        "forearm_r:tx": "p1/forearm_r:tx", "forearm_r:ty": "p1/forearm_r:ty", "forearm_r:tz": "p1/forearm_r:tz",
        "upperarm_r:tx": "p1/upperarm_r:tx", "upperarm_r:ty": "p1/upperarm_r:ty", "upperarm_r:tz": "p1/upperarm_r:tz"
    }

    missing_channels = [v for k, v in channel_map.items() if v not in kinect_data]
    if missing_channels:
        print(f"Missing channels: {', '.join(missing_channels)}")
        return

    try:
        hand_r = (kinect_data[channel_map["hand_r:tx"]], kinect_data[channel_map["hand_r:ty"]], kinect_data[channel_map["hand_r:tz"]])
        forearm_r = (kinect_data[channel_map["forearm_r:tx"]], kinect_data[channel_map["forearm_r:ty"]], kinect_data[channel_map["forearm_r:tz"]])
        upperarm_r = (kinect_data[channel_map["upperarm_r:tx"]], kinect_data[channel_map["upperarm_r:ty"]], kinect_data[channel_map["upperarm_r:tz"]])
    except KeyError as e:
        print(f"KeyError during gesture check: {e}")
        return

    distance_hand_forearm = compute_distance(hand_r, forearm_r)
    distance_forearm_upperarm = compute_distance(forearm_r, upperarm_r)

    current_time = time.time()
    if (
        distance_hand_forearm > THRESHOLD_HAND_FOREARM and
        distance_forearm_upperarm > THRESHOLD_FOREARM_UPPERARM
    ):
        if not gesture_active and current_time - last_trigger_time > DEBOUNCE_TIME:
            print("Right arm is extended!")
            op('image_switch_trigger')[0, 0] = '1'
            gesture_active = True
            last_trigger_time = current_time
    else:
        if gesture_active:
            print("Right arm is no longer extended.")
            op('image_switch_trigger')[0, 0] = '0'
            gesture_active = False

def onValueChange(channel, sampleIndex, val, prev):
    global last_check_time

    current_time = time.time()
    if current_time - last_check_time >= CHECK_DELAY:
        last_check_time = current_time
        kinect_data = {chan.name: chan.eval() for chan in op('null_kinect').chans()}
        check_gesture(kinect_data)
