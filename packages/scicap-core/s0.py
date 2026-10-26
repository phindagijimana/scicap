"""Locate the fetched S0 T1w. Never download. Never copy NIfTI.

Public bytes may already exist under ``shared/data/external/ds000003/``.
Pytest must not fetch OpenNeuro. A git-annex pointer (~140 bytes, often
starting with ``..``) is treated as absent. Gzip magic ``\\x1f\\x8b`` is
required for ``.nii.gz``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

GZIP_MAGIC = b"\x1f\x8b"
ANNEX_MIN_BYTES = 1024
ACCESSION = "ds000003"
T1W_REL = Path("sub-01") / "anat" / "sub-01_T1w.nii.gz"
S0_REL_FROM_WORKSPACE = f"shared/data/external/{ACCESSION}/{T1W_REL.as_posix()}"
S0_REL_FROM_SCICAP = f"../{S0_REL_FROM_WORKSPACE}"
BIDS_REL_FROM_SCICAP = f"../shared/data/external/{ACCESSION}"

_ABSENT_REASON = (
    "shared/data/external/ds000003 has no public T1w bytes; "
    "pytest does not download; JSON sidecars remain"
)


def _folder_root() -> Path:
    return Path(__file__).resolve().parents[2]


def workspace_root() -> Path:
    return _folder_root().parent


def shared_root() -> Path:
    folder = _folder_root()
    for candidate in (folder.parent / "shared", folder / "shared"):
        if candidate.is_dir():
            return candidate
    return folder.parent / "shared"


def external_root() -> Path:
    return shared_root() / "data" / "external"


def manifest_t1w_path() -> Path:
    return external_root() / ACCESSION / T1W_REL


def is_annex_or_pointer(path: Path) -> bool:
    """True for tiny annex/LFS/HTML stand-ins. Not a public T1w."""
    try:
        size = path.stat().st_size
        head = path.read_bytes()[:16]
    except OSError:
        return True
    if size < ANNEX_MIN_BYTES:
        return True
    if head.startswith(b"..") or head.startswith(b"<") or head.startswith(b"version"):
        return True
    return False


def is_public_gzip_t1w(path: Path) -> bool:
    """Require gzip magic. Reject 140-byte git-annex pointers."""
    if not path.is_file():
        return False
    if is_annex_or_pointer(path):
        return False
    try:
        head = path.read_bytes()[:2]
    except OSError:
        return False
    return head == GZIP_MAGIC


def find_ds000003_t1w() -> Path | None:
    """Return the on-disk public T1w, or None. Does not download."""
    preferred = manifest_t1w_path()
    if is_public_gzip_t1w(preferred):
        return preferred.resolve()
    root = external_root() / ACCESSION
    if not root.is_dir():
        return None
    hits = [
        path.resolve()
        for path in root.rglob("*")
        if path.is_file()
        and path.name.lower().endswith(".nii.gz")
        and "t1w" in path.name.lower()
        and is_public_gzip_t1w(path)
    ]
    if hits:
        return sorted(hits)[0]
    return None


def s0_status() -> dict[str, Any]:
    """Record whether fetched S0 bytes are usable. Not an evaluation."""
    path = find_ds000003_t1w()
    present = path is not None
    return {
        "present": present,
        "path": str(path) if path is not None else None,
        "accession": ACCESSION,
        "relpath": S0_REL_FROM_WORKSPACE,
        "bytes_in_git": False,
        "download_in_pytest": False,
        "gzip_magic": present,
        "reason": (
            "public T1w present under shared/data/external/ds000003"
            if present
            else _ABSENT_REASON
        ),
    }
