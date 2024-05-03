from hashlib import md5
bits = 32

def simhash(token_map: dict) -> str:
    # Generates simhash fingerprint given a map of tokens and their weights (in our case, occurrences in a web page)

    bit_map = dict()

    for word in token_map:
        bit_map[word] = bin(0xFFFFFFFF & int(md5(word.encode()).hexdigest(), bits))[2:].zfill(bits) # 32 least significant bits
    
    vector = [0] * bits # Vector with 32 zeroes

    # Looping through every word in the map {word -> binary}
    for k, v in bit_map.items():
        # Looping through every bit in the binary representation of a word
        for i in range(bits):
            if(v[i] == "1"):
                vector[i] += token_map[k]
            else:
                vector[i] -= token_map[k]

    for i in range(bits):
        # Creating final binary string for both vectors
        if vector[i] > 0:
            vector[i] = "1"
        else:
            vector[i] = "0"

    return "".join(vector) # returns 32-bit fingerprint


def get_similarity_score(fpA: str, fpB: str):
    # Given two fingerprints, generate a similarity score
    
    similarity_count = 0
    for i in range(bits):
        if fpA[i] == fpB[i]: # if bit i is the same in both vectors
            similarity_count += 1

    return similarity_count / bits # number of same bits in the same place / 32 bits


if __name__ == "__main__":
    t1 = {"this": 1, "is": 1, "the": 1, "first": 1, "string": 1}
    t2 = {"this": 1, "is": 1, "the": 1, "firs": 1, "string": 1}

    fingerprintA = simhash(t1)
    fingerprintB = simhash(t2)
    print(fingerprintA, fingerprintB)

    print(get_similarity_score(fingerprintA, fingerprintB))