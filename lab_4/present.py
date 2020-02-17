#!/usr/bin/env python3

# Present skeleton file for 50.042 FCS

##################
# Wang Zijia 1002885
##################

# constants
FULLROUND = 31

# S-Box Layer
sbox = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
        0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]
sbox_x = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

# PLayer
pmt = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51,
       4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55,
       8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59,
       12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]

# pass two bytestrings to this function
def XOR(a, b):
    r = b''
    print(a,b)
    for x, y in zip(a, b):
        r += (x ^ y).to_bytes(1, 'big')
    return r


def rol(val, r_bits, max_bits): return \
    (val << r_bits % max_bits) & (2**max_bits - 1) | \
    ((val & (2**max_bits - 1)) >> (max_bits - (r_bits % max_bits)))
# Rotate left: 0b1001 --> 0b0011


def ror(val, r_bits, max_bits): return \
    ((val & (2**max_bits - 1)) >> r_bits % max_bits) | \
    (val << (max_bits - (r_bits % max_bits)) & (2**max_bits - 1))
# Rotate right: 0b1001 --> 0b1100


def genRoundKeys(key):
    # len(key) = 80 bits => 20 bits in hex
    # len(roundKey) = 64 leftmost bits of K => 12 bits in hex
    round_keys = {}
    round_keys[0] = 32
    # key = "0x%020x" % key
    key = '{0:080b}'.format(key)
    for i in range(1, 33):
        # ---------- get round key from the key and store into round_key{} --------
        round_key = key[:64]
        round_keys[i] = int(round_key, 2)
        # ---------- update the key -----------
        # 1. Rotate the key by 61 bit positions to the left
        # print("rount number: ", i)
        rotated_key = '{0:080b}'.format(rol(int(key, 2), 61, 80))
        # print("rotated key: ", rotated_key)
        # 2. Sbox
        sub_key_1 = sbox[sbox_x.index("%01x" % (int(rotated_key[:4], 2)))]
        rotated_key = '{0:04b}'.format(sub_key_1) + rotated_key[4:]
        # print("new rotated key: ", rotated_key)
        # 3. substitute k19-k15 with XOR result
        round_counter = '{0:05b}'.format(i)
        sub_key_2 = ''
        for j in range(0, 5):
            if rotated_key[60:65][j] == round_counter[j]:
                sub_key_2 += '0'
            else:
                sub_key_2 += '1'
        key = rotated_key[:60] + sub_key_2 + rotated_key[65:]
        # print("new key: ", key)

    # print("round keys: ", round_keys)
    return round_keys


def addRoundKey(state, Ki):
    Ki = '{0:080b}'.format(Ki)
    state = '{0:080b}'.format(state)
    result = ''
    for i in range(0, len(state)):
        result += '0' if state[i] == Ki[i] else '1'
    return int(result, 2)


def sBoxLayer(state):
    w = []
    for i in range(15, -1, -1):
        w.append(state[76-4*i:80-4*i])
    result_2 = ''
    for sub_w in w:
        result_2 += '{0:04b}'.format(sbox[sbox_x.index("%01x" % (int(sub_w, 2)))])
    return result_2


def sBoxLayer_inv(state):
    w = []
    state = '0000000000000000' + state
    for i in range(15, -1, -1):
        w.append(state[76-4*i:80-4*i])
    result_2 = ''
    for sub_w in w:
        result_2 += '{0:04b}'.format(sbox.index(int(sub_w, 2)))
    return result_2


def pLayer(state):
    state = state[::-1]
    result_3 = ''
    for i in range(0, 64):
        # print("for i = ", i,",", "index: ", pmt.index(i), "change to: ", state[pmt.index(i)])
        result_3 += state[pmt.index(i)]
    return int(result_3[::-1], 2)


def pLayer_inv(state):
    state = state[::-1]
    result_3 = ''
    for i in range(0, 64):
        result_3 += state[pmt[i]]
    return result_3[::-1]


def present_round(state, roundKey):
    state = '{0:080b}'.format(state)
    roundKey = '{0:080b}'.format(roundKey)
    # print("state: ", state)
    # print("roundKey: ", roundKey)
    result_1 = ''
    for i in range(0, len(state)):
        result_1 += '0' if state[i] == roundKey[i] else '1'
    # print("result 1: ", result_1)
    result_2 = sBoxLayer(result_1)
    # print("result 2: ", result_2)
    result_3 = pLayer(result_2)
    # print("result 3: ", result_3)
    return result_3


def present_inv_round(state, roundKey):
    state = '{0:080b}'.format(state)
    roundKey = '{0:080b}'.format(roundKey)
    result_3 = pLayer_inv(state)
    result_2 = "0000000000000000" + sBoxLayer_inv(result_3)
    result_1 = ''
    for i in range(0, len(state)):
        result_1 += '0' if result_2[i] == roundKey[i] else '1'
    return int(result_1, 2)


def present(plain, key):
    K = genRoundKeys(key)
    state = plain
    for i in range(1, FULLROUND + 1):
        state = present_round(state, K[i])
    state = addRoundKey(state, K[32])
    return state


def present_inv(cipher, key):
    K = genRoundKeys(key)
    state = cipher
    state = addRoundKey(state, K[32])
    for i in range(FULLROUND, 0, -1):
        state = present_inv_round(state, K[i])
    return state


if __name__ == "__main__":
    # Testvector for key schedule
    key1 = 0x00000000000000000000
    keys = genRoundKeys(key1)
    keysTest = {0: 32, 1: 0, 2: 13835058055282163712, 3: 5764633911313301505, 4: 6917540022807691265,
                5: 12682149744835821666, 6: 10376317730742599722, 7: 442003720503347, 8: 11529390968771969115,
                9: 14988212656689645132, 10: 3459180129660437124, 11: 16147979721148203861, 12: 17296668118696855021,
                13: 9227134571072480414, 14: 4618353464114686070, 15: 8183717834812044671, 16: 1198465691292819143,
                17: 2366045755749583272, 18: 13941741584329639728, 19: 14494474964360714113, 20: 7646225019617799193,
                21: 13645358504996018922, 22: 554074333738726254, 23: 4786096007684651070, 24: 4741631033305121237,
                25: 17717416268623621775, 26: 3100551030501750445, 27: 9708113044954383277, 28: 10149619148849421687,
                29: 2165863751534438555, 30: 15021127369453955789, 31: 10061738721142127305, 32: 7902464346767349504}
    for k in keysTest.keys():
        assert keysTest[k] == keys[k]
    
    # Testvectors for single rounds without keyscheduling
    plain1 = 0x0000000000000000
    key1 = 0x00000000000000000000
    round1 = present_round(plain1, key1)
    round11 = 0xffffffff00000000
    assert round1 == round11

    round2 = present_round(round1, key1)
    round22 = 0xff00ffff000000
    assert round2 == round22

    round3 = present_round(round2, key1)
    round33 = 0xcc3fcc3f33c00000
    assert round3 == round33

    # invert single rounds
    plain11 = present_inv_round(round1, key1)
    assert plain1 == plain11
    plain22 = present_inv_round(round2, key1)
    assert round1 == plain22
    plain33 = present_inv_round(round3, key1)
    assert round2 == plain33

    # Everything together
    plain1 = 0x0000000000000000
    key1 = 0x00000000000000000000
    cipher1 = present(plain1, key1)
    plain11 = present_inv(cipher1, key1)
    assert plain1 == plain11

    plain2 = 0x0000000000000000
    key2 = 0xFFFFFFFFFFFFFFFFFFFF
    cipher2 = present(plain2, key2)
    plain22 = present_inv(cipher2, key2)
    assert plain2 == plain22

    plain3 = 0xFFFFFFFFFFFFFFFF
    key3 = 0x00000000000000000000
    cipher3 = present(plain3, key3)
    plain33 = present_inv(cipher3, key3)
    assert plain3 == plain33

    plain4 = 0xFFFFFFFFFFFFFFFF
    key4 = 0xFFFFFFFFFFFFFFFFFFFF
    cipher4 = present(plain4, key4)
    plain44 = present_inv(cipher4, key4)
    assert plain4 == plain44
    print("All test cases passed !!!")
