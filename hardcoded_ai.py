

class HardcodedAi:

    def __init__(self):
        pass

    def run(self, input_vector=None):
        if input_vector is None:
            return [0, 0]

        ret_val = [0, 0]
        if input_vector[0] < input_vector[4]:
            ret_val[0] = 1
        else:
            ret_val[1] = 1

        return ret_val

# ballx = 0, bally = 1, lastballx = 2, lastbally = 3, mey = 4, enemyy = 5