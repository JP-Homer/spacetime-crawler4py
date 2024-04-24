from hashlib import md5

def simhash(token_map: dict) -> str:
    # Generates simhash fingerprint given a map of tokens and their weights (in our case, occurrences in a web page)

    bit_map = dict()

    for word in token_map:
        bit_map[word] = bin(0xFFFF & int(md5(word.encode()).hexdigest(), 16))[2:].zfill(16) # 16 least significant bits
    
    vector = [0] * 16 # Vector with 16 zeroes

    # Looping through every word in the map {word -> binary}
    for k, v in bit_map.items():
        # Looping through every bit in the binary representation of a word
        for i in range(16):
            if(v[i] == "1"):
                vector[i] += token_map[k]
            else:
                vector[i] -= token_map[k]

    for i in range(16):
        # Creating final binary string for both vectors
        if vector[i] > 0:
            vector[i] = "1"
        else:
            vector[i] = "0"

    return "".join(vector) # returns 16-bit fingerprint


def get_similarity_score(fpA: str, fpB: str):
    # Given two fingerprints, generate a similarity score
    
    similarity_count = 0
    for i in range(16):
        if fpA[i] == fpB[i]: # if bit i is the same in both vectors
            similarity_count += 1

    return similarity_count / 16 # number of same bits in the same place / 16 bits


if __name__ == "__main__":
    t1 = {"hello": 2, "goodbye": 1, "yellow": 3, "new": 5}
    t2 = {"hello": 2, "yellow": 3}

    fingerprintA = simhash(t1)
    fingerprintB = simhash(t2)
    print(fingerprintA, fingerprintB)

    print(get_similarity_score(fingerprintA, fingerprintB))