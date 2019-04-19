
# This file was *autogenerated* from the file map2curve_ft.sage
from sage.all_cmdline import *   # import sage library

_sage_const_3 = Integer(3); _sage_const_2 = Integer(2); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_4 = Integer(4); _sage_const_48 = Integer(48); _sage_const_0x396c8c005555e1568c00aaab0000aaab = Integer(0x396c8c005555e1568c00aaab0000aaab); _sage_const_0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab = Integer(0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab); _sage_const_0xd201000000010000 = Integer(0xd201000000010000); _sage_const_0x5d543a95414e7f1091d50792876a202cd91de4547085abaa68a205b2e5a7ddfa628f1cb4d9e82ef21537e293a6691ae1616ec6e786f0c70cf1c38e31c7238e5 = Integer(0x5d543a95414e7f1091d50792876a202cd91de4547085abaa68a205b2e5a7ddfa628f1cb4d9e82ef21537e293a6691ae1616ec6e786f0c70cf1c38e31c7238e5)# H2C-xxx-SHA512-FT- outputs curve points that do not necessarily lie in the subgroup.
# H2C-xxx-SHA512-FT-Clear would include cofactor clearing.
# https://www.ietf.org/id/draft-irtf-cfrg-hash-to-curve-03.txt

from hash_to_base import *
from utils import *

# BLS12-381 G1 curve
t = -_sage_const_0xd201000000010000 
pp = lambda x: ((x-_sage_const_1 )**_sage_const_2 ) * ((x**_sage_const_4  - x**_sage_const_2  + _sage_const_1 )/_sage_const_3 ) + x
p = _sage_const_0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab 
assert is_prime(p)
assert p%_sage_const_3  == _sage_const_1 
assert p == pp(t)

F = GF(p)
A = F(_sage_const_0 )
B = F(_sage_const_4 )
E = EllipticCurve([A,B])  # y^2 = x^3 + 4
S = sqrt(F(-_sage_const_3 ))
assert is_square(_sage_const_1 +B) == false
h = _sage_const_0x396c8c005555e1568c00aaab0000aaab   # co-factor for G1

# BLS12-381 G2 curve
K2 = F ['U']; (U,) = K2._first_ngens(1)
F2 = F.extension(U**_sage_const_2 +_sage_const_1 , names=('root',)); (root,) = F2._first_ngens(1)
A2 = F2(_sage_const_0 )
B2 = F2(_sage_const_4 *root+_sage_const_1 )
E2 = EllipticCurve([A2,B2])
## define S2?
h2 = _sage_const_0x5d543a95414e7f1091d50792876a202cd91de4547085abaa68a205b2e5a7ddfa628f1cb4d9e82ef21537e293a6691ae1616ec6e786f0c70cf1c38e31c7238e5   # co-factor for G2

h2c_suite = "H2C-BLS12_381_1-SHA512-FT-"

def f(x):
    return F(x**_sage_const_3  + A*x + B)

def map2curve_ft(alpha):
    u = h2b_from_label(h2c_suite, alpha)
    u = F(u)

    w = (S*u)/(_sage_const_1 +B+u**_sage_const_2 )
    x1 = (-_sage_const_1 +S)/_sage_const_2 -u*w
    x2 = -_sage_const_1 -x1
    x3 = _sage_const_1 +_sage_const_1 /w**_sage_const_2 
    e = legendre_symbol(u,p)
    if is_square( f(x1) ) :
        return E( [ x1, e * sqrt(f(x1)) ])
    elif is_square( f(x2) ) :
        return E( [ x2, e * sqrt(f(x2)) ])
    else:
        return E( [ x3, e * sqrt(f(x3)) ])

def map2curve_ft_clear(alpha):
    return h * map2curve_ft(alpha)

SQRT_MINUS3 = sqrt(F(-_sage_const_3 ))              # Field arithmetic
ONE_SQRT3_DIV2 = F((-_sage_const_1 +SQRT_MINUS3)/_sage_const_2 ) # Field arithmetic
ORDER_OVER_2 = ZZ((p - _sage_const_1 )/_sage_const_2 )           # Integer arithmetic

def map2curve_ft_slp(alpha):
    u = h2b_from_label(h2c_suite, alpha)
    tv("u ", u, _sage_const_48 )

    u = F(u)
    t0 = u**_sage_const_2                  # u^2
    t0 = t0+B+_sage_const_1                # u^2+B+1
    t0 = _sage_const_1 /t0                 # 1/(u^2+B+1)
    t0 = t0*u                 # u/(u^2+B+1)
    t0 = t0*SQRT_MINUS3       # sqrt(-3)u/(u^2+B+1)
    assert t0 == F(sqrt(F(-_sage_const_3 ))*u/(u**_sage_const_2 +B+_sage_const_1 ))
    tv("t0", t0, _sage_const_48 )

    x1 = ONE_SQRT3_DIV2-u*t0  # (-1+sqrt(-3))/2-sqrt(-3)u^2/(u^2+B+1)
    assert x1 == F((-_sage_const_1 +sqrt(F(-_sage_const_3 )))/_sage_const_2 -sqrt(F(-_sage_const_3 ))*u**_sage_const_2 /(u**_sage_const_2 +B+_sage_const_1 ))
    tv("x1", x1, _sage_const_48 )

    x2 = -_sage_const_1 -x1
    assert x2 == F(-_sage_const_1 -((-_sage_const_1 +sqrt(F(-_sage_const_3 )))/_sage_const_2 -sqrt(F(-_sage_const_3 ))*u**_sage_const_2 /(u**_sage_const_2 +B+_sage_const_1 )))
    tv("x2", x2, _sage_const_48 )

    t1 = t0**_sage_const_2 
    t1 = _sage_const_1 /t1
    x3 = t1+_sage_const_1 
    assert x3 == F(_sage_const_1 +_sage_const_1 /t0**_sage_const_2 )
    tv("x3", x3, _sage_const_48 )

    e = u**ORDER_OVER_2
    assert e == legendre_symbol(u,p)
    tv("e", e, _sage_const_48 )

    fx1 = x1**_sage_const_3 +B
    assert fx1 == F(x1**_sage_const_3 +B)
    tv("fx1", fx1, _sage_const_48 )

    s1 = fx1**ORDER_OVER_2
    if s1 == _sage_const_1 :
        y1 = e*sqrt(fx1)
        tv("y1", y1, _sage_const_48 )
        return E(x1, y1)

    fx2 = x2**_sage_const_3 +B
    assert fx2 == F(x2**_sage_const_3 +B)
    tv("fx2", fx2, _sage_const_48 )

    s2 = fx2**ORDER_OVER_2
    if s2 == _sage_const_1 :
        y2 = e*sqrt(fx2)
        tv("y2", y2, _sage_const_48 )
        return E(x2, y2)

    fx3 = x3**_sage_const_3 +B
    assert fx3 == F(x3**_sage_const_3 +B)
    tv("fx3", fx3, _sage_const_48 )

    y3 = e*sqrt(fx3)
    tv("y3", y3, _sage_const_48 )
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
        tv("x", pB[_sage_const_0 ], _sage_const_48 )
        tv("y", pB[_sage_const_1 ], _sage_const_48 )
        print "~~~"

