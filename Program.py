import random
import time

# User interface


def Start():
    print("\nWelcome to my program for finding a solution to the set partition problem with optimalisation")
    Questions()
    print("\nThank you for using my program!")


def Questions():
    print("_________________________________")
    withSave = AskWithSave()
    fileInput = AskFileInput()

    if fileInput:
        FileInput(withSave)
    else:
        TerminalInput(withSave)


def AskFileInput():
    print("\nHow do you want to read the entry set? \n1 - terminal input \n2 - for reading form the file")
    readMethod = input()
    if readMethod == '1':
        return False
    if readMethod == '2':
        return True

    print("\nWrong input")
    return AskFileInput()


def TerminalInput(withSave):
    print("\nInput comma-seperated elements of the set. \nIf you input single number, then that many elements will be randomly generated")
    inputElems = input()
    if "," in inputElems:
        elems = [int(elem) for elem in inputElems.split(",")]
    else:
        noOfElems = int(inputElems)
        elems = [random.randint(0, 20) for ii in range(0, noOfElems)]

    print('\nInto how many subsets do you want to partition the set?')
    n = int(input())
    useMyFit = ChooseFitFun()

    print('\nWhich approach do you want to use?')
    print("h - heuristic")
    print("o - optimal by bruteforce")
    print('b - both heuristic and bruteforce')

    while True:
        approach = input()

        if approach == 'h':
            print("\n________RESULTS________\n")
            start = time.time()
            h = Heuristic(elems, n, useMyFit)
            end = time.time()
            PresentResult(h, elems, 1, True, end-start,
                          ("2" if useMyFit else "1"), withSave)
            print("\nDo you want to use the bruteforce approach as well? (y or n)")
            alsoBrute = input()
            if alsoBrute == "y":
                start = time.time()
                bf = BruteForce(elems, n, useMyFit)
                end = time.time()
                PresentResult(bf, elems, 2, False, end-start,
                              ("2" if useMyFit else "1"), withSave)
            break

        if approach == 'o':
            print("\n________RESULTS________\n")
            start = time.time()
            bf = BruteForce(elems, n, useMyFit)
            end = time.time()
            PresentResult(bf, elems, 1, False, end-start,
                          ("2" if useMyFit else "1"), withSave)
            print("\nDo you want to use the heuristic approach as well? (y or n)")
            alsoHeur = input()
            if alsoHeur == "y":
                start = time.time()
                h = Heuristic(elems, n, useMyFit)
                end = time.time()
                PresentResult(h, elems, 2, True, end-start,
                              ("2" if useMyFit else "1"), withSave)
            break

        if approach == 'b':
            print("\n________RESULTS________\n")
            start = time.time()
            h = Heuristic(elems, n, useMyFit)
            end = time.time()
            PresentResult(h, elems, 1, True, end-start,
                          ("2" if useMyFit else "1"), withSave)
            start = time.time()
            bf = BruteForce(elems, n, useMyFit)
            end = time.time()
            PresentResult(bf, elems, 2, False, end-start,
                          ("2" if useMyFit else "1"), withSave)
            break

    print("\nDo you want to compute another problem? (y or n)")
    again = input()
    if again == 'y':
        Questions()


def AskWithSave():
    print("\nWhich output method do you want use?")
    print("1 - display in terminal window")
    print("2 - display in terminal window and save to the file")
    ans = input()
    if ans == "1":
        return False
    if ans == "2":
        return True
    print("Wrong input")
    return AskWithSave()


def PresentResult(result, S, count, useHeur, time, ff, withSave):
    if useHeur:
        print("\nPartition", count, " - heuristic approach")
    else:
        print("\nPartition", count, " - brute force approach")

    print("Set:", *S, sep=" ")
    print("Partition:", *result['bestPartition'], sep=" ")
    print("Sum of weights:", *[
          round(sum(ii), 2) for ii in result['bestPartition']], sep=" ")
    print("Fitness function ("+ff+") value:", int(round(result['bestVal'])))
    print("Calculated in:", "{0:.4g}".format(time), "s")

    if withSave:
        if count == 1:
            f = open("output.txt", "w")
        else:
            f = open("output.txt", "a")

        if useHeur:
            f.write("Partition " + str(count) + " - heuristic approach")
        else:
            f.write("Partition " + str(count) + " - brute force approach")

        f.write("\nSet: " + " ".join(str(item) for item in S))
        f.write("\nPartition: " + " ".join(str(item)
                                           for item in result['bestPartition']))
        f.write("\nSum of weights: " +
                " ".join([str(round(sum(ii), 2)) for ii in result['bestPartition']]))
        f.write("\nFitness function ("+ff+") value: " +
                str(int(round(result['bestVal']))))
        f.write("\nCalculated in: " + "{0:.4g}".format(time) + " s\n\n")


def ChooseFitFun():
    print("\nWhich fitness function do you want to use? (1 or 2)")
    print("The function that rewards a partition where the sum of weights for consecutive subsets")
    print("1 - is the same")
    print('2 - increaces in the linear manner')
    fit = input()
    if fit == '1':
        return False
    if fit == '2':
        return True
    print("\nWrong input")
    return ChooseFitFun()


def FileInput(withSave):
    f = open("input.txt", "r")
    line1 = f.readline()
    count = 0
    while line1 != "":
        count += 1

        line2 = f.readline()
        line3 = f.readline()
        line4 = f.readline()

        subsets = int(line1)
        useHeur = line2[0] == 'h'
        myFit = line3[0] == '2'
        elems = [int(s) for s in line4.split(",")]

        if len(elems) == 1:
            noOfElems = elems[0]
            elems = [random.randint(1, 20) for ii in range(0, noOfElems)]

        if useHeur:
            start = time.time()
            result = Heuristic(elems, subsets, myFit)
            end = time.time()

        else:
            start = time.time()
            result = BruteForce(elems, subsets, myFit)
            end = time.time()

        PresentResult(result, elems, count, useHeur,
                      end-start, line3[0], withSave)
        line1 = f.readline()
    f.close()


# BruteForce


def generateStepN(S, n, part, info, useMyFitness, sumofidx):

    # full partition
    if len(part) == len(S):

        # eliminate empty subsets
        if not (all(any(elem == subsetIndex for elem in part)) for subsetIndex in range(0, n)):
            return

        # diff computation
        sums = [0]*n

        for ii in range(0, len(part)):
            sums[part[ii]] += S[ii]

        val = Fitness2(sums, sumofidx) if useMyFitness else Fitness1(sums)

        if val < info['bestVal']:
            info['bestVal'] = val
            info['bestPartition'] = part

        return

    # recursion
    for ii in range(0, n):
        generateStepN(S, n, part+[ii], info, useMyFitness, sumofidx)


def MapPartition(info, S, n):
    subsets = []
    for ii in range(0, n):
        subsets.append([S[jj] for jj in range(0, len(S))
                        if info['bestPartition'][jj] == ii])
    info['bestPartition'] = subsets


def Fitness1(sums):
    return max(sums)-min(sums)


def Fitness2(sums, sumofidx):
    val = 0
    s = sum(sums)

    for ii in range(0, len(sums)):
        val += abs((ii+1)/sumofidx*s - sums[ii])
    return val


def BruteForce(S, n, useMyFitness=False):
    if n > 1 and n <= len(S):
        info = {'bestVal': float('inf'), 'bestPartition': []}
        sumofidx = 0
        for ii in range(1, n+1):
            sumofidx += ii
        generateStepN(S, n, [], info, useMyFitness, sumofidx)
    MapPartition(info, S, n)
    return info

# Heuristic


def Heuristic(S, n, useMyFit):

    subsets = []
    for ii in range(0, n):
        subsets.append([])

    sortedS = sorted(S)

    ii = len(S)-1

    if useMyFit:
        s = sum(S)
        k = 0
        for jj in range(0, n):
            k += (jj+1)
        coeff = s/k

    while ii >= 0:
        smallestIndex = n-1

        smallestValue = Aux2(subsets[smallestIndex], smallestIndex,
                             coeff) if useMyFit else Aux1(subsets[smallestIndex])
        for jj in range(0, n):
            val = Aux2(subsets[jj], jj, coeff) if useMyFit else Aux1(
                subsets[jj])
            if val < smallestValue:
                smallestValue = val
                smallestIndex = jj

        subsets[smallestIndex].append(sortedS[ii])
        ii -= 1
    if useMyFit:
        return {"bestPartition": subsets, "bestVal": sum(abs(sum(subsets[i])-coeff*(i+1)) for i in range(0, n))}
    else:
        return {"bestPartition": subsets, "bestVal": max([sum(subset) for subset in subsets])-min([sum(subset) for subset in subsets])}


def Aux1(subset):
    return sum(subset)


def Aux2(subset, i, coeff):
    return (sum(subset)-(i+1)*coeff)


Start()
