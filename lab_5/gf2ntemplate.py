# 50.042 FCS Lab 5 Modular Arithmetics
# Year 2019

#####################
# Wang Zijia 1002885
#####################

import copy


class Polynomial2:
    def __init__(self, coeffs):
        self.coeffs = coeffs
        pass

    def add(self, p2):
        p1 = self.coeffs
        p2 = p2.coeffs
        # check length
        # print("************* from add, p2: ", p2)
        if len(p1) == len(p2):
            pass
        elif len(p1) > len(p2):
            for i in range(len(p1)-len(p2)):
                p2.append(0)
        else:
            for i in range(len(p2)-len(p1)):
                p1.append(0)

        p3 = [p1[i] ^ p2[i] for i in range(len(p1))]
        return Polynomial2(p3)

    def sub(self, p2):
        return self.add(p2)

    def mul(self, p2, modp=None):
        p1_coe = ''.join(str(coeff) for coeff in self.coeffs)
        p1_num = int(p1_coe, 2)
        p2_coe = ''.join(str(coeff) for coeff in p2.coeffs)
        p2_num = int(p2_coe[::-1], 2)  # from higher to lower
        if modp:
            modp_coe = ''.join(str(coeff) for coeff in modp.coeffs)
            reduction = True
            modp_num = int(modp_coe, 2)
        else:
            reduction = False
        # print("p1: ", p1, "with coefficient: ", p1_coe)
        # print("p2: ", p2, "with coefficient: ", p2_coe, "p2 number: ", p2_num)
        # print("modp: ", modp, "with coefficient: ", modp_coe)

        result_table = [p2.coeffs]  # from lower to higher
        # print(result_table)
        no_bit = len(p2_coe)
        for i in range(1, len(p1_coe)):
            # print("power :", i, "reduction: ", reduction)
            previous_result = ''.join(str(bit) for bit in result_table[i-1][::-1])  # from higher to lower
            shifted_result = [int(bit) for bit in ('{0:0%ib}' % no_bit).format(int(previous_result, 2) << 1)[::-1]]  # from lower to higher
            # print("previous result (from last result, higher to lower): ", previous_result)
            # print("after shifter, result (lower to higher): ", shifted_result)
            if reduction:
                mod_result = Polynomial2(shifted_result).add(modp)
                shifted_result = mod_result.coeffs[:no_bit]
                # print("after mod, result: ", shifted_result)
            result_table.append(shifted_result)
            # print("*** ", result_table[i][])
            if result_table[i][-1] == 1 and modp:
                reduction = True
            else:
                reduction = False

        # print(result_table)

        result = Polynomial2([0])
        for i in range(len(p1_coe)):
            if p1_coe[i] == '1':
                result = result.add(Polynomial2(result_table[i]))
        # print(result)
        return result

    def div(self, p2):
        p1_coe = self.coeffs
        p2_coe = p2.coeffs
        # print("p1: ", p1_coe)
        # print("p2: ", p2_coe)
        # q := 0
        q = [0]
        # r := a
        r = p1_coe
        # d := deg(b)
        d = len(p2_coe) - 1
        # c = 1
        degree_r = (len(r)-1) - r[::-1].index(1)
        # print("degree of r: ", degree_r, "d: ", d)
        while degree_r >= d:
            # print("degree_r: ", degree_r)
            s_list = []
            # s :=lc(r)/c x^(deg(r)-d)
            for i in range(degree_r - d):
                s_list.append(0)
            s_list.append(1)
            # print(s_list)
            # q := q + s
            q = (Polynomial2(q).add(Polynomial2(s_list))).coeffs
            # r := r-sb
            sb = Polynomial2(s_list).mul(p2)
            r = (Polynomial2(r).sub(sb)).coeffs
            degree_r = (len(r)-1) - r[::-1].index(1)
            # print("*** r: ", r, "degree_r: ", degree_r)
        return Polynomial2(q), Polynomial2(r)

    def __str__(self):
        result = ''.join(self.coeffs[i]*'x^{}+'.format(i) for i in range(len(self.coeffs)-1, -1, -1))[:-1]
        return result

    def getInt(p):
        return p.coeffs[::-1]
        pass


class GF2N:
    affinemat = [[1, 0, 0, 0, 1, 1, 1, 1],
                 [1, 1, 0, 0, 0, 1, 1, 1],
                 [1, 1, 1, 0, 0, 0, 1, 1],
                 [1, 1, 1, 1, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1, 0, 0, 0],
                 [0, 1, 1, 1, 1, 1, 0, 0],
                 [0, 0, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1]]

    def __init__(self, x, n=8, ip=Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])):
        self.x = x
        self.n = n
        self.ip = ip
        if type(self.x) != list:
            self.coeffs = [int(bit) for bit in "{0:01b}".format(x)[::-1]]
        else:
            self.coeffs = self.x

    def add(self, g2):
        return Polynomial2(self.coeffs).add(Polynomial2(g2.coeffs))

    def sub(self, g2):
        return Polynomial2(self.coeffs).add(Polynomial2(g2.coeffs))

    def mul(self, g2):
        return Polynomial2(self.coeffs).mul(Polynomial2(g2.coeffs), self.ip)

    def div(self, g2):
        p, r = Polynomial2(self.coeffs).div(Polynomial2(g2.coeffs))
        return GF2N(p.coeffs), GF2N(r.coeffs)

    def getPolynomial2(self):
        return Polynomial2(self.coeffs)


    def __str__(self):
        result = ''.join(self.coeffs[i]*'x^{}+'.format(i) for i in range(len(self.coeffs)-1, -1, -1))[:-1]
        return result

    def getInt(self):
        result = 0
        for i in range(len(self.coeffs)):
            result += (self.coeffs[i]*(2**i))
        return result

    def mulInv(self):
        pass

    def affineMap(self):
        pass


print('\nTest 1')
print('======')
print('p1=x^5+x^2+x')  # 100110
print('p2=x^3+x^2+1')  # 001101
p1 = Polynomial2([0, 1, 1, 0, 0, 1])
p2 = Polynomial2([1, 0, 1, 1])
p3 = p1.add(p2)
print('p3= p1+p2 = ', p3)  # 101011
# print("p3 int: ", p3.getInt())

print('\nTest 2')
print('======')
print('p4=x^7+x^4+x^3+x^2+x')     # 10011110
print('modp=x^8+x^7+x^5+x^4+1')  # 110110001
# p4 = Polynomial2([0,1,1,1,1,0,0,1])
# modp = Polynomial2([1,1,0,1,1,0,0,0,1])
p4 = Polynomial2([0, 1, 1, 1, 1, 0, 0, 1])
modp = Polynomial2([1, 0, 0, 0, 1, 1, 0, 1, 1])
p5 = p1.mul(p4, modp)
print('p5=p1*p4 mod (modp)=', p5)

print('\nTest 3')
print('======')
print('p6=x^12+x^7+x^2')  # 1000010000100
print('p7=x^8+x^4+x^3+x+1')  # 100011011
p6 = Polynomial2([0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
p7 = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
p8q, p8r = p6.div(p7)
print('q for p6/p7=', p8q)  # 10001 from lower to higher
print('r for p6/p7=', p8r)  # 111101 from lower to higher

# ####
print('\nTest 4')
print('======')
g1 = GF2N(100)
g2 = GF2N(5)
print('g1 = ', g1.getPolynomial2())
print('g2 = ', g2.getPolynomial2())
g3 = g1.add(g2)
print('g1+g2 = ', g3)

print('\nTest 5')
print('======')
ip = Polynomial2([1, 1, 0, 0, 1])
print('irreducible polynomial', ip)
g4 = GF2N(0b1101, 4, ip)
g5 = GF2N(0b110, 4, ip)
print('g4 = ', g4.getPolynomial2())
print('g5 = ', g5.getPolynomial2())
g6 = g4.mul(g5)
# print('g4 x g5 = ', g6.p)
print('g4 x g5 = ', g6)

#
print('\nTest 6')
print('======')
g7 = GF2N(0b1000010000100, 13, None)
g8 = GF2N(0b100011011, 13, None)
print('g7 = ', g7.getPolynomial2())
print('g8 = ', g8.getPolynomial2())
q, r = g7.div(g8)
print('g7/g8 =')
print('q = ', q.getPolynomial2())
print('r = ', r.getPolynomial2())
#
# print('\nTest 7')
# print('======')
# ip = Polynomial2([1,1,0,0,1])
# print('irreducible polynomial',ip)
# g9 = GF2N(0b101,4,ip)
# print('g9 = ',g9.getPolynomial2())
# print('inverse of g9 =',g9.mulInv().getPolynomial2())
#
# print('\nTest 8')
# print('======')
# ip = Polynomial2([1,1,0,1,1,0,0,0,1])
# print('irreducible polynomial',ip)
# g10 = GF2N(0xc2,8,ip)
# print('g10 = 0xc2')
# g11 = g10.mulInv()
# print('inverse of g10 = g11 =', hex(g11.getInt()))
# g12 = g11.affineMap()
# print('affine map of g11 =',hex(g12.getInt()))


p1 = Polynomial2([0,0,1])
p2 = Polynomial2([1,0,1,1])
p3 = p1.mul(p2)
print(p1, p2, p3)