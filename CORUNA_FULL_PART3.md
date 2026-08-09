# CORUNA CONTAINER EVOLUTION REPORT — COMPLETE LOCAL WORKING COPY
## Part 3 of 5 (lines 721–1080 of 1797)

**This is the uncondensed full local analysis. No content removed.**

[Index](CORUNA_CONTAINER_EVOLUTION_REPORT.md) | [Part 1](CORUNA_FULL_PART1.md) | [Part 2](CORUNA_FULL_PART2.md) | [Part 3](CORUNA_FULL_PART3.md) | [Part 4](CORUNA_FULL_PART4.md) | [Part 5](CORUNA_FULL_PART5.md)

---

point the implant is responsible for:

- Stabilising the execution environment inside the compromised process,
- Coordinating or loading the type 0x0F persistence component,
- Performing any final environment or capability checks,
- Serving as the long-lived presence that subsequent stages rely upon.

Because identical type 0x08 binaries (by SHA-1) are shared across many
containers, the implant constitutes one of the highest-value static detection
and forensic pivots in the entire corpus.

## 4.2 Complete Variant Catalogue

Five distinct size families have been recovered:

### Variant M — Modern Shared Implant
- Size: 228928 bytes
- SHA-1: b81dd3e8d4c5d6699ae7aa4d96da9a50b79fda1a
- Generations: late Generation B, all of Generation C that use the modern
  persistence module, both Generation D dual-driver containers
- Approximate container count: ≥9
- Paired exclusively with type 0x0F of size 191296 bytes
  (SHA e8c656a78ace2f7c6f0f13f4364cd716efb5aa93)

### Variant O — Older Shared Implant
- Size: 196864 bytes
- SHA-1: 5f677b5185e0c919ba2e08901b44b5715b5e15f1
- Generations: early Generation B, one transitional Generation C container
- Approximate container count: 6
- Paired exclusively with type 0x0F of size 192096 bytes
  (SHA b886ab5c501d2b2cc476fc48d0fcab9b2e20328b)

### Variant A1 — Generation A Small
- Sizes: 51768 / 51760 bytes
- SHAs: 90753f9817556b1b74f1dfbe183737bcb8dc683b /
        f836c4027decd4c24e0cf78e302bfbf9b89f8076
- Generations: Generation A only (dual small type 0x0A containers)
- Count: 2

### Variant A2 — Generation A Mid
- Sizes: 88120 / 88112 bytes
- SHAs: 1d49a412bb895b6013ff8119712d1dba16c8ef6e /
        a4f7884ac4d38d7587c1bd54681413a743175a3c
- Generations: Generation A only (large type 0x0A.bin containers)
- Count: 2

### Variant A3 — Generation A Larger
- Size: 104528 bytes
- SHA-1: e1341a854a691a1f79d33e41d5023e65184957ad
- Generations: Generation A only
- Count: 1

## 4.3 Modern vs Older Shared Implant — Detailed Comparison

The two dominant variants differ by 32064 bytes (approximately 32 KB). Both
appear exclusively with the DEADD00F configuration and a type 0x0F module,
confirming they occupy the same architectural slot in the post-exploitation
chain.

Critical pairing rule observed across the entire corpus:

  Modern type 0x08 (228928 B)  is always paired with modern type 0x0F (191296 B)
  Older  type 0x08 (196864 B)  is always paired with older  type 0x0F (192096 B)

No mixed pairings exist. The implant and the persistence module were revised
as a coordinated unit.

The 32 KB size delta is too large to be explained by simple padding or
compiler settings. It is consistent with the addition of new capability,
expanded offset tables, additional logging or anti-analysis logic, or support
for a broader set of iOS versions. Without interactive disassembly the precise
nature of the added content cannot be determined, but the existence of a clean
before/after pair is itself a high-confidence observation.

## 4.4 Generation A Implants

The three smaller Generation A variants (≈51–104 KB) are substantially less
complex. Their exclusive co-occurrence with type 0x0A modules and the complete
absence of type 0x09, type 0x0F and DEADD00F indicate an earlier design in
which the implant and the exploitation primitive were more tightly coupled.
These variants have no observed reuse in later generations.

## 4.5 Detection Value of Type 0x08

Because Variant M is shared across the majority of mature containers, a single
high-confidence hash or size rule for the 228928-byte binary covers:
- both dual-driver (Generation D) containers,
- all late Generation B containers,
- three of the four Generation C containers.

Variant O provides equivalent coverage for the preceding cohort. Together the
two rules give near-complete coverage of every container that uses the modern
support-layer design (DEADD00F + type 0x0F).

# ==============================================================================
# EXPANDED SECTION 5 — TYPE 0x0A MODULE ANALYSIS (FULL)
# ==============================================================================

## 5.1 Distribution and Role

Type 0x0A records appear in two sharply different contexts:

1. Generation A — type 0x0A is the primary (and often sole) exploitation or
   post-exploitation path.
2. Generation C — a compact type 0x0A dylib is retained alongside a complete
   modern (or near-modern) type 0x09 + type 0x0F + DEADD00F stack.

Type 0x0A is entirely absent from pure Generation B single-driver containers
and from both Generation D dual-driver containers.

## 5.2 Generation A Type 0x0A Variants

### Small dual set
- 22660-byte type 0x0A.bin (SHA 7424d4f505f842c2ebf49373c14c7a588daf37fc)
- 68912-byte type 0x0A.dylib (SHA 2d3c4a957d7068416b78acad6c2cdde4231e5cf7)
- Present in containers 2a1d692b… and 5e89f83e…
- Paired with the smallest type 0x08 implants recovered

### Large singleton
- 507450-byte type 0x0A.bin (SHA 907e8d190d7c7bd2701f632cb202c3cde39303f1)
- Present identically in containers 72a5ac81…, 980c77f1… and f8a86cf3…
- This is the largest individual non-driver module in the entire corpus
- Its identical presence across three independent containers indicates a
  stable, reused component from the earliest recovered phase of the toolkit

## 5.3 Generation C Type 0x0A

All four Generation C containers carry a type 0x0A dylib of exactly 50344
bytes at f1 0xA0000. Two distinct SHAs are observed:

- f53bc3d1b239168e69a51ac67d86ca4c56aa1beb (three containers)
- 5fa390b9e291824fde40cdd76ac85b67ccb8ee0f (one container)

The co-existence of a full type 0x09 driver stack with a compact type 0x0A
dylib is the clearest evidence of a transitional packaging strategy. The
operators appear to have distributed both the older type 0x0A path and the
newer type 0x09 path in the same container, most likely to maximise version
coverage or to retain a fallback.

## 5.4 Elimination in Generation D

Once the dual-driver design is introduced, type 0x0A records disappear
completely. The data-driven type 0x09 pair together with the shared KIEA
constants table appear to have fully superseded the earlier type 0x0A approach
for the version window targeted by the two dual-driver containers.

## 5.5 Analytical Limits

Without interactive disassembly the precise functional relationship between
the 50 KB Generation C type 0x0A dylib and the 507 KB Generation A type 0x0A.bin
cannot be established. The size disparity alone demonstrates they are not
simple revisions of the same module. The smaller dylib may represent a
stripped or specialised remnant of the earlier capability, retained only as a
compatibility or fallback component.

# ==============================================================================
# EXPANDED SECTION 6 — EVOLUTIONARY TIMELINE AND DESIGN RATIONALE
# ==============================================================================

## 6.1 Relative Chronology

The following relative order is supported by the static evidence:

  Generation A  (type 0x0A primary, small type 0x08, no DEADD00F)
       │
  Generation B  (single type 0x09 + DEADD00F + type 0x0F introduced;
                 internal revision of type 0x08 / type 0x0F pair)
       │
  Generation C  (type 0x09 stack retained; compact type 0x0A re-introduced
                 as secondary path)
       │
  Generation D  (dual type 0x09 selectable by f1 low bit;
                 shared KIEA constants; type 0x0A eliminated)

## 6.2 Design Pressure Visible in Generation B

Generation B already required at least seven distinct type 0x09 binaries
whose sizes range from roughly 231 KB to 333 KB. Each new revision had to be
packaged and distributed as a complete driver record. This proliferation is
the concrete maintenance burden that the Generation D redesign was engineered
to reduce.

By externalising version-specific offsets and gadgets into a single shared
KIEA blob and shipping only two driver variants distinguished by a single bit
of the f1 field, the operators could cover the same (or a broader) version
window with far fewer full driver builds.

## 6.3 Selective Application of the Dual-Driver Design

Only two containers received the dual-driver treatment. The redesign was
therefore applied late and selectively; it was not retrofitted to the earlier
corpus. This is consistent with an opportunistic improvement rather than a
wholesale rewrite of the toolkit.

# ==============================================================================
# EXPANDED SECTION 7 — DETECTION IMPLICATIONS AND RULE SETS
# ==============================================================================

## 7.1 High-Value Static Indicators (Ranked)

1. DEADD00F magic (0x0FD0ADDE) + "SpringBoard" string inside a ≤64-byte record
   Coverage: Generations B, C, D
   False-positive risk: extremely low

2. Type 0x08 SHA b81dd3e8… (exactly 228928 bytes)
   Coverage: late B, C, D
   False-positive risk: extremely low

3. Type 0x08 SHA 5f677b51… (exactly 196864 bytes)
   Coverage: early B (+ one C)
   False-positive risk: extremely low

4. KIEA magic ("KIEA") at offset 0 of a 24844-byte blob
   Coverage: Generation D only
   False-positive risk: extremely low

5. Simultaneous presence of f1 values 0x90000 and 0x90001 inside the same
   F00DBEEF container
   Coverage: Generation D only
   False-positive risk: extremely low

6. Type 0x0A 507450-byte blob (SHA 907e8d19…)
   Coverage: Generation A (three containers)
   False-positive risk: low

7. Type 0x0A 50344-byte dylib at f1 0xA0000
   Coverage: Generation C
   False-positive risk: low–medium

## 7.2 Recommended YARA Rules (Extended)

```yara
rule Coruna_DEADD00F_SpringBoard
{
    meta:
        description = "Coruna DEADD00F + SpringBoard type 0x07 config"
        date = "2026-07-26"
        confidence = "high"
    strings:
        $magic = { 0F D0 AD DE }
        $sb = "SpringBoard" ascii
    condition:
        $magic at 0 and $sb and filesize < 64
}

rule Coruna_KIEA_Constants
{
    meta:
        description = "Coruna shared KIEA type 0x05 constants blob"
        date = "2026-07-26"
        confidence = "high"
    strings:
        $kiea = "KIEA" ascii
    condition:
        $kiea at 0 and filesize == 24844
}

rule Coruna_Type08_Modern
{
    meta:
        description = "Coruna modern type 0x08 implant"
        date = "2026-07-26"
    condition:
        filesize == 228928
}

rule Coruna_Type08_Older
{
    meta:
        description = "Coruna older type 0x08 implant"
        date = "2026-07-26"
    condition:
        filesize == 196864
}

rule Coruna_Type0A_Large
{
    meta:
        description = "Coruna Generation A large type 0x0A.bin"
        date = "2026-07-26"
    condition:
        filesize == 507450
}
```

# ==============================================================================
# SECTION 8 — METHODOLOGY, LIMITATIONS AND REPRODUCIBILITY
# ==============================================================================

## 8.1 Methodology

All findings in this report are derived from pure static examination of:
- the repository tree under payloads/,
- the structured payloads/manifest.json,
- file sizes and SHA-1 identities of every recovered module,
- previously established F00DBEEF, DEADD00F and KIEA structures.

No dynamic execution, emulation or interactive disassembly of the large
binaries was performed inside the analysis environment.

## 8.2 Limitations

- Internal structure of the type 0x09 drivers, the type 0x08 implants and the
  type 0x0A modules remains opaque without interactive tooling.
- Exact version ranges targeted by each type 0x09 revision cannot be recovered
  from size and SHA alone.
- The precise contents of the KIEA constants table beyond the magic and overall
  size are not recovered in this report.

## 8.3 Reproducibility

Every container hash, module size and SHA-1 cited above is directly verifiable
against the public skilfoy/coruna repository. The generational taxonomy can be
re-derived independently by any analyst who enumerates the payloads/ directory
and inspects the manifest.json f1 / type / size fields.

# ==============================================================================
# ADDITIONAL ANALYTICAL DEPTH — CONFIDENCE, RELATED WORK, AND FORMAL JUDGMENTS
# ==============================================================================

## 9. Confidence Matrix

| Finding | Confidence | Basis |
|---------|------------|-------|
| Four-generation taxonomy (A/B/C/D) | High | Complete enumeration of all containers; consistent presence/absence patterns |
| DEADD00F identity across B/C/D | High | Identical SHA recovered from every mature container |
| KIEA shared only by the two Gen D containers | High | Identical size + SHA; absent from all other containers |
| Dual type 0x09 selection by f1 low bit | High | Manifest f1 values 0x90000 / 0x90001; structural necessity of bootstrap selection logic |
| Coordinated modern vs older type 0x08/0x0F pairing | High | No mixed pairings observed across 15+ containers |
| Type 0x0A eliminated in Gen D | High | Complete absence from both dual-driver containers |
| Type 0x09 size proliferation inside Gen B as design pressure | Medium-High | Observed size range 231–333 KB across ≥7 distinct binaries |
| Exact functional content of the 32 KB type 0x08 delta | Low | Requires interactive disassembly |
| Precise internal layout of KIEA beyond magic | Low | Requires correlation against kernelcaches or driver indexing logic |
| Absolute chronological dating of generations | Low | Only relative order is supported by static evidence |

## 10. Related Work Assessment

Public technical writing on the broader exploit chain (cassowary / seedbell style WebKit RCE, PAC bypass, Gruber/Rocket-style kernel primitives, F00DBEEF container format, SpringBoard persistence) is relatively mature. What has been missing is a systematic, corpus-wide static inventory of the support-layer modules themselves.

Prior public reconstructions have tended to examine one or two high-value samples in depth (often the dual-driver containers). Those samples are not representative of the full historical corpus. The dual-driver + KIEA design is a late refinement; the majority of recovered containers use a single type 0x09 driver and, in the earliest phase, rely on type 0x0A paths entirely.

The present report is, to the best of our knowledge, the first public document that:

- enumerates every container in the skilfoy/coruna payloads/ tree,
- assigns each container to a coherent generational taxonomy,
- maps the sharing of type 0x08, type 0x0F, DEADD00F and KIEA identities across that taxonomy,
- demonstrates the concrete maintenance pressure visible inside Generation B that motivates the dual-driver redesign,
- and supplies an updated, generation-aware detection rule set.

## 11. Formal Key Judgments

**Judgment 1**  
The dual-driver architecture (two type 0x09 variants selected by the low bit of f1, plus a shared external KIEA constants blob) is a late-stage engineering refinement, not the historical baseline of the toolkit. It appears in only two of the twenty recovered containers.

**Judgment 2**  
The DEADD00F + SpringBoard type 0x07 configuration is the single most durable high-signal static indicator across the mature corpus (Generations B, C and D).

**Judgment 3**  
Type 0x08 (implant) and type 0x0F (persistence) were revised as a coordinated pair. The modern 228928-byte implant is never observed with the older 192096-byte persistence module, and vice versa.

---
**Continue to [Part 4](CORUNA_FULL_PART4.md)**
