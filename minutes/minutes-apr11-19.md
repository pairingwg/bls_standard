
# Meeting notes Apr 11, 2019, 6.30 pm EST

* Attendees:

    Kirk Baird
    Vitalik Buterin
    Justin Drake
    Dankrad Feist
    Sergey Gorbunov
    Paul Hauner
    Danny Ryan
    Hsiao-Wei Wang
    Hoeteck Wee

* Justin: The Ethereum 2.0 team is keen to boost the BLS standardisation effort.
Indeed, many projects are intending to launch in 2019 and standardisation takes time. 

* Sergey: The BLS signatures draft is intended for the wide community and not just the
blockchain community. We choose IETF/CFRG for several reasons:

     - generally regarded as the industry standard. E.g. TLS 1.3, EdDSA, etc
     - BLS signatures builds upon two IETF/CFRG drafts: one for pairing-friendly
     curves, and another for hashing to curves
     - can get valuable feedback from a broad community of academic cryptographers and
     industry experts.

* Which hashing algorithm? General support for Fouque-Tibouchi for BLS12-381.

     - 15% overhead over hash-and-test (see numbers below)
     - constant-time implementations for forward-compatibility (even though we do
     not know any use cases with such a requirement off-hand)
     - slower signing does not seem to be a big deal, and signing unlikely to be a bottleneck
     - most players are not too opinitiated about which algorithm to use.

* Suggestion: limit the scope of options in the BLS signatures draft, e.g.
  fix BLS12-381 curves, etc.

* General support for (i) standardizing two variants of the scheme,
  one where signatures are in G1, another where signatures are in G2,
  and (ii) standardizing aggregation algorithms

* Etherum 2.0 consensus. Enshrine key registration; don’t enshrine
  user-level transaction. Data layer / agnostic. Contract can specify
  whatever signature scheme they want. Don’t even have a notion of
  transaction. Centralized spec, outsourcing implementation. All the implementations
  are open-source.

* Etherum uses proof of possession for protect against rogue key attacks
  in consensus. Domain separation could maybe be left to the application level.

* Serialization: need to point all the way to bits. The rest should be at the
  application or networking level, etc.

     - as a starting point, we could follow the zcash [serialization](
     https://github.com/zkcrypto/pairing/blob/183a64b08e9dc7067f78624ec161371f1829623e/src/bls12_381/ec.rs#L837)
     - this should be handled in the draft for pairing-friendly curves.

* Will not limit the length of the messages.

     - consistent with Ed25519: "The inputs to the signing procedure is the private key,
     32-octet string, and a message M of arbitrary size."
     - arbitrary-length messages already handled by hash-to-curve anyway

* Should create a Telegram channel -- update: [link](https://t.me/blsstandardwg)


## Appendix


### Benchmarks for hashing onto BLS-381 G1

These numbers are on an i7 processor.

* hash-and-test x cofactor: hashing takes 140 μs and signing 370 μs
* map2curve_ft x cofactor: hashing takes 200 μs and signing 430 μs

Here is a breakdown of the costs:

* map2curve_ft computes 3 square roots (90 μs) plus extra operations
* hash-and-test computes 2 = 1+0.5+0.25+0.125 +... square roots (60 μs)
* 1 cofactor multiplication (80 μs),
* signing is hash plus 1 G1-exp (130 μs)

Note that Chia implements indifferentiable hashing and makes two calls to map2curve_ft.
This incurs an additional cost of 120 μs.

### Proposed agenda (Sergey)

For BLS, we're looking for immediate feedback on the following questions: 

1) Hashing algorithms. There are three variants we consider: 
* hash-and-test (not constant time) 
* Fouque-Tibouchi Method (map2curve_ft) : hits 5/8 points
* repeat map2curve_ft twice and add the outputs points to hit all points on the curve. 

   Our implementation for map2curve_ft adds 15% vs hash-and-test method. 

2) Protection against rogue key attacks. 
* Message augmentation:    pk = g^sk,   sig = H(pk, m)^sk
* Proof of possession:     pk = ( u=g^sk,  H'(u)^sk ),    sig = H(m)^sk
* Linear combination:    agg =  sig_1^t_1 ... sig_n^t_n

3) We're planning on standardizing 2 variants of the scheme, one where signatures are in G1, another where signatures are in G2. 

4) Serialization. Agree on methods for conversions between strings and curve points.

For instance, for transactions in blockchains one could consider instantiating the scheme in the following ciphersuite: 

* Use hash-and-test (since constant time is not required for signatures)
* Use message augmentation to protect against rogue key attacks (since all messages signed in transactions are already distinct). 
* Put signatures in G2 (since public keys have to live on the chain in clear; but signatures can be compressed). 


### Pointers

* Implementations

   https://github.com/ethereum/eth2.0-specs/blob/master/specs/bls_signature.md
   https://github.com/sigp/signature-schemes
   https://github.com/ethereum/eth2.0-pm/issues/13/

* Jubjub -- https://z.cash/technology/jubjub/

* Hashing to G2

   https://github.com/Chia-Network/bls-signatures/blob/master/SPEC.md
   https://eprint.iacr.org/2017/419.pdf
