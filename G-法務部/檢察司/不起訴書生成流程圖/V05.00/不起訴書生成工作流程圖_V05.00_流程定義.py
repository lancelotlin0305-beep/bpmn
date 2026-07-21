# -*- coding: utf-8 -*-
"""檢察官不起訴書生成工作流程圖(書類生成系統 × 波特玩系統)
執行: python3 不起訴書生成工作流程圖_V01.00_流程定義.py [輸出資料夾]
"""
import sys, os
sys.path.insert(0, r"C:\Users\User\.claude\plugins\marketplaces\lancelot-skills\plugins\geo-bpmn-flow-builder\skills\geo-bpmn-flow-builder\scripts")
from bpmn_builder import Proc, emit


def build():
    p = Proc("不起訴書生成工作流程圖", "檢察官不起訴書生成工作流程圖",
             ["檢察官"], version="V05.00",
             bands=[("書類生成系統", ["s", "t0", "t1", "t1b"]),
                    ("波特玩系統", ["t2", "t3", "t4", "t5", "t5b", "t5c",
                                    "t6", "t7", "t8"]),
                    ("漢書系統", ["t9", "e"])])
    p.add("s",   "start",   "開始", 0)
    p.add("t0",  "task",    "登錄書類生成系統", 0, kind="user")
    p.add("t1",  "task",    "查詢並點開個案", 0, kind="user")
    p.add("t1b", "task",    "由書類生成系統連線波特玩", 0, kind="system")
    p.add("t3",  "task",    "匯入移送書、偵訊筆錄與警詢筆錄", 0, kind="user")
    p.add("t2",  "task",    "明確指定書類類型(不起訴書)", 0, kind="user")
    p.add("t4",  "task",    "波特玩主動詢問不起訴原因", 0, kind="system")
    p.add("t5",  "task",    "輸入不起訴原因", 0, kind="user")
    p.add("t5b", "task",    "波特玩詢問適用法規條款(條/款)", 0, kind="system")
    p.add("t5c", "task",    "選擇適用法規條款", 0, kind="user")
    p.add("t6",  "task",    "波特玩生成不起訴書草稿", 0, kind="system")
    p.add("t7",  "task",    "檢視草稿內容", 0, kind="user")
    p.add("t8",  "task",    "直接調整草稿內文", 0, kind="user")
    p.add("t9",  "task",    "複製內文或下載後匯入漢書系統", 0, kind="user")
    p.add("e",   "end",     "完成", 0)

    p.add("d1", "input",  "移送書", 0)
    p.add("d2", "input",  "偵訊筆錄", 0)
    p.add("d4", "input",  "警詢筆錄", 0)
    p.add("d3", "output", "不起訴書草稿", 0)
    p.add("d5", "output", "不起訴書(定稿)", 0)
    p.assoc("d1", "t3"); p.assoc("d2", "t3"); p.assoc("d4", "t3")
    p.assoc("t6", "d3"); p.assoc("t9", "d5")

    p.flow("s", "t0"); p.flow("t0", "t1"); p.flow("t1", "t1b")
    p.flow("t1b", "t3"); p.flow("t3", "t2"); p.flow("t2", "t4")
    p.flow("t4", "t5"); p.flow("t5", "t5b"); p.flow("t5b", "t5c")
    p.flow("t5c", "t6")
    p.flow("t6", "t7")
    p.flow("t7", "t8")
    p.flow("t8", "t9")
    p.flow("t9", "e")
    return p


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    emit(build(), outdir, fmt="drawio", src=__file__,
         change="移除需調整與條款正確兩閘道:檢視後直接調整草稿;條款改由檢察官直接選擇", change_kind="結構", change_source="口頭指示")
    print("done ->", os.path.abspath(outdir))
