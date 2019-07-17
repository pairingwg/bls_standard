# Meeting notes July 15, 2019

* Attendees:
Armando Faz,
Bram cohen,
Carl Beekhuizen,
Dan Middleton,
Chih Cheng Liang,
Hoeteck Wee,
Justin Drake,
Mariano Sorgente,
Mike Lodder,
Raid Wahby,
Sean Bowe,
Sergey Gorbunov,
Victor Servant,
Zaki Manian,
zhenfei Zhang

----------------

Useful links:
[Pairing draft](https://github.com/pairingwg/pfc_standard)
[Hash to curve draft](https://tools.ietf.org/html/draft-irtf-cfrg-hash-to-curve-04)
Current references:
* https://github.com/kwantam/bls_sigs_ref
* https://github.com/sigp/milagro_bls/
* https://github.com/hyperledger/ursa/blob/master/libursa/src/bls/mod.rs
* https://github.com/mikelodder7/bls12-381-comparison


----------------


Sergey: opening

* a summery of the current state of the draft
  * dependencies: pairing draft, hash to curve; both to be presented at next IETF meeting
  * summery from last meeting:
    * agreed to decouple BLS standard for blockchain from BLS draft for IETF
    * Etherum is looking for deployment this fall
    * we expect to have BLS standard for blockchain by end of this summer

* decide the right format for the spec: python sudo codes
  * Justin: will use BLS to deposit contract. No performance requirement there; pseudo code is sufficient
  * Mike: Signature is not the bottleneck for them either.
  * Bram: do not require constant time code for reference implementation
  * Justin: Harmony also launched BLS signature
  * Justin: the standard needs to handle edge cases; pseudo code may not be sufficient
  * Discussions on proof of possession, etc
  * consensus: for bls standard for blockchain, a high level spec, with pseudo codes to cover edge cases;
IETF draft may need a more detailed spec.

----------------

Status of hash to curve draft
* Riad: the draft is updated for the coming IETF meeting, two major changes:
  * first one is how to hash strings to the field. Previously uses sha256, described [here](https://github.com/pairingwg/bls_standard/blob/master/minutes/spec-v1.md#hash-to-curve).
    The revised draft will use hkdf as specified by [RFC-5869](https://tools.ietf.org/html/rfc5869).
    This change is __NOT__ backward compatible with current BLS implementations.
  * the other change is on domain separation, ciphersuite, etc. It is not expected to impact BLS standard.
  * time line for hash to curve draft: closer to feature complete. It still needs pseudo code, test vectors, clean ups, etc.
    They do not have an exact deadline, but expect that the delta between current version and the final one will be minor.

* Sergey: our plan is to freeze some version of hash to curve draft, and use that version for BLS standard for blockchain.
* Bram: fine with the change for now
* Raid: concerned about backward compatibility; a possible solution: use csid to separate implementation versions.
* Justin: spec looks good, happy with hkdf. Clarifications may need: shall we pass msg or msg digest to hkdf to extract?
* Justin: restrict msg to 32 bytes digest
* Bram: api should take 32 bytes, not necessarily digest
* Hoeteck: we shall follow ECDSA draft
  * 2 modes for signing: pre-hash mode and normal mode.
  * need to check the length of pre-hashed message

----------------

Updates on implementations

* Mike: confusion on non-constant time hash to group based on hkdf
* Riad: hkdf is used for hash to field, not to group. So hash to curve still remains constant time.

* Riad: reference implementation,
  * no major changes
  * added/adding more more test cases: must fail tests for non group elements
  * should also put those test cases in the spec

* Armando: no update.
* Kirk: on holiday

* Sergey: update proof of possession and aggregation for spec; update code after that

----------------

Misc

* Mike: working on bbs+ signature with selective opening; is looking for faster pairing curve implementation.
* Sergey: pairing friendly curves is done by another draft
* Armando: Mike can take a look at [relic](https://github.com/relic-toolkit/relic)

* Justin: serialization issue
* Riad: zcash use size/length to imply the which group the element lies in;
  * [issue](https://github.com/pairingwg/bls_standard/issues/16) on bls standard github
  * backward compatibility - zcash is not able to decode
* next step: everyone takes a look at the [issue](https://github.com/pairingwg/bls_standard/issues/16) and discuss it during the next call?

----------------

Next step:

* Justin: what more work need to be done? proof of possession, aggregation, and ciphersuite ids.
* Riad: serialization format for signature and proof of possession, domain separation.
* Hoeteck: serialization for curve point will imply serialization for signatures
