from hashlib import md5

def simhash(bit_map: dict, tokens: dict):
    vector = [0] * 16 # Vector with 16 zeroes

    # Looping through every word in the map {word -> binary}
    for k, v in bit_map.items():
        # Looping through every bit in the binary representation of a word
        for i in range(16):
            if(v[i] == "1"):
                vector[i] += tokens[k]
            else:
                vector[i] -= tokens[k]

    return vector


def get_similarity_score(tokensA: dict, tokensB: dict):
    '''tokensA and tokensB represent the words with corresponding weights
    returns similarity score (0-1) by simhashing both dictionaries'''

    # Dictionaries which map {word -> binary representation of hashed word}
    bit_mapA = dict()
    bit_mapB = dict()

    for word in tokensA:
        bit_mapA[word] = bin(0xFFFF & int(md5(word.encode()).hexdigest(), 16))[2:].zfill(16) # 16 least significant bits

    for word in tokensB:
        bit_mapB[word] = bin(0xFFFF & int(md5(word.encode()).hexdigest(), 16))[2:].zfill(16) # 16 least significant bits
    
    vectorA = simhash(bit_mapA, tokensA)
    vectorB = simhash(bit_mapB, tokensB)

    similarity_count = 0

    for i in range(16):
        # Creating final binary string for both vectors
        if vectorA[i] > 0:
            vectorA[i] = 1
        else:
            vectorA[i] = 0
            
        if vectorB[i] > 0:
            vectorB[i] = 1
        else:
            vectorB[i] = 0

    for i in range(16):
        if vectorA[i] == vectorB[i]: # if bit i is the same in both vectors
            similarity_count += 1

    return similarity_count / 16 # number of same bits in the same place / 16 bits