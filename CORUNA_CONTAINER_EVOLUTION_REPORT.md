# Coruna Payload Container Evolution & Module Comparative Analysis

**Classification**: UNCLASSIFIED // RESEARCH  
**Date**: 2026-07-26 (expanded 2026-07-27)  
**Status**: Complete multi-part intelligence-grade report

This is the complete original-research report on the Coruna payload container corpus. Full analytical content is published across four parts:

| Part | Content | Link |
|------|---------|------|
| **Part 1** | Executive summary, taxonomy, Gen D & C complete entry tables, Type 0x08/0x0A overview | [CORUNA_REPORT_PART1.md](CORUNA_REPORT_PART1.md) |
| **Part 2** | Full expanded inventory (all containers), Type 0x08 complete variant catalogue, Type 0x0A full analysis | [CORUNA_REPORT_PART2.md](CORUNA_REPORT_PART2.md) |
| **Part 3** | Complete Generation B entry tables, size clustering, timeline, design pressure, YARA rules, confidence matrix, key judgments | [CORUNA_REPORT_PART3.md](CORUNA_REPORT_PART3.md) |
| **Part 4** | Detection combination logic, coverage matrix, formal decision tree, relative dating arguments, methodology, reproducibility checklist, all appendices (type 0x09 register, f1 namespace, generation membership) | [CORUNA_REPORT_PART4.md](CORUNA_REPORT_PART4.md) |

**Companion report**: [DUAL_DRIVER_SUPPORT_LAYER_ORIGINAL_RESEARCH.md](DUAL_DRIVER_SUPPORT_LAYER_ORIGINAL_RESEARCH.md)

---

## Quick Key Judgments

1. Dual-driver + KIEA is a **late-stage refinement** (only 2 of 20 containers).
2. DEADD00F + SpringBoard is the most durable high-signal indicator (Gen B/C/D).
3. Type 0x08 and type 0x0F were revised as a coordinated pair (no mixed pairings).
4. Type 0x0A was primary in Gen A, retained as fallback in Gen C, eliminated in Gen D.
5. Gen B already required ≥7 distinct type 0x09 builds (231–333 KB) — the maintenance cost the dual-driver design amortizes.

## Four-Generation Taxonomy (Summary)

| Gen | Designation | Count | Defining Features |
|-----|-------------|-------|-------------------|
| A | Early Type-0x0A | 5 | Type 0x0A primary; no type 0x09/0x0F/DEADD00F |
| B | Classic Single Type-0x09 | 8 | Single type 0x09 + DEADD00F + type 0x0F |
| C | Transitional | 4 | Type 0x09 stack + retained type 0x0A dylib |
| D | Dual-Driver | 2 | Two type 0x09 (f1 0x90000/0x90001) + shared KIEA |

Start with [Part 1](CORUNA_REPORT_PART1.md).
