previous_trigger_value = '0'

def monitor_trigger():
    global previous_trigger_value
    
    trigger_op = op('image_switch_trigger') 

    if trigger_op is None:
        print("Error: Text DAT 'image_switch_trigger' not found. Please check the operator name.")
        return 

    if trigger_op.numRows > 0 and trigger_op.numCols > 0:
        current_trigger_value = trigger_op[0, 0].val

        if current_trigger_value is not None:
            if previous_trigger_value == '0' and current_trigger_value == '1':
                print("Trigger activated! Rising edge detected.")
                switch_image()
            
            previous_trigger_value = current_trigger_value
        else:
            print("Error: Trigger value is None.")
    else:
        print("Error: The Text DAT doesn't have any rows or columns.")
