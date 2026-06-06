mcp-name: io.github.CSOAI-ORG/agent-content-watermark-mcp

# Agent Content Watermark MCP

[![MEOK AI Labs](https://img.shields.io/badge/MEOK-AI%20Labs-667eea)](https://meok.ai)
[![EU AI Act](https://img.shields.io/badge/EU%20AI%20Act-Compliant-22c55e)](https://councilof.ai)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-Install-3775a9)](https://pypi.org/project/agent_content_watermark_mcp/)

> Agent Content Watermark MCP - dedicated EU AI Act Article 50(2) GenAI watermarking with C2PA mani...

Agent Content Watermark MCP - dedicated EU AI Act Article 50(2) GenAI watermarking with C2PA manifest envelope. MIT. By MEOK AI Labs.

---

## 🚀 Quick Start

```bash
# Install via pip
pip install agent_content_watermark_mcp

# Or install via Smithery
npx -y @smithery/cli@latest install agent-content-watermark-mcp --client claude
```

## ✨ Features

- AI content watermarking
- Article 50 compliance
- Detection & verification
- Batch processing
- API integration

## 📖 Documentation

- [Full Documentation](https://docs.meok.ai/agent-content-watermark-mcp)
- [API Reference](https://api.meok.ai)
- [EU AI Act Compliance Guide](https://councilof.ai/compliance)

## 🛡️ Compliance

This MCP server is built with **EU AI Act compliance** built-in:

- ✅ Article 9 — Risk Management System
- ✅ Article 13 — Transparency & Instructions for Use
- ✅ Article 15 — Bias Detection & Testing
- ✅ Article 26 — FRIA Support (where applicable)
- ✅ Article 50 — AI Content Watermarking (where applicable)

Need help getting compliant? **[Book a free 15-min diagnostic →](https://cal.com/csoai/august-audit)**

## 🏢 Enterprise

Need custom development, SLA guarantees, or white-label deployment?

- **Pro:** $99/mo — Full MCP suite + EU AI Act tracking
- **Enterprise:** $499/mo — Custom dev + SLA + Dedicated support

[View Pricing →](https://councilof.ai/pricing) | [Contact Sales →](mailto:sales@csoai.org)

## 🤝 Part of the MEOK Ecosystem

This server is part of the **[MEOK AI Labs](https://meok.ai)** ecosystem — 300+ MCP servers for sovereign AI governance.

| Domain | Purpose |
|--------|---------|
| [councilof.ai](https://councilof.ai) | EU AI Act compliance marketplace |
| [safetyof.ai](https://safetyof.ai) | AI safety & monitoring |
| [meok.ai](https://meok.ai) | Sovereign AI platform |
| [cobolbridge.ai](https://cobolbridge.ai) | Legacy modernization |

## 📜 License

MIT © [CSOAI-ORG](https://github.com/CSOAI-ORG)

---

<p align="center">
  <sub>Built with 💜 by <a href="https://meok.ai">MEOK AI Labs</a> · UK Companies House 16939677</sub>
</p>
## Licence

MIT. By [MEOK AI Labs](https://meok.ai) (CSOAI LTD, UK Companies House 16939677).

<!-- BUY-LADDER:START -->

## 💸 Try MEOK in 30 seconds — instant buy ladder

| Tier | Price | What you get | Stripe |
|---|---|---|---|
| Smoke test | **£1** | Signed sample MCP-Hardening report + Article 50 PDF | <https://buy.stripe.com/dRmcN75ScdQS7oh1Uc8k90U> |
| Quick Kit | **£9** | EU AI Act Article 50 implementation guide (C2PA + EU-Icon) | <https://buy.stripe.com/cNi00la8s1460ZT0Q88k90V> |
| Founder Call | **£29** | 30-min 1-on-1 with the founder | <https://buy.stripe.com/8x228ta8s6oqbExaqI8k90W> |

> Refundable. UK Stripe — VAT-clean. Builds on the 81-MCP MEOK fleet.
> Verify any signed report at <https://meok.ai/verify>.

<!-- BUY-LADDER:END -->


## Configuration

Add to your `claude_desktop_config.json` (Claude Desktop) or your MCP client config:

```json
{
  "mcpServers": {
    "agent-content-watermark-mcp": {
      "command": "uvx",
      "args": ["agent-content-watermark-mcp"]
    }
  }
}
```

Or: `pip install agent-content-watermark-mcp` then run the `agent-content-watermark-mcp` command (stdio transport).

## Examples

Once configured, ask your assistant, for example:
- "Use `generate_watermark` to …"
- "Use `verify_watermark` to …"
- "Use `attach_c2pa_manifest` to …"
