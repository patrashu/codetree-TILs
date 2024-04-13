"""
1~P번까지 P명의 산타들이 이브를 준비하던 중, 루돌프가 반란 => 루돌프를 잡아라

(1). 게임 구성
- N*N / M턴에 걸쳐 진행되며, 매 턴마다 루돌프와 산타들이 한 번씩 움직임
- 루돌프 움직이고, 산타는 1~P 순서대로 (산타 pos 저장)
- 이때 기절 / 격자 밖 산타들은 탈락이라 움직일 수 없음 (산타 status 저장)

(2). 루돌프 움직임
- 가장 가까운 산타를 향해 한칸 돌진 / 탈락하지 않은 산타 중에서 (기절도 가능)
- 가까운 산타가 2명 이상이면, r / c가 큰 산타를 향해 돌진 (sort)
- 루돌프는 8방향 이동 가능 

(3). 산타 움직임
- 1~P 순서대로 움직이며, 기절/탈락 산타는 못 움직임 (0, 1, 2)
- 산타는 루돌프에게 가까워지는 방향으로 1칸 이동 (이동)
- 다른 산타가 있거나 게임판 밖으로는 이동할 수 없음 
- 움직일 수 없거나, 움직여도 가까워질 수 없으면 산타는 움직이지 않음 (가까워져야 함)
- 4방향 중 한곳으로 이동, min direc이 여러개면 상우하좌 순서대로 (상우하좌 순)

(4). 충돌
- 산타와 루돌프가 만나면 충돌함 
- 루돌프 충돌 => 산타가 C점수 + 루돌프가 이동해온 방향으로 C만큼 밀려남
- 산타가 충돌 => 산타가 D점수 + 자신이 이동한 반대방향으로 D만큼 밀려남
- 결국엔 산타가 뒤로 밀려난다는 뜻 
- 밀려난 위치가 격자 밖이면 탈락
- 밀려난 칸에 다른 산타가 있으면 상호작용

(5). 상호작용
- 루돌프와 충돌 후 포물선 궤적으로 이동하여 착지하게 되는 칸에서만 상호작용 가능
- 도착하는 칸에 산타가 있으면 1칸 밀려남 (연쇄 상호작용)

(6). 기절
- 산타는 루돌프와 충돌하면 기절하게 됨 (1턴 기절) (time flag)
- 기절한 산타는 못 움직임
- 루돌프가 돌진 대상으로 선택할 수 있음

(7). 종료
- M턴에 거쳐 루/산 순서대로 움직인 후 게임 종료
- P 산타가 중간에 모두 탈락하면 즉시 종료
- 탈락 안한 산타는 매턴 1점씩 부여

M턴 동안
- 루 -> 연쇄충돌체크 -> 산타 -> 연쇄충돌체크
- 중간에 모두 탈락할 시 즉시 종료
- 매 턴 탈락하지 않은 산타는 1점 추가
"""




if __name__ == '__main__':
    N, M, P, C, D = map(int, input().split())
    rx, ry = map(int, input().split())
    rx, ry = rx-1, ry-1
    santa, pos_to_pid, score, status, stime = {}, {}, [0]*P, [0]*P, [0]*P
    direc = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

    for _ in range(P):
        pid, r, c = map(int, input().split())
        santa[pid-1] = [r-1, c-1]
        pos_to_pid[(r-1, c-1)] = pid-1

    time, cnt = M, P
    while cnt and time:
        # deer
        r_candits = []
        for i in range(P):
            if status[i] == 2:
                continue
            cx, cy = santa[i]
            r_candits.append(((rx-cx)**2 + (ry-cy)**2, cx, cy, i))

        r_candits.sort(key=lambda x: [x[0], -x[1], -x[2]])
        _, cx, cy, pid = r_candits[0]
        r_candits.clear()
        for i in range(8):
            nx, ny = rx+direc[i][0], ry+direc[i][1]
            tmp = (cx-nx)**2 + (cy-ny)**2
            r_candits.append((tmp, i, nx, ny))

        r_candits.sort(key=lambda x: x[0])
        _, td, tx, ty = r_candits[0]
        if (tx, ty) != (cx, cy):
            rx, ry = tx, ty
        else:
            rx, ry = tx, ty
            score[pid] += C # 점수 추가
            c_q = []
            tmp = C
            while True:
                tpid = pos_to_pid[(tx, ty)]
                ntx, nty = tx+direc[td][0]*tmp, ty+direc[td][1]*tmp
                if ntx < 0 or ntx >= N or nty < 0 or nty >= N:
                    c_q.append([tpid, tx, ty, ntx, nty, False]) # pid, px, py, status
                    break
                else:
                    c_q.append([tpid, tx, ty, ntx, nty, True])
                    flag = pos_to_pid.get((ntx, nty), -1)
                    if flag == -1: # finish cascade
                        break
                    else:
                        tx, ty = ntx, nty
                        tmp = 1

            for tpid, tx, ty, ntx, nty, tflag in c_q[::-1]:
                if not tflag:
                    status[tpid] = 2
                    del pos_to_pid[(tx, ty)]
                    cnt -= 1
                else:
                    if tpid == pid:
                        status[tpid], stime[tpid] = 1, 2 # 기절 + time
                    del pos_to_pid[(tx, ty)]
                    santa[tpid] = [ntx, nty]
                    pos_to_pid[(ntx, nty)] = tpid

        # santa
        for i in range(P):
            if status[i]: # 기절 or out
                continue
            
            cx, cy = santa[i]
            bound, s_candits = (rx-cx)**2 + (ry-cy)**2, []
            for k in range(0, 8, 2):
                dx, dy = direc[k]
                nx, ny = cx+dx, cy+dy
                tmp = (rx-nx)**2 + (ry-ny)**2
                if nx < 0 or nx >= N or ny < 0 or ny >= N: # 범위 밖
                    continue
                if bound <= tmp or pos_to_pid.get((nx, ny), -1) != -1: # 가깝지않고 산타있으면
                    continue
                s_candits.append((tmp, k, nx, ny))
            
            if not s_candits:
                continue
            s_candits.sort(key=lambda x: [x[0], x[1]])
            _, td, tx, ty = s_candits[0]

            # not collapse
            if (tx, ty) != (rx, ry):
                santa[i][0], santa[i][1] = tx, ty
                del pos_to_pid[(cx, cy)]
                pos_to_pid[(tx, ty)] = i

            else:
                score[pid] += D # 점수 추가
                c_q = []
                tmp = D
                tpid = pos_to_pid[(cx, cy)]
                santa[tpid][0], santa[tpid][1] = tx, ty
                del pos_to_pid[(cx, cy)]
                pos_to_pid[(tx, ty)] = tpid

                while True:
                    ntx, nty = tx-direc[td][0]*tmp, ty-direc[td][1]*tmp
                    if ntx < 0 or ntx >= N or nty < 0 or nty >= N:
                        c_q.append([tpid, tx, ty, False]) # pid, px, py, status
                        break
                    else:
                        c_q.append([tpid, ntx, nty, True])
                        flag = pos_to_pid.get((ntx, nty), -1)
                        if flag == -1: # finish cascade
                            break
                        else:
                            tx, ty = ntx, nty
                            tpid = pos_to_pid[(tx, ty)]
                            tmp = 1

                for tpid, tx, ty, tflag in c_q[::-1]:
                    if not tflag:
                        status[tpid] = 2
                        del pos_to_pid[(tx, ty)]
                        cnt -= 1
                    else:
                        if tpid == pid:
                            status[tpid], stime[tpid] = 1, 2 # 기절 + time
                        stx, sty = santa[tpid]
                        santa[tpid][0], santa[tpid][1] = tx, ty
                        del pos_to_pid[(stx, sty)]
                        pos_to_pid[(tx, ty)] = tpid

        for i in range(P):
            if stime[i] > 0:
                stime[i] -= 1
                if stime[i] == 0 and status[i] == 1:
                    status[i] = 0
        
        # 1점 추가
        for i in range(P):
            if status[i] == 2:
                continue
            score[i] += 1
        time -= 1

    print(*score)