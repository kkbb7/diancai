#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""终端打字练习工具 — 支持中英文，统计速度和准确率。"""

import time
import random
import sys
import os

if os.name == "nt":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ── 练习文本库 ──────────────────────────────────────────────

EN_TEXTS = {
    "easy": [
        "the quick brown fox jumps over the lazy dog",
        "all good things come to those who wait",
        "practice makes perfect every single day",
        "the early bird catches the worm at dawn",
        "keep it simple and stupid is the key",
        "a journey of a thousand miles begins with a single step",
        "life is what happens when you are busy making other plans",
        "the only way to do great work is to love what you do",
        "it does not matter how slowly you go as long as you do not stop",
    ],
    "medium": [
        "The quick brown fox jumps over the lazy dog near the riverbank.",
        "Debugging is twice as hard as writing the code in the first place.",
        "Any fool can write code that a computer can understand; good programmers write code that humans can understand.",
        "First, solve the problem. Then, write the code. Never confuse the two.",
        "Measuring programming progress by lines of code is like measuring aircraft building progress by weight.",
        "Simplicity is prerequisite for reliability. Complex systems fail in complex ways.",
    ],
    "hard": [
        "The five boxing wizards jump quickly. Pack my box with five dozen liquor jugs. How vexingly quick daft zebras jump!",
        "Python's `collections.deque` provides O(1) popleft() — use it when you need a FIFO queue. For LIFO, a plain list with pop() suffices.",
        "To thoroughly troubleshoot intermittent connectivity issues, systematically examine firewall configurations, DNS resolution, and TLS certificate chains across all intermediary proxies.",
    ],
}

ZH_TEXTS = {
    "easy": [
        "今天天气真好，适合出去走走。",
        "学习编程需要耐心和坚持。",
        "一杯咖啡，一本好书，一个下午。",
        "每天进步一点点，日积月累就会有大变化。",
        "世界上最遥远的距离，不是生与死，而是我在你面前，你却在玩手机。",
        "山海自有归期，风雨自有相逢。",
        "星光不问赶路人，时光不负有心人。",
        "愿你出走半生，归来仍是少年。",
        "人间烟火气，最抚凡人心。",
        "所有的相遇，都是久别重逢。",
    ],
    "medium": [
        "生活不止眼前的苟且，还有诗和远方的田野。你赤手空拳来到人世间，为找到那片海不顾一切。",
        "我们听过无数的道理，却仍旧过不好这一生。这世上所有的久处不厌，都是因为用心。",
        "你要做一个不动声色的大人了。不准情绪化，不准偷偷想念，不准回头看。去过自己另外的生活。",
        "年轻时总以为能遇上许许多多的人，而后你就明白，所谓机缘，不过就那么几次。",
        "如果有来生，要做一棵树，站成永恒，没有悲欢的姿势。一半在尘土里安详，一半在风里飞扬。",
        "我行过许多地方的桥，看过许多次数的云，喝过许多种类的酒，却只爱过一个正当最好年龄的人。",
    ],
    "hard": [
        "而世之奇伟、瑰怪、非常之观，常在于险远，而人之所罕至焉，故非有志者不能至也。尽吾志也而不能至者，可以无悔矣，其孰能讥之乎？",
        "我从小就喜欢下雨，若某个傍晚暴雨狂风，便是我来看你。暴雨吹倒教学楼，压断白杨树，闪电击中信号塔，世界末日来临之际，我便跨越山海，穿过人潮，来到你身边。",
        "你知道吗？我年轻的时候想做许多事，我想谈恋爱、周游世界，就是人们年轻的时候都想做的那些事。可是这些事我一件都没做成。你知道为什么吗？因为每当我想做什么事的时候，总有一件别的事冒出来，把我牵住了。",
    ],
}


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def show_banner():
    print("""
  +====================================+
  |       [~] 终 端 打 字 练 习       |
  |          typing trainer            |
  +====================================+
  """)


def choose_mode():
    print("  选择语言 / Select language:")
    print("    1. 中文")
    print("    2. English")
    print("    3. 混合 / Mixed")
    while True:
        ch = input("\n  输入选择 (1/2/3): ").strip()
        if ch == "1":
            return "zh"
        elif ch == "2":
            return "en"
        elif ch == "3":
            return "mixed"
        else:
            print("  请输入 1、2 或 3")


def choose_level():
    print("\n  选择难度 / Difficulty:")
    print("    1. 简单 / Easy")
    print("    2. 中等 / Medium")
    print("    3. 困难 / Hard")
    while True:
        ch = input("\n  输入选择 (1/2/3): ").strip()
        if ch == "1":
            return "easy"
        elif ch == "2":
            return "medium"
        elif ch == "3":
            return "hard"
        else:
            print("  请输入 1、2 或 3")


def calculate_cpm(correct_chars, seconds):
    """字/分钟"""
    if seconds <= 0:
        return 0
    return round(correct_chars / (seconds / 60))


def highlight_errors(target, user_input):
    """绿色=正确, 红色=错误"""
    result = []
    GREEN_BG = "\033[42m"
    RED_BG = "\033[41m"
    RESET = "\033[0m"
    tl, ul = len(target), len(user_input)
    for i in range(max(tl, ul)):
        if i >= ul:
            result.append(f"{RED_BG}{target[i]}{RESET}")
        elif i >= tl:
            result.append(f"{RED_BG}{user_input[i]}{RESET}")
        elif user_input[i] == target[i]:
            result.append(f"{GREEN_BG}{user_input[i]}{RESET}")
        else:
            result.append(f"{RED_BG}{user_input[i]}{RESET}")
    return "".join(result)


def one_round(mode, level):
    if mode == "zh":
        text = random.choice(ZH_TEXTS[level])
    elif mode == "en":
        text = random.choice(EN_TEXTS[level])
    else:
        pool = ZH_TEXTS[level] + EN_TEXTS[level]
        text = random.choice(pool)

    clear()
    show_banner()
    print(f"  模式: {mode}  |  难度: {level}  |  按 Enter 开始计时\n")
    print("  " + "-" * 60)
    print(f"  {text}")
    print("  " + "-" * 60)

    input("\n  准备好了就按 Enter...")

    clear()
    show_banner()
    print(f"\n  >>> 开始! 输入以下内容后按 Enter:\n")
    print(f"  {text}\n")

    start = time.time()
    user_input = input("  > ")
    elapsed = time.time() - start

    correct = 0
    for i in range(min(len(text), len(user_input))):
        if user_input[i] == text[i]:
            correct += 1

    total_chars = len(text)
    accuracy = (correct / total_chars * 100) if total_chars > 0 else 0
    cpm = calculate_cpm(correct, elapsed)

    clear()
    show_banner()
    print(f"\n  ============ 本局结果 ============\n")
    print(f"  用时:     {elapsed:.1f}s")
    print(f"  速度:     {cpm} 字/分钟")
    print(f"  正确率:   {accuracy:.1f}%")
    print(f"\n  逐字对比 (绿=对  红=错):\n")
    print(f"  {highlight_errors(text, user_input)}")

    return correct, elapsed, total_chars


def main():
    clear()
    show_banner()
    print("  每次练习一句话，打完看速度和正确率。\n")

    mode = choose_mode()
    level = choose_level()

    total_correct = 0
    total_time = 0
    rounds = 0

    while True:
        correct, elapsed, total = one_round(mode, level)
        total_correct += correct
        total_time += elapsed
        rounds += 1

        avg_cpm = calculate_cpm(total_correct, total_time) if total_time > 0 else 0
        print(f"\n  ============ 累计 ({rounds} 局) ============")
        print(f"  总用时:      {total_time:.0f}s")
        print(f"  平均速度:    {avg_cpm} 字/分钟")
        print(f"  总正确字数:  {total_correct}")
        print("  " + "-" * 40)

        cmd = input("\n  继续 (Enter) / 换难度 (d) / 退出 (q): ").strip().lower()
        if cmd == "q":
            print(f"\n  练习结束! 共 {rounds} 局，平均速度 {avg_cpm} 字/分钟。加油!\n")
            break
        elif cmd == "d":
            level = choose_level()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  已退出，下次再来练!\n")
        sys.exit(0)
