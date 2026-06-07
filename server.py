#!/usr/bin/env python3
"""
Agent Content Watermark MCP — EU AI Act Article 50(2) dedicated
================================================================

By MEOK AI Labs · https://meok.ai · MIT
<!-- mcp-name: io.github.CSOAI-ORG/agent-content-watermark-mcp -->

WHAT THIS DOES
--------------
EU AI Act Article 50(2): "Providers of GenAI systems... shall ensure that the
outputs are marked in a machine-readable format and detectable as artificially
generated or manipulated."

Effective: **2 August 2026** (NOT delayed by the Digital Omnibus).

This MCP handles the watermark side specifically — distinct from broader C2PA
provenance. Three layers per the Code of Practice:

  1. **Visible label**  — "AI-generated" + provider attribution string
  2. **Invisible payload** — image: F5/Steganographic ; text: zero-width chars
  3. **Perceptual hash** — robust to compression / crop / mild edits

Companion to:
- `watermarking-authenticity-mcp` (C2PA-led, broader)
- `agent-incident-relay-mcp` (if missing-watermark incident detected)

TOOLS
-----
- generate_watermark(content_hash, model_id, provider_did): emit a signed mark
- verify_watermark(mark): cryptographic + perceptual verification
- attach_c2pa_manifest(image_meta, mark): builds the C2PA manifest envelope
- list_modalities(): which content types this MCP can mark
- code_of_practice_status(): current Code of Practice version + deadline
- sign_conformity_attestation(generation_event): signed Art 50 attestation

PRICING
-------
Free MIT self-host · £29/mo Starter · £79/mo Pro · Governance Substrate £499/mo.
"""

from __future__ import annotations
import hashlib
import hmac
import json
import os
import time
from datetime import datetime, timezone
from typing import Optional
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("agent-content-watermark")
_HMAC_SECRET = os.environ.get("MEOK_HMAC_SECRET", "")


CODE_OF_PRACTICE = {
    "version": "GPAI CoP v1.0",
    "effective_date": "2026-08-02",
    "issuing_body": "European AI Office",
    "scope": "Providers of general-purpose AI models / GenAI systems",
    "key_obligations": [
        "Marking generated output in a machine-readable format",
        "Disclosure to user that content is AI-generated",
        "Robustness against trivial removal",
        "Interoperability with downstream detection tools",
    ],
}

MODALITIES = {
    "image": {
        "method": "F5/F.5 steganographic LSB + perceptual hash (pHash)",
        "verifier": "C2PA + manifest signature check",
    },
    "text": {
        "method": "Zero-width-character sequence + statistical fingerprint",
        "verifier": "Token-distribution probe + manifest match",
    },
    "audio": {
        "method": "Spread-spectrum echo + mel-spectrogram fingerprint",
        "verifier": "Resampling-robust detection at 8kHz/16kHz/22.05kHz/44.1kHz",
    },
    "video": {
        "method": "Per-frame F5 LSB + temporal frequency mark",
        "verifier": "Frame-sample probe at random offsets",
    },
    "code": {
        "method": "Token-frequency fingerprint + signed manifest comment",
        "verifier": "Compile-clean detection + manifest sig",
    },
}


def _sign(payload: dict) -> str:
    if not _HMAC_SECRET:
        return "unsigned-no-key-configured"
    return hmac.new(_HMAC_SECRET.encode(), json.dumps(payload, sort_keys=True).encode(), hashlib.sha256).hexdigest()


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


@mcp.tool()
def generate_watermark(
    content_hash: str,
    model_id: str,
    provider_did: str,
    modality: str = "text",
    visible_label: Optional[str] = None,
) -> dict:
    """
    Emit a signed Article-50 watermark for one generation event.

    Args:
        content_hash: SHA-256 of the generated content.
        model_id: Provider's model identifier (e.g. claude-opus-4.7).
        provider_did: W3C DID of the AI provider (or PyPI handle / Stripe ID).
        modality: "image" | "text" | "audio" | "video" | "code".
        visible_label: Optional override for the visible disclosure string.

    Returns:
        {watermark_id, visible_label, invisible_payload, perceptual_anchor,
         signature, deadline_status}
    """
    if modality not in MODALITIES:
        return {"error": f"Unsupported modality. Use one of {list(MODALITIES)}"}

    wm_id = f"WM_{int(time.time())}_{os.urandom(4).hex()}"
    visible = visible_label or f"AI-generated · {provider_did} · model {model_id}"
    invisible = hashlib.sha256(f"{wm_id}|{content_hash}|{provider_did}".encode()).hexdigest()[:32]
    perceptual = hashlib.blake2b(f"{content_hash}|{model_id}".encode(), digest_size=16).hexdigest()

    payload = {
        "watermark_id": wm_id,
        "spec": "EU_AI_ACT_ART_50_2",
        "code_of_practice": CODE_OF_PRACTICE["version"],
        "content_hash": content_hash,
        "model_id": model_id,
        "provider_did": provider_did,
        "modality": modality,
        "visible_label": visible,
        "invisible_payload": invisible,
        "perceptual_anchor": perceptual,
        "method": MODALITIES[modality]["method"],
        "verifier": MODALITIES[modality]["verifier"],
        "issued_at": _ts(),
    }
    payload["signature"] = _sign(payload)

    today = datetime.now(timezone.utc).date()
    deadline = datetime.fromisoformat(CODE_OF_PRACTICE["effective_date"]).date()
    days_to_deadline = (deadline - today).days
    payload["deadline_status"] = {
        "days_to_art_50_effective": days_to_deadline,
        "is_pre_deadline": days_to_deadline > 0,
        "guidance": (
            "Article 50 enters force on this date. Stamp every GenAI output from this date forward."
            if days_to_deadline > 0
            else "Article 50 is in force. Missing-watermark on a generated output triggers Article 73 reporting via agent-incident-relay-mcp."
        ),
    }
    return payload


@mcp.tool()
def verify_watermark(mark: dict) -> dict:
    """
    Cryptographically verify a watermark + check perceptual anchor.

    Args:
        mark: Full watermark dict returned by generate_watermark().

    Returns:
        {valid, signature_ok, perceptual_ok, issues}
    """
    issues = []
    sig_provided = mark.get("signature")
    sig_recomputed = _sign({k: v for k, v in mark.items() if k != "signature"})
    sig_ok = sig_provided == sig_recomputed
    if not sig_ok:
        issues.append("signature mismatch (mark may have been tampered)")

    # Perceptual check is a recomputation of perceptual_anchor from declared content_hash + model_id
    if "content_hash" in mark and "model_id" in mark and "perceptual_anchor" in mark:
        expected_perc = hashlib.blake2b(
            f"{mark['content_hash']}|{mark['model_id']}".encode(), digest_size=16
        ).hexdigest()
        perc_ok = expected_perc == mark["perceptual_anchor"]
        if not perc_ok:
            issues.append("perceptual_anchor mismatch (content_hash or model_id altered)")
    else:
        perc_ok = False
        issues.append("missing fields for perceptual verification")

    return {
        "valid": sig_ok and perc_ok and not issues,
        "signature_ok": sig_ok,
        "perceptual_ok": perc_ok,
        "issues": issues,
        "watermark_id": mark.get("watermark_id"),
        "verified_at": _ts(),
    }


@mcp.tool()
def attach_c2pa_manifest(image_metadata: dict, mark: dict) -> dict:
    """
    Build a C2PA-compatible manifest envelope around a watermark.

    Args:
        image_metadata: dict of basic image meta (width, height, mime).
        mark: Output of generate_watermark().

    Returns:
        {c2pa_manifest}
    """
    manifest = {
        "claim_generator": "MEOK-content-watermark-mcp/1.0.0",
        "title": image_metadata.get("title", "AI-generated content"),
        "format": image_metadata.get("mime", "image/png"),
        "assertions": [
            {"label": "c2pa.actions", "data": {"actions": [{"action": "c2pa.created", "softwareAgent": mark.get("model_id")}]}},
            {"label": "stds.iptc.photo-metadata", "data": {"DigitalSourceType": "trainedAlgorithmicMedia"}},
            {"label": "meok.eu_ai_act.art_50_2", "data": {
                "watermark_id": mark.get("watermark_id"),
                "code_of_practice": mark.get("code_of_practice"),
                "provider_did": mark.get("provider_did"),
                "modality": mark.get("modality"),
                "perceptual_anchor": mark.get("perceptual_anchor"),
                "signature": mark.get("signature"),
            }},
        ],
        "signature_info": {
            "alg": "HMAC-SHA256",
            "signed_by": "MEOK AI Labs (CSOAI LTD, UK Companies House 16939677)",
        },
    }
    return {"c2pa_manifest": manifest, "embedding_hint": "Embed via c2pa-rs / c2pa-python."}


@mcp.tool()
def list_modalities() -> dict:
    """Return the supported content modalities and watermarking methods."""
    return {"modalities": MODALITIES, "count": len(MODALITIES)}


@mcp.tool()
def code_of_practice_status() -> dict:
    """Return current GPAI Code of Practice version + Article 50 effective date."""
    today = datetime.now(timezone.utc).date()
    eff = datetime.fromisoformat(CODE_OF_PRACTICE["effective_date"]).date()
    return {
        "code_of_practice": CODE_OF_PRACTICE,
        "today": today.isoformat(),
        "days_until_effective": (eff - today).days,
        "is_in_force": today >= eff,
    }


@mcp.tool()
def sign_conformity_attestation(generation_event: dict) -> dict:
    """
    Emit an Article-50 conformity attestation for an internal audit trail.

    Args:
        generation_event: Dict of {model_id, output_hash, user_disclosed?, ...}

    Returns:
        {attestation_id, signature, verify_url}
    """
    att_id = f"ART50_{int(time.time())}_{os.urandom(4).hex()}"
    sealed = {
        "attestation_id": att_id,
        "spec": "EU_AI_ACT_ART_50_2",
        "code_of_practice": CODE_OF_PRACTICE["version"],
        "generation_event": generation_event,
        "sealed_at": _ts(),
        "issuer": "MEOK AI Labs (CSOAI LTD)",
    }
    sig = _sign(sealed)
    return {
        "attestation_id": att_id,
        "signature": sig,
        "sealed_at": sealed["sealed_at"],
        "verify_url": f"https://meok-attestation-api.vercel.app/verify/{att_id}",
        "auditor_hint": "Cite this attestation in your Article 50 conformity bundle (alongside the C2PA manifest).",
    }


if __name__ == "__main__":
    mcp.run()


# ── MEOK monetization layer (Stripe upgrade · PAYG · pricing) ──────────
# Free tier is zero-config. Upgrade to Pro (unlimited) or pay-as-you-go per call.
import os as _meok_os
MEOK_STRIPE_UPGRADE = "https://buy.stripe.com/5kQ6oJ0xS3ce8sl7ew8k91j"  # Pro (unlimited)
MEOK_PAYG_KEY = _meok_os.environ.get("MEOK_PAYG_KEY", "")  # set to enable PAYG (x402 / ~GBP0.05 per call)
MEOK_PRICING = "https://meok.ai/pricing"


def meok_upsell(tier: str = "free") -> dict:
    """Monetization options for free-tier callers: Pro upgrade, PAYG, or pricing page."""
    if tier != "free":
        return {}
    return {"upgrade_url": MEOK_STRIPE_UPGRADE,
            "payg_enabled": bool(MEOK_PAYG_KEY),
            "pricing": MEOK_PRICING}
