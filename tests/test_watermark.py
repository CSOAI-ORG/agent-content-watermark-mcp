"""Smoke tests for agent-content-watermark-mcp."""
import sys, os, inspect, traceback, hashlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import (
    generate_watermark,
    verify_watermark,
    attach_c2pa_manifest,
    list_modalities,
    code_of_practice_status,
    sign_conformity_attestation,
    CODE_OF_PRACTICE,
)


def _content_hash(content="hello world"):
    return hashlib.sha256(content.encode()).hexdigest()


def test_generate_returns_watermark_id():
    r = generate_watermark(_content_hash(), "claude-opus-4.7", "did:meok:csoai-org", "text")
    assert r["watermark_id"].startswith("WM_")
    assert r["spec"] == "EU_AI_ACT_ART_50_2"


def test_generate_text_modality():
    r = generate_watermark(_content_hash(), "claude-opus-4.7", "did:meok:csoai-org", "text")
    assert r["modality"] == "text"
    assert "zero-width" in r["method"].lower()


def test_generate_image_modality():
    r = generate_watermark(_content_hash(), "model-x", "did:meok:y", "image")
    assert "F5" in r["method"] or "F.5" in r["method"]
    assert "C2PA" in r["verifier"]


def test_generate_unknown_modality():
    r = generate_watermark(_content_hash(), "model-x", "did:meok:y", "smell")
    assert "error" in r


def test_verify_round_trip():
    ch = _content_hash()
    mark = generate_watermark(ch, "claude-opus-4.7", "did:meok:csoai-org", "text")
    v = verify_watermark(mark)
    assert v["signature_ok"] is True
    assert v["perceptual_ok"] is True


def test_verify_detects_tampering():
    ch = _content_hash()
    mark = generate_watermark(ch, "claude-opus-4.7", "did:meok:csoai-org", "text")
    mark["content_hash"] = "tampered"  # change content but signature stays
    v = verify_watermark(mark)
    assert v["valid"] is False


def test_attach_c2pa_manifest_includes_art50():
    mark = generate_watermark(_content_hash(), "claude-opus-4.7", "did:meok:csoai-org", "image")
    c = attach_c2pa_manifest({"mime": "image/png", "title": "test"}, mark)
    labels = [a["label"] for a in c["c2pa_manifest"]["assertions"]]
    assert any("art_50_2" in l for l in labels)


def test_list_modalities():
    r = list_modalities()
    assert "image" in r["modalities"]
    assert "text" in r["modalities"]
    assert r["count"] == 5


def test_code_of_practice_status():
    r = code_of_practice_status()
    assert r["code_of_practice"]["version"] == CODE_OF_PRACTICE["version"]
    assert "days_until_effective" in r


def test_sign_conformity_attestation():
    r = sign_conformity_attestation({"model_id": "claude-opus-4.7", "output_hash": "x"})
    assert r["attestation_id"].startswith("ART50_")
    assert "verify_url" in r


if __name__ == "__main__":
    g = dict(globals())
    fns = [v for k, v in g.items() if k.startswith("test_") and inspect.isfunction(v)]
    p = f = 0
    for fn in fns:
        try:
            fn(); print(f"OK {fn.__name__}"); p += 1
        except Exception as e:
            print(f"X  {fn.__name__}: {type(e).__name__}: {e}"); traceback.print_exc(); f += 1
    print(f"\n{p} passed, {f} failed")
