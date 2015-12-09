# cover 0: covered 1: clear -1: no chess here
# col 0(id1) 1(id2)
# kind 
# 0 帅 * 1 0
# 1 士 * 2 2
# 2 相 * 2 4
# 3 车 * 2 6
# 4 马 * 2 8
# 5 炮 * 2 10
# 6 兵 * 5 
# move
# 翻面 -1
# 上下左右 0 1 2 3
# 炮上下左右 4 5 6 7

import random

op_norm = [0, 1, 2 ,3]
op_pao = [4, 5, 6, 7]



def Hash(num):
		if num == 0: 
			ret = 0
		elif num <= 2:
			ret = 1
		elif num <= 4:
			ret = 2
		elif num <= 6:
			ret = 3
		elif num <= 8:
			ret = 4
		elif num <= 10:
			ret = 5
		else:
			ret = 6
		return ret

class chess:
	def output(self):
		for i in range(4):
			for j in range(8):
				print(' ',self.kind[i][j],end=' ')
			print()
		print("---")
		for i in range(4):
			for j in range(8):
				print(' ',self.col[i][j],end=' ')
			print()
		print("----")
		for i in range(4):
			for j in range(8):
				print(' ',self.cover[i][j],end=' ')
			print()
	def __init__(self):
		#random initiation
		#self.log = log
		self.cover = [[0 for i in range(8)] for i in range(4)]
		self.col = [[-1 for i in range(8)] for i in range(4)]
		self.kind = [[-1 for i in range(8)] for i in range(4)]
		self.cnt = []
		self.cnt.append(16) 
		self.cnt.append(16)
		cnt1 = cnt2 = 0
		# red 0 
		# blue 1
		red = []
		blue = []
		for i in range(4):
			for j in range(8):
				tt = random.randint(1,100)
				if (tt & 1):
					if cnt1 == 16:
						cnt2 += 1
						self.col[i][j] = 0
						red.append((i,j))
					else:
						cnt1 += 1
						self.col[i][j] = 1
						blue.append((i,j))
				else:
					if cnt2 == 16:
						cnt1 += 1
						self.col[i][j] = 1
						blue.append((i,j))
					else:
						cnt2 += 1
						self.col[i][j] = 0
						red.append((i,j))
		choose = [i for i in range(16)]
		random.shuffle(choose)
		cnt = 0
		for obj in red:
			self.kind[obj[0]][obj[1]] = Hash(choose[cnt])
			cnt += 1
		random.shuffle(choose)
		cnt = 0
		for obj in blue:
			self.kind[obj[0]][obj[1]] = Hash(choose[cnt])
			cnt += 1

	def __inBoard__(self, x, y):
		return x >= 0 and x < 4 and y >= 0 and y < 8;

	def __swap__(self, x, y, xx, yy):
		self.cover[x][y], self.cover[xx][yy] = self.cover[xx][yy], self.cover[x][y]
		self.col[x][y], self.col[xx][yy] = self.col[xx][yy], self.col[x][y]
		self.kind[xx][yy] = self.kind[x][y]
		#self.kind[x][y], self.kind[xx][yy] = self.kind[xx][yy], self.kind[x][y]

	def __eat__(self, attack, defend):
		if attack == 0 and defend == 6:
			return False
		if attack == 5:
			ret = True
		elif attack == 6:
			if defend == 0 or defend == 6:
				ret = True
			else:
				ret = False
		else:
			if attack <= defend:
				ret = True
			else: 
				ret = False
		return ret

	def __corss__(self, x, y, xx, yy):
		if x == xx:
			if y > yy:
				if self.__inBoard__(x, yy + 1) and self.cover[x][yy + 1] == -1:
					ret = False
				else:
					ret = True
			elif y < yy:
				if self.__inBoard__(x, yy - 1) and self.cover[x][yy - 1] == -1:
					ret = False
				else:
					ret = True
			else:
				ret = False
		elif y == yy:
			if x > xx:
				if self.__inBoard__(xx + 1, y) and self.cover[xx + 1][y] == -1:
					ret = False
				else:
					ret = True
			elif x < xx:
			 	if self.__inBoard__(xx - 1, y) and self.cover[xx - 1][y] == -1:
			 		ret = False
			 	else:
			 		ret = True
			else:
				ret = False
		else:
			ret = False
		return ret


	def __move__(self, x, y, xx, yy):
		global flag
		ret = False
		if self.kind[x][y] == 5:
			if x == xx:
				if y == yy - 1 or y == yy + 1:
					ret = True
			elif y == yy:
				if x == xx - 1 or x == xx + 1:
					ret = True
			jump = False
			if x == xx:
				if y == yy - 2 or y == yy + 2:
					jump = True
			elif y == yy:
				if x == xx - 2 or x == xx + 2:
					jump = True	
			if jump == True:
				if x == xx:
					if y == yy + 2 or y == yy - 2:
						if self.__corss__(x, y, xx, yy):
							ret = True
							flag = True
				elif y == yy:
					if x == xx + 2 or x == xx - 2:
						if self.__corss__(x, y, xx, yy):
							ret = True
							flag = True	

		else: 
			if x == xx:
				if y == yy - 1 or y == yy + 1:
					ret = True
				else:
					ret = False
			elif y == yy:
				if x == xx - 1 or x == xx + 1:
					ret = True
				else:
					ret = False
			else:
				ret = False
		return ret

	def check(self, color, res):
		#x, y, xx, yy = map(int, res.split(' '))
		x = res['posx']
		y = res['posy']
		xx = res['tox']
		yy = res['toy']
		#print(color,' ',res['posx'],' ',res['posy'],' ',res['tox'],' ',res['toy'])

		#print("-------------------------------")
		#self.output()


		if (x == xx and y == yy) and self.__inBoard__(x, y):
			if self.cover[x][y] == 0:
				ret = 'right'
				error = 'good'
				self.cover[x][y] = 1
			else:
				ret = 'wrong'
				error = 'Cannot Flip'
			return ret, error

		flag = False

		if self.__inBoard__(x, y) and self.__inBoard__(xx, yy) and self.__move__(x, y, xx, yy):
			if self.cover[x][y] == 1:
				if self.col[x][y] == color:
					if self.cover[xx][yy] == 0:
						ret = 'wrong'
						error = 'Invalid Move'
					else:
						if self.cover[xx][yy] == -1:
							if self.kind[x][y] == 5 and flag == True:
								ret = 'wrong'
								error = 'Invalid Move of Pao'
								return ret, error
							self.cover[xx][yy] = 1
							self.col[xx][yy] = self.col[x][y]
							self.kind[xx][yy] = self.kind[x][y]
							self.cover[x][y] = -1
							ret = 'right'
							error = 'good'
						else:
							if self.kind[x][y] == 5 and flag == False:
								ret = 'wrong'
								error = 'Pao Can Not Eat'
								return ret, error
							if self.__eat__(self.kind[x][y], self.kind[xx][yy]):
								ret = 'right'
								error = 'good'
								self.kind[xx][yy] = self.kind[x][y]
								self.col[xx][yy] = self.col[x][y]
								self.cover[xx][yy] = 1
								self.cover[x][y] = -1
								self.cnt[color^1] = self.cnt[color^1] - 1
							else:
								ret = 'wrong'
								error = 'Can Not Eat'
				else:
					ret = 'wrong'
					error = 'Not Your Chess'
			else:
				ret = 'wrong'
				error = 'No Chess or Not Flipped Yet'
		else:
			ret = 'wrong'
			error = 'Out of the Board or Invalid Move'
		
		if self.cnt[0] == 0 or self.cnt[1] == 0:
			ret = 'end'
			error = 'good'
		

		return ret, error

	




