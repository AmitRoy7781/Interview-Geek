def getHash(input):
    hash_value = 0
    p = 1
    base = 67
    mod = 961748927
    for x in input:
        hash_value += (ord(x) * p)
        hash_value %= mod
        p = p * base
        p %= mod

    return hash_value

print(getHash("123456"))