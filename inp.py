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
def howManyMachine(wayMap) :
    maxMachin = wayMap[0][0][0]
    for detail in wayMap :
        for step in detail :
            maxMachin = step[0] if maxMachin < step[0] else maxMachin
    return maxMachin + 1

def queInit(wayMap) :
    count = howManyMachine(wayMap)
    machineQue = [[] for _ in range(count)]
    
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
    # время простоя каждого станка;
    prostoi = [0 for _ in range(len(inProcess))]
    # время «пролеживания» деталей в ожидании обработки на каждом станке.
        # время обработки каждой детали, если пролеживаний не будет
    def funk(detail) :
        s = 0
        for step in detail : s += step[1]
        return s

    minFullCost = [funk(detail) for detail in wayMap]
    prolejivanie = [0 for _ in range(len(wayMap))]

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
        inProcess[machine] = detail
        times[machine] = cost
        # отметить время начинания обработки
        _writeInLog(machine, detail)
        # удалить из очереди
        machineQue[machine].remove(machineQue[machine][detailIndx])

    # первый шаг
    for machine in range(len(machineQue)) :
        if len(machineQue[machine]) > 0 :
            _letsWork(machine)

    # поиск номера станка, на котором обработка закончится ранее всех
    def findStep(times) :
        tmp = zip(range(len(times)), times)
        tmp = tuple(filter(lambda m : m[1] > 0, tmp))

        if len(tmp) == 0 : return -1

        waa = min(tmp, key=lambda n: n[1])[0]

        minMahine = tmp[0]  #(machine, time)
        for m in tmp[1:] : 
            if minMahine[1] > m[1] : minMahine = m
        
        assert minMahine[0] == waa, "неверный min"

        return minMahine[0]

    while True :
        machine = findStep(times)
        if machine == -1 : 
            return log, T, prolejivanie, prostoi
        
        detail = inProcess[machine]
        cost = times[machine]
        T += cost

        for i in range(len(times)) : times[i] -= cost

        for i in range(len(times)) :
            # assert times[i] >= 0 , "times[i] должно быть >= нуля"
            if times[i] == 0 :
                assert inProcess[i] != -1 , "times[i] == 0 при inProc[i] != -1"
                
                # удалить деталь из обработки inProc
                detail = inProcess[i]
                inProcess[i] = -1
                # отметить время завершения обработки
                _writeInLog(i, detail, False)
                # если это был последний этап обработки детали, то посчитать время пролеживания
                if len(wayMap[detail]) == 0 :
                    prolejivanie[detail] = T - minFullCost[detail]

                # положить эту деталь в очередь на следующий станок
                if len(wayMap[detail]) > 0 :
                    # найти следующий этап обработки для детали (которая только что закончила обработку)
                    newMachine, newCost = wayMap[detail].pop(0)
                    machineQue[newMachine].append((detail, newCost))

                #     # Если деталь была положена в очередь, проверить : в работе ли сейчас машина, в чью очередь полжили деталь
                #     if inProcess[newMachine] == -1 :
                #         # если машина свободна, то начать обработку на ней
                #         assert times[newMachine] <= 0 , "время на отдельном станке считается неверно"
                #         prostoi[newMachine] += abs(times[newMachine])
                #         _letsWork(newMachine)
                
                # # проверить очередь, если не пуста добавить в обработку деталь из очереди
                # if len(machineQue[i]) != 0 :
                #     #  отметить время начала обработки детали
                #     prostoi[i] += abs(times[i])
                #     _letsWork(i)
        
        for i in range(len(machineQue)) :
            if inProcess[i] == -1 :
                # проверить очередь, если не пуста добавить в обработку деталь из очереди
                if len(machineQue[i]) != 0 :
                    #  отметить время начала обработки детали
                    prostoi[i] += abs(times[i])
                    _letsWork(i)



wayMap = Inp("input.txt")
log, T, prolejivanie, prostoi = mainProc(wayMap)

for i, machine in enumerate(log):
    print(f'machine {i}')
    for time, event in machine.items():
        print(f'\t{time} | {event}')

print(f'простой: {prostoi}')