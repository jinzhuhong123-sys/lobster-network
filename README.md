# 🦞 Lobster Network — 小龙虾网络

> Multi-agent AI learning network with differentiated student development, message-driven infrastructure, and cross-domain knowledge transfer.

**让AI像人一样在社群中学习。**

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

## 📁 Project Structure

```
lobster-network/
├── core/                          # Core infrastructure
│   ├── dispatcher/                # V3-V6 task dispatchers
│   │   ├── go_coach_dispatcher_v6_nocturnal.py  # Latest: night-time scheduler
│   │   ├── go_coach_dispatcher_v4.py
│   │   └── go_coach_dispatcher_v3.py
│   ├── agents/                    # Agent definitions
│   │   └── lobster_agent.py       # Base lobster agent
│   ├── coach/                     # Coach module
│   │   └── hermes_coach.py        # Coach Hermes (诸葛马)
│   └── utils/                     # Utilities
│       ├── process_go_move.py     # Go move processor
│       ├── run_training_round.py  # Training round runner
│       └── monitor.py             # System monitor
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
├── docs/                          # Documentation
│   ├── NETWORK_CONSTRUCTION_PHILOSOPHY.md
│   ├── OPEN_SOURCE_COLLABORATION_PLAN.md
│   └── training_README.md
├── config/                        # Configuration
│   └── brain.json                 # Agent brain config
└── tests/                         # Tests (to be added)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- SSH access to the training server
- Required packages: `openai`, `requests`, `playwright`

### Installation

```bash
git clone https://github.com/zhugebin-hub/lobster-network.git
cd lobster-network
pip install -r requirements.txt
```

### Run a Training Round

```bash
# Run dispatcher (V6 nocturnal mode)
python core/dispatcher/go_coach_dispatcher_v6_nocturnal.py

# Run individual trainer
python domains/go/trainers/qoder_go_trainer_v1.py
```

## 🔄 Four-Layer Feedback Loop

| Layer | Frequency | Actor | Function |
|-------|-----------|-------|----------|
| L1 | Instant | System | Auto-evaluation after each task |
| L2 | Daily | Coach | Performance analysis & strategy |
| L3 | Weekly | Community | Cross-student learning & sharing |
| L4 | Per-task | User | Acceptance testing & direction |

## 🌐 Cross-Domain Transfer

The same learning framework applies across domains:

- **Go Domain**: 685 problems solved, 86% win rate (qoder), 10,337 games (小陈)
- **Poster Domain**: HTML+Playwright visual skill, PPT generation pipeline
- **Future Domains**: Extensible to any skill domain with the same architecture

## 👥 Contributors

- **诸葛斌教授** — Project Maintainer, Direction Setting
- **诸葛马 (Hermes)** — Domain Expert, Coach, PR Reviewer
- **qoder小龙虾** — Core Contributor, Technical Lead
- **小陈** — Tester, Go Domain Practitioner
- **诸葛虾** — Tester, Speed Learner

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

## 📬 Contact

- Project: [GitHub Issues](https://github.com/zhugebin-hub/lobster-network/issues)
- Institution: 浙江工商大学 信息与电子工程学院 / 人工智能学院

---

*"Differentiation over homogeneity. Real tasks over simulation. Sedimentation over speed."*
