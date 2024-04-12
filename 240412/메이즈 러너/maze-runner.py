"""
1. N * N 미로
2. 각 칸은 3가지 상태 중 하나를 가진다
- 빈칸 : 이동 가능한 칸
- 벽 : 이동할 수 없는 칸 / 내구도가 1~9 / 회전하면 1씩 깎임 / 0되면 빈칸
- 출구 : 도착하면 즉시 탈출

3. 1초마다 한 칸씩 움직임
- 동시에 움직인다
- 상하좌우로 움직일 수 있으며, 벽이 없는 곳으로만 이동 가능
- 움직이는 칸이 현재 머무르던 칸보다 맨해튼 거리가 가까워야함
- 2개 이상이면 상/하 우선
- 몬움직이면 x
- 한 칸에 여러명이 있을 수 있음

4. 이동했으면 회전함
- 한 명 이상의 참가자 + 출구를 포함하는 가장 작은 정사각형 searching
- 여러 개면 r이 작은 것을 우선, 그래도 같은면 c 우선
- 선택 영역은 왼쪽 90도 회전, 내구도 -= 1

5. K초 동안 반복, 그 전에 끝나면 종료
- 종료 후 모든 참가자 이동 거리 합 + 출구 좌표 출력
"""
from copy import deepcopy
from collections import defaultdict

def rotate(matrix):
    return [list(mtrx) for mtrx in zip(*matrix[::-1])]

if __name__ == '__main__':
    N, M, K = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]
    direc = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    player_to_pid = defaultdict(list)
    pid_to_player = {}

    for i in range(M):
        a, b = map(int, input().split())
        player_to_pid[(a-1, b-1)].append(i)
        pid_to_player[i] = [a-1, b-1]

    px, py = map(int, input().split())
    px, py = px-1, py-1

    cnt, time, move = M, K, 0
    while cnt and time:
        # move
        exit_pid = []
        for pid, (cx, cy) in pid_to_player.items():
            candits = []
            bound = abs(px-cx) + abs(py-cy)
            for k in range(4):
                nx, ny = cx+direc[k][0], cy+direc[k][1]
                if nx < 0 or nx >= N or ny < 0 or ny >= N or arr[nx][ny] != 0:
                    continue
                tmp = abs(px-nx) + abs(py-ny)
                if tmp < bound:
                    candits.append((k, tmp, nx, ny))
            
            # check
            if not candits:
                continue
            
            # update
            candits.sort(key=lambda x: (x[1], x[0]))
            _, _, nx, ny = candits[0]
            if (px, py) == (nx, ny):
                exit_pid.append(pid)

            pid_to_player[pid] = [nx, ny]
            _idx = player_to_pid[(cx, cy)].index(pid)
            player_to_pid[(cx, cy)].pop(_idx)
            player_to_pid[(nx, ny)].append(pid)
            move += 1

        # remove
        for pid in exit_pid:
            tx, ty = pid_to_player[pid]
            del pid_to_player[pid]
            _idx = player_to_pid[(tx, ty)].index(pid)
            player_to_pid[(tx, ty)].pop(_idx)
            cnt -= 1
        
        if cnt == 0:
            break

        # find sub arr
        ans = []
        grid = 2
        while grid <= N:
            for p in range(0, N-grid+1):
                for q in range(0, N-grid+1):
                    exit_pos, player_pos = [], []
                    for i in range(p, p+grid):
                        for j in range(q, q+grid):
                            if (px, py) == (i, j): # if
                                exit_pos.append((i, j))
                            elif len(player_to_pid[(i, j)]) > 0:
                                player_pos.extend(player_to_pid[(i, j)])

                    if len(exit_pos) > 0 and len(player_pos) > 0:
                        ans.append((p, q, grid, exit_pos, player_pos))

            if len(ans) > 0:
                break
            else:
                grid += 1

        ans.sort(key=lambda x: (x[2], x[0], x[1]))
        # rotate and update
        p, q, grid, exit_pos, player_pos = ans[0]
        for tx, ty in exit_pos:
            arr[tx][ty] = -11

        bef_to_cur = {}
        for i in range(p, p+grid):
            for j in range(q, q+grid):
                ox, oy = i-p, j-q
                rx, ry = oy, grid-ox-1
                bef_to_cur[(rx+p, ry+q)] = [i, j]
        new_arr = deepcopy(arr)
        
        visit = [False]*M
        for (tx, ty), (cx, cy) in bef_to_cur.items():
            new_arr[tx][ty] = arr[cx][cy]
            if new_arr[tx][ty] == -11:
                new_arr[tx][ty] = 0
                px, py = tx, ty
            elif new_arr[tx][ty] > 0:
                new_arr[tx][ty] -= 1
            for _pid in player_pos:
                ccx, ccy = pid_to_player[_pid]
                if not visit[_pid] and (ccx, ccy) == (cx, cy):
                    _idx = player_to_pid[(cx, cy)].index(_pid)
                    player_to_pid[(cx, cy)].pop(_idx)
                    player_to_pid[(tx, ty)].append(_pid)
                    pid_to_player[_pid] = [tx, ty]
                    visit[_pid] = True

        arr = new_arr
        time -= 1
   
    print(move)
    print(px+1, py+1)