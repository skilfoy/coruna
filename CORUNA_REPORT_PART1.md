# Coruna Payload Container Evolution & Module Comparative Analysis

**Classification**: UNCLASSIFIED // RESEARCH  
**Date**: 2026-07-26  
**Authors**: Static analysis (original research)  
**Repository**: https://github.com/skilfoy/coruna  
**Scope**: Complete static inventory and comparative analysis of every payload container, the Type 0x08 implant family, and Type 0x0A modules  

**Methodological note**: All findings derived from repository tree, `payloads/manifest.json`, file sizes, SHA-1 identities, and previously established F00DBEEF / DEADD00F / KIEA structures. No dynamic execution performed.

---

## 1. Executive Summary & Key Judgments

- The Coruna corpus contains **20 distinct payload containers** (including one anomalous raw.bin entry).
- These containers form **four clear architectural generations**.
- The dual-driver + shared KIEA constants design appears in **only two** containers and represents a late, deliberate redesign rather than the historical baseline.
- The DEADD00F + SpringBoard type 0x07 configuration is present across the three mature generations and is the most durable high-signal static indicator.
- Type 0x08 (post-exploitation implant) exists in at least **five distinct size/SHA variants**, showing clear evolutionary stages.
- Type 0x0A modules are concentrated in the earliest generation and in a transitional hybrid generation; they largely disappear once the dual-driver design is introduced.

**Primary judgment**: The dual-driver architecture we previously reverse-engineered is a late-stage refinement optimized for maintainability of version-specific kernel offsets. Earlier containers relied on single type 0x09 drivers (or type 0x0A paths) with offsets presumably compiled in or handled differently.

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

This timeline is derived purely from static presence/absence and identity of the support-layer records.

---

## 3. Detailed Inventory of All Containers

### 3.1 Generation D — Dual-Driver Containers (Complete Entry Tables)

#### Container `377bed7460f7538f96bbad7bdc2b8294bdc54599`

**Generation**: D (Dual-Driver / Data-Driven)  
**Notes**: Dual-driver (data-driven). Primary subject of prior original research. Largest type 0x09 pair.

| Entry | Filename | f1 (dec) | f1 (hex) | Type | Size (bytes) | SHA-1 |
|-------|----------|----------|----------|------|--------------|-------|
| entry0 | `entry0_type0x08.dylib` | 524288 | 0x80000 | 0x08 | 228928 | `b81dd3e8d4c5d6699ae7aa4d96da9a50b79fda1a` |
| entry1 | `entry1_type0x09.dylib` | 589824 | 0x90000 | 0x09 | 333520 | `603f703de67c3ead9614c780224153e37e5fcd3b` |
| entry2 | `entry2_type0x0f.dylib` | 983040 | 0xF0000 | 0x0F | 191296 | `e8c656a78ace2f7c6f0f13f4364cd716efb5aa93` |
| entry3 | `entry3_type0x07.bin` | 458757 | 0x70005 | 0x07 | 44 | `ea2db48aec8c6215bee0cedc49f084832b5090f2` |
| entry4 | `entry4_type0x05.bin` | 327680 | 0x50000 | 0x05 | 24844 | `f41d90fda2ffe35c5bc332b7944b6f0243b92ed7` |
| entry5 | `entry5_type0x09.dylib` | 589825 | 0x90001 | 0x09 | 330304 | `aace95993995df8c01194f68d1203081c6b9a6bc` |
| entry6 | `entry6_type0x07.bin` | 458752 | 0x70000 | 0x07 | 468 | `629744abf54ff0cbbaf463fa4ff8100192eea933` |

**Structural observations**:
- Contains exactly two type 0x09 records (f1 0x90000 and 0x90001).
- Shares the identical KIEA type 0x05 blob (24844 bytes).
- Uses the modern type 0x08 (228928 B) and modern type 0x0F (191296 B).
- DEADD00F primary config is present and identical to all other mature containers.

#### Container `1334417664270db20af705f422878c53c8378203`

**Generation**: D (Dual-Driver / Data-Driven)  
**Notes**: Dual-driver (data-driven). Second confirmed instance of shared KIEA + dual type 0x09.

| Entry | Filename | f1 (dec) | f1 (hex) | Type | Size (bytes) | SHA-1 |
|-------|----------|----------|----------|------|--------------|-------|
| entry0 | `entry0_type0x08.dylib` | 524288 | 0x80000 | 0x08 | 228928 | `b81dd3e8d4c5d6699ae7aa4d96da9a50b79fda1a` |
| entry1 | `entry1_type0x09.dylib` | 589824 | 0x90000 | 0x09 | 284048 | `172b89e4fd8be280eb0d8ff6744941e995816c63` |
| entry2 | `entry2_type0x0f.dylib` | 983040 | 0xF0000 | 0x0F | 191296 | `e8c656a78ace2f7c6f0f13f4364cd716efb5aa93` |
| entry3 | `entry3_type0x07.bin` | 458757 | 0x70005 | 0x07 | 44 | `ea2db48aec8c6215bee0cedc49f084832b5090f2` |
| entry4 | `entry4_type0x05.bin` | 327680 | 0x50000 | 0x05 | 24844 | `f41d90fda2ffe35c5bc332b7944b6f0243b92ed7` |
| entry5 | `entry5_type0x09.dylib` | 589825 | 0x90001 | 0x09 | 263536 | `0cfd609835402e89cccee0a36b31bbd8087cd663` |
| entry6 | `entry6_type0x07.bin` | 458752 | 0x70000 | 0x07 | 468 | `60b91ea5178e92498b529a47182868c1244b024b` |

**Structural observations**:
- Contains exactly two type 0x09 records (f1 0x90000 and 0x90001).
- Shares the identical KIEA type 0x05 blob (24844 bytes).
- Uses the modern type 0x08 (228928 B) and modern type 0x0F (191296 B).
- DEADD00F primary config is present and identical to all other mature containers.

### 3.2 Generation C — Transitional Containers (Complete Entry Tables)

#### Container `1b2cbbde08f8b2330b7400abcb97c9573973e942`

**Generation**: C (Transitional — Type 0x09 + Type 0x0A)  
**Notes**: Transitional. Single type 0x09 + compact type 0x0A dylib. Modern implant/persistence pair.

| Entry | Filename | f1 (dec) | f1 (hex) | Type | Size (bytes) | SHA-1 |
|-------|----------|----------|----------|------|--------------|-------|
| entry0 | `entry0_type0x08.dylib` | 524288 | 0x80000 | 0x08 | 228928 | `b81dd3e8d4c5d6699ae7aa4d96da9a50b79fda1a` |
| entry1 | `entry1_type0x09.dylib` | 589824 | 0x90000 | 0x09 | 300912 | `a284d84fbdd4b6c0613769047f8f4f2f55d91f9e` |
| entry2 | `entry2_type0x0f.dylib` | 983040 | 0xF0000 | 0x0F | 191296 | `e8c656a78ace2f7c6f0f13f4364cd716efb5aa93` |
| entry3 | `entry3_type0x07.bin` | 458757 | 0x70005 | 0x07 | 44 | `ea2db48aec8c6215bee0cedc49f084832b5090f2` |
| entry4 | `entry4_type0x0a.dylib` | 655360 | 0xA0000 | 0x0A | 50344 | `f53bc3d1b239168e69a51ac67d86ca4c56aa1beb` |
| entry5 | `entry5_type0x07.bin` | 458752 | 0x70000 | 0x07 | 468 | `15f4077e0d802a2c3abc3e79ea96e8aeb2bec119` |

**Structural observations**:
- Single type 0x09 driver only (no dual-driver selection).
- Retains a compact type 0x0A dylib (50344 bytes, f1=0xA0000).
- No type 0x05 / KIEA record present.
- DEADD00F configuration is present.

#### Container `c8a14d79a27953242d60243ee2f505a85d9232cc`

**Generation**: C (Transitional — Type 0x09 + Type 0x0A)  
**Notes**: Transitional. Structurally near-identical module set to f4120dc6…

| Entry | Filename | f1 (dec) | f1 (hex) | Type | Size (bytes) | SHA-1 |
|-------|----------|----------|----------|------|--------------|-------|
| entry0 | `entry0_type0x08.dylib` | 524288 | 0x80000 | 0x08 | 228928 | `b81dd3e8d4c5d6699ae7aa4d96da9a50b79fda1a` |
| entry1 | `entry1_type0x09.dylib` | 589824 | 0x90000 | 0x09 | 284048 | `172b89e4fd8be280eb0d8ff6744941e995816c63` |
| entry2 | `entry2_type0x0f.dylib` | 983040 | 0xF0000 | 0x0F | 191296 | `e8c656a78ace2f7c6f0f13f4364cd716efb5aa93` |
| entry3 | `entry3_type0x07.bin` | 458757 | 0x70005 | 0x07 | 44 | `ea2db48aec8c6215bee0cedc49f084832b5090f2` |
| entry4 | `entry4_type0x0a.dylib` | 655360 | 0xA0000 | 0x0A | 50344 | `f53bc3d1b239168e69a51ac67d86ca4c56aa1beb` |
| entry5 | `entry5_type0x07.bin` | 458752 | 0x70000 | 0x07 | 468 | `60b91ea5178e92498b529a47182868c1244b024b` |

#### Container `e9f898587620186e31119fbf32660f26c1e048e0`

**Generation**: C (Transitional — Type 0x09 + Type 0x0A)  
**Notes**: Transitional. Uses older type 0x08/0x0F pair while still carrying type 0x0A.

| Entry | Filename | f1 (dec) | f1 (hex) | Type | Size (bytes) | SHA-1 |
|-------|----------|----------|----------|------|--------------|-------|
| entry0 | `entry0_type0x08.dylib` | 524288 | 0x80000 | 0x08 | 196864 | `5f677b5185e0c919ba2e08901b44b5715b5e15f1` |
| entry1 | `entry1_type0x09.dylib` | 589824 | 0x90000 | 0x09 | 284048 | `fa7f7a9e84299b654d9eb5f54d09ead4c5a696c3` |
| entry2 | `entry2_type0x0f.dylib` | 983040 | 0xF0000 | 0x0F | 192096 | `b886ab5c501d2b2cc476fc48d0fcab9b2e20328b` |
| entry3 | `entry3_type0x07.bin` | 458757 | 0x70005 | 0x07 | 44 | `ea2db48aec8c6215bee0cedc49f084832b5090f2` |
| entry4 | `entry4_type0x0a.dylib` | 655360 | 0xA0000 | 0x0A | 50344 | `5fa390b9e291824fde40cdd76ac85b67ccb8ee0f` |
| entry5 | `entry5_type0x07.bin` | 458752 | 0x70000 | 0x07 | 468 | `60b91ea5178e92498b529a47182868c1244b024b` |

#### Container `f4120dc6717a489435d86943472c5a2444aac8e6`

**Generation**: C (Transitional — Type 0x09 + Type 0x0A)  
**Notes**: Transitional. Module set matches c8a14d79… closely.

| Entry | Filename | f1 (dec) | f1 (hex) | Type | Size (bytes) | SHA-1 |
|-------|----------|----------|----------|------|--------------|-------|
| entry0 | `entry0_type0x08.dylib` | 524288 | 0x80000 | 0x08 | 228928 | `b81dd3e8d4c5d6699ae7aa4d96da9a50b79fda1a` |
| entry1 | `entry1_type0x09.dylib` | 589824 | 0x90000 | 0x09 | 284048 | `172b89e4fd8be280eb0d8ff6744941e995816c63` |
| entry2 | `entry2_type0x0f.dylib` | 983040 | 0xF0000 | 0x0F | 191296 | `e8c656a78ace2f7c6f0f13f4364cd716efb5aa93` |
| entry3 | `entry3_type0x07.bin` | 458757 | 0x70005 | 0x07 | 44 | `ea2db48aec8c6215bee0cedc49f084832b5090f2` |
| entry4 | `entry4_type0x0a.dylib` | 655360 | 0xA0000 | 0x0A | 50344 | `f53bc3d1b239168e69a51ac67d86ca4c56aa1beb` |
| entry5 | `entry5_type0x07.bin` | 458752 | 0x70000 | 0x07 | 468 | `60b91ea5178e92498b529a47182868c1244b024b` |

**End of Part 1** — Continue to [Part 2](CORUNA_REPORT_PART2.md)
