class PidController:

	def __init__(self, sp, p, i, d):
		
		# initialize with sp as desired value
		# p, i, d as (P)(I)(D)-Controller

		self.sp = sp
		self.pv = 0
		self.KP = (0, 0.5)[p]
		self.KI = (0, 0.5)[i]
		self.KD = (0, 0.5)[d]
		self.pEnabled = p
		self.iEnabled = i
		self.dEnabled = d
		self.errorSum = [0]

	def setKP(self, kp):
		if self.pEnabled:
			self.KP = kp
		else:
			raise RuntimeError('p not enable thus kp can\'t be changed.')

	def setKI(self, ki):
		if self.iEnabled:
			self.KI = ki
		else:
			raise RuntimeError('i not enable thus ki can\'t be changed.')

	def setKD(self, kd):
		if self.dEnabled:
			self.KD = kd
		else:
			raise RuntimeError('d not enable thus kd can\'t be changed.')

	def __getError(self):
		error = self.sp - self.pv
		return error

	def __getP(self):
		return self.__getError() * self.KP

	def __getI(self):
		return sum(self.errorSum) * self.KI

	def __getD(self):
		return (self.__getError() - self.errorSum[-1]) * self.KD

	def getPower(self, pv):
		self.pv = pv
		ret = self.__getP() + self.__getI() + self.__getD()
		self.errorSum.append(self.__getError())
		return 100*ret/self.sp
