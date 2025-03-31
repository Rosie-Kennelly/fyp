def monitor_trigger():
    trigger_op = op('image_switch_trigger') 

    if trigger_op is None:
        print("Error: Text DAT 'image_switch_trigger' not found. Please check the operator name.")
        return 

    if trigger_op.numRows > 0 and trigger_op.numCols > 0:
        trigger_value = trigger_op[0, 0].val

        if trigger_value is not None:
            if trigger_value == '1': 
                print("Trigger activated!")
                switch_image() 
                trigger_op[0, 0] = '0' 
            else:
                print("Waiting for trigger to switch images.")
        else:
            print("Error: Trigger value is None.")
    else:
        print("Error: The Text DAT doesn't have any rows or columns.")
