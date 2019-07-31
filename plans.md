# BLS Standard Draft -- Plans (Jul 31, 2019)

We outline our plans for the next iteration of the draft.

## Major

* Refer to hash-to-curve spec.

* Ciphersuite for BLS signatures will include (i) ciphersuite for
  hash-to-curve which specifies the curve and which groups the 
  public keys and signatures live in, as well as the underlying
  "data hash" (i.e. SHA256, etc), (ii) rogue-key protection
  mechanism (POP vs AUG). E.g. BLS12381G2-SHA256-SSWU-RO-AUG,
  encoded in ASCII as an octet string.

* For proof-of-possession mechanism against rogue
  key attacks, the ciphersuite will provide domain
  separation for the proofs of possession and the actual signing.

* Ciphersuite will be specified via the parameter DST for hash-to-curve.

* For message augmentation, we will use "pk || message" as the input
  to hash-to-curve.

* Signing will take variable-length messages as in hash-to-curve. For
"pre-hashed messages", the signing algorithm takes as input the
hash. As long as the pre-hash algorithm is collision-resistant, a
standard cryptographic argument guarantees that the signature
authenticates the message.

* We will assume access to serialize and unserialize algorithms from
the underlying groups. For public keys, we assume the same
serialization format is used throughout (we expect that this will be
the compressed point format in most applications). Whenever we need to
serialize a public key in the context of messag augmentation and PoP,
we will use the same serialization.

* We will use HKDF for key generation.

* Unlike the [EdDSA](https://tools.ietf.org/html/rfc8032) spec, there will
not be a separate pre-hash or contextualized mode.

