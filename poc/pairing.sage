p = 7549; A = 0; B = 1; n = 157; k = 6; t = 14
F = GF(p); E = EllipticCurve(F, [A, B])
R.<x> = F[]; K.<a> = GF(p^k, modulus=x^k+2)
EK = E.base_extend(K)
P = EK(3050, 5371); Q = EK(6908*a^4, 3231*a^3)
P.ate_pairing(Q, n, k, t)

s = Integer(randrange(1, n))
(s*P).ate_pairing(Q, n, k, t) == P.ate_pairing(s*Q, n, k, t)
P.ate_pairing(s*Q, n, k, t) == P.ate_pairing(Q, n, k, t)^s
