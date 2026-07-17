# -*- coding: utf-8 -*-
"""統計標籤判斷(偵查類)工作流程圖:書類生成系統 × 波特玩智慧判斷 × 刑案管理系統
執行: python 統計標籤判斷_偵查類_工作流程圖_V02.00_流程定義.py [輸出資料夾]
"""
import sys, os
sys.path.insert(0, r"C:\Users\User\.claude\plugins\cache\lancelot-skills\bpmn-flow-builder\20260710.16\skills\bpmn-flow-builder\scripts")
from bpmn_builder import Proc, emit


def build():
    p = Proc("統計標籤判斷_偵查類_工作流程圖", "統計標籤判斷(偵查類)工作流程圖",
             ["檢察官", "刑案管理系統使用者"], version="V02.00",
             bands=[("書類生成系統", ["s", "a1", "a2"]),
                    ("波特玩系統", ["a3", "a4", "a5"]),
                    ("刑案管理系統", ["sftp", "a6", "a7", "a8", "a9",
                                      "a10", "gw", "a11", "e"])])
    p.add("s",   "start",   "開始", 0)
    p.add("a1",  "task",    "完成起訴書或不起訴書", 0, kind="user")
    p.add("a2",  "task",    "執行列印或儲存", 0, kind="user")
    p.add("a3",  "task",    "呼叫波特玩智慧判斷並傳送書類內文", 0, kind="system")
    p.add("a4",  "task",    "波特玩判讀個案欄位", 0, kind="system")
    p.add("a5",  "task",    "整理判讀結果並拋轉至SFTP", 0, kind="system")
    p.add("sftp","database","SFTP", 1)
    p.add("a6",  "task",    "登入刑案管理系統", 1, kind="user")
    p.add("a7",  "task",    "進入偵查類案件查詢個案", 1, kind="user")
    p.add("a8",  "task",    "點選「AI應用」按鈕", 1, kind="user")
    p.add("a9",  "task",    "帶出SFTP判讀資料", 1, kind="system")
    p.add("a10", "task",    "檢視判讀資料是否符合需求", 1, kind="user")
    p.add("gw",  "gateway", "符合?", 1)
    p.add("a11", "task",    "點選引用,欄位資訊存入刑案管理系統", 1, kind="user")
    p.add("e",   "end",     "結束", 1)

    p.add("d1", "input",  "起訴書/不起訴書內文", 0)
    p.add("d2", "output", "欄位判讀結果", 0)
    p.add("n1", "note",   "符合→否時:後續由統計處收集不符資訊,回饋進行判讀邏輯調整", 1)
    p.assoc("d1", "a3"); p.assoc("a5", "d2"); p.assoc("gw", "n1")

    p.flow("s", "a1"); p.flow("a1", "a2"); p.flow("a2", "a3")
    p.flow("a3", "a4"); p.flow("a4", "a5"); p.flow("a5", "sftp")
    p.flow("sftp", "a6"); p.flow("a6", "a7"); p.flow("a7", "a8")
    p.flow("a8", "a9"); p.flow("a9", "a10"); p.flow("a10", "gw")
    p.flow("gw", "a11", "符合→是")
    p.flow("gw", "e", "符合→否(不引用)")
    p.flow("a11", "e")
    return p


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    emit(build(), outdir, fmt="drawio", src=__file__,
         change="符合→否加註解:統計處收集資訊回饋調整判讀邏輯", change_kind="結構", change_source="流程說明")
    print("done ->", os.path.abspath(outdir))
