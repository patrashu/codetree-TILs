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
    # arr[px][py] = -1 # exit

    cnt, time, move = M, K, 0
    while cnt and time:
        # move
        exit_pid = []
        for pid, (cx, cy) in pid_to_player.items():
            candits = []
            bound = abs(px-cx) + abs(py-cy)
            for k in range(4):
                nx, ny = cx+direc[k][0], cy+direc[k][1]
                if nx < 0 or nx >= N or ny < 0 or ny >= N or arr[nx][ny] > 0:
                    continue
                tmp = abs(px-nx) + abs(py-ny)
                if tmp < bound:
                    candits.append((i, tmp, nx, ny))
            
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

        # find sub arr
        ans = []
        grid = 2
        while grid <= N:
            for p in range(0, N-grid):
                for q in range(0, N-grid):
                    exit_pos, player_pos = [], []
                    for i in range(p, p+grid):
                        for j in range(q, q+grid):
                            if (i, j) == (px, py): # if
                                exit_pos.append((i, j))
                            elif player_to_pid[(i, j)]:
                                player_pos.extend(player_to_pid[(i, j)])
                    if exit_pos and player_pos:
                        ans.append((p, q, grid, exit_pos, player_pos))
            if ans:
                break
            grid += 1

        # rotate and update
        p, q, grid, exit_pos, player_pos = ans[0]
        for tx, ty in exit_pos:
            arr[tx][ty] = -11
        for _pid in player_pos:
            tx, ty = pid_to_player[_pid]
            arr[tx][ty] = -(_pid+1)

        sub_arr = [mtrx[q:q+grid] for mtrx in arr[p:p+grid]]
        sub_arr = rotate(sub_arr)

        for i in range(p, p+grid):
            for j in range(q, q+grid):
                arr[i][j] = sub_arr[i-p][j-q]
                if arr[i][j] > 0:
                    arr[i][j] -= 1
                else:
                    if arr[i][j] == -11:
                        arr[i][j] = 0
                        px, py = i, j
                    elif arr[i][j] < 0:
                        _pid = -arr[i][j]
                        _pid -= 1
                        cx, cy = pid_to_player[_pid]
                        _idx = player_to_pid[(cx, cy)].index(_pid)
                        player_to_pid[(cx, cy)].pop(_idx)
                        player_to_pid[(i, j)].append(_pid)
                        pid_to_player[_pid] = [i, j]
                        arr[i][j] = 0
        
        time -= 1
        # print(cnt, time)
        # for k, v in pid_to_player.items():
        #     print(k, v)
        # print()
        # break
   
    print(move)
    print(px+1, py+1)