# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L24 selftest — 断言写在实现旁边，改坏了立刻红。"""
import impl


def main():
    impl.l24_selftest()
    print("PASS L24 marginal-value-clock")


if __name__ == "__main__":
    main()
