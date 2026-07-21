# -*- coding: utf-8 -*-
"""檢察官不起訴書生成工作流程圖(書類生成系統 × 波特王系統)
執行: python3 不起訴書生成工作流程圖_V01.00_流程定義.py [輸出資料夾]
"""
import sys, os
sys.path.insert(0, r"C:\Users\User\.claude\plugins\marketplaces\lancelot-skills\plugins\geo-bpmn-flow-builder\skills\geo-bpmn-flow-builder\scripts")
from bpmn_builder import Proc, emit


def build():
    p = Proc("不起訴書生成工作流程圖", "檢察官不起訴書生成工作流程圖",
             ["檢察官", "波特王系統"], version="V01.00")
    p.add("s",   "start",   "開始", 0)
    p.add("t1",  "task",    "於書類生成系統點開個案並連線波特王", 0, kind="user")
    p.add("t2",  "task",    "明確指定書類類型(不起訴書)", 0, kind="user")
    p.add("t3",  "task",    "匯入移送書與偵訊筆錄", 0, kind="user")
    p.add("t4",  "task",    "詢問不起訴原因", 1, kind="system")
    p.add("t5",  "task",    "輸入不起訴原因", 0, kind="user")
    p.add("t6",  "task",    "生成不起訴書草稿", 1, kind="system")
    p.add("t7",  "task",    "檢視草稿內容", 0, kind="user")
    p.add("gw",  "gateway", "需調整", 0)
    p.add("t8",  "task",    "直接調整草稿內文", 0, kind="user")
    p.add("t9",  "task",    "複製內文或下載後匯入翰書系統", 0, kind="user")
    p.add("e",   "end",     "完成", 0)

    p.add("d1", "input",  "移送書", 0)
    p.add("d2", "input",  "偵訊筆錄", 0)
    p.add("d3", "output", "不起訴書草稿", 1)
    p.assoc("d1", "t3"); p.assoc("d2", "t3"); p.assoc("t6", "d3")

    p.flow("s", "t1"); p.flow("t1", "t2"); p.flow("t2", "t3")
    p.flow("t3", "t4"); p.flow("t4", "t5"); p.flow("t5", "t6")
    p.flow("t6", "t7")
    p.flow("t7", "gw")
    p.flow("gw", "t8", "需調整→是")
    p.flow("gw", "t9", "需調整→否")
    p.flow("t8", "t9")
    p.flow("t9", "e")
    return p


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    emit(build(), outdir, fmt="drawio", src=__file__,
         change="初版產出", change_kind="初版", change_source="流程說明")
    print("done ->", os.path.abspath(outdir))
