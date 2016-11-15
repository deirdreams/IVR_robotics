import ev3dev.ev3 as ev3
import time

leftMotor = ev3.LargeMotor('outA')
rightMotor = ev3.LargeMotor('outD')
leftMotor.connected
rightMotor.connected
sonar = ev3.UltrasonicSensor(ev3.INPUT_1)
sonar.connected
sonar.mode = 'US-DIST-CM' # will return value in mm

gyro = ev3.GyroSensor()
gyro.connected
gyro.mode = 'GYRO-ANG'

def resetWheels():
	leftMotor.reset()
	rightMotor.reset()

def moveForward():
	leftMotor.run_direct(duty_cycle_sp = 50)
	rightMotor.run_direct(duty_cycle_sp = 50)


def moveBackwards():
	leftMotor.run_direct(duty_cycle_sp = -50)
	rightMotor.run_direct(duty_cycle_sp = -50)

def moveForwardTimed():
	leftMotor.run_timed(duty_cycle_sp = 50, time_sp = 800)
	rightMotor.run_timed(duty_cycle_sp = 50, time_sp = 800)

def checkSurroundings():
	while True:
		if sonar.value() < 80:
			turnLeft90Degrees()
			moveForwardTimed()
			turnRight90Degrees()
			moveForwardTimed()
		else:
			moveForward()

def turnLeft90Degrees():
	rest()
	target = gyro.value + 90
	while (gyro.value < target):
			rightMotor.run_direct(duty_cycle_sp = 50)
	reset()

def turnRight90Degrees():
	reset()
	target = gyro.value + 90
	while (gyro.value < target):
			leftMotor.run_direct(duty_cycle_sp = 50)
	reset()

