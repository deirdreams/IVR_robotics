class PidController:

	def __init__(self, sp):
		self.sp = sp
		self.pv = 0
		self.KP = 0.5
		self.KI = 0.5
		self.KD = 0.5
		self.errorSum = [0]

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
