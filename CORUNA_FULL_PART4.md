# CORUNA CONTAINER EVOLUTION REPORT — COMPLETE LOCAL WORKING COPY
## Part 4 of 5 (lines 1081–1440 of 1797)

**This is the uncondensed full local analysis. No content removed.**

[Index](CORUNA_CONTAINER_EVOLUTION_REPORT.md) | [Part 1](CORUNA_FULL_PART1.md) | [Part 2](CORUNA_FULL_PART2.md) | [Part 3](CORUNA_FULL_PART3.md) | [Part 4](CORUNA_FULL_PART4.md) | [Part 5](CORUNA_FULL_PART5.md)

---

**Judgment 4**  
Type 0x0A served as the primary path in the earliest recovered generation and was retained as a secondary/fallback path during a transitional period; it was eliminated once the dual-driver design was introduced.

**Judgment 5**  
The proliferation of distinct type 0x09 binary sizes inside Generation B (231–333 KB) constitutes direct evidence of the maintenance cost that the dual-driver + shared-constants design was intended to amortize.

## 12. Recommendations for Further Static Work

1. Interactive Mach-O analysis of the modern versus older type 0x08 implants to identify the concrete contents of the 32 KB delta.
2. Extraction of the first several hundred bytes of the KIEA blob followed by correlation against known XNU structure layouts for iOS 17.0–17.2.1.
3. Comparative string and import analysis of the 507450-byte Generation A type 0x0A.bin against the 50344-byte Generation C type 0x0A dylib.
4. Full export-trie and load-command inspection of bootstrap.dylib to confirm the precise selection and constants-passing logic that activates only when both 0x90000 and 0x90001 records are present.

## 13. Document Control and Continuity

- This report is the second major original-research publication derived from the skilfoy/coruna corpus.
- Companion document: DUAL_DRIVER_SUPPORT_LAYER_ORIGINAL_RESEARCH.md (focused exclusively on the Generation D design).
- The present document supplies the evolutionary context that situates the dual-driver design as a late refinement.
- All hashes, sizes and structural claims are reproducible against the public repository.

**End of expanded analytical sections.**

# ==============================================================================
# PRIORITY 1 COMPLETION — FULL GENERATION B TECHNICAL INVENTORY
# ==============================================================================

This block replaces the previous summary-style treatment of Generation B with
complete per-container entry tables and expanded structural analysis. Generation
B is the largest cohort in the corpus and the generation in which the
proliferation of distinct type 0x09 builds is most clearly visible.

------------------------------------------------------------------------------
3.3 GENERATION B — CLASSIC SINGLE TYPE-0x09 (COMPLETE)
------------------------------------------------------------------------------

Generation B is defined by the following invariant structure:

  - Exactly one type 0x09 record (f1 = 0x90000)
  - One type 0x08 implant
  - One type 0x0F persistence module
  - DEADD00F primary type 0x07 configuration (f1 = 0x70005)
  - Secondary type 0x07 configuration (f1 = 0x70000)
  - No type 0x05 (KIEA)
  - No second type 0x09
  - No type 0x0A

Within this invariant structure two sub-cohorts exist, distinguished solely by
which coordinated implant/persistence pair is present.

### 3.3.1 Older Implant/Persistence Cohort

All five containers below use:

  type 0x08 = 196864 bytes (SHA 5f677b5185e0c919ba2e08901b44b5715b5e15f1)
  type 0x0F = 192096 bytes (SHA b886ab5c501d2b2cc476fc48d0fcab9b2e20328b)

#### Container 226cbd845c5f470075505392be8693ec6d4f5ba3

| # | Filename | f1 (hex) | Type | Size | SHA-1 / Notes |
|---|--------------------------|----------|------|--------|----------------------------------------|
| 0 | entry0_type0x08.dylib | 0x80000 | 0x08 | 196864 | 5f677b51… (older shared implant) |
| 1 | entry1_type0x09.dylib | 0x90000 | 0x09 | 300912 | 2a446a3b89acca0f1baaf01b7bc69e83242615cb |
| 2 | entry2_type0x0f.dylib | 0xF0000 | 0x0F | 192096 | b886ab5c… (older shared persistence) |
| 3 | entry3_type0x07.bin | 0x70005 | 0x07 | 44 | ea2db48a… (DEADD00F, universal) |
| 4 | entry4_type0x07.bin | 0x70000 | 0x07 | 468 | secondary config |

#### Container 38af3c8ba461079a0edc83585023f76843066dcf

| # | Filename | f1 (hex) | Type | Size | SHA-1 / Notes |
|---|--------------------------|----------|------|--------|----------------------------------------|
| 0 | entry0_type0x08.dylib | 0x80000 | 0x08 | 196864 | 5f677b51… |
| 1 | entry1_type0x09.dylib | 0x90000 | 0x09 | 284048 | fa7f7a9e84299b654d9eb5f54d09ead4c5a696c3 |
| 2 | entry2_type0x0f.dylib | 0xF0000 | 0x0F | 192096 | b886ab5c… |
| 3 | entry3_type0x07.bin | 0x70005 | 0x07 | 44 | ea2db48a… |
| 4 | entry4_type0x07.bin | 0x70000 | 0x07 | 468 | secondary config |

#### Container 4800048658463f971e752ff93c1767e9ae7f3431

| # | Filename | f1 (hex) | Type | Size | SHA-1 / Notes |
|---|--------------------------|----------|------|--------|----------------------------------------|
| 0 | entry0_type0x08.dylib | 0x80000 | 0x08 | 196864 | 5f677b51… |
| 1 | entry1_type0x09.dylib | 0x90000 | 0x09 | 249024 | 1f084486add0b36a9c28d7862003748f6214fa52 |
| 2 | entry2_type0x0f.dylib | 0xF0000 | 0x0F | 192096 | b886ab5c… |
| 3 | entry3_type0x07.bin | 0x70005 | 0x07 | 44 | ea2db48a… |
| 4 | entry4_type0x07.bin | 0x70000 | 0x07 | 468 | secondary config |

#### Container 5258f6e3eef3eda249179aa1122b50b03cbeea18

| # | Filename | f1 (hex) | Type | Size | SHA-1 / Notes |
|---|--------------------------|----------|------|--------|----------------------------------------|
| 0 | entry0_type0x08.dylib | 0x80000 | 0x08 | 196864 | 5f677b51… |
| 1 | entry1_type0x09.dylib | 0x90000 | 0x09 | 232256 | 2c3b7f3f627d968e996790a0d1a9ef7ab16aac73 |
| 2 | entry2_type0x0f.dylib | 0xF0000 | 0x0F | 192096 | b886ab5c… |
| 3 | entry3_type0x07.bin | 0x70005 | 0x07 | 44 | ea2db48a… |
| 4 | entry4_type0x07.bin | 0x70000 | 0x07 | 468 | secondary config |

#### Container 7a1cef00016b950be42f5288ead21fa6fccc3107

| # | Filename | f1 (hex) | Type | Size | SHA-1 / Notes |
|---|--------------------------|----------|------|--------|----------------------------------------|
| 0 | entry0_type0x08.dylib | 0x80000 | 0x08 | 196864 | 5f677b51… |
| 1 | entry1_type0x09.dylib | 0x90000 | 0x09 | 333504 | c90bbcb57de6bd2010de6e074db74645fce63e59 |
| 2 | entry2_type0x0f.dylib | 0xF0000 | 0x0F | 192096 | b886ab5c… |
| 3 | entry3_type0x07.bin | 0x70005 | 0x07 | 44 | ea2db48a… |
| 4 | entry4_type0x07.bin | 0x70000 | 0x07 | 468 | secondary config |

Largest single-driver type 0x09 (333504 B). Only 16 bytes smaller than largest dual-driver primary (333520).

### 3.3.2 Newer Implant/Persistence Cohort

All three use type 0x08 = 228928 B (SHA b81dd3e8…) and type 0x0F = 191296 B (SHA e8c656a7…).

#### Container a78a94196b5d2c95865f6a8423a6b8eb86d07c6c — type 0x09 248784 B (SHA a1f063dd…)
#### Container ae7efd66ecde9e964cfe92f64e9b6461fce38f28 — type 0x09 300912 B (SHA a284d84f…)
#### Container b442ab113b829ff8c7bf34afa4d2d997889f308f — type 0x09 231264 B (SHA 564da86d…)

### 3.3.3 Generation B Type 0x09 Size Clustering Analysis

| Size (bytes) | Count | Cohort(s) | Notes |
|--------------|-------|-----------|-------|
| 333504 | 1 | Older | Largest single-driver; near dual-driver max |
| 300912 | 2 | Older + Newer | Most reused size across cohorts |
| 284048 | 1 | Older | Also appears in Gen C and Gen D primary |
| 249024 | 1 | Older | Unique |
| 248784 | 1 | Newer | Unique |
| 232256 | 1 | Older | Unique |
| 231264 | 1 | Newer | Smallest mature type 0x09 |

Key observations: ≥7 distinct driver builds inside one generation; size range ~100 KB; size 300912 crosses implant boundary; largest single-driver only 16 bytes smaller than largest dual-driver primary.

### 3.3.5 Generation B Summary Judgment

Generation B demonstrates that the classic single-driver architecture already required a non-trivial number of distinct type 0x09 builds to achieve version coverage. The later dual-driver selectable pair plus shared external constants is a direct response to that maintenance cost.

# ==============================================================================
# PRIORITY 5 — FULL DETECTION SECTION (EXPANDED)
# ==============================================================================

## 7. Detection Implications and Rule Sets (Complete)

### 7.1 Indicator Ranking

| Rank | Indicator | Coverage | Uniqueness | Ease of Match |
|------|-----------|----------|------------|---------------|
| 1 | DEADD00F magic + "SpringBoard" (≤64 B) | Gen B, C, D | Extremely high | Trivial |
| 2 | Type 0x08 modern SHA / exact 228928 B | Late B, C, D | Extremely high | Trivial |
| 3 | Type 0x08 older SHA / exact 196864 B | Early B (+1 C) | Extremely high | Trivial |
| 4 | KIEA magic at offset 0 + exact 24844 B | Gen D only | Extremely high | Trivial |
| 5 | Simultaneous f1 0x90000 + 0x90001 | Gen D only | Extremely high | Requires container parse |
| 6 | Type 0x0F modern / older size+SHA pairs | Paired with 2/3 | High | Trivial |
| 7 | Type 0x0A 507450 B blob | Gen A (3) | High | Trivial |
| 8 | Type 0x0A 50344 B dylib (f1 0xA0000) | Gen C | Medium-High | Easy |
| 9 | Secondary type 0x07 468 B variants | All mature | Low-Medium | Easy but noisy |

### 7.2 Primary YARA Rules

```yara
rule Coruna_DEADD00F_SpringBoard
{
    meta:
        description = "Coruna type 0x07 DEADD00F + SpringBoard configuration"
        author = "original research"
        date = "2026-07-26"
        confidence = "high"
        coverage = "Generations B, C, D"
    strings:
        $magic = { 0F D0 AD DE }
        $sb1 = "SpringBoard" ascii
        $sb2 = "SpringBoard" wide
    condition:
        $magic at 0 and any of ($sb*) and filesize < 80
}

rule Coruna_KIEA_Constants_Blob
{
    meta:
        description = "Coruna shared KIEA type 0x05 constants table"
        author = "original research"
        date = "2026-07-26"
        confidence = "high"
        coverage = "Generation D only"
    strings:
        $kiea = "KIEA" ascii fullword
    condition:
        $kiea at 0 and filesize == 24844
}

rule Coruna_Type08_Modern_Implant
{
    meta:
        description = "Coruna modern type 0x08 post-exploitation implant"
        author = "original research"
        date = "2026-07-26"
        confidence = "high"
        coverage = "Late Gen B, Gen C, Gen D"
    condition:
        filesize == 228928
}

rule Coruna_Type08_Older_Implant
{
    meta:
        description = "Coruna older type 0x08 post-exploitation implant"
        author = "original research"
        date = "2026-07-26"
        confidence = "high"
        coverage = "Early Gen B (+ one Gen C)"
    condition:
        filesize == 196864
}

rule Coruna_Type0A_Large_GenA
{
    meta:
        description = "Coruna Generation A large type 0x0A.bin"
        author = "original research"
        date = "2026-07-26"
        confidence = "high"
        coverage = "Generation A (three containers)"
    condition:
        filesize == 507450
}

rule Coruna_Type0A_Compact_GenC
{
    meta:
        description = "Coruna Generation C compact type 0x0A dylib"
        author = "original research"
        date = "2026-07-26"
        confidence = "medium-high"
        coverage = "Generation C"
    condition:
        filesize == 50344
}
```

### 7.3 Hash-Based Detection Lists

**Type 0x08 Implants**
- Modern: b81dd3e8d4c5d6699ae7aa4d96da9a50b79fda1a (228928 B)
- Older: 5f677b5185e0c919ba2e08901b44b5715b5e15f1 (196864 B)

**Type 0x0F Persistence**
- Modern: e8c656a78ace2f7c6f0f13f4364cd716efb5aa93 (191296 B)
- Older: b886ab5c501d2b2cc476fc48d0fcab9b2e20328b (192096 B)

**KIEA Constants**
- f41d90fda2ffe35c5bc332b7944b6f0243b92ed7 (24844 B)

**DEADD00F Primary Config**
- ea2db48aec8c6215bee0cedc49f084832b5090f2 (~44–49 B)

**Type 0x0A Large (Gen A)**
- 907e8d190d7c7bd2701f632cb202c3cde39303f1 (507450 B)

---
**Continue to [Part 5](CORUNA_FULL_PART5.md)**
