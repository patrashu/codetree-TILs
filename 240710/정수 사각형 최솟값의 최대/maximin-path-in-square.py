import sys

n = int(input())
arr = [list(map(int, input().split())) for _ in range(n)]
dp = [[sys.maxsize]*(n+1) for _ in range(n+1)]

for i in range(1, n+1):
    for j in range(1, n+1):
        dp[i][j] = min(arr[i-1][j-1], max(dp[i-1][j], dp[i][j-1]))

print(dp[-1][-1])