import sys


def createProgressBar(current):
    currentProgress = int(current * 40 // 100)
    return "[{}{}]".format("#" * currentProgress, "-" * (40 - currentProgress))
