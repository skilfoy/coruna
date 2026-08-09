# CORUNA CONTAINER EVOLUTION REPORT — COMPLETE LOCAL WORKING COPY
## Part 5 of 5 (lines 1441–1797 of 1797)

**This is the uncondensed full local analysis. No content removed.**

[Index](CORUNA_CONTAINER_EVOLUTION_REPORT.md) | [Part 1](CORUNA_FULL_PART1.md) | [Part 2](CORUNA_FULL_PART2.md) | [Part 3](CORUNA_FULL_PART3.md) | [Part 4](CORUNA_FULL_PART4.md) | [Part 5](CORUNA_FULL_PART5.md)

---

files are hashed offline).

### 7.4 Combination Logic

High-confidence alerts can be raised by any of the following combinations:

1. DEADD00F rule OR modern type 0x08 hash/size  
   → covers essentially all mature containers (B/C/D)

2. KIEA rule AND (presence of two type 0x09 records)  
   → Generation D dual-driver with very high specificity

3. Type 0x0A 507450 B AND small type 0x08 (≈50–105 KB)  
   → Generation A with high specificity

4. Type 0x0A 50344 B AND type 0x09 AND DEADD00F  
   → Generation C transitional packaging

Because the DEADD00F + SpringBoard pattern is both unique and present in every
mature container, it is the single best “first pass” indicator. Everything else
can be used for generational attribution or for confirmation.

### 7.5 False-Positive Discussion

- DEADD00F magic alone (without the SpringBoard string or size constraint) is
  theoretically possible in other contexts; the combination with “SpringBoard”
  and a tiny file size makes accidental matches extremely unlikely.

- Exact file-size rules for the type 0x08 and type 0x0F modules are safe only
  when the scanner is looking at discrete extracted modules or when the size
  is checked in conjunction with Mach-O headers. In a large disk image a
  random 228928-byte file is possible but statistically uncommon; pairing with
  the SHA or with Mach-O magic reduces residual risk to near zero.

- KIEA (“KIEA” at offset 0 + exact 24844 bytes) has no known benign collisions.

- The compact 50344-byte type 0x0A dylib is the weakest of the size-only rules
  and should preferably be combined with the presence of a type 0x09 or
  DEADD00F record.

### 7.6 Coverage Matrix

| Rule / Indicator | Gen A | Early B | Late B | Gen C | Gen D |
|-------------------------------|-------|---------|--------|-------|-------|
| DEADD00F + SpringBoard | | ✓ | ✓ | ✓ | ✓ |
| Type 0x08 modern (228928) | | | ✓ | ✓* | ✓ |
| Type 0x08 older (196864) | | ✓ | | ✓* | |
| KIEA (24844) | | | | | ✓ |
| Dual f1 0x90000+0x90001 | | | | | ✓ |
| Type 0x0A large (507450) | ✓ | | | | |
| Type 0x0A compact (50344) | | | | ✓ | |

\* One Generation C container uses the older implant/persistence pair.

The matrix shows that a scanner implementing only the DEADD00F rule plus the
two type 0x08 size/hash rules already achieves complete coverage of every
mature container in the corpus.

### 7.7 Recommended Deployment Order

1. Deploy DEADD00F + SpringBoard rule (highest coverage, lowest complexity).
2. Add exact size or SHA rules for the two type 0x08 implants.
3. Add KIEA rule for Generation D attribution.
4. Add type 0x0A size rules if Generation A or C coverage is required.
5. Optionally parse F00DBEEF containers for the dual-f1 condition when full
   container context is available.

# ==============================================================================
# PRIORITY 4 — FORMAL GENERATION DECISION TREE AND TIMELINE ARGUMENTS
# ==============================================================================

## 6.4 Formal Generation Assignment Decision Tree

```
START
  │
  ├─ Contains type 0x05 (KIEA) record?
  │     YES → Generation D (Dual-Driver)
  │             (confirm: two type 0x09 with f1 0x90000 and 0x90001)
  │     NO
  │
  ├─ Contains type 0x09 record?
  │     NO  → Generation A (or Anomalous if no type 0x0A either)
  │     YES
  │
  ├─ Contains type 0x0A record?
  │     YES → Generation C (Transitional)
  │     NO  → Generation B (Classic Single Type-0x09)
  │
  └─ (Optional sub-classification for Gen B)
        type 0x08 size == 228928 → Late B (modern implant)
        type 0x08 size == 196864 → Early B (older implant)
```

This tree is complete for the twenty containers examined; every container falls
into exactly one leaf.

## 6.5 Relative Dating Arguments

**Argument 1 — Type 0x0A primacy**  
Generation A containers contain only type 0x0A + small type 0x08. They lack
DEADD00F, type 0x09 and type 0x0F. No later generation reverts to this minimal
structure. Therefore Generation A is earlier than B/C/D.

**Argument 2 — Introduction of the modern support-layer triple**  
DEADD00F + type 0x09 + type 0x0F appear together for the first time in
Generation B and remain present in every subsequent mature container.

**Argument 3 — Implant/persistence coordinated revision**  
Inside Generation B an older type 0x08/0x0F pair and a newer pair coexist.
The newer pair is the only pair used by Generation D and by the majority of
Generation C.

**Argument 4 — Transitional retention of type 0x0A**  
Generation C carries both a full type 0x09 stack and a compact type 0x0A
dylib. Sits logically between pure single-driver Generation B and the dual-driver design.

**Argument 5 — Dual-driver as terminal refinement**  
Generation D introduces f1 low-bit driver selection + shared external constants
with no precedent in earlier generations. Only two containers. Latest recovered design.

Relative order: A → B (with internal implant revision) → C → D

## 6.6 Design-Pressure Narrative (Expanded)

In Generation B the operators already needed at least seven distinct type 0x09
binaries whose sizes ranged from 231 KB to 333 KB. Each new iOS point release
or security patch that changed relevant kernel offsets or PAC gadgets would
have required either a new full driver build or invasive binary patching.

The Generation D redesign attacks exactly this cost:

- Two driver variants are shipped instead of many.
- Version-specific data is externalised into a single shared 24 KB KIEA blob.
- Selection is reduced to a single bit test on the f1 field.
- The same KIEA blob can be paired with different driver builds.

# ==============================================================================
# PRIORITY 6 CONTINUATION — METHODOLOGY, LIMITATIONS, REPRODUCIBILITY
# ==============================================================================

## 8.4 Detailed Methodology

### Data Sources
- Repository tree under payloads/ (complete recursive listing)
- payloads/manifest.json (authoritative f1 / type / size / SHA index)
- Previously published dual-driver original research (companion report)
- Direct size and SHA-1 verification of extracted modules

### Analytical Steps Performed
1. Enumeration of every container directory and every entry record.
2. Construction of a presence/absence matrix for types 0x05, 0x07, 0x08, 0x09, 0x0A and 0x0F.
3. Identification of shared SHA-1 identities across containers.
4. Clustering of containers by identical module sets → four generations.
5. Size-distribution analysis of type 0x09 binaries inside Generation B.
6. Formulation of the relative chronology and design-pressure narrative.
7. Derivation of detection rules from the highest-signal shared artifacts.

### Tools Used
- Standard Unix utilities (find, ls, sha1sum equivalents via repository metadata)
- Python for table generation and consistency checks
- Manual cross-referencing of manifest.json against tree listings

No commercial disassembler, emulator, or dynamic analysis system was used.

## 8.5 Limitations (Expanded)

1. Internal code of the large binaries remains unexamined.
2. Precise layout and semantics of the KIEA constants table beyond magic and length are unknown.
3. Absolute dating is impossible. Only relative order is supported.
4. Secondary 468-byte type 0x07 records vary; exact purpose not recovered.
5. One anomalous container (raw.bin only) is left unclassified.
6. Analysis scoped to the skilfoy/coruna repository snapshot.

## 8.6 Reproducibility Checklist

- [ ] Clone https://github.com/skilfoy/coruna
- [ ] List all directories under payloads/
- [ ] Confirm 20 container directories (including the anomalous raw.bin entry)
- [ ] Parse payloads/manifest.json and extract f1 / type / size / SHA for every entry
- [ ] Verify that exactly two containers contain a type 0x05 record of 24844 bytes
- [ ] Verify that those two containers each contain two type 0x09 records whose f1 values are 0x90000 and 0x90001
- [ ] Verify that the DEADD00F SHA ea2db48a… appears in every container that also contains a type 0x09 record
- [ ] Verify the modern / older type 0x08 size split (228928 vs 196864)
- [ ] Confirm that no container mixes a modern type 0x08 with an older type 0x0F
- [ ] Confirm that type 0x0A is present in Generation A and Generation C only
- [ ] Re-derive the four-generation taxonomy using the decision tree in §6.4

# ==============================================================================
# EXPANDED APPENDICES
# ==============================================================================

## Appendix D — Complete Type 0x09 Size and Identity Register

| Size | SHA-1 (prefix) | Generation(s) | Container prefix(es) | Role |
|------|----------------|---------------|----------------------|------|
| 333520 | 603f703d… | D | 377bed74… | Dual primary |
| 333504 | c90bbcb5… | B (early) | 7a1cef00… | Single |
| 330304 | aace9599… | D | 377bed74… | Dual secondary |
| 300912 | a284d84f… | B (late), C | ae7efd66…, 1b2cbbde… | Single / C |
| 300912 | 2a446a3b… | B (early) | 226cbd84… | Single |
| 284048 | 172b89e4… | B, C, D | multiple | Multiple |
| 284048 | fa7f7a9e… | B (early), C | 38af3c8b…, e9f89858… | Single / C |
| 263536 | 0cfd6098… | D | 13344176… | Dual secondary |
| 249024 | 1f084486… | B (early) | 48000486… | Single |
| 248784 | a1f063dd… | B (late) | a78a9419… | Single |
| 232256 | 2c3b7f3f… | B (early) | 5258f6e3… | Single |
| 231264 | 564da86d… | B (late) | b442ab11… | Single |

## Appendix E — Generation Membership Quick Reference

**Generation D:** 377bed7460f7538f96bbad7bdc2b8294bdc54599, 1334417664270db20af705f422878c53c8378203  
**Generation C:** 1b2cbbde08f8b2330b7400abcb97c9573973e942, c8a14d79a27953242d60243ee2f505a85d9232cc, e9f898587620186e31119fbf32660f26c1e048e0, f4120dc6717a489435d86943472c5a2444aac8e6  
**Generation B (older):** 226cbd845c5f470075505392be8693ec6d4f5ba3, 38af3c8ba461079a0edc83585023f76843066dcf, 4800048658463f971e752ff93c1767e9ae7f3431, 5258f6e3eef3eda249179aa1122b50b03cbeea18, 7a1cef00016b950be42f5288ead21fa6fccc3107  
**Generation B (newer):** a78a94196b5d2c95865f6a8423a6b8eb86d07c6c, ae7efd66ecde9e964cfe92f64e9b6461fce38f28, b442ab113b829ff8c7bf34afa4d2d997889f308f  
**Generation A (dual small):** 2a1d692b7b5ba793527b2c14b48db21a3e5d2c5f, 5e89f83ec50c6223d664d3f3260ef874a3d6d796  
**Generation A (large):** 72a5ac816709f9c331f2b3afb76cd3d96517ea14, 980c77f1747afa9ac1fa5f8fbfb9e6663e9f82bb, f8a86cf368fdbbe294813926a2a229df041eb758  
**Anomalous:** 7a7d99099b035b2c6512b6ebeeea6df1ede70fbb

## Appendix F — f1 Namespace Reference (Complete)

| f1 (hex) | f1 (dec) | Type | Observed Role | Generations |
|----------|----------|------|---------------|-------------|
| 0x50000 | 327680 | 0x05 | KIEA shared constants | D |
| 0x70000 | 458752 | 0x07 | Secondary configuration | B, C, D |
| 0x70005 | 458757 | 0x07 | Primary DEADD00F / SpringBoard config | B, C, D |
| 0x80000 | 524288 | 0x08 | Post-exploitation implant | All |
| 0x90000 | 589824 | 0x09 | Primary (or sole) kernel driver | B, C, D |
| 0x90001 | 589825 | 0x09 | Secondary kernel driver (selectable) | D |
| 0xA0000 | 655360 | 0x0A | Compact type 0x0A dylib | C |
| 0xA0001 | 655361 | 0x0A | Generation A type 0x0A.bin (small) | A |
| 0xA0002 | 655362 | 0x0A | Generation A type 0x0A (dylib or large bin) | A |
| 0xF0000 | 983040 | 0x0F | Persistence / SpringBoard injection | B, C, D |

## Appendix G — Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-07-26 | Initial comparative survey and inventory |
| 1.1 | 2026-07-26 | Full Gen D/C tables, Type 0x08/0x0A analysis |
| 1.2 | 2026-07-26 | Complete Generation B entry tables and size analysis |
| 1.3 | 2026-07-27 | Full detection rule set, decision tree, methodology |
| 1.4 | 2026-07-27 | Expanded appendices, type 0x09 register |
| 1.5 | 2026-08-09 | Complete uncondensed local working copy published as CORUNA_FULL_PART1–5 |

Companion document:  
DUAL_DRIVER_SUPPORT_LAYER_ORIGINAL_RESEARCH.md

---

**End of complete local working copy.**

The published report (index + five FULL parts) contains the complete 1,797-line
local analysis with no analytical content removed: full technical inventory of
all 20 containers, complete Generation B entry tables, Type 0x08/0x0A analysis,
formal decision tree, full YARA suite, confidence matrix, key judgments,
methodology, reproducibility checklist, and all appendices.
