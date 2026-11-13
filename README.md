[![MCP Scorecard: 90/100](https://img.shields.io/badge/proofof.ai-90%2F100-5b21b6)](https://proofof.ai/scorecard/agent-content-watermark-mcp.html)

mcp-name: io.github.CSOAI-ORG/agent-content-watermark-mcp

# Agent Content Watermark MCP

[![MEOK AI Labs](https://img.shields.io/badge/MEOK-AI%20Labs-667eea)](https://meok.ai)
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

## How MEOK charges

MEOK has no subscriptions and no tiers. You pay per job, and only when the agreed artifact has been delivered to you. There is no public price list. See <https://meok.ai/pricing>.

This repository's source is MIT-licensed and free to self-host.

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
