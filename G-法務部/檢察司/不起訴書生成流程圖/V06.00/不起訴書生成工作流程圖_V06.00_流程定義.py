# -*- coding: utf-8 -*-
"""檢察官不起訴書生成工作流程圖(多頁):頁1 主流程、頁2 主流程+介接說明
執行: python 不起訴書生成工作流程圖_V06.00_流程定義.py [輸出資料夾]
"""
import sys, os
sys.path.insert(0, r"C:\Users\User\.claude\plugins\cache\lancelot-skills\bpmn-flow-builder\20260710.16\skills\bpmn-flow-builder\scripts")
from bpmn_builder import Proc, emit_multi


def build(prefix, pid, name, with_notes=False):
    q = lambda i: prefix + i
    p = Proc(pid, name, ["檢察官"],
             bands=[("書類生成系統", [q("s"), q("t0"), q("t1"), q("t1b")]),
                    ("波特玩系統", [q("t2"), q("t3"), q("t4"), q("t5"),
                                    q("t5b"), q("t5c"), q("t6"), q("t7"), q("t8")]),
                    ("漢書系統", [q("t9"), q("e")])])
    p.add(q("s"),   "start",   "開始", 0)
    p.add(q("t0"),  "task",    "登錄書類生成系統", 0, kind="user")
    p.add(q("t1"),  "task",    "查詢並點開個案", 0, kind="user")
    p.add(q("t1b"), "task",    "由書類生成系統連線波特玩", 0, kind="system")
    p.add(q("t3"),  "task",    "匯入移送書、偵訊筆錄與警詢筆錄", 0, kind="user")
    p.add(q("t2"),  "task",    "明確指定書類類型(不起訴書)", 0, kind="user")
    p.add(q("t4"),  "task",    "波特玩主動詢問不起訴原因", 0, kind="system")
    p.add(q("t5"),  "task",    "輸入不起訴原因", 0, kind="user")
    p.add(q("t5b"), "task",    "波特玩詢問適用法規條款(條/款)", 0, kind="system")
    p.add(q("t5c"), "task",    "選擇適用法規條款", 0, kind="user")
    p.add(q("t6"),  "task",    "波特玩生成不起訴書草稿", 0, kind="system")
    p.add(q("t7"),  "task",    "檢視草稿內容", 0, kind="user")
    p.add(q("t8"),  "task",    "直接調整草稿內文", 0, kind="user")
    p.add(q("t9"),  "task",    "複製內文或下載後匯入漢書系統", 0, kind="user")
    p.add(q("e"),   "end",     "完成", 0)

    p.add(q("d1"), "input",  "移送書", 0)
    p.add(q("d2"), "input",  "偵訊筆錄", 0)
    p.add(q("d4"), "input",  "警詢筆錄", 0)
    p.add(q("d3"), "output", "不起訴書草稿", 0)
    p.add(q("d5"), "output", "不起訴書(定稿)", 0)
    p.assoc(q("d1"), q("t3")); p.assoc(q("d2"), q("t3")); p.assoc(q("d4"), q("t3"))
    p.assoc(q("t6"), q("d3")); p.assoc(q("t9"), q("d5"))

    if with_notes:
        p.add(q("n1"), "note",
              "書類生成系統須與波特玩完成帳號驗證,並同時傳遞個案資料與個案案號至波特玩系統", 0)
        p.assoc(q("n1"), q("t1b"))

    p.flow(q("s"), q("t0")); p.flow(q("t0"), q("t1")); p.flow(q("t1"), q("t1b"))
    p.flow(q("t1b"), q("t3")); p.flow(q("t3"), q("t2")); p.flow(q("t2"), q("t4"))
    p.flow(q("t4"), q("t5")); p.flow(q("t5"), q("t5b")); p.flow(q("t5b"), q("t5c"))
    p.flow(q("t5c"), q("t6")); p.flow(q("t6"), q("t7")); p.flow(q("t7"), q("t8"))
    p.flow(q("t8"), q("t9")); p.flow(q("t9"), q("e"))
    return p


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    emit_multi([build("a_", "不起訴書生成工作流程圖", "檢察官不起訴書生成工作流程圖"),
                build("b_", "不起訴書生成工作流程圖_介接說明", "檢察官不起訴書生成工作流程圖(含介接說明)",
                      with_notes=True)],
               "不起訴書生成工作流程圖", outdir, version="V06.00", src=__file__,
               change="改多頁:頁1主流程(承V05.00)+頁2加連線波特玩之帳號驗證/資料傳遞說明",
               change_kind="結構", change_source="口頭指示")
    print("done ->", os.path.abspath(outdir))
