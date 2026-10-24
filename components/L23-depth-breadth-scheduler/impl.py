# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L23 — 深挖与铺开调度（迭代预算）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l23_allocate(lines, budget, min_each=0):
    """lines: [{"id","marginal","spent"}]. 按边际收益贪心分配，记录每线投入。

    贪心不是最优，但它是唯一能在不知道全局曲线时仍可解释的分法：
    每一份预算都必须能说出「为什么给它」。
    """
    remain = budget
    alloc = {l["id"]: 0 for l in lines}
    for l in lines:
        if min_each and remain >= min_each * len(lines):
            alloc[l["id"]] += min_each
            remain -= min_each
    order = sorted(lines, key=lambda l: -l["marginal"])
    if not order:
        return {"alloc": alloc, "left": remain, "order": [], "verdict": "no-lines"}
    unit = max(1, remain // max(1, len(order)))
    for l in order:
        take = min(unit, remain)
        alloc[l["id"]] += take
        remain -= take
    best = order[0]["id"]
    return {
        "alloc": alloc,
        "left": remain,
        "order": [l["id"] for l in order],
        "verdict": "single-line" if len(order) > 1 and order[0]["marginal"] > 3 * order[1]["marginal"] else "balanced",
        "advice": "下一轮优先深挖 %s（边际 %.2f）；其余保持最小投入" % (best, order[0]["marginal"]),
    }


def l23_demo():
    lines = [{"id": "A", "marginal": 9.0}, {"id": "B", "marginal": 2.0}, {"id": "C", "marginal": 0.5}]
    r = l23_allocate(lines, 900)
    print("  分配:", r["alloc"], "剩余", r["left"], "->", r["verdict"])
    print(" ", r["advice"])


def l23_selftest():
    r = l23_allocate([{"id": "A", "marginal": 9}, {"id": "B", "marginal": 2}], 900)
    assert r["order"] == ["A", "B"] and sum(r["alloc"].values()) + r["left"] == 900
    assert r["verdict"] == "single-line"
    r2 = l23_allocate([{"id": "A", "marginal": 3}, {"id": "B", "marginal": 2.5}], 100)
    assert r2["verdict"] == "balanced"
    assert l23_allocate([], 100)["verdict"] == "no-lines"
    return True


if __name__ == "__main__":
    l23_demo()
