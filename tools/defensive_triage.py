#!/usr/bin/env python3
"""Defensive evidence + static triage collector.

This script performs non-executing analysis only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import subprocess
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

TEXT_EXTENSIONS = {
    ".c",
    ".cc",
    ".cfg",
    ".cpp",
    ".cs",
    ".go",
    ".h",
    ".hpp",
    ".html",
    ".ini",
    ".java",
    ".js",
    ".json",
    ".kt",
    ".log",
    ".md",
    ".php",
    ".ps1",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".sql",
    ".swift",
    ".toml",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

BINARY_EXTENSIONS = {
    ".apk",
    ".bin",
    ".dylib",
    ".elf",
    ".exe",
    ".jar",
    ".mach-o",
    ".o",
    ".so",
}

DEPENDENCY_MANIFESTS = {
    "package.json",
    "package-lock.json",
    "npm-shrinkwrap.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "requirements.txt",
    "requirements-dev.txt",
    "Pipfile",
    "Pipfile.lock",
    "poetry.lock",
    "pyproject.toml",
    "go.mod",
    "go.sum",
    "Cargo.toml",
    "Cargo.lock",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "Gemfile",
    "Gemfile.lock",
    "composer.json",
    "composer.lock",
}

SUSPICIOUS_PATTERNS = {
    "exfiltration": re.compile(r"\b(exfil|upload|beacon|c2|command\s*&\s*control|webhook)\b", re.IGNORECASE),
    "persistence": re.compile(r"\b(launchd|cron|autorun|startup|runkey|plist|systemd)\b", re.IGNORECASE),
    "privilege": re.compile(r"\b(root|sudo|setuid|entitlement|sandbox\s*escape|privilege)\b", re.IGNORECASE),
    "obfuscation": re.compile(r"\b(base64|eval\(|atob\(|fromCharCode|xor|chacha|decrypt|unpack)\b", re.IGNORECASE),
}

URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
DOMAIN_RE = re.compile(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b")


@dataclass
class Match:
    path: str
    line_number: int
    kind: str
    value: str


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    total = len(data)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def is_text_candidate(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS


def is_binary_candidate(path: Path) -> bool:
    return path.suffix.lower() in BINARY_EXTENSIONS


def iter_files(repo: Path, output: Path) -> Iterable[Path]:
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        try:
            path.relative_to(output)
            continue
        except ValueError:
            pass
        yield path


def safe_text_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return []


def collect_iocs(path: Path, lines: list[str]) -> list[Match]:
    results: list[Match] = []
    for idx, line in enumerate(lines, start=1):
        for value in URL_RE.findall(line):
            results.append(Match(str(path), idx, "url", value))
        for value in IPV4_RE.findall(line):
            results.append(Match(str(path), idx, "ipv4", value))
        for value in DOMAIN_RE.findall(line):
            if value.lower().endswith((".js", ".json", ".html", ".txt", ".md")):
                continue
            results.append(Match(str(path), idx, "domain", value))
    return results


def collect_suspicious_patterns(path: Path, lines: list[str]) -> dict[str, list[int]]:
    findings: dict[str, list[int]] = {}
    for category, pattern in SUSPICIOUS_PATTERNS.items():
        line_hits = [idx for idx, line in enumerate(lines, start=1) if pattern.search(line)]
        if line_hits:
            findings[category] = line_hits[:30]
    return findings


def run_git(repo: Path, args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect defensive evidence and static triage signals.")
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Repository root path.")
    parser.add_argument("--output", type=Path, required=True, help="Output directory for reports.")
    args = parser.parse_args()

    repo = args.repo.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    file_hashes = []
    dependency_files = []
    iocs: list[Match] = []
    suspicious = {}
    high_entropy = []
    binary_files = []

    for path in iter_files(repo, output):
        rel_path = str(path.relative_to(repo))
        size = path.stat().st_size
        file_hashes.append(
            {
                "path": rel_path,
                "size": size,
                "sha256": sha256_file(path),
            }
        )

        if path.name in DEPENDENCY_MANIFESTS:
            dependency_files.append(rel_path)

        if is_binary_candidate(path):
            binary_files.append(rel_path)

        if is_text_candidate(path):
            lines = safe_text_lines(path)
            if lines:
                iocs.extend(collect_iocs(Path(rel_path), lines))
                pattern_hits = collect_suspicious_patterns(Path(rel_path), lines)
                if pattern_hits:
                    suspicious[rel_path] = pattern_hits
        elif size >= 4096:
            try:
                sample = path.read_bytes()[:65536]
                entropy = shannon_entropy(sample)
                if entropy >= 7.5:
                    high_entropy.append({"path": rel_path, "entropy": round(entropy, 3), "sample_bytes": len(sample)})
            except OSError:
                continue

    git_info = {
        "remote": run_git(repo, ["config", "--get", "remote.origin.url"]),
        "branch": run_git(repo, ["rev-parse", "--abbrev-ref", "HEAD"]),
        "head_commit": run_git(repo, ["rev-parse", "HEAD"]),
        "recent_commits": run_git(repo, ["log", "--max-count", "25", "--pretty=format:%H %ad %an %s", "--date=iso-strict"]),
        "last_commit_signature": run_git(repo, ["log", "-1", "--show-signature", "--pretty=format:%H %ad %an %s", "--date=iso-strict"]),
    }

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo": str(repo),
        "summary": {
            "total_files": len(file_hashes),
            "dependency_manifest_files": len(dependency_files),
            "ioc_matches": len(iocs),
            "suspicious_files": len(suspicious),
            "high_entropy_files": len(high_entropy),
            "binary_candidate_files": len(binary_files),
        },
        "git": git_info,
        "dependency_manifests": sorted(dependency_files),
        "binary_candidates": sorted(binary_files),
        "high_entropy_files": sorted(high_entropy, key=lambda x: x["entropy"], reverse=True),
        "suspicious_patterns": suspicious,
        "iocs": [m.__dict__ for m in iocs[:5000]],
        "file_hashes": sorted(file_hashes, key=lambda x: x["path"]),
    }

    report_path = output / "defensive_triage_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    summary_path = output / "defensive_triage_summary.md"
    summary_path.write_text(
        "\n".join(
            [
                "# Defensive Triage Summary",
                "",
                f"- Generated at: `{report['generated_at']}`",
                f"- Repository: `{report['repo']}`",
                f"- Total files hashed: **{report['summary']['total_files']}**",
                f"- Dependency manifest files: **{report['summary']['dependency_manifest_files']}**",
                f"- IOC matches: **{report['summary']['ioc_matches']}**",
                f"- Suspicious files: **{report['summary']['suspicious_files']}**",
                f"- High entropy files: **{report['summary']['high_entropy_files']}**",
                f"- Binary candidate files: **{report['summary']['binary_candidate_files']}**",
                "",
                "## Key outputs",
                "",
                f"- JSON report: `{report_path}`",
                f"- This summary: `{summary_path}`",
            ]
        ),
        encoding="utf-8",
    )

    print(f"Wrote {report_path}")
    print(f"Wrote {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
