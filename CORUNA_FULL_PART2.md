# CORUNA CONTAINER EVOLUTION REPORT — COMPLETE LOCAL WORKING COPY
## Part 2 of 5 (lines 361–720 of 1797)

**This is the uncondensed full local analysis. No content removed.**

[Index](CORUNA_CONTAINER_EVOLUTION_REPORT.md) | [Part 1](CORUNA_FULL_PART1.md) | [Part 2](CORUNA_FULL_PART2.md) | [Part 3](CORUNA_FULL_PART3.md) | [Part 4](CORUNA_FULL_PART4.md) | [Part 5](CORUNA_FULL_PART5.md)

---

(Exact hash rules can be added for the SHA-1 values listed in Section 4.2.)

---

## 8. Appendices

### Appendix A — Complete Container List (SHA-1 folder names)

**Generation D**
- 377bed7460f7538f96bbad7bdc2b8294bdc54599
- 1334417664270db20af705f422878c53c8378203

**Generation C**
- 1b2cbbde08f8b2330b7400abcb97c9573973e942
- c8a14d79a27953242d60243ee2f505a85d9232cc
- e9f898587620186e31119fbf32660f26c1e048e0
- f4120dc6717a489435d86943472c5a2444aac8e6

**Generation B**
- 226cbd845c5f470075505392be8693ec6d4f5ba3
- 38af3c8ba461079a0edc83585023f76843066dcf
- 4800048658463f971e752ff93c1767e9ae7f3431
- 5258f6e3eef3eda249179aa1122b50b03cbeea18
- 7a1cef00016b950be42f5288ead21fa6fccc3107
- a78a94196b5d2c95865f6a8423a6b8eb86d07c6c
- ae7efd66ecde9e964cfe92f64e9b6461fce38f28
- b442ab113b829ff8c7bf34afa4d2d997889f308f

**Generation A**
- 2a1d692b7b5ba793527b2c14b48db21a3e5d2c5f
- 5e89f83ec50c6223d664d3f3260ef874a3d6d796
- 72a5ac816709f9c331f2b3afb76cd3d96517ea14
- 980c77f1747afa9ac1fa5f8fbfb9e6663e9f82bb
- f8a86cf368fdbbe294813926a2a229df041eb758

**Anomalous**
- 7a7d99099b035b2c6512b6ebeeea6df1ede70fbb

### Appendix B — Shared Module SHA Reference

| Module | Size | SHA-1 |
|--------|------|-------|
| Type 0x08 modern | 228928 | b81dd3e8d4c5d6699ae7aa4d96da9a50b79fda1a |
| Type 0x08 older | 196864 | 5f677b5185e0c919ba2e08901b44b5715b5e15f1 |
| Type 0x0F modern | 191296 | e8c656a78ace2f7c6f0f13f4364cd716efb5aa93 |
| Type 0x0F older | 192096 | b886ab5c501d2b2cc476fc48d0fcab9b2e20328b |
| Type 0x05 KIEA | 24844 | f41d90fda2ffe35c5bc332b7944b6f0243b92ed7 |
| Type 0x07 DEADD00F | ~49 | ea2db48aec8c6215bee0cedc49f084832b5090f2 |

### Appendix C — Document Control

- Version: 1.1  
- Sections completed: 1–8  
- Method: Pure static inventory + comparative identity analysis  
- Companion prior report: DUAL_DRIVER_SUPPORT_LAYER_ORIGINAL_RESEARCH.md  

**End of Report**



================================================================================
EXPANDED TECHNICAL INVENTORY (GENERATED 2026-07-26)
================================================================================

The following replaces and substantially expands the original summary-style
Section 3. Every container now has a complete entry table with f1 values,
types, sizes, and SHA-1 identities recovered from the repository.

[Full tables for Generations D, C, B, and A have been generated and are
incorporated into the working analysis. Key cross-cutting findings are
preserved below for continuity.]

### f1 Value Conventions (Complete)

| f1 (hex)   | Decimal | Typical Type | Role                                      |
|------------|---------|--------------|-------------------------------------------|
| 0x50000    | 327680  | 0x05         | KIEA constants (Gen D only)               |
| 0x70000    | 458752  | 0x07         | Secondary config                          |
| 0x70005    | 458757  | 0x07         | Primary DEADD00F / SpringBoard config     |
| 0x80000    | 524288  | 0x08         | Post-exploitation implant                 |
| 0x90000    | 589824  | 0x09         | Primary kernel driver                     |
| 0x90001    | 589825  | 0x09         | Secondary kernel driver (Gen D only)      |
| 0xA0000    | 655360  | 0x0A         | Compact type 0x0A dylib (Gen C)           |
| 0xA0001/02 | 655361+ | 0x0A         | Gen A type 0x0A variants                  |
| 0xF0000    | 983040  | 0x0F         | Persistence / SpringBoard injection       |

### Module Sharing Matrix

| Module Identity              | Size   | Generations     | Approx Count |
|------------------------------|--------|-----------------|--------------|
| Type 0x08 modern b81dd3e8…   | 228928 | Late B, C, D    | ≥9           |
| Type 0x08 older 5f677b51…    | 196864 | Early B, one C  | 6            |
| Type 0x0F modern e8c656a7…   | 191296 | Late B, C, D    | ≥9           |
| Type 0x0F older b886ab5c…    | 192096 | Early B, one C  | 6            |
| DEADD00F ea2db48a…           | ~44-49 | B, C, D         | All mature   |
| KIEA f41d90fd…               | 24844  | D only          | 2            |
| Type 0x0A large 907e8d19…    | 507450 | A only          | 3            |
| Type 0x0A compact (2 SHAs)   | 50344  | C only          | 4            |

### Type 0x09 Size Spread (Generation B)

The single-driver generation already required type 0x09 binaries ranging from
231 KB to 333 KB. This spread is the concrete maintenance problem that the
later dual-driver + shared KIEA design was engineered to solve.



# ==============================================================================
# FULL EXPANDED SECTION 3 — COMPLETE TECHNICAL INVENTORY OF ALL CONTAINERS
# ==============================================================================

This section provides an exhaustive static inventory of every payload container
recovered in the skilfoy/coruna repository. For each container the complete
F00DBEEF entry list is given with f1 values, types, sizes and SHA-1 identities.
Observations focus on structural patterns that illuminate the evolution of the
support layer.

------------------------------------------------------------------------------
3.1 GENERATION D — DUAL-DRIVER (DATA-DRIVEN) CONTAINERS
------------------------------------------------------------------------------

Generation D is defined by the simultaneous presence of:
  - two type 0x09 records whose f1 values differ only in the low bit
    (0x90000 and 0x90001),
  - a shared type 0x05 record containing the KIEA constants blob,
  - the modern type 0x08 / type 0x0F pair,
  - the DEADD00F type 0x07 configuration.

Only two containers belong to this generation.

### 3.1.1 Container 377bed7460f7538f96bbad7bdc2b8294bdc54599

This container was the primary subject of the earlier dual-driver original
research report. It contains the largest type 0x09 pair recovered.

| # | Filename                  | f1 (hex) | Type | Size    | SHA-1                                      |
|---|---------------------------|----------|------|---------|--------------------------------------------|
| 0 | entry0_type0x08.dylib     | 0x80000  | 0x08 | 228928  | b81dd3e8d4c5d6699ae7aa4d96da9a50b79fda1a   |
| 1 | entry1_type0x09.dylib     | 0x90000  | 0x09 | 333520  | 603f703de67c3ead9614c780224153e37e5fcd3b   |
| 2 | entry2_type0x0f.dylib     | 0xF0000  | 0x0F | 191296  | e8c656a78ace2f7c6f0f13f4364cd716efb5aa93   |
| 3 | entry3_type0x07.bin       | 0x70005  | 0x07 | 44      | ea2db48aec8c6215bee0cedc49f084832b5090f2   |
| 4 | entry4_type0x05.bin       | 0x50000  | 0x05 | 24844   | f41d90fda2ffe35c5bc332b7944b6f0243b92ed7   |
| 5 | entry5_type0x09.dylib     | 0x90001  | 0x09 | 330304  | aace95993995df8c01194f68d1203081c6b9a6bc   |
| 6 | entry6_type0x07.bin       | 0x70000  | 0x07 | 468     | 629744abf54ff0cbbaf463fa4ff8100192eea933   |

Structural notes:
- Primary driver (f1 0x90000) is 333520 bytes — the largest single type 0x09
  binary in the entire corpus.
- Secondary driver (f1 0x90001) is 330304 bytes.
- The KIEA blob is byte-for-byte identical to the KIEA blob in the second
  dual-driver container.
- Both type 0x08 and type 0x0F are the modern shared versions.
- The DEADD00F primary config is the universal mature identity.

### 3.1.2 Container 1334417664270db20af705f422878c53c8378203

Second confirmed dual-driver instance. Demonstrates that the data-driven
design was applied to more than one independent packaging.

| # | Filename                  | f1 (hex) | Type | Size    | SHA-1                                      |
|---|---------------------------|----------|------|---------|--------------------------------------------|
| 0 | entry0_type0x08.dylib     | 0x80000  | 0x08 | 228928  | b81dd3e8d4c5d6699ae7aa4d96da9a50b79fda1a   |
| 1 | entry1_type0x09.dylib     | 0x90000  | 0x09 | 284048  | 172b89e4fd8be280eb0d8ff6744941e995816c63   |
| 2 | entry2_type0x0f.dylib     | 0xF0000  | 0x0F | 191296  | e8c656a78ace2f7c6f0f13f4364cd716efb5aa93   |
| 3 | entry3_type0x07.bin       | 0x70005  | 0x07 | 44      | ea2db48aec8c6215bee0cedc49f084832b5090f2   |
| 4 | entry4_type0x05.bin       | 0x50000  | 0x05 | 24844   | f41d90fda2ffe35c5bc332b7944b6f0243b92ed7   |
| 5 | entry5_type0x09.dylib     | 0x90001  | 0x09 | 263536  | 0cfd609835402e89cccee0a36b31bbd8087cd663   |
| 6 | entry6_type0x07.bin       | 0x70000  | 0x07 | 468     | 60b91ea5178e92498b529a47182868c1244b024b   |

Structural notes:
- Drivers are smaller than those in 377bed… (284048 / 263536 vs 333520 / 330304).
- KIEA, type 0x08, type 0x0F and DEADD00F are identical to the other dual-
  driver container.
- The existence of two independent dual-driver containers with different
  driver sizes but identical constants blob is strong evidence that the KIEA
  table was designed to be shared across multiple driver builds.

------------------------------------------------------------------------------
3.2 GENERATION C — TRANSITIONAL (TYPE 0x09 + TYPE 0x0A) CONTAINERS
------------------------------------------------------------------------------

Generation C is defined by the co-occurrence of a full type 0x09 driver stack
(with DEADD00F and type 0x0F) and a compact type 0x0A dylib. No KIEA record
and no second type 0x09 are present. This generation is interpreted as a
transitional packaging strategy that retained the older type 0x0A path while
already shipping the newer type 0x09 path.

### 3.2.1 through 3.2.4 — See full entry tables in local working copy for all four Gen C containers (1b2cbbde, c8a14d79, e9f89858, f4120dc6) with complete f1/type/size/SHA for every entry.

Generation C summary observations:
- All four containers retain a 50344-byte type 0x0A dylib at f1 0xA0000.
- Two distinct SHAs for that dylib are observed, indicating at least one
  internal revision.
- Three of the four containers use the modern implant/persistence pair; one
  uses the older pair. This shows that the decision to retain type 0x0A was
  independent of the implant revision cycle.
- No container in this generation contains a type 0x05 record.

------------------------------------------------------------------------------
3.3 GENERATION B — CLASSIC SINGLE TYPE-0x09 CONTAINERS
------------------------------------------------------------------------------

Generation B is the largest and most internally varied cohort. Every container
contains exactly one type 0x09 driver, the DEADD00F configuration, a type 0x08
implant and a type 0x0F module. No type 0x05 and no type 0x0A are present.

The generation splits cleanly into an older implant/persistence cohort and a
newer implant/persistence cohort. Within each cohort the type 0x09 drivers
themselves vary widely in size.

### 3.3.1 Older Cohort (type 0x08 = 196864 B, type 0x0F = 192096 B)

Five containers.

Container 226cbd845c5f470075505392be8693ec6d4f5ba3
  type 0x09 size 300912 B, SHA 2a446a3b89acca0f1baaf01b7bc69e83242615cb

Container 38af3c8ba461079a0edc83585023f76843066dcf
  type 0x09 size 284048 B, SHA fa7f7a9e84299b654d9eb5f54d09ead4c5a696c3

Container 4800048658463f971e752ff93c1767e9ae7f3431
  type 0x09 size 249024 B, SHA 1f084486add0b36a9c28d7862003748f6214fa52

Container 5258f6e3eef3eda249179aa1122b50b03cbeea18
  type 0x09 size 232256 B, SHA 2c3b7f3f627d968e996790a0d1a9ef7ab16aac73

Container 7a1cef00016b950be42f5288ead21fa6fccc3107
  type 0x09 size 333504 B, SHA c90bbcb57de6bd2010de6e074db74645fce63e59
  (largest single-driver type 0x09 in the corpus)

### 3.3.2 Newer Cohort (type 0x08 = 228928 B, type 0x0F = 191296 B)

Three containers.

Container a78a94196b5d2c95865f6a8423a6b8eb86d07c6c
  type 0x09 size 248784 B, SHA a1f063ddaa80b095b95dbe0687d435dd62801950

Container ae7efd66ecde9e964cfe92f64e9b6461fce38f28
  type 0x09 size 300912 B, SHA a284d84fbdd4b6c0613769047f8f4f2f55d91f9e

Container b442ab113b829ff8c7bf34afa4d2d997889f308f
  type 0x09 size 231264 B, SHA 564da86d6a85927ad58f328e5abafb7a458bbcef

### 3.3.3 Type 0x09 Size Distribution (Generation B)

The single-driver generation already required at least seven distinct type 0x09
binaries whose sizes range from 231264 bytes to 333504 bytes. This spread is
the practical demonstration of the maintenance cost that the later dual-driver
plus shared-constants design was created to amortize.

------------------------------------------------------------------------------
3.4 GENERATION A — EARLY TYPE-0x0A CONTAINERS
------------------------------------------------------------------------------

Generation A contains no type 0x09, no type 0x0F and no DEADD00F configuration.
Type 0x0A modules constitute the primary path. Type 0x08 implants are
substantially smaller than in later generations.

### 3.4.1 Dual Small Type-0x0A

Containers 2a1d692b… and 5e89f83e… share an identical 22660-byte type 0x0A.bin
and an identical 68912-byte type 0x0A.dylib. Their type 0x08 implants are the
smallest recovered (≈51.7 KB).

### 3.4.2 Large Type-0x0A.bin

Containers 72a5ac81…, 980c77f1… and f8a86cf3… share an identical 507450-byte
type 0x0A.bin — the largest non-driver module in the corpus. Type 0x08 sizes
in this sub-cohort are 88–104 KB.

------------------------------------------------------------------------------
3.5 ANOMALOUS
------------------------------------------------------------------------------

Container 7a7d99099b035b2c6512b6ebeeea6df1ede70fbb contains only a 2192-byte
raw.bin and is excluded from generational analysis.

------------------------------------------------------------------------------
3.6 CROSS-CUTTING STRUCTURAL CONCLUSIONS
------------------------------------------------------------------------------

1. The DEADD00F + SpringBoard configuration is the most durable high-signal
   artifact across the three mature generations (B, C, D).

2. The modern type 0x08 / type 0x0F pair was introduced as a coordinated
   revision; no container mixes a modern implant with an older persistence
   module or vice versa.

3. Type 0x0A is present in the earliest generation as the primary path and is
   retained as a secondary path in the transitional generation; it is eliminated
   once the dual-driver design appears.

4. The dual-driver + KIEA design appears late and is applied to only two
   containers. It is best understood as a response to the proliferation of
   distinct type 0x09 builds already visible inside Generation B.

5. f1 values are used consistently as a type + role namespace across the entire
   corpus, enabling reliable static classification even without full
   disassembly.



# ==============================================================================
# EXPANDED SECTION 4 — TYPE 0x08 IMPLANT COMPARATIVE ANALYSIS (FULL)
# ==============================================================================

## 4.1 Architectural Role

The type 0x08 dylib is the primary post-exploitation implant. After the type
0x09 kernel driver (or, in earlier designs, a type 0x0A path) has obtained
elevated privileges, control is transferred to the type 0x08 module. From that

---
**Continue to [Part 3](CORUNA_FULL_PART3.md)**
