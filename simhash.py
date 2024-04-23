from hashlib import md5

def simhash(bit_map: dict, tokens: dict):
    vector = [0] * 16

    for k, v in bit_map.items():
        for i in range(16):
            if(v[i] == "1"):
                vector[i] += tokens[k]
            else:
                vector[i] -= tokens[k]

    return vector


def get_similarity_score(tokensA: dict, tokensB: dict):
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
        if vectorA[i] > 0:
            vectorA[i] = 1
        else:
            vectorA[i] = 0
            
        if vectorB[i] > 0:
            vectorB[i] = 1
        else:
            vectorB[i] = 0

    for i in range(16):
        if vectorA[i] == vectorB[i]:
            similarity_count += 1

    return similarity_count / 16



if __name__ == "__main__":
    print(get_similarity_score({"tropical": 3, "hello": 1, "crash": 2}, {"tropical": 3, "hello": 1, "crash": 2}))
        
