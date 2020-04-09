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


def rule(que, ruleIndx, countOfDoneOperations) :
    # По длительности очередной операции (SIO – правило операции наибольшей продолжительности) max
    if ruleIndx == 0 :
        detailIndx = 0
        # выбираем детать с самой большой стоимостью
        for i in range(len(que)) :
            if que[detailIndx][1] < que[i][1] :
                detailIndx = i
        return detailIndx
    else :
        # Количество операций маршрута, которые уже выполнены max
        maxDetailIndx = 0
        maxDetail = que[maxDetailIndx][0]
        # выбираем детать с самой большой стоимостью
        for i in range(len(que)) :
            detail = que[i][0]
            if countOfDoneOperations[maxDetail] < countOfDoneOperations[detail] :
                maxDetailIndx = i
        return maxDetailIndx

def mainProc(wayMap, ruleIndx = 0) :
    machineQue = queInit(wayMap)    # [[(detaileIndx, cost), (detaileIndx, cost)], ]
    inProcess = [-1 for _ in range(len(machineQue))]
    T = 0
    # время простоя каждого станка;
    prostoi = [0 for _ in range(len(inProcess))]
    
    def funk(detail) :
        s = 0
        for step in detail : s += step[1]
        return s

    # время обработки деталей (без пролеживания, только непосредственная обработка)
    minFullCost = [funk(detail) for detail in wayMap]
    # время пролеживания деталей
    prolejivanie = [0 for _ in range(len(wayMap))]

    # время, как долго еще нужно обрабатывать деталь на станке
    times = [0 for _ in range(len(inProcess))]
    # количество операций, которые уже выполнены для детали
    countOfDoneOperations = [0 for i in range(len(wayMap))]
    # лог работы
    log = [{} for _ in range(len(inProcess))]
    # лог очередей на станках 
    queLog = ""
    def _queLogStep() :
        # T = 0 :
        # A : 1, 2, 3;
        s = 'Т = ' + str(T) + ' : \n'
        for i in range(len(machineQue)) :
            s += chr(ord('A') + i) + ' : '
            for detail, cost in machineQue[i] :
                s += str(detail) + ', '
            if inProcess[i] != -1 :
                s += 'обрабатывается = ' + str(inProcess[i])
            s += ';\n'
        s += '\n'
        return s

    def _writeInLog(machine, detail, push = True) :
        # log = [{time0: [(detail1, True)], time1 = [(detail1, False), (detail2, True)] }, {}, ...]
        if log[machine].get(T) == None :
            log[machine][T] = [(detail, push)]
        else :
            log[machine][T].append((detail, push))

    def _letsWork(machine, ruleIndx, countOfDoneOperations) :
        # найти в очереди индекс детали, которую стоит обработать
        detailIndx = rule(machineQue[machine], ruleIndx, countOfDoneOperations)
        # добавить в обработку
        detail, cost = machineQue[machine][detailIndx]
        inProcess[machine] = detail
        times[machine] = cost
        # отметить время начинания обработки
        _writeInLog(machine, detail)
        # удалить из очереди
        machineQue[machine].remove(machineQue[machine][detailIndx])
    
    queLog = _queLogStep();
    
    # первый шаг, первый запуск машин
    for machine in range(len(machineQue)) :
        if len(machineQue[machine]) > 0 :
            _letsWork(machine, ruleIndx, countOfDoneOperations)

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
        queLog += _queLogStep()
        # поиск номера станка, на котором обработка закончится ранее всех
        machine = findStep(times)
        if machine == -1 : 
            return log, T, prolejivanie, prostoi, queLog
        
        detail = inProcess[machine]
        cost = times[machine]
        T += cost

        for i in range(len(times)) : times[i] -= cost

        for i in range(len(times)) :
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
                
                countOfDoneOperations[detail] += 1

        for i in range(len(machineQue)) :
            if inProcess[i] == -1 :
                # проверить очередь, если не пуста добавить в обработку деталь из очереди
                if len(machineQue[i]) != 0 :
                    #  отметить время начала обработки детали
                    prostoi[i] += abs(times[i])
                    _letsWork(i, ruleIndx, countOfDoneOperations)


with open('out.txt', 'w', encoding='utf8') as file :
    ...

# основная работа программы
for ruleIndx in range(2) :
    # чтение входных данных
    wayMap = Inp("input.txt")

    text = "Правило предпочтения : "
    if ruleIndx == 0 :
        text += "По длительности очередной операции (SIO – правило операции наибольшей продолжительности) MAX. \n"
    else :
        text += "\n\nКоличество операций маршрута, которые уже выполнены MAX. \n"

    log, T, prolejivanie, prostoi, queLog = mainProc(wayMap, ruleIndx)

    def strOut(log, degree) :
        txt = ''
        times = [0, ]
        for i, machine in enumerate(log):
            txt += ("Станок " + chr(ord('A') + i) + ' : ')
            last = 0
            on = None
            for time, events in machine.items():
                if times.count(time) <= 0 : times.append(time)
                ch = '_ ' if on == None else on

                for i in range(last, time, degree) :
                    txt += ch

                for detail, isStart in events :
                    on = detail if isStart else None
                    if isStart :
                        on = str(detail) if detail > 9 else str(detail) + ' '
                last = time
                
            txt += '\n'
        # строка временной шкалы
        times.sort()
        sT = '           0'
        sT1 = '           |'
        last = 0
        for t in times :
            x =  ((t - last) // degree) * 2
            y = len(str(last))
            if x > y :
                for i in range(x - y) : sT += ' '
                for i in range(len(sT) - len(sT1)) : sT1 += ' '
                sT1 += '|'
                sT += str(t)
                last = t
        txt += (sT1 + '\n' + sT + '\n')

        return txt

    # запись и вывод результатов
    text += strOut(log, 1)

    text += "Производственный цикл : Т = " + str(T) + '\n'
    text += "Простои станков: " + "".join([chr(ord('A') + i) + ' = ' + str(prostoi[i]) + '  ' for i in range(len(prostoi))]) + '\n'
    text += "Время пролеживания деталей : " + "".join([str(i + 1) + ' = ' + str(prolejivanie[i]) + '  ' for i in range(len(prolejivanie))]) + '\n\n'
    text += "Состояние очередей на станках в \"особенных состояниях\" : " + '\n' + queLog
    with open('out.txt', 'a', encoding='utf8') as file :
        file.write(text, )
