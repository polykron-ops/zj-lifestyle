# cl — item 3, text half: families without a paid image pass

**The premise does not hold in this repo.** All 2,485 SKUs already carry a `family_letter` and a `family`; none is missing. No title or description text exists here: `supplier_description` and `supplier_colour` are empty for all 2,485, so there is nothing to classify from title text. The only text is `category_code`.

**What the data does support:** the 59 SKUs in `other` (letters A, S, P, M, C) mostly carry the worn-location in the second letter of `category_code` (AEZ, ANZ, ARZ, SE, SN, SR, SB). Script `scripts/cl_family_text.py` (self-test included) proposes:

| Proposed | SKUs |
|---|---|
| earrings | 26 |
| necklaces | 17 |
| rings | 5 |
| bracelets | 1 |
| loose pendant, no chain (P, PG) | 8 |
| unresolved (MW, CAF) | 2 |

Agreement with cs's reads: **6 of 6** `other` SKUs that cs read (2 loose pendants, 1 SN and 2 ANZ as necklace pendants, 1 AEZ as earring drop). n=6 is small, and what A and S stand for is unknown (inferred from the second letter only).

If adopted, family counts would move (on the 2,478-code pool; on cs's 2,485 dataset earrings 843→869, necklaces 759→776, rings 534→539, bracelets 241→242): earrings 842→868, necklaces 755→772, rings 534→539, bracelets 239→240, other 59→10. cs's dataset is not changed; this is a proposal. Forms inside a family (hook against stud against hoop) need alpha and geometry, so wait on pixel access.
