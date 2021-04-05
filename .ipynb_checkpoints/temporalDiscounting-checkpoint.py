import time
import os
import random
import itertools
import csv

DELAYS = [0.25, 0.5, 1, 3, 6, 12, 36, 60, 120, 300]
REWARDS = [1, 25, 54, 70, 93, 100, 200, 314, 364, 400, 500, 600, 631,
           700, 748, 800, 850, 900, 950, 1000]
TEST_REWARDS = [1, 500, 900]

MESSAGE = """The purpose of this study is to examine your preferences for different hypothetical dollar ammounts.
You will be asked to make a series of decisions between monetary alternatives. In making your decision, it is
important read carefully the two options. Specifically, notice when the money is given. You will indicate your
preferred dollar-amount by pressing the p and q buttons on your keyboard.
Press p if you prefer the right dollar-amount and q if you prefer the left dollar amount.
There are no right or wrong answers.
After you have made a decision, the next trial will be presented. You will be given 4 practice trials before
you start the real experiment."""

DELAYS_TO_STRING = {
    0.25: '1 Week',
    0.5: '2 Weeks',
    1: '1 Month',
    3: '3 Months',
    6: '6 Months',
    12: '1 Year',
    36: '3 Years',
    60: '5 Years',
    120: '10 Years',
    300: '25 Years'
}

STRING_TO_DELAY = {y:x for x,y in DELAYS_TO_STRING.items()}

DF = []

def choiceMethod(q, p):
    os.system('cls')
    question = f"{q}                    {p}\n"
    x = input(question)
    while x != 'p' and x != 'q':
        os.system('cls')
        print("Please press q if you prefer the left amount and press p if you prefer the right amount")
        x = input(question)
    if x == 'p':
        print(f"You prefered {p}")
    elif x == 'q':
        print(f"You prefered {q}")
    time.sleep(1)
    return x

def addToResults(val, q, p, mode='main'):
    dic = {}
    dic['Today'] = int((q.split()[0])[:-1])
    dic['Delay'] = STRING_TO_DELAY[' '.join(p.split()[2:4])]
    dic['Choice'] = val
    dic['Mode'] = mode
    DF.append(dic)

def practice():
    for _ in range(4):
        q = f"{random.choice(REWARDS)}$ Today (q)"
        p = f"1000$ in {DELAYS_TO_STRING[random.choice(DELAYS)]} (p)"
        val = choiceMethod(q, p)
        addToResults(val, q, p, mode='practice')
    os.system('cls')
    print("Practice is complete. Moving on to experiment.")
    time.sleep(3)
    return
    
def mainLoop(delay, isAscending):
    rewards = REWARDS
    if not isAscending:
        rewards.reverse()
    keptVal = None
    for reward in rewards:
        q = f"{reward}$ Today (q)"
        p = f"1000$ in {DELAYS_TO_STRING[delay]} (p)"
        val = choiceMethod(q, p)
        addToResults(val, q, p)
        if keptVal == None:
            keptVal = val
        elif val != keptVal:
            break
    return


def mainExperiment():
    ascendingDone = set()
    descendingDone = set()
    isAscending = True
    chosen = None
    fullDelays = []
    fullDelays.extend(DELAYS)
    fullDelays.extend(DELAYS)
    random.shuffle(fullDelays)
    for delay in fullDelays:
        if delay not in ascendingDone and delay not in descendingDone:
            chosen, isAscending = random.choice([(ascendingDone, True), (descendingDone, False)])
            chosen.add(delay)
        elif delay not in ascendingDone:
            isAscending = True
            ascendingDone.add(delay)
        elif delay not in descendingDone:
            isAscending = False
            descendingDone.add(delay)
        mainLoop(delay, isAscending)
        os.system('cls')
    print("The experiment is over. The window will now close")
    time.sleep(2)


def main():
    print(MESSAGE)
    while input("Press c and then Enter to continue: ") != 'c':
        print("You pressed the wrong button.")
    print("We will now begin the practice trials:")
    time.sleep(3)
    practice()
    mainExperiment()
    columns = ['Today', 'Delay', 'Choice', 'Mode']
    csv_file = 'experiment.csv'
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        for data in DF:
            writer.writerow(data)
main()