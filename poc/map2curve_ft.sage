# H2C-xxx-SHA512-FT- outputs curve points that do not necessarily lie in the subgroup.
# H2C-xxx-SHA512-FT-Clear would include cofactor clearing.
# https://www.ietf.org/id/draft-irtf-cfrg-hash-to-curve-03.txt

from hash_to_base import *
from utils import *

# BLS12-381 G1 curve
t = -0xd201000000010000
pp = lambda x: ((x-1)**2) * ((x**4 - x**2 + 1)/3) + x
p = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
assert is_prime(p)
assert p%3 == 1
assert p == pp(t)

F = GF(p)
A = F(0)
B = F(4)
E = EllipticCurve([A,B])  # y^2 = x^3 + 4
S = sqrt(F(-3))
assert is_square(1+B) == false
h = 0x396c8c005555e1568c00aaab0000aaab  # co-factor for G1

# BLS12-381 G2 curve
K2.<U> = F []
F2.<root> = F.extension(U^2+1)
A2 = F2(0)
B2 = F2(4*root+1)
E2 = EllipticCurve([A2,B2])
## define S2?
h2 = 0x5d543a95414e7f1091d50792876a202cd91de4547085abaa68a205b2e5a7ddfa628f1cb4d9e82ef21537e293a6691ae1616ec6e786f0c70cf1c38e31c7238e5  # co-factor for G2

h2c_suite = "H2C-BLS12_381_1-SHA512-FT-"

def f(x):
    return F(x**3 + A*x + B)

def map2curve_ft(alpha):
    u = h2b_from_label(h2c_suite, alpha)
    u = F(u)

    w = (S*u)/(1+B+u**2)
    x1 = (-1+S)/2-u*w
    x2 = -1-x1
    x3 = 1+1/w**2
    e = legendre_symbol(u,p)
    if is_square( f(x1) ) :
        return E( [ x1, e * sqrt(f(x1)) ])
    elif is_square( f(x2) ) :
        return E( [ x2, e * sqrt(f(x2)) ])
    else:
        return E( [ x3, e * sqrt(f(x3)) ])

def map2curve_ft_clear(alpha):
    return h * map2curve_ft(alpha)

SQRT_MINUS3 = sqrt(F(-3))              # Field arithmetic
ONE_SQRT3_DIV2 = F((-1+SQRT_MINUS3)/2) # Field arithmetic
ORDER_OVER_2 = ZZ((p - 1)/2)           # Integer arithmetic

def map2curve_ft_slp(alpha):
    u = h2b_from_label(h2c_suite, alpha)
    tv("u ", u, 48)

    u = F(u)
    t0 = u**2                 # u^2
    t0 = t0+B+1               # u^2+B+1
    t0 = 1/t0                 # 1/(u^2+B+1)
    t0 = t0*u                 # u/(u^2+B+1)
    t0 = t0*SQRT_MINUS3       # sqrt(-3)u/(u^2+B+1)
    assert t0 == F(sqrt(F(-3))*u/(u**2+B+1))
    tv("t0", t0, 48)

    x1 = ONE_SQRT3_DIV2-u*t0  # (-1+sqrt(-3))/2-sqrt(-3)u^2/(u^2+B+1)
    assert x1 == F((-1+sqrt(F(-3)))/2-sqrt(F(-3))*u**2/(u**2+B+1))
    tv("x1", x1, 48)

    x2 = -1-x1
    assert x2 == F(-1-((-1+sqrt(F(-3)))/2-sqrt(F(-3))*u**2/(u**2+B+1)))
    tv("x2", x2, 48)

    t1 = t0**2
    t1 = 1/t1
    x3 = t1+1
    assert x3 == F(1+1/t0**2)
    tv("x3", x3, 48)

    e = u^ORDER_OVER_2
    assert e == legendre_symbol(u,p)
    tv("e", e, 48)

    fx1 = x1^3+B
    assert fx1 == F(x1**3+B)
    tv("fx1", fx1, 48)

    s1 = fx1^ORDER_OVER_2
    if s1 == 1:
        y1 = e*sqrt(fx1)
        tv("y1", y1, 48)
        return E(x1, y1)

    fx2 = x2^3+B
    assert fx2 == F(x2**3+B)
    tv("fx2", fx2, 48)

    s2 = fx2^ORDER_OVER_2
    if s2 == 1:
        y2 = e*sqrt(fx2)
        tv("y2", y2, 48)
        return E(x2, y2)

    fx3 = x3^3+B
    assert fx3 == F(x3**3+B)
    tv("fx3", fx3, 48)

    y3 = e*sqrt(fx3)
    tv("y3", y3, 48)
    return E(x3, y3)


if __name__ == "__main__":
    enable_debug()
    print "## Fouque-Tibouchi to BLS12-381 G1"
    for alpha in map2curve_alphas:
        tv_text("alpha", pprint_hex(alpha))
    for alpha in map2curve_alphas:
        print "\n~~~"
        print("Input:")
        print("")
        tv_text("alpha", pprint_hex(alpha))
        print("")
        print("Intermediate values:")
        print("")
        pA, pB = map2curve_ft(alpha), map2curve_ft_slp(alpha)
        assert pA == pB
        print("")
        print("Output:")
        print("")
        tv("x", pB[0], 48)
        tv("y", pB[1], 48)
        print "~~~"
