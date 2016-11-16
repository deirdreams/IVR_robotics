import ev3dev.ev3 as ev3
import time

medium = ev3.MediumMotor('outB')

sonar = ev3.UltrasonicSensor()
sonar.connected

def objectDetected():
	val = sonar.value()
	#value in mm
	if val < 170:
		return True
	else:
		return False

#moves motor left to right (-90 to 90 degrees) until an object is detected in its path
def findObject():
	while 1: 
		medium.run_to_abs_pos(duty_cycle_sp=30, position_sp=-90)
		if objectDetected():
			medium.reset()
		time.sleep(1)
		medium.run_to_abs_pos(duty_cycle_sp=30, position_sp=90)
		if objectDetected():
			medium.reset()
		time.sleep(1)

