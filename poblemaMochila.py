def Mochila(*args):
    data = {
        "peso": list(map(int, args[0].strip().split())),
        "valores": list(map(int, args[1].strip().split())),
        "usado": [False] * len(args[0].strip().split()),
        "max": args[2],
        "valmax":-1
    }
    __rec__(data, 0, -1)
    print(data["valmax"])

def SacarVal(data):
    val = 0
    for i in range(0, len(data["peso"])):
        #if data["usado"][i]:
            val += data["valores"][i]*data["usado"][i]
    return val


def __rec__(data, peso, ultimo):
    if peso > data["max"]:
        data["usado"][ultimo] -= 1
        data["valmax"]=max(SacarVal(data),data["valmax"])
        data["usado"][ultimo] +=1
    else:
        for elem in range(0, len(data["peso"])):
            #if not data["usado"][elem]:
                data["usado"][elem] +=1
                __rec__(data, peso + data["peso"][elem],elem)
                data["usado"][elem] -= 1


print(Mochila("10 5 2 9 10", "7 8 2 4 25", 17))
