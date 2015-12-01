#!/usr/bin/env python3

import sys
import time
import json
import chess
import threading
import locale
from queue import Empty
from pprint import pprint
from stdio_ipc import ChildProcess

# meaning of op
# 翻面 -1
# 上下左右 0 1 2 3
# 炮上下左右 4 5 6 7

def action(ai):
    try:
        ai.send('action\n')
        message = ai.recv(timeout=1)
        posx, posy, tox, toy = map(int, message.strip().split(' '))
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
    try:
        ai.send('id\n%d\n' % id)
        name = ai.recv(timeout=1).strip()
    except Empty as e:
        return { 'err': 'timeout' }
    except Exception as e:
        print(e)
        return { 'err' : str(e) }
    return name

def finish(winner, err0, err1):
    global running

     # kill ai and write stdio log
    if type(ai0) is not dict:
        ai0.exit()
        ai0.save_stdio('ai0_stdin.log', 'ai0_stdout.log', 'ai0_stderr.log')
    if type(ai1) is not dict:
        ai1.exit()
        ai1.save_stdio('ai1_stdin.log', 'ai1_stdout.log', 'ai1_stderr.log')

    # write result
    result = {
        'user': [name0, name1],
        'err': [err0, err1],
        'id': [id0, id1],
        'total': steps,
        'result': winner,
        'init-board' : init_board,
        'step' : Record
    }

    if not is_p2dv:
        pprint(result)
    with open('result.json', 'w') as f:
        f.write(json.dumps(result))

    # exit
    running = False
    sys.exit(0)

def work(color, res):
    ret, error = board.check(color, res)
    if ret == 'right':
        pass
    elif ret == 'wrong':
        if color == 0:
            res['err'] = error
            finish(color_ai[1], '', '')
        else:
            res['err'] = error
            finish(color_ai[0], '', '')
    elif ret == 'end':
        finish(color_ai[color], '', '')

def check_both(ai0_success, ai1_success, res1, res2):
    if not ai0_success and not ai1_success:
        finish(2, res1['err'], res2['err'])
    elif not ai0_success and ai1_success:
        finish(1, res1['err'], '')
    elif not ai1_success and ai0_success:
        finish(0, '', res2['err'])

def spawnAI(args):
    try:
        ai = ChildProcess(args)
        return ai
    except:
        return { 'err': 'fail to spawn the program.' + str(sys.exc_info()[1]) }

def Record_Chess():
    for i in range(4):
        ret = []
        for j in range(8):
            ret.append({
                'kind' : board.kind[i][j],
                'color' : board.col[i][j]
            })
        init_board.append(ret)

def judge():
    global board, id0, id1, ai0, ai1, name0, name1, color_ai, steps, Record, init_board

    # start working
    steps = 0
    now_sit = 0
    Record = []
    init_board = []
    board = chess.chess()

    # record chess
    Record_Chess()

    # spawn AI
    seed_base = int(time.time() * 1e3) % 10000000000
    id0 = seed_base % 2
    id1 = 1 - id0
    color_ai = [None, None]
    color_ai[0] = 0 if id0 == 0 else 1
    color_ai[1] = 1 - color_ai[0]
    ai0 = spawnAI([sys.argv[1], '%.0f' % (seed_base+0)])
    ai1 = spawnAI([sys.argv[2], '%.0f' % (seed_base+1)])
    check_both(type(ai0) is not dict, type(ai1) is not dict, ai0, ai1)

    # send ID and get name
    res0 = send_id(ai0, id0)
    res1 = send_id(ai1, id1)
    name0 = res0 if type(res0) is not dict else '[Unknown]'
    name1 = res1 if type(res1) is not dict else '[Unknown]'
    check_both(type(res0) is not dict, type(res1) is not dict, res0, res1)

    while steps < 2000:
        steps += 1
        if now_sit == 0:
            res1 = action(ai0)
            Record.append(res1)
            check_both('err' not in res1, True, res1,'')
            
            work(id0, res1)
            message(ai0, id0, res1)
            message(ai1, id0, res1)

            now_sit = now_sit^1
        else:
            res2 = action(ai1)
            Record.append(res2)
            check_both(True, 'err' not in res2, '', res2)

            work(id1, res2)
            message(ai0, id1, res2)
            message(ai1, id1, res2)

            now_sit = now_sit^1

    # stpes exceeded
    finish(2, 'steps exceeded', 'steps exceeded')

def p2dv():
    t = threading.Thread(target=judge)
    t.start()

    while True:
        line = sys.stdin.readline()
        if not running:
            sys.stderr.write('finished\n')
            sys.stderr.flush()
            break

        if line == 'get steps\n':
            sys.stderr.write('%d\n'%steps)

        sys.stderr.flush()

def main():
    global running, is_p2dv

    if not (len(sys.argv) in [3, 4]):
        print('usage:   ./main.py ai0Path ai1Path')
        print('example: ./main.py ./sample_ai ./sample_ai')
        print('')
        sys.exit(1)

    running = True

    if len(sys.argv) == 4 and sys.argv[3] == 'p2dv':
        is_p2dv = True
        p2dv()
    else:
        is_p2dv = False
        judge()


locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
steps = 0
main()
