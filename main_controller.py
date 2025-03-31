def onValueChange(channel, sampleIndex, val, prev):
    print(f"Channel: {channel.name}, Value: {val}")
    op('text1').run()
    run("op('text4').run()", delayFrames=1)
