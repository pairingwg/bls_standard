
# Specification for BLS Signatures over BLS12-381 v1 (Apr 29, 2019)

This is an initial specification for BLS signatures. The objective is
to provide a specification which enable consistent implementations
with respect to low-level encoding and algorithmic choices.
Note that it does not cover protection against rogue key attacks. 

## Preliminaries

* [P1], [P2] are generators for the BLS12-381 curve; subgroups are of order r.

* ciphersuite is a fixed-length 8-bit string

* hashtoG1(x in {0,1}*) is construction #2 in WB18, instantiated with SHA (with 512-bit output)

* hashtoG2(x in {0,1}*) is construction #5 in WB18, instantiated with SHA (with 512-bit output)

* SHA(x) = SHA256(x || 0) || SHA256(x || 1), where 0, 1 are bits.

* a || b denotes (naive) string concatenation. In all our applications below,
a has a fixed length, so decoding is unique.

* WB18 [implementation](https://github.com/kwantam/bls12-381_hash)

* when converting between bit/octet strings and integers (i.e., int_to_string and string_to_int),
we use little-endian encoding as defined in the
[EdDSA spec](https://tools.ietf.org/html/rfc8032#section-5.1.2).


## Basic signature in G1

* key generation:

    - sk = x is 32 octets (256 bits)
    - compute x' = SHA(x) mod r
    - pk := x' * [P1]

* sign(sk, msg in {0,1}*, ciphersuite in {0,1}^8)

    - derive x' from sk as in key generation
    - H = hashtoG1(ciphersuite || msg)
    - output x' * H

## Basic signature in G2

As before, replace P1,G1 with P2,G2

## TODOs

* Specify a variant where we sign the concatenation of the public key and the message. Here,
the public key has a fixed length (which is determined by the ciphersuite).

* Generate test vectors for ciphersuite being all-zeroes.

* Specify how to represent curve points as octet strings.

* To add a ciphersuite "look up" table. The ciphersuite string will tell us
    - which curve to use
    - whether signatures sit in G1 or in G2
    - which encoding algorithm to use, e.g. WB18 vs FT12
    - which data hashing algorithm to use, namely SHA256 vs SHA
    - whether and how we clear the co-factor
    - possibly which mechanism is used to prevent rogue-key attacks (message augmentation vs
    proof of posession)

* To decide if we want separate ciphersuite strings for the signature scheme and hash-to-curve.

## Notes

* Assume SHA512 for now. If we decide to switch back to SHA256 later, the change should
be straight-forward.

* There will be no explicit pre-hash mode. If the signature algorithm
gets as input the hash H(M) of a huge message, then we should think of
this as signing H(M), and not signing M, pre-hashed. This has the
advantage of allowing the application to use a different data hash
algorithm.