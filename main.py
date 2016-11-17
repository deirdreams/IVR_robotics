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
                self.gyro = ev3.UltrasonicSensor(ev3.INPUT_4)
                self.stop = 0

        def __follow_line(self):
			while(not self.__objectDetected()):
				a = PidController(10, 1, 0, 0)
				val = a.getPower(self.color.value())/2
	        	self.leftMotor.run_direct(duty_cycle_sp=(50-val)/2)
	        	self.rightMotor.run_direct(duty_cycle_sp=(50+val)/2)


        def __resetMotors(self):
				self.rightMotor.reset()
                self.leftMotor.reset()
                return self

        def __runMotor(self, motor, sp):
                motor.run_direct(duty_cycle_sp=sp)
                return self

        def __turn90(self, direction):

                self.__resetMotors()

                if direction == 'r':
                        self.__runMotor(self.leftMotor, 30)
                        sleep(2.2)
                        self.__resetMotors()

                elif direction == 'l':
                        self.__runMotor(self.leftMotor, 30)
                        sleep(2.2)
                        self.__resetMotors()

                else:
                        raise RuntimeError('Unknown direction')


        def __objectDetected(self):
                val = self.sonar.value()
                #value in mm
                if val < 200:
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
        		self.head.run_to_abs_pos(duty_cycle_sp=30, position_sp=90)
        	elif direction == 'l':
        		self.head.run_to_abs_pos(duty_cycle_sp=30, position_sp=-90)
        	else:
                raise RuntimeError('Unknown direction')

        def __avoidObject(self, snapshot):
        	self.__resetMotors()
        	pid = PidController(snapshot, 1, 0, 0)
        	while (self.color.value() > 60):
        		self.__runMotor(self.leftMotor, 10)
        		self.__runMotor(self.rightMotor, pid.getPower(self.sonar.value()))

        def run(self):
                detected = 0
                #while(not detected):
                self.__follow_line()
                #       detected = self.__findObject()
                self.__resetMotors()
                val = self.sonar.value()
                self.__turn90('r')
                self.__turnHead90('l')
                #self.__findObject()
                self.__avoidObject(val)
                #self.follow_line()
