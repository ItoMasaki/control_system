
"""module calculate"""


def convertor(now_angular, privious_angular, operator):

    if now_angular - privious_angular < -350:
        operator = 1
    elif now_angular - privious_angular > 350:
        operator = -1
    else:
        pass

    if now_angular > 360:
        operator = -1
    elif now_angular < -1:
        operator = 1
    else:
        pass
    return operator


def differencer(goal_angular, now_angular, flag):
    if goal_angular - now_angular > 0:
        direction = 1
    else:
        direction = -1

    difference = abs(goal_angular - now_angular)
    print(difference, flush=True)
    if difference >= 10:
        velocity = 1.0
    elif difference < 10 and difference >= 5:
        velocity = 0.3
    else:
        velocity = 0.0
        flag = False
    return velocity*direction, flag


if __name__ == '__main__':
    pass
