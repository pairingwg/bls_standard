
# Meeting notes Jun 24, 2019

* Attendees:

    Kirk Baird
    Justin Drake
    Sergey Gorbunov
	Armando Faz
	Riad Wahby
	Bram Cohen
	Brian Vohaska
	Carl Beekhuizen
	Kobi Gurkan
	Mariano Sorgente
	Victor Servant
	Zhenfei Zhang
	
* Sergey: start with overview of implementations

     * Kirk: implementation matches Riad's, provided additional test vectors

     * Kobbi: gave suggestions on how to improve performance on sage.
     suggested adding test vectors for basic curve operations (ED: some test vectors already in pairing-friendly draft)

     * Riad: current implementation specifies message, secret key, and test checks that the verification is successful.

     * Armando: implementation in Go, some assembly implementations

      * Riad: Berkeley folks, [JEDI](https://people.eecs.berkeley.edu/~raluca/JEDIFinal.pdf), some low-level
	  [implementations](https://github.com/ucbrise/jedi-pairing)

     * Hoeteck: which curves to use and which functions to use will be specified in the pairing specific draft.

     * Riad: will check pairing-friendly draft to confirm consistency of the pairing function.

* Justin: target date for production-ready code -- Oct 8, 2019 (ED: no one else provided target dates)

* Kobi: motivated BLS12-377 (SNARKs) [ZEXE](https://eprint.iacr.org/2018/962.pdf) [implementation](https://github.com/scipr-lab/zexe)
[BLS12-377 code](https://github.com/scipr-lab/zexe/tree/master/algebra/src/curves/bls12_377)

     * Bram: how do sizes and performances compare? doing things inside snarks is a use case that’s far from now.

     * Kobbi: sizes are comparable

     * Riad: there might be slight speed improvements for 381 vs 377, but should be small. Hashing to g1 for 377 is no problem. Hashing to g2 for 377 should be about 2x worse, for non-constant should be 25-35% worse than for 381.

* Sergey: may be useful to have a self-contained description for the blockchain community independent of the IETF standards

* Justin: status of hash-to-curve?

    * Riad: see github [page](https://github.com/cfrg/draft-irtf-cfrg-hash-to-curve) for a substantially updated draft.
	hash to curve should be updated by the next ietf meeting.
	discussion on [domain separation](https://github.com/cfrg/draft-irtf-cfrg-hash-to-curve/issues/124)

* Justin / Kirk / Carl: will check that the Etherum production-ready code remains consistent with the current reference implementation / test vectors

* Sergey / Riad: short-term -- focus on and continue with BLS 12-381

* Carl: will people abandon BLS 12-381 if BLS-377 turns out to be the better one in 6 months' time?

