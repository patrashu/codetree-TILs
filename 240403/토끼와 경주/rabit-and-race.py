"""
1. 경주 시작 준비
- N*M 경기장에서 경주할 준비를 함
- 각 토끼에 고유 번호가 있으며, 한 번 움직일 때 꼭 이동해야하는 거리도 있음 (pid, d_i)

2. 경주 진행
- 우선순위가 높은 토끼를 뽑아 멀리 보내는 것을 K번 반복
- 우선순위
    - 총 점프 횟수가 적은 토끼
    - 현재 서있는 행+열 번호가 작은 토끼
    - 행번호가 작은 토끼
    - 열번호가 작은 토끼
    - 고유 번호가 작은 토끼
- i번째 토끼가 정해지면 각 방향으로 d_i만큼 이동했을 때의 위치를 구함
- 격자를 벗어나면 반대로 바꿔 이동
- 4개 위치 중 (행+열, 행, 열) 큰 순서대로 우선순위 => 가장 큰 위치로 이동
- r, c로 이동하면 나머지 토끼는 r+c만큼 점수를 얻음
- 위 과정을 K번의 턴 동안 반복
- K번 끝나면 (행+열, 행, 열, 고유번호) 큰 순서대로 우선순위가 높은 토끼를 골라 S를 더해줌
- 이때 꼭 주의할점은 K번의 턴 동안 움직였던 토끼 중 우선순위가 높은 토끼만 골라야 함

100 => 이동 준비
200 => 경주
300 => 이동거리 변경
400 => 최고 토끼 선정
"""
import heapq
from collections import defaultdict

def prepare(n, m, rabbits):
    new_rabbits, score, cur_pos = {}, {}, {}
    for i in range(0, len(rabbits), 2):
        score[rabbits[i]] = [0, 0] # 점프 횟수, 점수
        cur_pos[rabbits[i]] = [0, 0] # 좌표
        new_rabbits[rabbits[i]] = rabbits[i+1]
    return new_rabbits, score, cur_pos

def run(rabbits, score, pos, n, m, k, s):
    # initialize
    hq, visit = [], set()
    direc = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    for key, vaule in rabbits.items():
        cnt = score[key][0]
        x, y = pos[key]
        hq.append((cnt, x+y, x, y, key, vaule))
    heapq.heapify(hq)

    for _ in range(k):
        cnt, rc, r, c, pid, move = heapq.heappop(hq) # 가장 우선순위 높은거 pop

        # 4방향 check
        candits = []
        for i in range(4):
            remain, idx = None, i
            if i%2 == 0: remain = move % (2*n-2)
            elif i%2 == 1: remain = move % (2*m-2)
            cx, cy = pos[pid]

            while remain:
                dx, dy = direc[idx]
                if idx == 0:
                    if cx - remain < 0:
                        cx, remain, idx = 0, remain-cx, idx+2
                    else:
                        cx, remain = cx-remain, 0
                elif idx == 1:
                    if cy + remain < m:
                        cy, remain = cy+remain, 0
                    else:
                        cy, remain, idx = m-1, remain-(m-1-cy), idx+2
                elif idx == 2:
                    if cx + remain < n:
                        cx, remain = cx+remain, 0
                    else:
                        cx, remain, idx = n-1, remain-(n-1-cx), idx-2
                else:
                    if cy - remain < 0:
                        cy, remain, idx = 0, remain-cy, idx-2
                    else:
                        cy, remain = cy-remain, 0
            candits.append((cx+cy, cx, cy))

        # 하나 골라서 이동
        candits.sort(key=lambda x: (-x[0], -x[1], -x[2]))
        _, r, c = candits[0]
        pos[pid] = [r, c]

        # 점수 추가
        for kk, vv in score.items():
            if pid == kk:
                vv[0] += 1
            else:
                vv[1] += (r+c+2)

        visit.add(pid)
        heapq.heappush(hq, (cnt+1, r+c, r, c, pid, move))

    max_rabbits = []
    for pid in visit:
        x, y = pos[pid]
        max_rabbits.append((x+y, x, y, pid))
    
    max_rabbits.sort(key=lambda x: (-x[0], -x[1], -x[2], -x[3]))
    pid = max_rabbits[0][3]
    score[pid][1] += s
    return rabbits, score, pos

def change_move(move_dict, pid, l):
    move_dict[pid] *= l
    return

def select_king(score):
    max_value = 0
    for _, value in score.values():
        max_value = max(max_value, value)
    return max_value

if __name__ == '__main__':
    new_rabbits, score, cur_pos = None, None, None
    n, m = None, None

    for _ in range(int(input())):
        cmd, *line = list(map(int, input().split()))    
        if cmd == 100:
            n, m, p, *rabbits = line
            new_rabbits, score, cur_pos = prepare(n, m, rabbits)
        elif cmd == 200:
            new_rabbits, score, cur_pos = run(new_rabbits, score, cur_pos, n, m, line[0], line[1])
        elif cmd == 300:
            change_move(new_rabbits, line[0], line[1])
        else:
            print(select_king(score))