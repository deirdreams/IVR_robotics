class PidController:

	def __init__(self, sp, p, i, d):
		
		# initialize with sp as desired value
		# p, i, d as (P)(I)(D)-Controller

		self.sp = sp
		self.pv = 0
		self.KP = (0, 0.5)[p]
		self.KI = (0, 0.5)[i]
		self.KD = (0, 0.5)[d]
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
