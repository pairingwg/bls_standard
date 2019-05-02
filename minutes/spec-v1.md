
# Specification for BLS Signatures over BLS12-381 v1

**Initial draft: Apr 29, 2019. Current verison: May 1, 2019.**

This is an initial specification for BLS signatures. The objective is
to provide a specification which enable consistent implementations
with respect to low-level encoding and algorithmic choices.
Note that it does not cover aggregation or protection against rogue key attacks. 

## Preliminaries

* [P1], [P2] are generators for the BLS12-381 curve; subgroups are of order r. We use generators specified in the pairing-friendly curves standard: https://tools.ietf.org/html/draft-yonezawa-pairing-friendly-curves-01#section-4.2

* ciphersuite is a fixed-length 8-bit string.

* a || b denotes (naive) string concatenation. In all our applications below,
a or b has a fixed length, so decoding is unique.

* we use OS2IP from [RFC8017](https://tools.ietf.org/html/rfc8017)

### Hash to curve

We follow WB19 [paper](https://eprint.iacr.org/2019/403), [implementation](https://github.com/kwantam/bls12-381_hash). We will rely on the following subroutines:

* hash_to_field is a generic construction that uses a cryptographic hash function to output field elements:

~~~
hash_to_field(msg, ctr, p, m, hash_fn, hash_reps)

Parameters:
  - msg is the message to hash
  - ctr is an integer < 2^8 used to orthogonalize hash functions
  - p and m specify the field as GF(p^m)
  - hash_fn is a hash function, e.g., SHA256
  - hash_reps is the number of concatenated hash outputs
    used to produce an element of F_p

hash_to_field(msg, ctr, p, m, hash_fn, hash_reps) :=
    msg' = hash_fn(msg) || I2OSP(ctr, 1)
    for i in (1, ..., m):
        t = ""  // initialize to the empty string
        for j in (1, ..., hash_reps):
            t = t || hash_fn( msg' || I2OSP(i, 1) || I2OSP(j, 1) )
        e_i = OS2IP(t) mod p
    return (e_1, ..., e_m)
~~~

In the above, an element of the extension field GF(p^m) is represented by a vector V of elements of GF(p).
GF(p^m) defines a primitive element α, and the vector V represents the element determined by the inner
product of V with the vector (α^0, ..., α^{m-1}). For BLS12-381 G2, α = sqrt(-1).

* Using the above, define Hp and Hp2 as:

      Hp(msg, ctr)  := hash_to_field(msg, ctr, p, 1, SHA256, 2)

      Hp2(msg, ctr) := hash_to_field(msg, ctr, p, 2, SHA256, 2)

* Map1 and Map2 are the maps given in Section 4 of [WB19](https://eprint.iacr.org/2019/403).

* hashtoG1(msg in {0,1}\*) is construction #2 in WB19, instantiated with `Hp (msg, 0)` and `Hp (msg, 1)`. In particular,

        hashtoG1(msg) := (Map1(Hp(msg, 0)) * Map1(Hp(msg, 1)))^{1-z}

* hashtoG2(msg in {0,1}\*) is construction #5 in WB19, instantiated with `Hp2 (msg, 0)` and `Hp2 (msg, 1)`.


## Basic signature in G1

* key generation:

    - sk = x is 32 octets (256 bits)
    - compute x' = `hash_to_field(x, 0, r, 1, SHA256, 2)`
    - pk := x' * [P2]

* sign(sk, msg in {0,1}\*, ciphersuite in {0,1}^8)

    - derive x' from sk as in key generation
    - H = `hashtoG1(ciphersuite || msg)`
    - output x' * H

## Basic signature in G2

As before, replace P2, hashtoG1 with P1, hashtoG2

## TODOs

* Specify how to represent curve points as octet strings.

* Specify a variant where we sign the concatenation of the public key and the message. Here,
the public key has a fixed length (which is determined by the ciphersuite), and we need to
fix a representation of the public key as an octet string.

* Generate test vectors for ciphersuite being all-zeroes.

* To add a ciphersuite "look up" table. The ciphersuite string will tell us
    - which curve to use
    - whether signatures sit in G1 or in G2
    - which encoding algorithm to use, e.g. WB19 vs FT12
    - which data hashing algorithm to use, namely SHA256 vs SHA
    - whether and how we clear the co-factor
    - possibly which mechanism is used to prevent rogue-key attacks (message augmentation vs
    proof of posession)

  As a place-holder, we will use 0x01 for signatures in G1, 0x02 for signatures in G2.

* To decide if we want separate ciphersuite strings for the signature scheme and hash-to-curve.
Given that hash-to-curve is only used as an intermediate building, our motivating principle
here is that only the final application (e.g. signatures or VRFs) should provide the ciphersuite string.

## Design Rationale

* We hash the randomness during key generation to mitigate any attacks arising from
weak sources of randomness. This was also done in [EdDSA spec](https://tools.ietf.org/html/rfc8032).

* The specification uses SHA256 as used in many existing implementations.
If we decide to support SHA512 later, the change should be straight-forward.

* For hashing to curves, we use indifferentiable hashing in order to be "future-proof",
even though a weaker security notion (with a slightly more efficient instantiation) suffices for security for BLS signatures.

* There will be no explicit pre-hash mode. If the signature algorithm
gets as input the hash H(M) of a huge message, then we should think of
this as signing H(M), and not signing M, pre-hashed. This has the
advantage of allowing the application to use a different data hash
algorithm.
