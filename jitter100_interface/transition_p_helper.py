t_p=[[777,54,3,24,28],
[18,231,61,14,0],
[4,13,88,63,4],
[8,11,9,832,99],
[35,15,13,38,336]
]
counter = 0
for i in range(len(t_p)):
    counter = counter + 1
    for j in range(len(t_p[i])):
        if counter ==1:
            t_p[i][j]=t_p[i][j]/886
        elif counter ==2:
            t_p[i][j]=t_p[i][j]/324
        elif counter ==3:
            t_p[i][j]=t_p[i][j]/172
        elif counter ==4:
            t_p[i][j]=t_p[i][j]/959
        elif counter ==5:
            t_p[i][j]=t_p[i][j]/437

print(t_p)