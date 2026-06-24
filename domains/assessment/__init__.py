"""
8维度能力评估 — 域级入口 (Domain-level Entry)

实际实现位于 src/lobster_network/assessment/，此文件仅为便捷重导出。
使用:
    from lobster_network.assessment import EightDimEngine, DimensionProfile
"""

# 从框架层重导出
try:
    from lobster_network.assessment import (  # noqa: F401
        EightDimEngine, AssessmentResult,
        DimensionProfile, Dimension,
        ClawvardBridge, PracticeSession,
        DIMENSION_REGISTRY, DIMENSION_DESCRIPTIONS, DIMENSION_WEIGHTS,
    )
except ImportError:
    pass  # 框架层未安装时静默跳过

__all__ = [
    "EightDimEngine", "AssessmentResult",
    "DimensionProfile", "Dimension",
    "ClawvardBridge", "PracticeSession",
    "DIMENSION_REGISTRY", "DIMENSION_DESCRIPTIONS", "DIMENSION_WEIGHTS",
]
