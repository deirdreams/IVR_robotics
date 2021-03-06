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
			#self.__turnHead90('s')
			self.positions = [0 for i in range(25)]
			while(not self.__objectDetected() and self.touch.value() != 1 and self.__isOnLine(sens)):
				a = PidController(30, 1, 1, 0)
				val = a.getPower(self.color.value())/2
				if val > 70:
					val = 70
				if val < -70:
					val = -70
				 
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
			#print self.gyro.value()
            		if direction == 0:
               			while (self.gyro.value() < (self.gyroOnInit + 88)):
                    			self.__runMotor(self.leftMotor, 20)
					self.__runMotor(self.rightMotor, -20)
				#print self.gyro.value()
            		elif direction == 1:
                		while (self.gyro.value() > (self.gyroOnInit - 88)):
                    			self.__runMotor(self.rightMotor, 20)
					self.__runMotor(self.leftMotor, -20)
				#print self.gyro.value()



			elif direction == 's':
				while (abs(self.gyro.value() - self.gyroOnInit) % 360 > 10) :
					if spin:
						#print abs(self.gyro.value() - self.gyroOnInit)
						self.__runMotor(self.rightMotor, 30)
						self.__runMotor(self.leftMotor, -30)
					else:
						#print abs(self.gyro.value() - self.gyroOnInit)
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
			if val < 50:
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
				self.head.run_to_abs_pos(duty_cycle_sp=-50, position_sp=90)
			elif direction == 'l':
				self.head.run_to_abs_pos(duty_cycle_sp=50, position_sp=-90)
			elif direction == 's':
				self.head.run_to_abs_pos(duty_cycle_sp=50, position_sp=0)
			else:
				raise RuntimeError('Unknown direction')
	

		def __driveStraight(self):
			self.leftMotor.run_direct(duty_cycle_sp=40)
			self.rightMotor.run_direct(duty_cycle_sp=40)			


		def __avoidObject(self, snapshot):
			self.__resetMotors()
			pid = PidController(snapshot+80, 1, 0, 0)
			pid.setKP(1)
			i = 0
			while (self.touch.value() != 1):
				self.__runMotor(self.rightMotor, 20)
				#p = self.head.position
				#v = abs(-((self.gyro.value() -self.gyroOnInit-90)))
				#sign = 1
				#print -((self.gyro.value() - self.gyroOnInit-90))
				#if -((self.gyro.value() - self.gyroOnInit-90)) > 0:
				#		sign = sign
				#	v = v
				#else:
				#	sign *= -1
				#	v = -v
				#self.head.run_to_abs_pos(duty_cycle_sp=50*sign, position_sp=v)
				#sleep(0.3)
				i += 1
				if(i > 300 and self.color.value() < 20):
				   return
				self.__runMotor(self.leftMotor, (-pid.getPower(self.sonar.value())+10)/2)


		def run(self):
			detected = 0
			while (self.touch.value() != 1):
				self.__follow_line(100)
				#print self.__isOnLine(1), self.positions
				#       detected = self.__findObject()
				self.__resetMotors()
				val = self.sonar.value()
				self.gyroOnInit = self.gyro.value() + 10
				self.__turn90Gyro(1, 0)
				sleep(1.25)
				self.__turnHead90('r')
				sleep(1)
				self.__say('Avoiding object')
				self.__avoidObject(val)
				#self.__say('Object avoided')
				self.__turn90Gyro('s', 1)
				self.__turnHead90('s')
				self.__follow_line(100)

		
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
