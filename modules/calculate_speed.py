
"""module calculate"""


def space_time_convert(goal_angle):
    if goal_angle >= 180:
        goal_angle -= 360
    elif goal_angle <= -180:
        goal_angle += 360
    else:
        pass
    """return difference,direction"""
    if goal_angle >= 0:
        return abs(goal_angle), 1
    else:
        return abs(goal_angle), -1


def calculate_next(
    difference,
    direction,
    old_velocity,
    old_accelation
):
    """direction is vector,others are schalar"""
    """return velocity,accelation,true or false"""

    if old_velocity >= 1:
        return old_velocity, 0, 1  # no accelation

    if difference >= 10:
        #  [TODO] : make new way of calculate
        new_accelation = old_accelation+0.5
    elif difference < 10 and difference >= 5:
        if old_velocity > 0.3:
            new_accelation = old_accelation-0.1
        else:
            pass
    else:
        if old_velocity > 0:
            new_accelation = old_accelation-0.5
        else:
            old_velocity, 0, -1

    new_velocity = old_velocity+accelation*0.01
    return new_velocity, new_accelation, 1


if __name__ == '__main__':
    pass
