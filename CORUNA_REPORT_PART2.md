# CORUNA CONTAINER EVOLUTION REPORT — PART 2

**Continuation of the full intelligence-grade report.**  
See [index](CORUNA_CONTAINER_EVOLUTION_REPORT.md) for navigation.

---

## Expanded Section 3 Continuation + Type 0x08 / Type 0x0A Analysis

### Generation B Summary (from full inventory)

Generation B is the largest cohort. All containers share:
- Exactly one type 0x09 (f1 0x90000)
- One type 0x08 implant
- One type 0x0F persistence module
- DEADD00F primary + secondary type 0x07
- No type 0x05, no dual type 0x09, no type 0x0A

**Older cohort** (type 0x08 = 196864 B, type 0x0F = 192096 B):
- 226cbd84… — type 0x09 300912 B
- 38af3c8b… — type 0x09 284048 B
- 48000486… — type 0x09 249024 B
- 5258f6e3… — type 0x09 232256 B
- 7a1cef00… — type 0x09 333504 B (largest single-driver)

**Newer cohort** (type 0x08 = 228928 B, type 0x0F = 191296 B):
- a78a9419… — type 0x09 248784 B
- ae7efd66… — type 0x09 300912 B
- b442ab11… — type 0x09 231264 B

### Type 0x09 Size Distribution in Generation B

| Size (bytes) | Count | Cohort |
|--------------|-------|--------|
| 333504 | 1 | Older |
| 300912 | 2 | Both |
| 284048 | 1 | Older |
| 249024 | 1 | Older |
| 248784 | 1 | Newer |
| 232256 | 1 | Older |
| 231264 | 1 | Newer |

The spread (231–333 KB) across ≥7 distinct binaries is the maintenance cost the dual-driver design was built to amortize.

### Type 0x08 Complete Variant Catalogue

| Variant | Size | SHA-1 | Generations | Count |
|---------|------|-------|-------------|-------|
| Modern Shared | 228928 | b81dd3e8d4c5d6699ae7aa4d96da9a50b79fda1a | Late B, C, D | ≥9 |
| Older Shared | 196864 | 5f677b5185e0c919ba2e08901b44b5715b5e15f1 | Early B (+1 C) | 6 |
| Gen-A Large | 104528 | e1341a854a691a1f79d33e41d5023e65184957ad | A | 1 |
| Gen-A Mid | 88120/88112 | 1d49a412… / a4f7884a… | A | 2 |
| Gen-A Small | 51768/51760 | 90753f98… / f836c402… | A | 2 |

**Pairing rule**: Modern type 0x08 always with modern type 0x0F (191296); older always with older type 0x0F (192096). No mixed pairings. ~32 KB delta = major coordinated revision.

### Type 0x0A Analysis

- **Gen A primary**: small dual set (22660 + 68912) or large 507450 B blob (identical across 3 containers)
- **Gen C secondary**: 50344 B dylib at f1 0xA0000 (two SHAs observed)
- **Gen D**: eliminated entirely

**End of Part 2** — Continue to [Part 3](CORUNA_REPORT_PART3.md)
