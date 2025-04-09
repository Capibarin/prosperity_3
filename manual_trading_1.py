import itertools

matrix = [[1, 1.45, 0.52, 0.72], [0.7, 1, 0.31, 0.48], [1.95, 3.1, 1, 1.49], [1.34, 1.98, 0.64, 1]]

best_ss = 0
best_lst = []

for i in range(1, 5):
    lists = itertools.combinations([0, 1, 2, 3], i)

    for lst in lists:
        lst = [3] + list(lst) + [3]

        ss = 1

        for j in range(len(lst)-1):
            ss *= matrix[lst[j]][lst[j+1]]

        if ss > best_ss:
            best_ss = ss
            best_lst = lst

print(best_ss)
print(best_lst)