import math

kinect_chop = op('null_kinect') 

channels = {
    "hand_r": ["p1/hand_r:tx", "p1/hand_r:ty", "p1/hand_r:tz"],
    "forearm_r": ["p1/forearm_r:tx", "p1/forearm_r:ty", "p1/forearm_r:tz"],
    "upperarm_r": ["p1/upperarm_r:tx", "p1/upperarm_r:ty", "p1/upperarm_r:tz"],
}

def get_joint_position(joint):
    try:
        x = kinect_chop[channels[joint][0]].eval()
        y = kinect_chop[channels[joint][1]].eval()
        z = kinect_chop[channels[joint][2]].eval()
        return x, y, z
    except KeyError:
        print(f"Error: Missing data for joint '{joint}'")
        return None

def check_right_arm_extended():
    hand_r = get_joint_position("hand_r")
    forearm_r = get_joint_position("forearm_r")
    upperarm_r = get_joint_position("upperarm_r")

    if hand_r and forearm_r and upperarm_r:
        hx, hy, hz = hand_r
        fx, fy, fz = forearm_r
        ux, uy, uz = upperarm_r

        distance_hand_forearm = math.sqrt((fx - hx)**2 + (fy - hy)**2 + (fz - hz)**2)
        distance_forearm_upperarm = math.sqrt((fx - ux)**2 + (fy - uy)**2 + (fz - uz)**2)

        threshold_hand_forearm = 0.05  
        threshold_forearm_upperarm = 0.18 

        if distance_hand_forearm > threshold_hand_forearm and distance_forearm_upperarm > threshold_forearm_upperarm:
            print("Right arm is extended!")
            op('image_switch_trigger')[0, 0] = '1'  
        else:
            print("Right arm is not extended.")
            op('image_switch_trigger')[0, 0] = '0' 

    else:
        print("One or more joints have missing or invalid data.")

check_right_arm_extended()
