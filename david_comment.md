david's comments


Remaining issues:



- abstract: re-write with "what is it?" in mind first, history bits
can wait until the introduction. I suggest using developer-friendly
terms like "compression" and define aggregation later if the term is
needed. Example:

    BLS is a digital signature scheme with compression properties.
With a given set of signatures (sig_1, ..., sig_n) anyone can produce
a compressed signature sig_compressed. The same is true for a set of
private keys or public keys, while keeping the connection between sets
(a compressed public key is associated to its compressed public key).
Furthermore, the BLS signature scheme is deterministic, non-malleable,
and efficient. Its simplicity and cryptographic properties allows it
to be useful in a variety of use-cases, specifically when minimal
storage space or bandwidth are required.

- intro:

    - "2.  Verification requires 2 pairing operations." -> at this
point pairing is not defined, and what does that mean for the
developer? how does it compare to other signature schemes that do not
use pairing?

    - __comparison with classical signatures, such as ECDSA, from engineering perspective__

- section "1.1.  Terminology"

    - "P1" is defined but never seem to be used. Am I missing something?
      - __useful if we switch groups__


- section "1.2.2.  Security" -> do we need these security properties
in the RFC? It sounds to me like they would belong in a whitepaper
instead.

- "There are two variants of the scheme" -> It'd be nice if the
two variants were specified in this document, as they both have
use-cases.


- "4.  If r*Gamma != 0, output "INVALID" and stop" -> I had heard
a while ago that this membership check was patented for ECDH. Anyone
remembers something like this?

- you specify verifying aggregates of SAME msg and of DIFFERENT
msgs, but only have the aggregate algorithm for SAME msg specified.
  - __todo: add different msg aggregation__

- section "2.5.3.  Implementation optimizations". Two things:
    - this should be towards the end of the documentation as these are
optional recommendations. Perhaps after "security recommendations" or
as an appendix
    - is it really wise to have the standard contain this? Available
optimizations may change over time. I've also never seen an RFC
talking about optimizations.


- section "2.7.  Security analysis" -> I don't think this is necessary
to have that in the RFC.



- define "G2 membership test"


- section "3.4. Randomness considerations" needs a citation, for
example on ECDSA issues when the nonce is repeated

- section "4.  Implementation Status". Standards usually don't refer
to implementations AFAIK. I imagine this is because their state can
change, and new good implementations can arise after the RFC is set in
stone. I think this is good to have in the draft though, so perhaps
add an indication somewhere that this will be deleted in the final
document.
