import sys
import time
import json
import chess
from queue import Empty
from pprint import pprint
from stdio_ipc import ChildProcess

# meaning of op
# 翻面 -1
# 上下左右 0 1 2 3
# 炮上下左右 4 5 6 7

ff = open('procedure.json', 'w')

global red
global black



def action(ai):
	try:
		ai.send('action\n')
		message = ai.recv(timeout=1)
		posx, posy, tox, toy = map(int, message.split(' '))
	except Empty as e:
		return { 'err': 'timeout' }
	except :
		return { 'err': 'wrong format. your output: %s' % repr(message) }
	return { 'posx': posx, 'posy': posy, 'tox': tox, 'toy': toy }

def message(ai, id, res):
	x = res['posx']
	y = res['posy']
	xx = res['tox']
	yy = res['toy']
	ai.send('message\n%d %d %d %d %d %d\n' % (x, y, xx, yy, board.col[x][y], board.kind[x][y]))

def send_id(ai, id):
	ai.send('id\n%d\n' % id)

def finish(winner, err1, err2):
	 # kill ai and write stdio log
    if type(ai1) is not dict:
        ai1.exit()
        ai1.save_stdio('ai1_stdin.log', 'ai1_stdout.log', 'ai1_stderr.log')
    if type(ai2) is not dict:
        ai2.exit()
        ai2.save_stdio('ai2_stdin.log', 'ai2_stdout.log', 'ai2_stderr.log')

    # write result
    result = {
        'ai1_id': id1,
        'ai2_id': id2,
        'ai1_err': err1,
        'ai2_err': err2,
        'winner': winner,
    }
    pprint(result)
    with open('result.json', 'w') as f:
        f.write(json.dumps(result))

    procedure = {
    	'init-board' : init_board,
    	'step' : Record
    }
    ff.write(json.dumps(procedure))
    #ff.write(json.dumps(Record))
    # exit
    sys.exit(0)


def work(color, res):
	info = board.check(color, res)
	ret, error = info.split(' ')
	if ret == 'right':
		pass
	elif ret == 'wrong':
		if color == 0:
			res['err'] = error
			finish(1, res, '')
		else:
			res['err'] = error
			finish(0, '', res)
	elif ret == 'end':
		if color == 0:
			people = red
		else:
			people = black
		finish(people , '', '')

def check_both(ai1_success, ai2_success, res1, res2):
    if not ai1_success and not ai2_success:
        finish(0, res1['err'], res2['err'])
    elif not ai1_success and ai2_success:
        finish(2, res1['err'], '')
    elif not ai2_success and ai1_success:
        finish(1, '', res2['err'])

def spawnAI(args):
    try:
        ai = ChildProcess(args)
        return ai
    except:
        return { 'err': 'fail to spawn the program.' + str(sys.exc_info()[1]) }

if len(sys.argv) != 3:
    print('usage:   ./sample_judge.py AI1Path AI2Path')
    print('example: ./sample_judge.py ./sample_ai ./sample_ai')
    print('')
    sys.exit(1)

seed_base = int(time.time() * 1e3) % 10000000000
id1 = seed_base % 2
id2 = 1 - id1
if id1 == 0:
	red = 1
	black = 2
else:
	red = 2
	black = 1
ai1 = spawnAI([sys.argv[1], '%.0f' % (seed_base+0)])
ai2 = spawnAI([sys.argv[2], '%.0f' % (seed_base+1)])
check_both(type(ai1) is not dict, type(ai2) is not dict, ai1, ai2)

# send id
send_id(ai1, id1)
send_id(ai2, id2)

now_sit = 0

global board
global init_board
global Record 


def Record_Chess():
	for i in range(4):
		ret = []
		for j in range(8):
			ret.append({
				'kind' : board.kind[i][j],
				'color' : board.col[i][j]
			})
		init_board.append(ret)
		#ff.write(json.dumps(ret))
		#ff.write("\n")

board = chess.chess()

board.output()

Record = []
init_board = []

Record_Chess()

while True:
	if now_sit == 0:
		res1 = action(ai1)
		check_both('err' not in res1, True, res1,'')
		
		work(id1, res1)
		message(ai1, id1, res1)
		message(ai2, id1, res1)
		Record.append(res1)
		#Record_Procedure(res1)
		#now_sit = 1 - now_sit
	else:
		res2 = action(ai2)
		check_both(True, 'err' not in res2, '', res2)

		work(id2, res2)
		message(ai1, id2, res2)
		message(ai2, id2, res2)
		Record.append(res2)
		#Record_Procedure(res2)
		#now_sit = 1 - now_sit
	now_sit = 1 - now_sit

