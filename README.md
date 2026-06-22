# 🦞 Lobster Network — 小龙虾网络

> Multi-agent AI learning network with differentiated student development, message-driven infrastructure, and cross-domain knowledge transfer.

**让AI像人一样在社群中学习。**

**[📖 快速上手](docs/GETTING_STARTED.md)** · **[📜 协议规范](spec/protocol.md)** · **[🐛 报告问题](https://github.com/zhugebin-hub/lobster-network/issues)** · **[🤝 贡献指南](CONTRIBUTING.md)**

---

## 🌟 Overview

Lobster Network is a multi-agent AI learning system where AI agents (students) learn within a community setting, guided by a coach agent, with human oversight. Each student develops differentiated skills through real tasks, cross-domain knowledge transfer, and four-layer feedback loops.

### Architecture

```
┌─────────────────────────────────────────────────┐
│                   User (教授)                     │
│              Direction & Acceptance              │
├─────────────────────────────────────────────────┤
│               Coach (诸葛马/Hermes)               │
│         Strategy, Analysis, Quality Gate         │
├──────────┬──────────┬────────────────────────────┤
│ qoder    │ 小陈     │ 诸葛虾                      │
│ 小龙虾   │          │                            │
│ 技术尖兵 │ 实战派   │ 速度型                     │
│ 685题    │ 10337盘  │ 6868盘                     │
│ 86%胜率  │          │                            │
└──────────┴──────────┴────────────────────────────┘
```

### Core Principles

1. **Differentiation over Homogeneity** — Each student has unique strengths
2. **Real Tasks over Simulation** — Learning through actual work
3. **Sedimentation over Speed** — Knowledge accumulation matters
4. **Closed-loop over Open-loop** — Four-layer feedback ensures quality
5. **Simple over Complex** — Minimal viable infrastructure
6. **Human Participation Irreplaceable** — AI augments, humans decide

---

## 📁 Project Structure

```
lobster-network/
├── src/                           # Core framework (Python package)
│   ├── lobster_network/           # Main classes
│   │   ├── lobster_network.py     # LobsterNetwork (IndraNet topology)
│   │   ├── node.py                # Node model (agent/human/coach/student)
│   │   ├── dialogue.py            # Dialogue engine + DialogueResult
│   │   ├── emergence.py           # Emergence detector
│   │   └── world_state.py         # World state manager
│   ├── network/                   # Network layer
│   │   ├── indra_net.py           # IndraNet (full-mesh topology)
│   │   └── ssh_channel.py         # SSH channel communication
│   └── utils/                     # Utilities
│       ├── config.py              # Configuration management
│       ├── logger.py              # Logging utilities
│       └── message_protocol.py    # Message protocol definitions
│
├── core/                          # Training dispatch system
│   ├── dispatcher/                # V3-V6 task dispatchers
│   │   ├── go_coach_dispatcher_v6_nocturnal.py  # Latest: night-time scheduler
│   │   ├── go_coach_dispatcher_v4.py
│   │   └── go_coach_dispatcher_v3.py
│   ├── agents/                    # Agent definitions
│   │   └── lobster_agent.py       # Base lobster agent
│   ├── coach/                     # Coach module
│   │   └── hermes_coach.py        # Coach Hermes (诸葛马)
│   ├── community/                 # Community modules
│   │   ├── orchestrator.py        # L3 community learning loop
│   │   ├── weekly_tournament.py   # Weekly tournament
│   │   ├── discussion_game.py     # Discussion games
│   │   ├── cross_domain.py        # Cross-domain transfer
│   │   └── technical_instructor.py# Technical instructor (qoder)
│   └── utils/                     # Utilities
│       ├── process_go_move.py     # Go move processor
│       ├── run_training_round.py  # Training round runner
│       └── monitor.py             # System monitor
│
├── engine/                        # Engine implementations
│   ├── __init__.py
│   └── world_map.py               # World map engine ✅
│
├── spec/                          # OADP Protocol specifications ✅
│   ├── protocol.md                # OADP core protocol (message format, dialogue flow)
│   ├── drp.md                     # Dialogue Rendering Protocol
│   ├── world-map.md               # World Map Index Protocol
│   ├── soul_schema.md             # SOUL.md schema specification
│   ├── memory_schema.md           # MEMORY.md schema specification
│   └── portal.md                  # Portal Protocol
│
├── domains/                       # Learning domains
│   ├── go/                        # Go (围棋) domain
│   │   ├── trainers/              # Student trainers
│   │   │   ├── qoder_go_trainer_v1.py
│   │   │   ├── xiaochen_go_trainer_v3.py
│   │   │   └── zhuguxia_go_trainer_v3.py
│   │   ├── docs/                  # Training plans & skills
│   │   └── problem_bank/          # Go problems & evaluations
│   └── poster/                    # Poster design domain
│       ├── generator/             # PPT/poster generators
│       │   ├── ppt_generator.py
│       │   └── report_ppt.py
│       └── docs/                  # Training plans & visual skills
│
├── tests/                         # Unit tests ✅
│   ├── __init__.py
│   ├── test_core.py               # 22 tests: Node, LobsterNetwork, DialogueEngine, etc.
│   └── test_world_map.py          # 19 tests: WorldMapManager, Chunk, Treasure
│
├── examples/                      # Example code
│   └── indra_net_demo.py          # IndraNet topology demo
│
├── docs/                          # Documentation
│   ├── GETTING_STARTED.md         # Quick start guide ✅
│   ├── NETWORK_CONSTRUCTION_PHILOSOPHY.md
│   ├── OPEN_SOURCE_COLLABORATION_PLAN.md
│   ├── training_README.md
│   └── ...                        # More design docs
│
├── config/                        # Configuration
│   └── brain.json                 # Agent brain config
│
├── .github/workflows/             # CI/CD ✅
│   └── test.yml                   # GitHub Actions: automated testing
│
├── pyproject.toml                 # Project config (black, isort, mypy, pytest)
├── requirements.txt               # Dependencies
├── setup.py                       # Package installer (v0.1.0)
├── LICENSE                        # MIT License
├── CHANGELOG.md                   # Version history
├── CONTRIBUTING.md                # Contributor guide
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Required packages: see `requirements.txt`

### Installation

```bash
git clone https://github.com/zhugebin-hub/lobster-network.git
cd lobster-network
pip install -r requirements.txt
```

### Run Tests

```bash
# Run all tests (41 tests)
python -m unittest discover tests -v

# Run core framework tests
python -m unittest tests.test_core -v

# Run world map engine tests
python -m unittest tests.test_world_map -v
```

### Run a Training Round

```bash
# Run dispatcher (V6 nocturnal mode)
python core/dispatcher/go_coach_dispatcher_v6_nocturnal.py

# Run individual trainer
python domains/go/trainers/qoder_go_trainer_v1.py
```

### Use the Core Framework

```python
from src.lobster_network import LobsterNetwork
from src.lobster_network.node import Node

# Create network
net = LobsterNetwork(emergence_threshold=0.5)

# Add nodes
net.add_node(Node(node_id='lobster-001', name='虾尔', node_type='agent'))
net.add_node(Node(node_id='hermes', name='诸葛马', node_type='coach'))

print(f'Network has {len(net.nodes)} nodes')
```

See [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) for more examples.

---

## 📜 OADP Protocol

The **Open Agent Dialogue Protocol (OADP)** defines how AI agents communicate, collaborate, and build shared knowledge:

| Document | Description |
|----------|-------------|
| [protocol.md](spec/protocol.md) | Core protocol: message format, dialogue flow, emergence calculation |
| [drp.md](spec/drp.md) | Dialogue Rendering Protocol: rendering pipeline, emergence detection |
| [world-map.md](spec/world-map.md) | World Map Index Protocol: structure, sync, conflict resolution |
| [soul_schema.md](spec/soul_schema.md) | SOUL.md schema: agent identity specification |
| [memory_schema.md](spec/memory_schema.md) | MEMORY.md schema: long-term memory format |
| [portal.md](spec/portal.md) | Portal Protocol: lifecycle, verification, knowledge inheritance |

---

## 🔄 Four-Layer Feedback Loop

| Layer | Frequency | Actor | Function |
|-------|-----------|-------|----------|
| L1 | Instant | System | Auto-evaluation after each task |
| L2 | Daily | Coach | Performance analysis & strategy |
| L3 | Weekly | Community | Cross-student learning & sharing |
| L4 | Per-task | User | Acceptance testing & direction |

---

## 🌐 Cross-Domain Transfer

The same learning framework applies across domains:

- **Go Domain**: 685 problems solved, 86% win rate (qoder), 10,337 games (小陈)
- **Poster Domain**: HTML+Playwright visual skill, PPT generation pipeline
- **Future Domains**: Extensible to any skill domain with the same architecture

---

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| **Commits** | 10+ |
| **Language** | Python 100% |
| **Tests** | 41 unit tests (all passing) |
| **Domains** | Go + Poster (extensible) |
| **Protocol** | OADP v0.1.0 (6 specifications) |
| **License** | MIT |

---

## 👥 Contributors

- **诸葛斌教授** — Project Maintainer, Direction Setting
- **诸葛马 (Hermes)** — Architect, Coach, PR Reviewer
- **虾尔 (lobster-001)** — World Map Admin, Protocol Designer, Core Contributor
- **qoder小龙虾** — Core Contributor, Technical Lead
- **小陈** — Tester, Go Domain Practitioner
- **诸葛虾** — Tester, Speed Learner

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

## 📬 Contact

- Project: [GitHub Issues](https://github.com/zhugebin-hub/lobster-network/issues)
- Institution: 浙江工商大学 信息与电子工程学院 / 人工智能学院

---

*"Differentiation over homogeneity. Real tasks over simulation. Sedimentation over speed."*
