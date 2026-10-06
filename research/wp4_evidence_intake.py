"""Read-only local evidence integrity audit; no authenticity or source promotion."""
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

MAX_ARTIFACT_BYTES = 10 * 1024 * 1024


def _pointer(value, pointer):
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ValueError("JSON_POINTER_INVALID")
    for raw in pointer[1:].split("/"):
        if re.search(r"~(?![01])", raw):
            raise ValueError("JSON_POINTER_INVALID")
        key = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(value, dict):
            value = value[key]
        elif isinstance(value, list) and re.fullmatch(r"0|[1-9][0-9]*", key):
            value = value[int(key)]
        else:
            raise ValueError("LOCATOR_NOT_FOUND")
    return value


def audit_artifact(root, entry):
    """Hash and locate content inside root only. Metadata is not authentication."""
    integrity = []
    metadata = []
    result = {"integrity_valid": False, "integrity_issues": integrity,
              "metadata_issues": metadata, "source_verified": False,
              "execution_readiness": "BLOCKED"}
    if not isinstance(entry, dict):
        integrity.append("ENTRY_INVALID")
        return result
    result["artifact_id"] = entry.get("artifact_id")
    if not isinstance(entry.get("artifact_id"), str) or not entry["artifact_id"].strip():
        metadata.append("ARTIFACT_ID_REQUIRED")
    if entry.get("kind") not in ("ORIGINAL_SNAPSHOT", "REVIEW_RECORD"):
        metadata.append("ARTIFACT_KIND_INVALID")
    source = entry.get("source_url")
    try:
        url = urlsplit(source) if isinstance(source, str) else None
        if url is None or url.scheme != "https" or not url.hostname or url.username or url.password:
            metadata.append("SOURCE_URL_REQUIRED")
    except ValueError:
        metadata.append("SOURCE_URL_REQUIRED")
    try:
        acquired = datetime.fromisoformat(entry.get("retrieved_at"))
        if acquired.tzinfo is None or acquired.utcoffset() is None:
            raise ValueError()
    except (ValueError, TypeError):
        metadata.append("RETRIEVAL_TIME_UNKNOWN")
    if not isinstance(entry.get("claim"), str) or not entry["claim"].strip():
        metadata.append("CLAIM_REQUIRED")
    if not isinstance(entry.get("limitations"), str) or not entry["limitations"].strip():
        metadata.append("LIMITATIONS_REQUIRED")
    relative = entry.get("path")
    if not isinstance(relative, str) or not relative.strip():
        integrity.append("PATH_INVALID")
        return result
    try:
        root = Path(root).resolve(strict=True)
        requested = Path(relative)
        if requested.is_absolute() or ".." in requested.parts:
            raise ValueError()
        path = (root / requested).resolve()
        if not path.is_relative_to(root):
            raise ValueError()
    except (OSError, ValueError):
        integrity.append("PATH_OUTSIDE_ROOT")
        return result
    if not path.is_file():
        integrity.append("ARTIFACT_MISSING")
        return result
    try:
        if path.stat().st_size > MAX_ARTIFACT_BYTES:
            integrity.append("ARTIFACT_TOO_LARGE")
            return result
        with path.open("rb") as stream:
            raw = stream.read(MAX_ARTIFACT_BYTES + 1)
        if len(raw) > MAX_ARTIFACT_BYTES:
            integrity.append("ARTIFACT_TOO_LARGE")
            return result
    except OSError:
        integrity.append("ARTIFACT_UNREADABLE")
        return result
    result["actual_bytes"] = len(raw)
    result["actual_sha256"] = hashlib.sha256(raw).hexdigest()
    expected_hash = entry.get("sha256")
    if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected_hash):
        integrity.append("HASH_REQUIRED")
    elif expected_hash.lower() != result["actual_sha256"]:
        integrity.append("HASH_MISMATCH")
    size = entry.get("bytes")
    if type(size) is not int or size < 0:
        integrity.append("EXPECTED_SIZE_REQUIRED")
    elif size != len(raw):
        integrity.append("SIZE_MISMATCH")
    locator = entry.get("locator")
    if not isinstance(locator, dict):
        integrity.append("LOCATOR_REQUIRED")
    else:
        try:
            encoding = locator.get("encoding", "utf-8-sig")
            if encoding not in ("utf-8-sig", "utf-8", "cp950", "big5"):
                raise ValueError("ENCODING_INVALID")
            text = raw.decode(encoding)
            if locator.get("type") == "JSON_POINTER":
                _pointer(json.loads(text), locator.get("value"))
            elif locator.get("type") == "TEXT":
                needle = locator.get("value")
                if not isinstance(needle, str) or not needle.strip():
                    raise ValueError("LOCATOR_INVALID")
                if needle not in text:
                    raise ValueError("LOCATOR_NOT_FOUND")
            else:
                raise ValueError("LOCATOR_INVALID")
        except (ValueError, TypeError, KeyError, IndexError, RecursionError):
            integrity.append("LOCATOR_INVALID_OR_NOT_FOUND")
    result["integrity_valid"] = not integrity
    result["metadata_complete"] = not metadata
    result["artifact_kind"] = entry.get("kind")
    return result


def audit_intake(root, entries):
    if not isinstance(entries, list) or len(entries) > 100:
        return {"intake_valid": False, "issues": ["ENTRY_LIST_INVALID"],
                "artifacts": [], "source_verified": False}
    results = [audit_artifact(root, entry) for entry in entries]
    ids = [entry.get("artifact_id") for entry in entries if isinstance(entry, dict)]
    issues = []
    if not entries:
        issues.append("INTAKE_EMPTY")
    if any(ids[i] == ids[j] for i in range(len(ids)) for j in range(i)):
        issues.append("DUPLICATE_ARTIFACT_ID")
    return {"intake_valid": not issues and all(
                row["integrity_valid"] and row.get("metadata_complete", False)
                for row in results),
            "issues": issues, "artifacts": results, "source_verified": False,
            "execution_readiness": "BLOCKED"}
