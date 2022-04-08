import re
import json
import random


def ishave(data):
    data = json.dumps(data, ensure_ascii=False)
    pat = '#\*(.*?)\*#'
    r = re.findall(pat, data)
    if r == []:
        return json.loads(data)
    else:
        for key in r:
            data = data.replace('#*{}*#'.format(key), func_map[key]())
        return json.loads(data)



def radnint():
    a = str(random.randint(0,100))

    return a



func_map = {'radnint':radnint}

