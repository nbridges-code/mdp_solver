from sys import argv
from copy import deepcopy
from math import inf


class State:
    def __init__(self, string):
        args = string.split(" ")
        self.reward = float(args[0])
        self.terminal = int(args[1])
        self.actions_count = int(args[2])
        self.actions = {}
        self.num = -1


class Action:
    def __init__(self, successorCount, num):
        self.successorCount = int(successorCount)
        self.set = {}
        self.num = num


def getInput():
    nextLine = input()
    while nextLine == "" or nextLine.find("#") != -1:
        # eat newlines and comments
        nextLine = input()
    return nextLine


def main():
    if len(argv) != 4:
        print("Bad args.")
        exit(-1)

    discountFactor = float(argv[2])
    terminationThreshold = float(argv[3])

    numOfStates = int(getInput()[18:])
    startState = int(getInput()[13:])

    stateList = []
    for currentState in range(numOfStates):
        newState = State(getInput())
        newState.num = currentState
        newStateActions = []
        for j in range(newState.actions_count):
            sep = getInput().split(" ")
            successors = int(sep[0])
            toAdd = Action(successors, j)
            for k in range(1, successors * 2, 2):
                toAdd.set[int(sep[k])] = float(sep[k + 1])
            newStateActions.append(toAdd)
        newState.actions = newStateActions
        stateList.append(newState)

    currentThreshold = inf
    uOld = {}
    uNew = {}
    for state in stateList:
        uOld[state.num] = state.reward
        uNew[state.num] = state.reward
    backupsPerformed = 0
    outputList = {}

    while currentThreshold > terminationThreshold:
        updateThreshold = -inf
        for state in stateList:
            currentMax = -inf
            indexOfMax = -1
            for action in state.actions:
                currentSum = 0
                for current in action.set:
                    index = int(current)
                    currentSum += action.set[index] * uNew[index]
                if currentSum > currentMax:
                    indexOfMax = action.num
                    currentMax = currentSum
            if currentMax == -inf:
                outputList[state] = ""
                continue
            uNew[state.num] = state.reward + (discountFactor * currentMax)
            outputList[state] = indexOfMax
            difference = abs(uOld[state.num] - uNew[state.num])
            if difference > updateThreshold:
                updateThreshold = difference
            backupsPerformed += 1
        if updateThreshold != -inf:
            currentThreshold = updateThreshold
        uOld = deepcopy(uNew)

    for i in outputList:
        print(outputList[i])

    print(str(backupsPerformed) + " backups performed.")


if __name__ == "__main__":
    main()