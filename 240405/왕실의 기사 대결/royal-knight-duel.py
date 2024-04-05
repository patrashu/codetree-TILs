"""
LxL 체스판에서 대결 준비

(1). 기사 이동
- 왕에게 명령 받은 기사는 상하좌우 중 한 곳으로 이동할 수 있음.
- 이동하려는 칸에 기사가 있으면 연쇄적으로 밀려남
- 이동하려는 방향의 끝에 벽이 있다면 모든 기사는 이동할 수 없음
- 사라진 기사한테 명령 내리면 반응이 없음.

(2). 데미지
- 명령 받은 기사가 밀치면 밀려난 기사는 피해를 입게 됨.
- w*h 직사각형 내에 놓여있는 함정의 수 만큼만 피해를 입음
- 체력이상으로 데미지를 받을 경우 체스판에서 사라짐
- 명령 받은 기사는 피해를 입지 않음
- 모두 밀리고나서 대미지를 입게 됨.

(3) Q번 반복
- 생존한 기사들이 총 받은 대미지의 합을 출력하는 프로그램

0, 1, 2 => 빈칸, 함정, 벽
r, c, h, w, k => (r, c)에서 (r+h, c+w) 직사각형 형태이며, 초기 체력이 K라는 것을 의미
초기에 기사끼리 겹치지 않음. 기사와 벽이 겹쳐서 주어지지 않음

Q개의 줄에 걸쳐서 왕의 명령이 주어짐
- i번 기사 방향 d로 한 칸이동
"""
from collections import deque, defaultdict

def find_group(pos, cur_pos, pid, nd, direc):
    sx, sy = cur_pos[pid][:2]
    visit, knight = set(), set()
    visit.add((sx, sy))
    knight.add(pid)
    dq = deque([(sx, sy)])
    length = len(pos)

    while dq:
        cx, cy = dq.popleft()
        for i in range(4):
            dx, dy = direc[i]
            nx, ny = cx+dx, cy+dy
            if nx < 0 or nx >= length or ny < 0 or ny >= length or pos[nx][ny] == 0:
                continue
            if (nx, ny) not in visit:
                if pos[nx][ny] in knight:
                    visit.add((nx, ny))
                    dq.append((nx, ny))
                else:
                    ddx, ddy = direc[nd]
                    if (nx-ddx, ny-ddy) in visit:
                        knight.add(pos[nx][ny])
                        visit.add((nx, ny))
                        dq.append((nx, ny))
    return visit, knight

if __name__ == '__main__':
    L, N, Q = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(L)]
    pos = [[0]*L for _ in range(L)]
    direc = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    init_hp, cur_hp = {}, {}
    cur_pos = {}

    # initialize
    for i in range(N):
        x, y, h, w, k = map(int, input().split())
        init_hp[i+1], cur_hp[i+1] = k, k
        for tx in range(x-1, x+h-1):
            for ty in range(y-1, y+w-1):
                pos[tx][ty] = i+1
        cur_pos[i+1] = [x-1, y-1, x+h-1, y+w-1]

    cmds = [list(map(int, input().split())) for _ in range(Q)]
    for pid, nd in cmds:
        if cur_hp[pid] == 0:
            continue

        # find_group / move (cascade)
        visit, knights = find_group(pos, cur_pos, pid, nd, direc)
        move_flag = True
        damage = [0]*(N+1)

        visit_dq = deque(list(visit))
        dx, dy = direc[nd]
        for cx, cy in visit_dq:
            nx, ny = cx+dx, cy+dy
            if nx < 0 or nx >= L or ny < 0 or ny >= L or arr[nx][ny] == 2:
                move_flag = False
                break
            if arr[nx][ny] == 1:
                if pos[cx][cy] != pid:
                    damage[pos[cx][cy]] += 1
        
        if not move_flag:
            continue

        # damage 처리
        remove_set = set()
        for i in range(1, N+1):
            cur_hp[i] -= damage[i]
            if cur_hp[i] <= 0:
                cur_hp[i] = 0
                remove_set.add(i)
        
        # 이동할건데 
        # remove_set에 있으면 0처리
        new_pos = [[0]*L for _ in range(L)]
        for i, j in visit_dq:
            if (i, j) in visit_dq:
                if pos[i][j] in remove_set:
                    continue
                nx, ny = i+dx, j+dy
                new_pos[nx][ny] = pos[i][j]
            else:
                new_pos[i][j] = pos[i][j]

        for k, (x1, y1, x2, y2) in cur_pos.items():
            if k in knights:
                continue
            for i in range(x1, x2):
                for j in range(y1, y2):
                    new_pos[i][j] = k
        pos = new_pos

        # 시작 좌표 갱신
        for knight in knights:
            if knight in remove_set:
                continue
            x1, y1, x2, y2 = cur_pos[knight]
            cur_pos[knight] = [x1+dx, y1+dy, x2+dx, y2+dy]

    ans = 0
    cur_hp = [[k, v] for k, v in cur_hp.items() if v > 0]
    for k, v in cur_hp:
        ans += init_hp[k] - v   
    print(ans)