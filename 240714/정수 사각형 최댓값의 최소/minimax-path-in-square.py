n = int(input())
arr = [list(map(int, input().split())) for _ in range(n)]
dp = [[0] * (n+1) for _ in range(n+1)]

for i in range(1, n+1):
    for j in range(1, n+1):
        if i == 1 and j == 1:
            dp[i][j] = arr[i-1][j-1]
        elif j == 1:
            dp[i][j] = max(arr[i-1][j-1], dp[i-1][j])
        elif i == 1:
            dp[i][j] = max(arr[i-1][j-1], dp[i][j-1])
        else:
            dp[i][j] = max(min(dp[i-1][j], dp[i][j-1]), arr[i-1][j-1])

print(dp[-1][-1])