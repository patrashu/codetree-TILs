def rotate_right(arr):
    return [list(matrix) for matrix in zip(*arr[::-1])]

def add_flour(arr):
    target = [idx for idx, k in enumerate(arr) if k == min(arr)]
    for idx in target:
        arr[idx] += 1
    return arr

def roll_up(arr, N):
    sub_arr, cur_idx = [[arr[1], arr[0]]], 2
    # roll up
    while True:
        r, c = len(sub_arr), len(sub_arr[0])
        if cur_idx+c <= N:
            sub_arr.append(arr[cur_idx:cur_idx+c])
            cur_idx += c
        if cur_idx+r < N:
            sub_arr = rotate_right(sub_arr)
        else:
            break
    
    remain_idx = N-cur_idx
    for i in range(len(sub_arr)):
        if i == (len(sub_arr)-1):
            sub_arr[i].extend(arr[cur_idx:])
        else:
            sub_arr[i].extend([0]*remain_idx)
    return sub_arr

def push(sub_arr):
    r, c = len(sub_arr), len(sub_arr[0])
    new_arr = [[0]*c for _ in range(r)]
    direc = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    # diffuse
    for i in range(r):
        for j in range(c):
            if sub_arr[i][j] == 0:
                continue
            for k in range(4):
                nx, ny = i+direc[k][0], j+direc[k][1]
                if nx < 0 or nx >= r or ny < 0 or ny >= c or sub_arr[nx][ny] == 0:
                    continue
                if sub_arr[i][j] < sub_arr[nx][ny] or sub_arr[i][j]-sub_arr[nx][ny] < 5:
                    continue
                q = (sub_arr[i][j]-sub_arr[nx][ny]) // 5
                new_arr[i][j] -= q
                new_arr[nx][ny] += q

    # update
    for i in range(r):
        for j in range(c):
            sub_arr[i][j] += new_arr[i][j]

    # push
    new_arr = []
    for j in range(c):
        for i in range(r-1, -1, -1):
            if sub_arr[i][j] == 0:
                continue
            new_arr.append(sub_arr[i][j])

    return new_arr

def half_two_times(sub_arr, N):
    length = N//2
    new_arr = [sub_arr[:length][::-1], sub_arr[length:]]
    tmp_arr = [row[:length//2] for row in new_arr]
    tmp_arr = rotate_right(rotate_right(tmp_arr))
    for row in new_arr:
        tmp_arr.append(row[length//2:])
    return tmp_arr

if __name__ == '__main__':
    N, K = map(int, input().split())
    arr = list(map(int, input().split()))
    time, sub = 0, max(arr) - min(arr)

    while sub > K:
        arr = add_flour(arr)
        sub_arr = roll_up(arr, N) # (PxQ matrix)
        sub_arr = push(sub_arr) # (N Scalar)
        sub_arr = half_two_times(sub_arr, N)
        arr = push(sub_arr)
        time += 1
        sub = max(arr)-min(arr)

    print(time)