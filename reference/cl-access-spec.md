# cl — access spec for a read-only credential on `zj1-images` (item 11)

**Status:** specification only. cl has not requested, listed or fetched anything, and the AWS variables already in cl's environment are still unused. cs writes David's grant guide; this is what that guide has to grant.

## What cl cannot supply, and why
**The exact prefixes.** The Space's prefix names live in cs's inventory, which is in the ZJ1 repo; cl may not read it, and listing the Space to find them would use the very credential being specified. The table below therefore names each prefix by **role**, and **cs fills in the prefix strings and counts from the inventory** before David signs.

## The finding that shapes the ask
The eligible pool's sources are not obviously in the Space. cs's scripts read the 2,478 new codes from local zips (`…/261111_additional_images_unzipped/<zip>/…`, the import of 2026-11-11 "still to be processed"), while the Space inventory covers the **11,703-image legacy photo map** (`saphirim`, `tamirzuman`) and its derivatives. Two consequences, both for cs to confirm:
1. **Items 8 and 9 (dating the 2,485) may need no Space access at all.** They need either the new-code zips themselves or only their metadata.
2. **Zip entry mtime (rung 2) cannot come from the Space.** An object's `LastModified` is its upload time, not the file's date; zip time exists only inside an archive. If the originals are loose objects, rung 2 is unavailable from there and only EXIF (rung 1) and folder name (rung 3) remain.

## Scope A: dating (items 8 and 9). The narrow ask
| Role | Prefix (cs fills) | Why | Objects | Bytes actually read |
|---|---|---|---|---|
| Originals of the 2,478 new codes, **if they are in the Space** | `<cs: prefix>` | EXIF `DateTimeOriginal` per source file | **4,423** source images (3,217 unique; from `data/dataset_2485.csv`) | **≤ 283 MB**: first 64 KB of each (4,423 × 64 KB), by HTTP range |
| Originals of the 7 legacy-2023 SKUs | `<cs: prefix>` | same | ≤ 7 SKUs' files | negligible |

If those originals are **not** in the Space, Scope A needs no credential: cs supplies, or David points cl at, the zips (or a copy of their central directories plus the first 64 KB of each entry).

## Scope B: only after A and only if David says so (item 1's census pixels, and its extension)
| Role | Prefix (cs fills) | Objects | Bytes |
|---|---|---|---|
| Best source per SKU for the 2,478 new codes (if in the Space) | `<cs: prefix>` | 2,478 | **unknown**: no file-size column exists in the data; at roughly 1 MB per 1,600 px JPEG, about 2 to 4 GB, unverified |
| Legacy photo-map originals, for the 11,695-SKU extension | `<cs: prefix>` | 11,703 | **unknown**; the whole Space is 34.8 GB over 403,652 objects, so this is a fraction of it |

## Never needed, so never in scope
The delivery sizes (320, 500, 640, 1000 px at 46,801 objects each; 9,531 at 1,500; 8,098 at 1,280), the 11,694 cutout PNGs, the manifests, and every prefix not named above. That is most of the 403,652 objects.

## Operations: list and get, nothing else
- **Allowed:** `ListObjectsV2` restricted to the named prefixes; `GetObject`, including `Range` reads.
- **Not granted:** Put, Delete, ACL, versioning, multipart, lifecycle, bucket listing (`ListAllMyBuckets`), any other bucket.
- **A limit to check, not assume:** if "Space" means DigitalOcean Spaces, access keys are scoped **per bucket** (read or read/write/delete), not per prefix. Then the credential cannot enforce the prefix list: only cl's conduct can, which David can audit but not rely on. **The narrowest real option is for cs to copy the Scope A objects (or just the zips' metadata) into a small separate bucket and issue a read-only key for that one.** cs to say which is feasible.

## What cl will do with it
List only the named prefixes; fetch only by range for Scope A; keep in the repo the key name, size, EXIF fields and dates (never the image bytes); delete scratch bytes at the end; write nothing to the Space; stop on the first 403 or any prefix not in this table; report the number of list and get requests and the bytes fetched in the item's four-line report; never commit the credential.

## Cost, to settle before the grant
Reading from a Space can count against its **bandwidth allowance**, which is metered beyond a free amount. Scope A is under 0.3 GB. Scope B is larger and unknown. This repo's limit is US$0, so **David or cs should confirm the allowance covers it**, or Scope B stays unrequested.

## Revocation
The key should be created for this round, listed by name in the grant guide, and revoked when cl's round closes (Wednesday 02:00).

## Questions for cs, in the order they unlock things
1. Are the 2,478 new codes' originals in `zj1-images`, and under which prefix? (If not, Scope A needs no credential.)
2. Does the bucket allow per-prefix keys, or can the Scope A objects go into a small separate bucket?
3. Are the new-code zips still available intact, so zip entry mtime can be read?
