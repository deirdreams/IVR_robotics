import ev3dev.ev3 as ev3  
from time import sleep

class Pablo:

	def __init__(self):
		self.leftMotor = ev3.LargeMotor('outC')
		self.rightMotor = ev3.LargeMotor('outD')
		self.head = ev3.MediumMotor('outB')
		self.color = ev3.ColorSensor(ev3.INPUT_2)
		self.sonar = ev3.UltrasonicSensor(ev3.INPUT_1)
		self.gyro = ev3.UltrasonicSensor(ev3.INPUT_4)
		self.direction = 0

	def __detectLoop(self):
		#0 for left turn, 1 for right turn
		self.__resetMotors()
		if self.color.value() > 60:
			self.direction = self.direction
		else:
			sefl.direction = not self.direction
		if direction:
				self.leftMotor.run_direct(duty_cycle_sp = 10)
				self.rightMotor.run_direct(duty_cycle_sp = 30)
		else:
				self.leftMotor.run_direct(duty_cycle_sp = 30)
				self.rightMotor.run_direct(duty_cycle_sp = 10)

		return self

	def __follow_line(self, i):
		i = i
		while (color.value() > 60):
				self.__detectLoop(i)
				print self.color.value()
		#ev3.Sound.speak('Line found').wait()
		while (color.value() < 60):
				self.__detectLoop(i)
				print self.color.value()
		i = not i
		self.__follow_line(i)

	def __resetMotors(self):
		self.rightMotor.reset()
		self.leftMotor.reset()
		return self

	def __runMotor(self, motor):
		motor.run_direct(duty_cycle_sp=30)
		return self

	def __turn90(self, direction):

		self.__resetMotors()

		if direction == 'r':
			self.__runMotor(self.leftMotor)
			sleep(2.2)
			self.__resetMotors()

		elif direction == 'l':
			self.__runMotor(self.leftMotor)
			sleep(2.2)
			self.__resetMotors()

		else:
			raise RuntimeError('Unknown direction')

	
	def __objectDetected(self):
		val = self.sonar.value()
		#value in mm
		if val < 170:
			return True
		else:
			return False

	def __findObject(self):
		detected = 0
		self.head.run_to_abs_pos(duty_cycle_sp=30, position_sp=-90)

		if self.__objectDetected():
			detected = 1

		sleep(1)

		self.head.run_to_abs_pos(duty_cycle_sp=30, position_sp=90)

		if self.__objectDetected():
			detected = 1

		sleep(1)
		return detected

	def run(self):
		detected = False
		while(not detected):
			self.__detectLoop(self.direction)
			print self.sonar.value()
			detected = self.__objectDetected()








