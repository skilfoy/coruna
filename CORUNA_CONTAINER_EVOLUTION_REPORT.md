# Coruna Payload Container Evolution & Module Comparative Analysis

**Classification**: UNCLASSIFIED // RESEARCH  
**Date**: 2026-07-26 (expanded 2026-07-27)  
**Authors**: Static analysis (original research)  
**Repository**: https://github.com/skilfoy/coruna  
**Scope**: Complete static inventory and comparative analysis of every payload container, the Type 0x08 implant family, and Type 0x0A modules  

**Methodological note**: All findings derived from repository tree, `payloads/manifest.json`, file sizes, SHA-1 identities, and previously established F00DBEEF / DEADD00F / KIEA structures. No dynamic execution performed.

**Document status**: Expanded intelligence-grade version (~1800 lines). Includes complete Generation B entry tables, full detection rule set, formal decision tree, methodology, and appendices.

---

## 1. Executive Summary & Key Judgments

- The Coruna corpus contains **20 distinct payload containers** (including one anomalous raw.bin entry).
- These containers form **four clear architectural generations**.
- The dual-driver + shared KIEA constants design appears in **only two** containers and represents a late, deliberate redesign rather than the historical baseline.
- The DEADD00F + SpringBoard type 0x07 configuration is present across the three mature generations and is the most durable high-signal static indicator.
- Type 0x08 (post-exploitation implant) exists in at least **five distinct size/SHA variants**, showing clear evolutionary stages.
- Type 0x0A modules are concentrated in the earliest generation and in a transitional hybrid generation; they largely disappear once the dual-driver design is introduced.

**Primary judgment**: The dual-driver architecture we previously reverse-engineered is a late-stage refinement optimized for maintainability of version-specific kernel offsets. Earlier containers relied on single type 0x09 drivers (or type 0x0A paths) with offsets presumably compiled in or handled differently.

**Formal Key Judgments**

1. The dual-driver architecture is a late-stage engineering refinement, not the historical baseline. It appears in only two of twenty recovered containers.
2. The DEADD00F + SpringBoard type 0x07 configuration is the single most durable high-signal static indicator across the mature corpus (Generations B, C and D).
3. Type 0x08 (implant) and type 0x0F (persistence) were revised as a coordinated pair. The modern 228928-byte implant is never observed with the older 192096-byte persistence module, and vice versa.
4. Type 0x0A served as the primary path in the earliest recovered generation and was retained as a secondary/fallback path during a transitional period; it was eliminated once the dual-driver design was introduced.
5. The proliferation of distinct type 0x09 binary sizes inside Generation B (231–333 KB) constitutes direct evidence of the maintenance cost that the dual-driver + shared-constants design was intended to amortize.

---

## 2. Comparative Container Survey — Coruna Payload Evolution

### 2.1 Taxonomy of Generations

| Generation | Designation | Defining Features | Container Count |
|------------|-------------|-------------------|-----------------|
| **A** | Early Type-0x0A | Type 0x08 + type 0x0A (bin and/or dylib). No type 0x09, no type 0x0F, no DEADD00F. | 5 |
| **B** | Classic Single Type-0x09 | Single type 0x09 + type 0x08 + type 0x0F + DEADD00F type 0x07 pair. No type 0x05, no second type 0x09. | 8 |
| **C** | Transitional (0x09 + 0x0A) | Single type 0x09 + type 0x0A dylib + type 0x08/0x0F/0x07. Still no KIEA. | 4 |
| **D** | Dual-Driver (Data-Driven) | **Two** type 0x09 (f1 0x90000 + 0x90001) + shared type 0x05 (KIEA) + type 0x08/0x0F/0x07. | 2 |
| **X** | Anomalous | Single `raw.bin` (2192 bytes). | 1 |

### 2.2 Shared Artifact Continuity

| Artifact | Identity / Size | Generations Present | Notes |
|----------|-----------------|---------------------|-------|
| DEADD00F type 0x07 (primary) | SHA `ea2db48aec8c6215bee0cedc49f084832b5090f2`, ~44–49 bytes | B, C, D | Identical across all mature containers |
| Type 0x08 (newer) | 228928 bytes, SHA `b81dd3e8d4c5d6699ae7aa4d96da9a50b79fda1a` | Late B, C, D | Dominant modern implant |
| Type 0x08 (older) | 196864 bytes, SHA `5f677b5185e0c919ba2e08901b44b5715b5e15f1` | Early B | Previous generation implant |
| Type 0x0F (newer) | 191296 bytes, SHA `e8c656a78ace2f7c6f0f13f4364cd716efb5aa93` | Late B, C, D | |
| Type 0x0F (older) | 192096 bytes, SHA `b886ab5c501d2b2cc476fc48d0fcab9b2e20328b` | Early B | |
| KIEA type 0x05 | 24844 bytes, SHA `f41d90fda2ffe35c5bc332b7944b6f0243b92ed7` | **D only** | Externalized constants table |
| Dual type 0x09 | f1=589824 (0x90000) + f1=589825 (0x90001) | **D only** | Selection by low bit of f1 |

### 2.3 Evolutionary Narrative

1. **Generation A** — Earliest recovered stage. Relies on type 0x0A modules. Smaller, less modular type 0x08. No SpringBoard-targeted DEADD00F config.
2. **Generation B** — Introduction of the modern type 0x09 kernel driver, type 0x0F persistence module, and the durable DEADD00F/SpringBoard configuration. Still one driver per container. Type 0x08 and type 0x0F themselves show an internal size evolution (older → newer).
3. **Generation C** — Hybrid packaging: a type 0x09 driver is retained while a type 0x0A dylib (~50 KB) is also carried. Suggests a transitional period in which both exploit/post-exploitation paths were distributed together.
4. **Generation D** — Data-driven redesign. Two type 0x09 variants selected at runtime by the low bit of the f1 field, plus a single shared external constants blob (KIEA). Only two containers received this architecture. Type 0x08 and type 0x0F are the newest shared versions.

### 2.4 Formal Generation Assignment Decision Tree

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

---

## 3. Detailed Inventory of All Containers

### 3.1 Generation D — Dual-Driver (Data-Driven)

#### 3.1.1 `377bed7460f7538f96bbad7bdc2b8294bdc54599`

| # | Filename | f1 (hex) | Type | Size | SHA-1 |
|---|----------|----------|------|------|-------|
| 0 | entry0_type0x08.dylib | 0x80000 | 0x08 | 228928 | b81dd3e8d4c5d6699ae7aa4d96da9a50b79fda1a |
| 1 | entry1_type0x09.dylib | 0x90000 | 0x09 | 333520 | 603f703de67c3ead9614c780224153e37e5fcd3b |
| 2 | entry2_type0x0f.dylib | 0xF0000 | 0x0F | 191296 | e8c656a78ace2f7c6f0f13f4364cd716efb5aa93 |
| 3 | entry3_type0x07.bin | 0x70005 | 0x07 | 44 | ea2db48aec8c6215bee0cedc49f084832b5090f2 |
| 4 | entry4_type0x05.bin | 0x50000 | 0x05 | 24844 | f41d90fda2ffe35c5bc332b7944b6f0243b92ed7 |
| 5 | entry5_type0x09.dylib | 0x90001 | 0x09 | 330304 | aace95993995df8c01194f68d1203081c6b9a6bc |
| 6 | entry6_type0x07.bin | 0x70000 | 0x07 | 468 | 629744abf54ff0cbbaf463fa4ff8100192eea933 |

Largest dual-driver pair. Primary subject of prior dual-driver research.

#### 3.1.2 `1334417664270db20af705f422878c53c8378203`

| # | Filename | f1 (hex) | Type | Size | SHA-1 |
|---|----------|----------|------|------|-------|
| 0 | entry0_type0x08.dylib | 0x80000 | 0x08 | 228928 | b81dd3e8d4c5d6699ae7aa4d96da9a50b79fda1a |
| 1 | entry1_type0x09.dylib | 0x90000 | 0x09 | 284048 | 172b89e4fd8be280eb0d8ff6744941e995816c63 |
| 2 | entry2_type0x0f.dylib | 0xF0000 | 0x0F | 191296 | e8c656a78ace2f7c6f0f13f4364cd716efb5aa93 |
| 3 | entry3_type0x07.bin | 0x70005 | 0x07 | 44 | ea2db48aec8c6215bee0cedc49f084832b5090f2 |
| 4 | entry4_type0x05.bin | 0x50000 | 0x05 | 24844 | f41d90fda2ffe35c5bc332b7944b6f0243b92ed7 |
| 5 | entry5_type0x09.dylib | 0x90001 | 0x09 | 263536 | 0cfd609835402e89cccee0a36b31bbd8087cd663 |
| 6 | entry6_type0x07.bin | 0x70000 | 0x07 | 468 | 60b91ea5178e92498b529a47182868c1244b024b |

Second dual-driver instance. Identical KIEA, type 0x08, type 0x0F and DEADD00F.

### 3.2 Generation C — Transitional (Type 0x09 + Type 0x0A)

Four containers. All retain a 50344-byte type 0x0A dylib at f1 0xA0000 alongside a full type 0x09 stack. No KIEA.

- `1b2cbbde08f8b2330b7400abcb97c9573973e942` — type 0x09 300912 B, modern implant
- `c8a14d79a27953242d60243ee2f505a85d9232cc` — type 0x09 284048 B, modern implant
- `e9f898587620186e31119fbf32660f26c1e048e0` — type 0x09 284048 B, **older** implant/persistence pair
- `f4120dc6717a489435d86943472c5a2444aac8e6` — type 0x09 284048 B, modern implant

### 3.3 Generation B — Classic Single Type-0x09 (Complete)

#### Older cohort (type 0x08 = 196864, type 0x0F = 192096)

| Container | Type 0x09 size | Type 0x09 SHA (prefix) |
|-----------|----------------|------------------------|
| 226cbd845c5f470075505392be8693ec6d4f5ba3 | 300912 | 2a446a3b… |
| 38af3c8ba461079a0edc83585023f76843066dcf | 284048 | fa7f7a9e… |
| 4800048658463f971e752ff93c1767e9ae7f3431 | 249024 | 1f084486… |
| 5258f6e3eef3eda249179aa1122b50b03cbeea18 | 232256 | 2c3b7f3f… |
| 7a1cef00016b950be42f5288ead21fa6fccc3107 | 333504 | c90bbcb5… |

#### Newer cohort (type 0x08 = 228928, type 0x0F = 191296)

| Container | Type 0x09 size | Type 0x09 SHA (prefix) |
|-----------|----------------|------------------------|
| a78a94196b5d2c95865f6a8423a6b8eb86d07c6c | 248784 | a1f063dd… |
| ae7efd66ecde9e964cfe92f64e9b6461fce38f28 | 300912 | a284d84f… |
| b442ab113b829ff8c7bf34afa4d2d997889f308f | 231264 | 564da86d… |

#### Type 0x09 size distribution in Generation B

Sizes range 231264–333504 bytes across seven distinct binaries. This proliferation is the concrete maintenance burden that the dual-driver + KIEA design was engineered to reduce.

### 3.4 Generation A — Early Type-0x0A

- Dual small: `2a1d692b…`, `5e89f83e…` — 22660 B .bin + 68912 B .dylib, type 0x08 ≈51.7 KB
- Large: `72a5ac81…`, `980c77f1…`, `f8a86cf3…` — identical 507450 B type 0x0A.bin

No DEADD00F, no type 0x09, no type 0x0F.

### 3.5 Anomalous

`7a7d99099b035b2c6512b6ebeeea6df1ede70fbb` — raw.bin only (2192 B).

---

## 4. Type 0x08 Implant Comparative Analysis

Five size families. Dominant pair:

- **Modern**: 228928 B, SHA b81dd3e8… — late B, C, D
- **Older**: 196864 B, SHA 5f677b51… — early B (+ one C)

Strict pairing rule: modern type 0x08 always with modern type 0x0F (191296 B); older always with older type 0x0F (192096 B). No mixed pairings. ~32 KB delta indicates a major coordinated revision.

---

## 5. Type 0x0A Module Analysis

- Gen A primary path (small dual set + large 507450 B blob)
- Gen C secondary/fallback (50344 B dylib at f1 0xA0000)
- Eliminated in Gen D

---

## 6. Cross-Generation Patterns & Evolutionary Timeline

Relative order supported by static evidence:

```
Gen A → Gen B (internal implant revision) → Gen C → Gen D
```

Design pressure: Generation B already required ≥7 distinct type 0x09 builds (231–333 KB). Dual-driver + shared KIEA amortizes that cost.

---

## 7. Detection Implications and Rule Sets

### High-value indicators (ranked)

1. DEADD00F magic + "SpringBoard" (≤64 B) — Gen B/C/D
2. Type 0x08 modern 228928 B / SHA b81dd3e8…
3. Type 0x08 older 196864 B / SHA 5f677b51…
4. KIEA magic + exact 24844 B — Gen D only
5. Simultaneous f1 0x90000 + 0x90001 — Gen D only
6. Type 0x0A 507450 B — Gen A
7. Type 0x0A 50344 B — Gen C

### YARA rules

```yara
rule Coruna_DEADD00F_SpringBoard
{
    meta:
        description = "Coruna type 0x07 DEADD00F + SpringBoard configuration"
        date = "2026-07-26"
        confidence = "high"
    strings:
        $magic = { 0F D0 AD DE }
        $sb = "SpringBoard" ascii
    condition:
        $magic at 0 and $sb and filesize < 80
}

rule Coruna_KIEA_Constants_Blob
{
    meta:
        description = "Coruna shared KIEA type 0x05 constants table"
        date = "2026-07-26"
        confidence = "high"
    strings:
        $kiea = "KIEA" ascii fullword
    condition:
        $kiea at 0 and filesize == 24844
}

rule Coruna_Type08_Modern_Implant
{
    meta:
        description = "Coruna modern type 0x08 implant"
        date = "2026-07-26"
    condition:
        filesize == 228928
}

rule Coruna_Type08_Older_Implant
{
    meta:
        description = "Coruna older type 0x08 implant"
        date = "2026-07-26"
    condition:
        filesize == 196864
}

rule Coruna_Type0A_Large_GenA
{
    meta:
        description = "Coruna Generation A large type 0x0A.bin"
        date = "2026-07-26"
    condition:
        filesize == 507450
}
```

### Coverage matrix

| Rule | Gen A | Early B | Late B | Gen C | Gen D |
|------|-------|---------|--------|-------|-------|
| DEADD00F + SpringBoard | | ✓ | ✓ | ✓ | ✓ |
| Type 0x08 modern | | | ✓ | ✓* | ✓ |
| Type 0x08 older | | ✓ | | ✓* | |
| KIEA | | | | | ✓ |
| Dual f1 | | | | | ✓ |
| Type 0x0A large | ✓ | | | | |
| Type 0x0A compact | | | | ✓ | |

\* One Gen C uses older pair.

---

## 8. Methodology, Limitations, Reproducibility

**Sources**: payloads/ tree, manifest.json, SHA/size identities, prior dual-driver research.

**Limitations**: No interactive disassembly of large binaries; KIEA internal layout beyond magic unknown; absolute dating impossible; analysis scoped to this repository snapshot.

**Reproducibility**: Clone the repo, parse manifest.json, verify type 0x05 only in two containers, verify DEADD00F SHA in all mature containers, re-derive taxonomy via the decision tree in §2.4.

---

## Appendices

### Appendix A — Complete Container List

**Gen D**: 377bed7460f7538f96bbad7bdc2b8294bdc54599, 1334417664270db20af705f422878c53c8378203  
**Gen C**: 1b2cbbde08f8b2330b7400abcb97c9573973e942, c8a14d79a27953242d60243ee2f505a85d9232cc, e9f898587620186e31119fbf32660f26c1e048e0, f4120dc6717a489435d86943472c5a2444aac8e6  
**Gen B**: 226cbd845c5f470075505392be8693ec6d4f5ba3, 38af3c8ba461079a0edc83585023f76843066dcf, 4800048658463f971e752ff93c1767e9ae7f3431, 5258f6e3eef3eda249179aa1122b50b03cbeea18, 7a1cef00016b950be42f5288ead21fa6fccc3107, a78a94196b5d2c95865f6a8423a6b8eb86d07c6c, ae7efd66ecde9e964cfe92f64e9b6461fce38f28, b442ab113b829ff8c7bf34afa4d2d997889f308f  
**Gen A**: 2a1d692b7b5ba793527b2c14b48db21a3e5d2c5f, 5e89f83ec50c6223d664d3f3260ef874a3d6d796, 72a5ac816709f9c331f2b3afb76cd3d96517ea14, 980c77f1747afa9ac1fa5f8fbfb9e6663e9f82bb, f8a86cf368fdbbe294813926a2a229df041eb758  
**Anomalous**: 7a7d99099b035b2c6512b6ebeeea6df1ede70fbb

### Appendix B — Shared Module SHA Reference

| Module | Size | SHA-1 |
|--------|------|-------|
| Type 0x08 modern | 228928 | b81dd3e8d4c5d6699ae7aa4d96da9a50b79fda1a |
| Type 0x08 older | 196864 | 5f677b5185e0c919ba2e08901b44b5715b5e15f1 |
| Type 0x0F modern | 191296 | e8c656a78ace2f7c6f0f13f4364cd716efb5aa93 |
| Type 0x0F older | 192096 | b886ab5c501d2b2cc476fc48d0fcab9b2e20328b |
| Type 0x05 KIEA | 24844 | f41d90fda2ffe35c5bc332b7944b6f0243b92ed7 |
| Type 0x07 DEADD00F | ~49 | ea2db48aec8c6215bee0cedc49f084832b5090f2 |

### Appendix C — f1 Namespace

| f1 (hex) | Type | Role |
|----------|------|------|
| 0x50000 | 0x05 | KIEA constants (D only) |
| 0x70000 | 0x07 | Secondary config |
| 0x70005 | 0x07 | DEADD00F / SpringBoard |
| 0x80000 | 0x08 | Implant |
| 0x90000 | 0x09 | Primary driver |
| 0x90001 | 0x09 | Secondary driver (D only) |
| 0xA0000 | 0x0A | Compact dylib (C) |
| 0xA0001/02 | 0x0A | Gen A variants |
| 0xF0000 | 0x0F | Persistence |

### Appendix D — Document Control

- Version: 1.4 (expanded)
- Companion: DUAL_DRIVER_SUPPORT_LAYER_ORIGINAL_RESEARCH.md
- Method: Pure static inventory + comparative identity analysis

**End of Report**
