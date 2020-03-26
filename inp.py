def Inp(filename) :
    ways = [] # маршруты всех деталей

    with open(filename, 'r') as file:
        for line in file :
            if line == '' or line == '\n' : break

            detailWay = [] # Маршрут одной детали [(A, 1), (C, 4), (B, 5)]
            for partOfWay in line.split('\t') :
                tmp = partOfWay.upper().split(' ')
                tmp = (ord(tmp[0]) - ord('A'), int(tmp[1]))
                detailWay.append(tmp)

            ways.append(detailWay)

    return ways

# массив очередей к станкам
# сколько станков? TODO неверно, может быть больше
def how1ManyMachine(wayMap) :
    count = max([len(way) for way in wayMap])
    return count

def queInit(wayMap) :
    howManyMachine = lambda wayMap : max([len(way) for way in wayMap])
    machineQue = [[] for _ in range(howManyMachine(wayMap))]
    
    for detaileIndx in range(len(wayMap)) :
        machine, cost = wayMap[detaileIndx].pop(0)
        machineQue[machine].append((detaileIndx, cost))    
    return machineQue

def rule(que) :
    detailIndx = 0
    # выбираем детать с самой большой стоимостью
    for i in range(len(que)) :
        if que[detailIndx][1] < que[i][1] :
            detailIndx = i
    
    return detailIndx

def mainProc(wayMap) :
    machineQue = queInit(wayMap)    # [[(detaileIndx, cost), (detaileIndx, cost)], ]
    inProcess = [-1 for _ in range(len(machineQue))]

    T = 0
    times = [0 for _ in range(len(inProcess))]
    log = [{} for _ in range(len(inProcess))]

    def _writeInLog(machine, detail, push = True) :
        # log = [{time0: [(detail1, True)], time1 = [(detail1, False), (detail2, True)] }, {}, ...]
        if log[machine].get(T) == None :
            log[machine][T] = [(detail, push)]
        else :
            log[machine][T].append((detail, push))

    def _letsWork(machine) :
        # найти в очереди индекс детали, которую стоит обработать
        detailIndx = rule(machineQue[machine])
        # добавить в обработку
        detail, cost = machineQue[machine][detailIndx]
        inProcess[machine] = machineQue[machine][detailIndx]
        times[machine] = cost
        detail = machineQue[machine][detailIndx][0]
        # отметить время начинания обработки TODO
        _writeInLog(machine, detail)
        # удалить из очереди
        machineQue[machine].remove(machineQue[machine][detailIndx])

    # первый шаг
    for machine in range(len(machineQue)) :
        if len(machineQue[machine]) > 0 :
            _letsWork(machine)

    # поиск номера станка, на котором обработка закончится ранее всех
    def findStep(inProcess) :
        tmp = zip(tuple(range(len(inProcess))), inProcess)
        tmp = tuple(filter(lambda n : n[1] != -1, tmp))

        if len(tmp) == 0 : return -1

        i = tmp[0]  #(machine, (detail, cost))
        for n in tmp[1:] : 
            if i[1][1] > n[1][1] : i = n
        return i[0]

    while True :
        machine = findStep(inProcess)
        if machine == -1 : 
            return log
        
        detail, fullCost = inProcess[machine]
        cost = times[machine]
        T += cost

        for i in range(len(times)) : times[i] -= cost

        for i in range(len(times)) :
            if times[i] <= 0 :
                # проверить есть ли в обработке деталь, если есть то
                if inProcess[i] != -1 :
                    # удалить деталь из обработки inProc
                    detail, cost = inProcess[i]
                    inProcess[i] = -1
                    # отметить время завершения обработки
                    _writeInLog(i, detail, False)
                    # положить эту деталь в очередь на следующий станок
                    if len(wayMap[detail]) > 0 :
                        # найти следующий этап обработки для детали (которая только что закончила обработку)
                        newMachine, newCost = wayMap[detail].pop(0)
                        machineQue[newMachine].append((detail, newCost))

                        # Если деталь была положена в очередь, проверить : в работе ли сейчас машина, в чью очередь полжили деталь
                        if inProcess[newMachine] == -1 :
                            # если машина свободна, то начать обработку на ней
                            _letsWork(newMachine)
                    
                
                if inProcess[i] != -1 : 
                    raise Exception("новая машина для обработки совпадает с предыдущей. Скорее всего ошибка во входных данных -- деталь обрабатывается на одном и том же станке дважды")
                
                # проверить очередь, если не пуста добавить в обработку деталь из очереди
                if len(machineQue[i]) != 0 :
                    #  отметить время начала обработки детали
                    _letsWork(i)
        
        print("f")

        

wayMap = Inp("input.txt")
log = mainProc(wayMap)

print("f")

