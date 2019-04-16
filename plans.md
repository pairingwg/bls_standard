# BLS Standard Draft -- Plans

We outline our plans for the next iteration of the draft.

## Major

* Add a section for signatures defined over the BLS12-381 curve,
following the [EdDSA](https://tools.ietf.org/html/rfc8032) spec.

* For hash_to_G1, we will use H2C-BLS12_381_1-SHA512-FT-Clear (to be added
to the hash-to-curve spec).

   - The destination group is the set of points in the G1 group
   of the BLS12_381 curve.
   
   - hash2base uses SHA-512 modulo p with label "H2C-BLS12_381_1-SHA512-FT-Clear"

   - HashToCurve is the Fouque-Tibouchi method map2curve_ft
   
   - The final output is multiplied by the cofactor.										

  We will remove the suite_string since this is already taken into
  account in the hashing algorithm (namely, the label in hash2base) in
  the hash-to-curve spec.

* Add a contextualized extension of the scheme analogous to Ed25519ctx.

* Add implementation for proof-of-possession mechanism against rogue
key attacks where we use the context mode to implement domain
separation for the proofs of possession and the actual signing.


## Minor

* Move the text for the "try-and-increment approach" for hashing onto
curves to the Appendix.  We will also refer to this approach as
"hash-and-test" to avoid incorrect implementations that simply
increment the x-coordinate by 1.

