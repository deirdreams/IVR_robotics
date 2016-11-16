import ev3dev.ev3 as ev3  
from time import sleep

class Pablo:

	def __init__(self):
		self.leftMotor = ev3.LargeMotor('outC')
		self.rightMotor = ev3.LargeMotor('outD')
		self.color = ev3.ColorSensor(ev3.INPUT_2)
		self.sonar = ev3.UltrasonicSensor(ev3.INPUT_1)
		self.gyro = ev3.UltrasonicSensor(ev3.INPUT_4)

	def __detectLoop(self, direction):
		#0 for left turn, 1 for right turn
		self.__resetMotors()

		if direction:
				self.leftMotor.run_direct(duty_cycle_sp = 20)
				self.rightMotor.run_direct(duty_cycle_sp = 30)
		else:
				self.leftMotor.run_direct(duty_cycle_sp = 30)
				self.rightMotor.run_direct(duty_cycle_sp = 20)

		return self

	def __follow_line(self):
		i = i
		while (color.value() > 60):
				self.__detectLoop(i)
				print color.value()
		#ev3.Sound.speak('Line found').wait()
		while (color.value() < 60):
				self.__detectLoop(i)
				print color.value()
		i = not i
		self.follow_line(i)

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

	


	def run(self):
		while(True):
			self.__follow_line()







