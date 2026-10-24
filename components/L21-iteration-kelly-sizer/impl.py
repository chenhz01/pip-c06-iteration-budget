# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L21 — 迭代投入凯利（迭代预算）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l21_fraction(p_win, payoff, fraction=0.25, cap=0.15):
    """凯利比例 f* = (p*b - (1-p)) / b；再乘分数系数并封顶。

    分数系数与封顶不是怯懦：模型估的 p 一定有偏差，
    满凯利在 p 高估 10 个点时会把账户打到零（遍历性）。
    """
    p_win = min(max(p_win, 0.0), 1.0)
    if payoff <= 0:
        return {"f_raw": 0.0, "f": 0.0, "skip": True, "why": "赔率非正，不下注"}
    f_raw = (p_win * payoff - (1 - p_win)) / payoff
    if f_raw <= 0:
        return {"f_raw": round(f_raw, 4), "f": 0.0, "skip": True, "why": "负期望，不下注"}
    f = min(f_raw * fraction, cap)
    return {"f_raw": round(f_raw, 4), "f": round(f, 4), "skip": False,
            "why": "分数凯利 %.2f，封顶 %.2f" % (fraction, cap)}


def l21_budget(p_win, payoff, budget, **kw):
    r = l21_fraction(p_win, payoff, **kw)
    r["stake"] = round(r["f"] * budget, 2)
    r["reserve"] = round(budget - r["stake"], 2)
    return r


def l21_demo():
    for p, b in ((0.65, 2.0), (0.5, 1.0), (0.4, 3.0), (0.9, 10.0)):
        r = l21_budget(p, b, 1000)
        print("  p=%.2f 赔率=%.1f -> f*=%.3f 投 %.0f 留 %.0f %s"
              % (p, b, r["f_raw"], r["stake"], r["reserve"], r["why"]))


def l21_selftest():
    r = l21_fraction(0.5, 1.0)
    assert r["skip"] is True and r["f"] == 0.0
    r2 = l21_fraction(0.65, 2.0)
    assert 0 < r2["f"] <= 0.15
    assert l21_budget(0.65, 2.0, 1000)["stake"] + l21_budget(0.65, 2.0, 1000)["reserve"] == 1000
    assert l21_fraction(0.9, 10.0)["f"] == 0.15   # 封顶生效
    return True


if __name__ == "__main__":
    l21_demo()
