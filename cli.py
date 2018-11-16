import os
import json

from main import main
from pprint import pprint

if __name__ == "__main__":
    level, quests = 0, 1
    for i in range(quests):
        input_file = r'data\level{0}\level{0}-in{1}.json'.format(level, i + 1)
        output_file = os.path.splitext(input_file)[0] + ".out"

        with open(input_file, 'r') as fi:
            input = json.load(fi)
            pprint(input)

            result = main(input)
            pprint(result)

            with open(output_file, 'w+') as fo:
                fo.write(result)
