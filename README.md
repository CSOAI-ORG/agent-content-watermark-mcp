# Agent Content Watermark MCP

> ## 🧱 Part of the MEOK Governance Substrate (£499/mo)
> See [meok.ai/article-50-kit](https://meok.ai/article-50-kit).

# EU AI Act Article 50(2) GenAI watermarking — dedicated MCP

<!-- mcp-name: io.github.CSOAI-ORG/agent-content-watermark-mcp -->

[![PyPI](https://img.shields.io/pypi/v/agent-content-watermark-mcp)](https://pypi.org/project/agent-content-watermark-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## What this does

Article 50(2) of the EU AI Act ([Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)) requires providers of GenAI systems to mark outputs in a **machine-readable format detectable as artificially generated**.

Effective: **2 November 2026** (post-Omnibus delay).

This MCP handles the watermark side dedicatedly — distinct from the broader C2PA provenance work in `watermarking-authenticity-mcp`. It produces three layers per the GPAI Code of Practice:

1. **Visible label** — human-readable disclosure (`AI-generated · <provider> · model <id>`)
2. **Invisible payload** — modality-specific stego (F5 LSB for image, zero-width for text, spread-spectrum for audio, etc.)
3. **Perceptual anchor** — survives compression / crop / mild edits

## Tools

| Tool | Purpose |
|---|---|
| `generate_watermark(content_hash, model_id, provider_did, modality)` | Emit signed mark |
| `verify_watermark(mark)` | Cryptographic + perceptual verification |
| `attach_c2pa_manifest(image_metadata, mark)` | Build C2PA envelope |
| `list_modalities()` | 5 supported: image · text · audio · video · code |
| `code_of_practice_status()` | Current GPAI CoP version + days until 2 Nov 2026 |
| `sign_conformity_attestation(generation_event)` | Article-50 attestation for audit |

## Why this exists

Watermarking is one of the few Article 50 obligations that has *no native tooling* in most agent stacks. Providers building on Claude / GPT / Gemini are responsible — those models don't ship watermarks by default.

Missing-watermark on a generated output triggers Article 73 reporting via [`agent-incident-relay-mcp`](https://github.com/CSOAI-ORG/agent-incident-relay-mcp).

## Sister MCPs

- `watermarking-authenticity-mcp` — broader C2PA + Article 50 + Article 73 dispatch
- `eu-ai-act-compliance-mcp` — Article 50 text + thresholds
- `agent-incident-relay-mcp` — missing-watermark incident broadcaster
- `mcp-spec-compliance-mcp` — ensure your own MCP server.json passes audit

Full catalogue: [meok.ai/anthropic-registry](https://meok.ai/anthropic-registry)

## Pricing

| Option | Price |
|---|---|
| Self-host MIT | £0 |
| Universal PAYG | £29/mo + £0.0002/call |
| Governance Substrate | £499/mo |
| A2A Substrate | £999/mo |
| Defence | £4,990/mo |

Buy: https://meok.ai/governance

## Licence

MIT. By [MEOK AI Labs](https://meok.ai) (CSOAI LTD, UK Companies House 16939677).
