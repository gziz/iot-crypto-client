from random import SystemRandom
from typing import Tuple, Final
import hashlib

def ceil(a: int, b: int) -> int:
    return -(a // -b)

def shaHash(m: str) -> int:
    m_bytes = bytes(m, "utf-8")
    BLOCKSIZE = 65536
    blocks = ceil(len(m_bytes), BLOCKSIZE)

    hasher = hashlib.sha1()

    for i in range(blocks):
        curr_block = m_bytes[i * BLOCKSIZE : i * BLOCKSIZE + BLOCKSIZE]
        hasher.update(curr_block)

    hex = "0x" + hasher.hexdigest()
    return int(hex, 0)
    

class EllipticCurve:
    INF_POINT = None

    def __init__(self, p: int, a: int, b: int) -> None:
        self.p = p
        self.a = a
        self.b = b

    def add(self, P1: Tuple, P2: Tuple) -> Tuple:
        if P1 == self.INF_POINT:
            return P2
        if P2 == self.INF_POINT:
            return P1

        x1, y1 = P1
        x2, y2 = P2

        if self.mod_equal(x1, x2) and self.mod_equal(y1, -y2):
            return self.INF_POINT

        if self.mod_equal(x1, x2) and self.mod_equal(y1, y2):
            u = self.mod_reduce((3 * x1 * x1 + self.a) * self.mod_inverse(2 * y1))
        else:
            u = self.mod_reduce((y1 - y2) * self.mod_inverse(x1 - x2))

        v = self.mod_reduce(y1 - u * x1)
        x3 = self.mod_reduce(u * u - x1 - x2)
        y3 = self.mod_reduce(-u * x3 - v)
        return (x3, y3)

    def multiply(self, k: int, P: Tuple[int]) -> Tuple[int]:
        Q = self.INF_POINT
        while k != 0:
            if k & 1 != 0:
                Q = self.add(Q, P)
            P = self.add(P, P)
            k >>= 1
        return Q

    # helper functions

    def mod_reduce(self, x, n=None):
        n = n or self.p
        return x % n

    def mod_equal(self, x, y, n=None):
        return self.mod_reduce(x - y, n) == 0

    def mod_inverse(self, x, n=None):
        n = n or self.p
        if self.mod_reduce(x) == 0:
            return None
        return pow(x, n - 2, n)


class ECDSA(EllipticCurve):
    P: Final = int(0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF)
    A: Final = int(0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC)
    B: Final = int(0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B)
    G: Final = (int(0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296),
                int(0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5))
    N: Final = int(0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551)

    def __init__(self):
        super().__init__(self.P, self.A, self.B)
        self.n = self.N
        self.G = self.G
        self.rnd = SystemRandom()

    def key_pair_gen(self):
        d = self.rnd.randrange(self.n - 1)
        Q = self.multiply(d, self.G)

        self.d, self.Q = d, Q
        return Q, d

    def sign(self, message: str, d: int = None) -> Tuple[int]:
        while True:
            k = self.rnd.randrange(1, self.n - 1)
            x1, _ = self.multiply(k, self.G)

            r = self.mod_reduce(x1, self.n)
            if r == 0:
                continue

            k_inv = self.mod_inverse(k, self.n)

            e = shaHash(message)
            s = k_inv * (e + d * r) % self.n
            if s == 0:
                continue

            self.r, self.s = r, s
            return r, s

    def verify(
        self, message, r: int = None, s: int = None, Q: Tuple[int] = None
    ) -> bool:
        e = shaHash(message)
        w = self.mod_inverse(s, self.n)

        u1 = self.mod_reduce(e * w, self.n)
        u2 = self.mod_reduce(r * w, self.n)

        X = self.add(self.multiply(u1, self.G), self.multiply(u2, Q))
        if X == self.INF_POINT:
            return False

        x1, _ = X
        v = self.mod_reduce(x1, self.n)

        return "True" if v == r else "False"
