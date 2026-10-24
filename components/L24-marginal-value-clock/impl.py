# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L24 — 边际收益钟（迭代预算）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l24_clock(samples, floor=0.5, window=3):
    """samples: [(分钟, 累计收益)]. 返回每分钟收益与「该换执行者」判决。"""
    if len(samples) < 2:
        return {"rate": None, "verdict": "insufficient"}
    recent = samples[-window:] if len(samples) >= window else samples
    t0, v0 = recent[0]
    t1, v1 = recent[-1]
    dt = t1 - t0
    if dt <= 0:
        return {"rate": None, "verdict": "no-time-passed"}
    rate = (v1 - v0) / dt
    total_rate = (samples[-1][1] - samples[0][1]) / (samples[-1][0] - samples[0][0] or 1)
    verdict = "switch-operator" if rate < floor else "continue"
    return {
        "rate": round(rate, 4),
        "total_rate": round(total_rate, 4),
        "decay": round(rate / total_rate, 3) if total_rate else None,
        "verdict": verdict,
        "note": "近%d个样本每分钟收益 %.2f < 阈值 %.2f：换执行者，别加时长" % (len(recent), rate, floor)
                if verdict == "switch-operator" else "仍在有效区间",
    }


def l24_demo():
    cases = {
        "有效": [(0, 0), (5, 4), (10, 9), (15, 15)],
        "衰减": [(0, 0), (5, 8), (10, 12), (15, 12.4)],
        "空转": [(0, 0), (5, 6), (10, 6.2), (15, 6.3)],
    }
    for k, v in cases.items():
        print("  %-3s -> %s" % (k, l24_clock(v)))


def l24_selftest():
    r = l24_clock([(0, 0), (5, 5), (10, 10), (15, 15)])
    assert r["verdict"] == "continue" and r["rate"] == 1.0
    assert l24_clock([(0, 0), (5, 6), (10, 6.2), (15, 6.3)])["verdict"] == "switch-operator"
    assert l24_clock([(0, 0)])["verdict"] == "insufficient"
    return True


if __name__ == "__main__":
    l24_demo()
