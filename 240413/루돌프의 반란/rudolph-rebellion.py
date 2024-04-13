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
                score[i] += D # 점수 추가
                c_q = []
                tmp = D
                tpid = pos_to_pid[(cx, cy)]
                santa[tpid][0], santa[tpid][1] = tx, ty
                del pos_to_pid[(cx, cy)]
                pos_to_pid[(tx, ty)] = tpid

                while True:
                    ntx, nty = tx-direc[td][0]*tmp, ty-direc[td][1]*tmp
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
                            tpid = pos_to_pid[(tx, ty)]
                            tmp = 1

                for tpid, tx, ty, ntx, nty, tflag in c_q[::-1]:
                    if not tflag:
                        status[tpid] = 2
                        del pos_to_pid[(tx, ty)]
                        cnt -= 1
                    else:
                        if tpid == i:
                            status[tpid], stime[tpid] = 1, 2 # 기절 + time
                        del pos_to_pid[(tx, ty)]
                        santa[tpid] = [ntx, nty]
                        pos_to_pid[(ntx, nty)] = tpid

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