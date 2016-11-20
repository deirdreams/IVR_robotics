import ev3dev.ev3 as ev3
from time import sleep
from pid import PidController

class Pablo:

		def __init__(self):
			self.leftMotor = ev3.LargeMotor('outC')
			self.rightMotor = ev3.LargeMotor('outD')
			self.head = ev3.MediumMotor('outB')
			self.color = ev3.ColorSensor(ev3.INPUT_2)
			self.sonar = ev3.UltrasonicSensor(ev3.INPUT_1)
			self.gyro = ev3.GyroSensor(ev3.INPUT_4)
			self.touch = ev3.TouchSensor(ev3.INPUT_3)
			self.stop = 0
			self.positions = [0 for i in range(25)]
	                self.gyroOnInit = self.gyro.value()

		def __say(self, sentence):
			self.__resetMotors()
			if type(sentence) is str:
				ev3.Sound.seak(sentence)
			else:
				raise ValueError('Input is not a string')

		def __isOnLine(self, sens):
			self.positions.append(self.color.value())
			#print self.color.value()
			self.positions.pop(0)
			whites = [i for i in self.positions if i > 60]
			return not len(whites) == sens


		def __follow_line(self, sens):
			self.__turnHead90('s')
			self.positions = [0 for i in range(25)]
			while(not self.__objectDetected() and self.touch.value() != 1 and self.__isOnLine(sens)):
				a = PidController(30, 1, 1, 0)
				val = a.getPower(self.color.value())/2
				#print val
				self.leftMotor.run_direct(duty_cycle_sp=(50-val)/2)
				self.rightMotor.run_direct(duty_cycle_sp=(50+val)/2)


		def __resetMotors(self):
			self.rightMotor.reset()
			self.leftMotor.reset()
			return self

		def __say(self, sentence):
                        self.__resetMotors()
                        if type(sentence) is str:
                                ev3.Sound.speak(sentence).wait()
                        else:
                                raise ValueError('Input is not a string')

		def __runMotor(self, motor, sp):
			motor.run_direct(duty_cycle_sp=sp)
			return self


        	def __turn90Gyro(self, direction, spin):
			self.__resetMotors()
			#0 for right 1 for left
            		if direction == 0:
               			 while (self.gyro.value() < (self.gyroOnInit + 88)):
                    			self.__runMotor(self.leftMotor, 20)
					self.__runMotor(self.rightMotor, -20)
            		elif direction == 1:
                		while (self.gyro.value() > (self.gyroOnInit - 88)):
                    			self.__runMotor(self.rightMotor, 20)
					self.__runMotor(self.leftMotor, -20)


			elif direction == 's':
				while (abs(self.gyro.value() - self.gyroOnInit) > 10) :
					if spin:
						print abs(self.gyro.value() - self.gyroOnInit)
						self.__runMotor(self.rightMotor, 30)
						self.__runMotor(self.leftMotor, -30)
					else:
						print abs(self.gyro.value() - self.gyroOnInit)
                                                self.__runMotor(self.leftMotor, 30)
						self.__runMotor(self.rightMotor, -30)


			else:
				raise RuntimeError('Unkown direction')
			self.__resetMotors()

		def __turn90(self, direction):
			self.__resetMotors()
			#0 for right 1 for left
			if direction == 'r':
					self.__runMotor(self.leftMotor, 20)
					self.__runMotor(self.rightMotor, -20)

					sleep(1.15)
					self.__resetMotors()
			elif direction == 'l':
					self.__runMotor(self.rightMotor, 20)
					self.__runMotor(self.leftMotor, -20)

					sleep(1.15)
					self.__resetMotors()

			else:
					raise RuntimeError('Unknown direction')


		def __objectDetected(self):
			val = self.sonar.value()
			#value in mm
			if val < 100:
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

		def __turnHead90(self, direction):
			if direction == 'r':
				self.head.run_to_abs_pos(duty_cycle_sp=-50, position_sp=95)
			elif direction == 'l':
				self.head.run_to_abs_pos(duty_cycle_sp=50, position_sp=-95)
			elif direction == 's':
				self.head.run_to_abs_pos(duty_cycle_sp=50, position_sp=0)
			else:
				raise RuntimeError('Unknown direction')


		def __driveStraight(self):
			self.leftMotor.run_direct(duty_cycle_sp=40)
			self.rightMotor.run_direct(duty_cycle_sp=40)


		def __avoidObject(self, snapshot):
			self.__resetMotors()
			pid = PidController(snapshot, 1, 0, 0)
			pid.setKP(100)
			i = 0
			while (self.touch.value() != 1):
				self.__runMotor(self.rightMotor, 20)
				i += 1
				if(i > 300 and self.color.value() < 50):
				   return
			#print -pid.getPower(self.sonar.value())
				self.__runMotor(self.leftMotor, -pid.getPower(self.sonar.value())/2)


		def run(self):
			detected = 0
		#while self.__isOnLine():
				#while(not detected):
			while (self.touch.value() != 1):
				self.__follow_line(100)
				#print self.__isOnLine(1), self.positions
				#       detected = self.__findObject()
				self.__resetMotors()
				val = self.sonar.value()
				self.gyroOnInit = self.gyro.value()
				self.__turn90Gyro(1, 0)
				sleep(2)
				self.__turnHead90('r')
				sleep(1)
				#self.__findObject()
				self.__say('Avoiding object')
				self.__avoidObject(val)
				self.__follow_line(100)
				#self.__turnHead90('s')
				#self.follow_line()


		def runBroken(self, d, s):
			while (self.touch.value() != 1):
				self.__follow_line(23)
				self.__resetMotors()
				self.__say('End of line. Finding new line.')
				sleep(1)
				self.__resetMotors()
				self.__turn90Gyro(d, 0)
				self.__resetMotors()
				sleep(1)
				while(not self.color.value() < 40):
					self.__driveStraight()
				ev3.Sound.speak('Line Found.')
				if d == 0:
					sleep(0.3)
				else:
					sleep(0.5)
				self.__resetMotors()
				#self.__say('Line found.')
				sleep(1)
				self.__turn90Gyro('s', s)
				sleep(1)
				self.__resetMotors()
				sleep(1)
				self.runBroken(not d, not s)
				sleep(2)
				self.runBroken(not d, not s)

		def runStraight(self):
			self.__say('Following line.')
			self.__follow_line(23)
			self.__say('End of line. Nowhere to go.')
