from ev3dev.ev3 import ev3

leftMotor = ev3.LargeMotor('outA')
rightMotor = ev3.LargeMotor('outD')
leftMotor.connected
rightMotor.connected
color = ev3.ColorSensor(ev3.INPUT_2)
color.connected

def detectLoop(direction):
	#0 for left turn, 1 for right turn
	if direction:
		leftMotor.run_direct(duty_cycle_sp = 10)
		rightMotor.run_direct(duty_cycle_sp = 30)
	else:
		leftMotor.run_direct(duty_cycle_sp = 30)
		rightMotor.run_direct(duty_cycle_sp = 10)

def main():
	i = 1
	while (color.value()):
		detectLoop(i)
	ev3.Sound.speak('Line found').wait()
	i = not i
	while (not color.value()):
		detectLoop(i)
	i = not i
	main()
