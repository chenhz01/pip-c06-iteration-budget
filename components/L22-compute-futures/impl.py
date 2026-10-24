# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L22 — 计算预算期货（迭代预算）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l22_reserve(rounds_left, cost_samples, safety=0.9):
    """为未来轮次预留：用历史单轮成本的 90 分位 × 剩余轮次 × 安全系数。"""
    if not cost_samples:
        return {"reserve": 0, "per_round": None, "note": "无历史成本，无法预留"}
    s = sorted(cost_samples)
    idx = min(len(s) - 1, int(len(s) * safety))
    p90 = s[idx]
    avg = sum(s) / len(s)
    return {
        "per_round": round(avg, 2),
        "p90": p90,
        "rounds_left": rounds_left,
        "reserve": round(p90 * rounds_left, 2),
        "note": "按 p90 而非均值预留：均值会让一半的轮次预算不够",
    }


def l22_plan(budget, rounds_left, cost_samples, safety=0.9):
    r = l22_reserve(rounds_left, cost_samples, safety)
    spend_now = max(0.0, budget - r["reserve"])
    return {
        "budget": budget,
        "reserve": r["reserve"],
        "can_spend_now": round(spend_now, 2),
        "ratio": round(spend_now / budget, 3) if budget else 0.0,
        "verdict": "tight" if spend_now <= 0 else ("ok" if spend_now / budget >= 0.3 else "starved"),
        "note": r["note"],
    }


def l22_demo():
    costs = [100, 120, 140, 150, 200, 900]
    print(" ", l22_reserve(3, costs))
    for b in (1000, 4000):
        print("  预算%-5d 剩3轮 -> %s" % (b, l22_plan(b, 3, costs)))


def l22_selftest():
    r = l22_reserve(3, [100, 100, 100, 100])
    assert r["reserve"] == 300
    p = l22_plan(1000, 3, [100, 100, 100, 100])
    assert p["can_spend_now"] == 700 and p["verdict"] == "ok"
    assert l22_plan(200, 3, [100, 100])["verdict"] == "tight"
    return True


if __name__ == "__main__":
    l22_demo()
