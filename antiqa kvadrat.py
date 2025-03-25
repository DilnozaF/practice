n=int(input())
size=2*n-1
matrix=[[0]*size for _ in range (size)]
for i in range(size):
    for j in range(size):
        matrix[i][j]=min(i,j,size-i-1, size-j-1)+1
for i in range(size):
    for j in range(size):
        print(matrix[i][j], end=" ")
    print()