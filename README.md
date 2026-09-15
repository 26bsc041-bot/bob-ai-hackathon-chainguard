# 🚀 ChainGuard AI

> Supply Chain Disruption Assistant & Fleet Utilisation Optimizer

---

## 👥 Team

| Field | Value |
|---|---|
| **Team Name** | ChainGuard |
| **Track** | AI |
| **Team Lead** | Neev Jain — 26bsc041@charusat.edu.in |
| **Members** | Prinidh Pandit, Palak Chauhan, Tirtha Pandya |

---

## 🎯 Problem Statement

Supply chains can be disrupted by road closures, weather, accidents, delays, and fleet availability issues. Operations teams need a simple way to identify high-risk shipments, understand disruption impact, and take faster corrective action.

---

## 💡 Solution

ChainGuard AI is a Streamlit-based supply chain operations assistant that analyses shipment risk, disruption impact, fleet availability, and cold-chain conditions. It provides operational insights and recommendations through an AI-style operations copilot.

---

## ✨ Key Features

- **Shipment Risk Scoring:** Identifies and prioritises high-risk and critical shipments.
- **Disruption Impact Analysis:** Helps operations teams understand how disruptions can affect shipments.
- **Fleet Utilisation:** Identifies idle or available vehicles that can be considered for redeployment.
- **Cold-Chain Monitoring:** Displays temperature conditions for temperature-sensitive shipments.
- **AI Copilot:** Provides operational insights for fleet availability and shipments requiring immediate attention.

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| **Languages** | Python |
| **Frameworks** | Streamlit, Pandas |
| **IBM Technologies** | IBM Bob |
| **Databases** | None |
| **Other** | GitHub Actions |

---

## 📁 Repository Structure

```text
├── src/                  # Application source code
├── docs/                 # Written documentation
│   ├── problem-statement.md
│   ├── solution-overview.md
│   ├── architecture.md
│   └── setup-guide.md
├── demo/                 # Demo artifacts
│   ├── screenshots/      # App screenshots
│   ├── demo-video-link.txt
│   └── live-demo-url.txt
├── presentation/         # Presentation materials
└── submission.yaml       # Structured submission metadata
## ⚡ How to Run


# 1. Clone the repo
git clone https://github.com/26bsc041-bot/bob-ai-hackathon-chainguard.git
cd bob-ai-hackathon-chainguard

# 2. Install dependencies
pip install streamlit pandas

# 4. Run the project
streamlit run src/app.py

## 🖥️ Demo

| Artifact | Link |
|---|---|
| 📹 Demo Video | [See demo/demo-video-link.txt](demo/demo-video-link.txt) |
| 🌐 Live Demo | [See demo/live-demo-url.txt](demo/live-demo-url.txt) |
| 🖼️ Screenshots | [See demo/screenshots/](demo/screenshots/) |
| 📊 Presentation | [See presentation/slides.pdf](presentation/) |

---

## ⚠️ Known Limitations

The current MVP uses simulated demonstration data.
It does not yet connect to live logistics systems or real-time vehicle tracking.
External IoT temperature sensors and production logistics feeds are not currently integrated.
The AI Copilot currently provides rule-based operational insights rather than a production AI model.

---

## 🏅 What We're Most Proud Of

We are most proud of building a complete supply-chain operations dashboard that combines shipment risk, disruption analysis, fleet utilisation, cold-chain monitoring, and an AI-style operations copilot in one simple interface.
The MVP demonstrates how operations teams can identify urgent shipments, understand disruption impact, and make faster fleet-related decisions.
---
