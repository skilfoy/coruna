# CORUNA CONTAINER EVOLUTION REPORT — PART 3

**Continuation of the full intelligence-grade report.**  
See [index](CORUNA_CONTAINER_EVOLUTION_REPORT.md) for navigation.

---

## Timeline, Design Pressure, Confidence Matrix, Key Judgments

### Relative Chronology

```
Gen A (type 0x0A primary, small type 0x08, no DEADD00F)
  → Gen B (single type 0x09 + DEADD00F + type 0x0F; internal implant revision)
    → Gen C (type 0x09 stack + retained compact type 0x0A)
      → Gen D (dual type 0x09 + shared KIEA; type 0x0A eliminated)
```

### Design-Pressure Narrative

Generation B already required ≥7 distinct type 0x09 binaries (231–333 KB). Each new iOS point release that changed kernel offsets required a new full driver build. Packaging many near-duplicate multi-hundred-kilobyte drivers is expensive and increases forensic footprint.

Generation D attacks exactly this cost:
- Two driver variants instead of many
- Version-specific data externalized into one shared 24 KB KIEA blob
- Selection reduced to a single bit test on f1
- Same KIEA blob pairable with different driver builds (demonstrated by the two dual-driver containers)

Only two containers received this treatment → late, selective application.

### Confidence Matrix

| Finding | Confidence | Basis |
|---------|------------|-------|
| Four-generation taxonomy | High | Complete enumeration; consistent presence/absence |
| DEADD00F identity across B/C/D | High | Identical SHA in every mature container |
| KIEA shared only by two Gen D containers | High | Identical size + SHA; absent elsewhere |
| Dual type 0x09 selection by f1 low bit | High | Manifest f1 values; structural necessity |
| Coordinated modern/older type 0x08/0x0F pairing | High | No mixed pairings across 15+ containers |
| Type 0x0A eliminated in Gen D | High | Complete absence from both dual-driver containers |
| Type 0x09 size proliferation as design pressure | Medium-High | Observed 231–333 KB range across ≥7 binaries |
| Exact content of 32 KB type 0x08 delta | Low | Requires interactive disassembly |
| Precise KIEA internal layout | Low | Requires kernelcache correlation |
| Absolute chronological dating | Low | Only relative order supported |

### Formal Key Judgments

1. Dual-driver architecture is a late-stage refinement, not the historical baseline (2 of 20 containers).
2. DEADD00F + SpringBoard is the most durable high-signal static indicator (Gen B/C/D).
3. Type 0x08 and type 0x0F were revised as a coordinated pair (no mixed pairings).
4. Type 0x0A was primary in Gen A, retained as fallback in Gen C, eliminated in Gen D.
5. Gen B type 0x09 size proliferation (231–333 KB) is direct evidence of the maintenance cost the dual-driver design amortizes.

### Recommendations for Further Static Work

1. Interactive Mach-O analysis of modern vs older type 0x08 (32 KB delta).
2. First hundreds of bytes of KIEA correlated against XNU structures (iOS 17.0–17.2.1).
3. String/import comparison of 507450 B Gen A type 0x0A.bin vs 50344 B Gen C dylib.
4. Export-trie and load-command inspection of bootstrap.dylib for selection/constants-passing logic.

**End of Part 3** — Continue to [Part 4](CORUNA_REPORT_PART4.md)
