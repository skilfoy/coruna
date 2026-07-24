# Defensive Analysis Playbook (Enterprise-Safe)

This playbook is for **defensive security research only**. It is designed to support triage and incident response without reproducing or operationalizing malware behavior.

## 1) Authorization and governance

- Confirm written authorization for analysis before any handling or execution.
- Define incident owner, escalation path, and reporting cadence.
- Define evidence retention period and chain-of-custody requirements.
- Ensure legal/compliance sign-off for any runtime detonation activity.

## 2) Isolated lab requirements

- Use disposable, non-production hosts dedicated to malware research.
- No production credentials, tokens, VPN profiles, or corp trust roots.
- No clipboard/file sharing between analyst workstation and detonation host.
- Default-deny network policy with tightly controlled egress and full logging.

## 3) Evidence ingestion first

- Create a cryptographic inventory (SHA-256) of all repository files.
- Capture repository provenance (remote URL, branch, commit, contributor history).
- Capture dependency manifests and produce an SBOM.
- Record signing status and commit authenticity where available.

Use the helper script in this repository:

```bash
python3 /home/runner/work/coruna/coruna/tools/defensive_triage.py \
  --repo /home/runner/work/coruna/coruna \
  --output /tmp/coruna-analysis
```

## 4) Static triage before any execution

- Extract candidate IOCs (URLs, IPv4 addresses, suspicious domains).
- Identify suspicious scripting behavior:
  - data exfiltration patterns
  - persistence/autostart patterns
  - privilege escalation or entitlement abuse patterns
  - obfuscation/deobfuscation patterns
- Identify high-entropy or binary-heavy artifacts for deeper reverse engineering.

## 5) Controlled detonation decision gate

Only proceed to runtime analysis after explicit approval by security leadership/legal.

Required controls:
- pre-approved test plan and stop conditions
- strict egress controls and DNS logging
- full telemetry capture (process, file, network, memory, and system changes)
- disposable image rollback after each run

## 6) Detection engineering output

- Convert observed artifacts into:
  - EDR detections
  - SIEM correlations
  - IOC blocklists/watchlists
  - YARA/Sigma detections (where relevant)
- Record confidence and expected false-positive/false-negative behavior.

## 7) Containment and remediation

- Isolate potentially affected endpoints.
- Rotate exposed credentials and revoke active sessions.
- Remove or pin risky dependencies and lock vulnerable supply-chain paths.
- Harden policy controls (execution controls, egress, least privilege, monitoring).

## 8) Reporting package

Produce two outputs:

1. **Executive summary**
   - scope, impact, risk, timeline, and remediation status
2. **Technical appendix**
   - attack chain, evidence, IOCs, detections, and confidence ratings

## Deliverables checklist

- [ ] Authorization and governance record
- [ ] Evidence bundle (hashes, provenance, dependency inventory, SBOM)
- [ ] Static triage report
- [ ] Runtime analysis approval record (if performed)
- [ ] Detection pack and containment actions
- [ ] Executive + technical report
