import ev3dev.ev3 as ev3

leftMotor = ev3.LargeMotor('outA')
rightMotor = ev3.LargeMotor('outD')
#print leftMotor.address, rightMotor.address
leftMotor.reset()
rightMotor.reset()
leftMotor.connected
rightMotor.connected
color = ev3.ColorSensor(ev3.INPUT_2)
color.connected

def detectLoop(direction):
        #0 for left turn, 1 for right turn
        leftMotor.reset()
        rightMotor.reset()
        if direction:
                leftMotor.run_direct(duty_cycle_sp = 10)
                rightMotor.run_direct(duty_cycle_sp = 30)
        else:
                leftMotor.run_direct(duty_cycle_sp = 30)
                rightMotor.run_direct(duty_cycle_sp = 10)

def main(i):
        i = i
        while (color.value() > 60):
                detectLoop(i)
                print color.value()
        #ev3.Sound.speak('Line found').wait()
        #i = not i
        while (color.value() < 60):
                detectLoop(i)
                print color.value()
        i = not i
        main(i)

main(0)

