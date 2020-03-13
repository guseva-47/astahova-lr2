def Inp(filename) :
    ways = [] # маршруты всех деталей

    with open(filename, 'r') as file:
        for line in file :
            if line == '' or line == '\n' : break

            detailWay = [] # Маршрут одной детали [(A, 1), (C, 4), (B, 5)]
            for partOfWay in line.split('\t') :
                tmp = partOfWay.split(' ')
                tmp = (str(tmp[0]), int(tmp[1]))
                detailWay.append(tmp)

            ways.append(detailWay)

    return ways

result = Inp('input.txt')
print(result)