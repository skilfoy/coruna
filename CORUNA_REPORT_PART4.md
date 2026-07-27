# CORUNA CONTAINER EVOLUTION REPORT — PART 4

**Continuation of the full intelligence-grade report.**  
See [index](CORUNA_CONTAINER_EVOLUTION_REPORT.md) for navigation.

---

## Detection Rules, Decision Tree, Methodology, Appendices

### Formal Generation Assignment Decision Tree

```
START
  │
  ├─ Contains type 0x05 (KIEA)?
  │     YES → Generation D (confirm two type 0x09: 0x90000 + 0x90001)
  │     NO
  │
  ├─ Contains type 0x09?
  │     NO  → Generation A (or Anomalous)
  │     YES
  │
  ├─ Contains type 0x0A?
  │     YES → Generation C (Transitional)
  │     NO  → Generation B (Classic Single Type-0x09)
  │
  └─ Sub-classify Gen B by type 0x08 size:
        228928 → Late B | 196864 → Early B
```

### Primary YARA Rules

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

### Hash-Based Detection Lists

- Type 0x08 modern: `b81dd3e8d4c5d6699ae7aa4d96da9a50b79fda1a` (228928 B)
- Type 0x08 older: `5f677b5185e0c919ba2e08901b44b5715b5e15f1` (196864 B)
- Type 0x0F modern: `e8c656a78ace2f7c6f0f13f4364cd716efb5aa93` (191296 B)
- Type 0x0F older: `b886ab5c501d2b2cc476fc48d0fcab9b2e20328b` (192096 B)
- KIEA: `f41d90fda2ffe35c5bc332b7944b6f0243b92ed7` (24844 B)
- DEADD00F: `ea2db48aec8c6215bee0cedc49f084832b5090f2` (~44–49 B)
- Type 0x0A large: `907e8d190d7c7bd2701f632cb202c3cde39303f1` (507450 B)

### Coverage Matrix

| Rule | Gen A | Early B | Late B | Gen C | Gen D |
|------|-------|---------|--------|-------|-------|
| DEADD00F + SpringBoard | | ✓ | ✓ | ✓ | ✓ |
| Type 0x08 modern | | | ✓ | ✓* | ✓ |
| Type 0x08 older | | ✓ | | ✓* | |
| KIEA | | | | | ✓ |
| Dual f1 0x90000+0x90001 | | | | | ✓ |
| Type 0x0A large | ✓ | | | | |
| Type 0x0A compact | | | | ✓ | |

\* One Gen C uses older pair.

### Methodology

Sources: payloads/ tree, manifest.json, SHA/size identities, prior dual-driver research.  
No commercial disassembler or dynamic analysis used. All conclusions limited to file-level metadata and established container structures.

### Limitations

- Internal code of large binaries unexamined
- KIEA layout beyond magic unknown
- Absolute dating impossible
- Scoped to this repository snapshot

### Reproducibility Checklist

- [ ] Clone https://github.com/skilfoy/coruna
- [ ] List payloads/ directories (20 containers)
- [ ] Parse manifest.json for f1/type/size/SHA
- [ ] Verify type 0x05 only in two containers
- [ ] Verify those two each have f1 0x90000 + 0x90001
- [ ] Verify DEADD00F SHA in every mature container
- [ ] Verify modern/older type 0x08 size split
- [ ] Confirm no mixed type 0x08/0x0F pairings
- [ ] Confirm type 0x0A only in Gen A and Gen C
- [ ] Re-derive taxonomy via decision tree above

### Appendix — f1 Namespace

| f1 (hex) | Type | Role |
|----------|------|------|
| 0x50000 | 0x05 | KIEA (D only) |
| 0x70000 | 0x07 | Secondary config |
| 0x70005 | 0x07 | DEADD00F / SpringBoard |
| 0x80000 | 0x08 | Implant |
| 0x90000 | 0x09 | Primary driver |
| 0x90001 | 0x09 | Secondary driver (D only) |
| 0xA0000 | 0x0A | Compact dylib (C) |
| 0xA0001/02 | 0x0A | Gen A variants |
| 0xF0000 | 0x0F | Persistence |

### Document Control

- Version: 1.4 (expanded, multi-part)
- Companion: DUAL_DRIVER_SUPPORT_LAYER_ORIGINAL_RESEARCH.md
- Local working copy: ~1 800 lines; published as index + 4 parts

**End of Report**
