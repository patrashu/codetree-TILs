from collections import defaultdict

if __name__ == '__main__':
    N, M, K = map(int, input().split())
    arr = defaultdict(list)
    for i in range(N):
        line = list(map(int, input().split()))
        for j in range(N):
            arr[(i, j)].append(line[j])
    
    direc = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    pos_to_player = {}
    players = []
    scores = [0]*M
    for i in range(M):
        a, b, d, s = map(int, input().split())
        pos_to_player[(a-1, b-1)] = i
        players.append([a-1, b-1, d, s, 0])

    for _ in range(K):
        for pid in range(M):
            # move
            cx, cy, cd, cp, cg = players[pid]
            dx, dy = direc[cd]
            nx, ny, nd = cx+dx, cy+dy, cd
            if nx < 0 or nx >= N or ny < 0 or ny >= N:
                nx, ny, nd = cx-dx, cy-dy, (cd+2)%4

            # check players
            if pos_to_player.get((nx, ny), -1) == -1:
                del pos_to_player[(cx, cy)]
                pos_to_player[(nx, ny)] = pid
                if arr[(nx, ny)][-1] > cg:
                    cg, arr[(nx, ny)][-1] = arr[(nx, ny)][-1], cg
                    arr[(nx, ny)].sort() 
                players[pid] = [nx, ny, nd, cp, cg]

            else:
                pid2 = pos_to_player[(nx, ny)]
                ccx, ccy, ccd, ccp, ccg = players[pid2]
                win_flag = True

                if cp+cg > ccp+ccg:
                    win_flag = True
                elif cp+cg < ccp+ccg:
                    win_flag = False
                else:
                    if cp > ccp:
                        win_flag = True
                    else:
                        win_flag = False

                # pid1이 이긴다 => 기존에 pid2도 이동해야 한다
                # pid2가 이긴다 => 그대로 총버리고 앞으로 한칸 이동한다
                if win_flag is False:
                    del pos_to_player[(cx, cy)]
                    scores[pid2] += (ccp+ccg-cp-cg)
                    tx, ty, td, ts, tg = nx, ny, nd, cp, 0
                    arr[(tx, ty)].append(cg)
                    arr[(tx, ty)].sort()

                    flag = False
                    for k in range(4):
                        ntd = (td+k)%4
                        ntx, nty = tx+direc[ntd][0], ty+direc[ntd][1]
                        if ntx < 0 or ntx >= N or nty < 0 or nty >= N or pos_to_player.get((ntx, nty), -1) != -1:
                            continue
                        break

                    pos_to_player[(ntx, nty)] = pid
                    if arr[(ntx, nty)][-1] > tg:
                        tg, arr[(ntx, nty)][-1] = arr[(ntx, nty)][-1], tg
                        arr[(ntx, nty)].sort() 
                    players[pid] = [ntx, nty, ntd, ts, tg]
                    
                    tx, ty, td, ts, tg = nx, ny, ccd, ccp, ccg
                    if arr[(tx, ty)][-1] > tg:
                        tg, arr[(tx, ty)][-1] = arr[(tx, ty)][-1], tg
                        arr[(tx, ty)].sort()
                        players[pid2][4] = tg
                
                # pid1이 nx, ny로, pid2는 따로
                else:  
                    del pos_to_player[(cx, cy)]
                    del pos_to_player[(nx, ny)]
                    scores[pid] += (cp+cg-ccp-ccg)
                    tx, ty, td, ts, tg = nx, ny, ccd, ccp, 0
                    arr[(tx, ty)].append(ccg)
                    arr[(tx, ty)].sort()
                    flag = False

                    for k in range(4):
                        ntd = (td+k)%4
                        ntx, nty = tx+direc[ntd][0], ty+direc[ntd][1]
                        if ntx < 0 or ntx >= N or nty < 0 or nty >= N or pos_to_player.get((ntx, nty), -1) != -1:
                            continue
                        break

                    pos_to_player[(ntx, nty)] = pid2
                    if arr[(ntx, nty)][-1] > tg:
                        tg, arr[(ntx, nty)][-1] = arr[(ntx, nty)][-1], tg
                        arr[(ntx, nty)].sort() 
                    players[pid2] = [ntx, nty, ntd, ts, tg]
                    
                    tx, ty, td, ts, tg = nx, ny, nd, cp, cg
                    pos_to_player[(tx, ty)] = pid
                    if arr[(tx, ty)][-1] > tg:
                        tg, arr[(tx, ty)][-1] = arr[(tx, ty)][-1], tg
                        arr[(tx, ty)].sort() 
                    players[pid] = [tx, ty, td, ts, tg]

    print(*scores)