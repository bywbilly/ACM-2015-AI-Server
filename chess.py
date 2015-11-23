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
				print(' ',self.kind[i][j],' ',self.col[i][j],end=' ')
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
		random.shuffle(self.kind);

	def __inBoard__(self, x, y):
		return x >= 0 and x < 4 and y >= 0 and y < 8;

	def __moveX__(self, x, op):
		if op == 0:
			ret = x - 1
		elif op == 1:
			ret = x + 1
		elif op == 2:
			ret = x
		else:
			ret = x
		return ret

	def __moveY__(self, y, op):
		if op == 0:
			ret = y
		elif op == 1:
			ret = y
		elif op == 2:
			ret = y - 1
		else:
			ret = y + 1
		return ret

	def __movePX__(self, x, op):
		if op == 4:
			ret = x - 2
		elif op == 5:
			ret = x + 2
		elif op == 6:
			ret = x
		else:
			ret = x
		return ret

	def __movePY__(self, y, op):
		if op == 4:
			ret = y
		elif op == 5:
			ret = y
		elif op == 6:
			ret = y - 2
		else:
			ret = y + 2
		return ret

	def __swap__(self, x, y, xx, yy):
		swap(self.cover[x][y], self.cover[xx][yy])
		swap(self.col[x][y], self.col[xx][yy])
		swap(self.kind[x][y], self.kind[xx][yy])

	def __eat__(self, attack, defend):
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
				if self.cover[x][yy + 1] == -1:
					ret = False
				else:
					ret = True
			else:
				if self.cover[x][yy - 1] == -1:
					ret = False
				else:
					ret = True
		else:
			if x > xx:
				if self.cover[xx + 1][y] == -1:
					ret = False
				else:
					ret = True
			else:
				if self.cover[xx - 1][y] == -1:
					ret = False
				else:
					ret = True
		return ret


	def check(self, color, res):
		x, y, op = map(int, res.split(' '))
		if self.__inBoard__(x, y):
			if op == -1:
				if self.cover[x][y] == 0:
					self.cover[x][y] = 1
					ret = 'right'
				else:
					ret = 'wrong'
					error = 'invalid operation'
			elif op in op_norm:
				if self.cover[x][y] == 1:
					if self.col[x][y] == color:
						xx = self.__moveX__(x, op)
						yy = self.__moveY__(y, op)
						if self.__inBoard__(xx, yy) and self.cover[xx][yy] == 1 and self.col[xx][yy] != color:
							if self.cover[xx][yy] == -1:
								self.swap(x, y, xx, yy)
								ret = 'right'
								error = 'good'
							else:
								if self.eat(self.kind[x][y], self.kind[xx][yy]):
									self.cover[x][y] = -1
									self.cover[xx][yy] = 1
									self.col[xx][yy] = color
									self.kind[xx][yy] = self.kind[x][y]
									self.cnt[color] = self.cnt[color] - 1

									ret = 'right'
									error = 'good'
								else:
									ret = 'wrong'
									error = 'cannot eat'
						else:
							ret = 'wrong'
							error = 'invalid operation'
					else:
						ret = 'wrong'
						error = 'invalid operation'
				else:
					ret = 'wrong'
					error = 'invalid operation'
			elif op in op_pao:
				if self.cover[x][y] == 1:
					if self.col[x][y] == color and self.kind[x][y] == 5:
						xx = self.__movePX__(x, op)
						yy = self.__movePY__(y, op)
						if self.__inBoard__(xx, yy) and self.cover[xx][yy] == 1 and self.col[xx][yy] != color:
							if self.cover[xx][yy] == (color^1):
								if self.eat(self.kind[x][y], self.kind[xx][yy]) and self.__cross__(x, y, xx, yy):
									self.cover[x][y] = -1
									self.cover[xx][yy] = 1
									self.col[xx][yy] = color
									self.kind[xx][yy] = self.kind[x][y]
									self.cnt[color] = self.cnt[color] - 1
									ret = 'right'
									error = 'good'
								else:
									ret = 'wrong'
									error = 'invalid operation'
							else:
								ret = 'wrong'
								error = 'invalid operation'
						else:
							ret = 'wrong'
							error = 'invalid operation'
					else:
						ret = 'wrong'
						error = 'invalid operation'
				else:
					ret = 'wrong'
					error = 'invalid operation'
			else:
				ret = 'wrong'
				error = 'invalid operation'
		else:
			ret = 'wrong'
			error = 'invalid pos'

		if cntb == 0 or cntr == 0:
			ret = 'end'

		return ret + ' ' + error

	




