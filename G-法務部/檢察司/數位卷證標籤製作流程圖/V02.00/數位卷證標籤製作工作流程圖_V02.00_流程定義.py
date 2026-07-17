# -*- coding: utf-8 -*-
"""數位卷證標籤製作工作流程圖:數位卷證系統 × 波特玩系統(OCR)
V02.00:依 RFP 工項拆解-v1(M2 數位卷證摘要及頁數判讀)補充——
  卷證類型辨識與關鍵資訊擷取(M2-02)、證據標題自動摘要(M2-03)、
  頁數起迄判讀與分段標記+證據清單(M2-04)、OCR準確率與工作階段保留註解。
執行: python 數位卷證標籤製作工作流程圖_V02.00_流程定義.py [輸出資料夾]
"""
import sys, os
sys.path.insert(0, r"C:\Users\User\.claude\plugins\cache\lancelot-skills\bpmn-flow-builder\20260710.16\skills\bpmn-flow-builder\scripts")
from bpmn_builder import Proc, emit


def build():
    p = Proc("數位卷證標籤製作工作流程圖", "數位卷證標籤製作工作流程圖",
             ["檢察事務官", "檢察官"], version="V02.00",
             bands=[("數位卷證系統", ["s", "a1", "a2", "a3"]),
                    ("波特玩系統", ["a4", "a5", "a5b", "a5c", "a5d",
                                    "a6", "a7", "gw", "a8", "a9"]),
                    ("卷證交付", ["a10", "e"])])
    p.add("s",  "start",   "開始", 0)
    p.add("a1", "task",    "登入數位卷證系統查詢數位卷證", 0, kind="user")
    p.add("a2", "task",    "開啟數位卷證PDF", 0, kind="user")
    p.add("a3", "task",    "以列印PDF方式下載產生卷證PDF檔", 0, kind="user")
    p.add("a4", "task",    "將卷證PDF匯入波特玩系統", 0, kind="user")
    p.add("a5", "task",    "執行OCR辨識", 0, kind="system")
    p.add("a5b","task",    "卷證類型辨識與關鍵資訊擷取", 0, kind="system")
    p.add("a5c","task",    "證據標題自動摘要", 0, kind="system")
    p.add("a5d","task",    "頁數起迄判讀與分段標記", 0, kind="system")
    p.add("a6", "task",    "數位標籤識別與製作", 0, kind="system")
    p.add("a7", "task",    "檢視標籤是否符合需求", 0, kind="user")
    p.add("gw", "gateway", "符合?", 0)
    p.add("a8", "task",    "人工調整標籤", 0, kind="user")
    p.add("a9", "task",    "產出帶標籤之卷證PDF檔", 0, kind="system")
    p.add("a10","task",    "使用帶標籤卷證PDF辦理案件", 1, kind="user")
    p.add("e",  "end",     "結束", 1)

    p.add("d1", "output", "卷證PDF檔", 0)
    p.add("d2", "output", "帶標籤卷證PDF檔", 0)
    p.add("d3", "output", "證據清單", 0)
    p.assoc("a3", "d1"); p.assoc("a9", "d2"); p.assoc("a5d", "d3")

    p.add("n1", "note", "數位卷證系統原可直接製作標籤,惟因加解密致換頁速度過慢、操作效率不佳,故改採本流程", 0)
    p.assoc("n1", "a2")
    p.add("n2", "note", "目前流程不含將帶標籤卷證回傳數位卷證系統", 1)
    p.assoc("n2", "a10")
    p.add("n3", "note", "RFP工項M2-01:OCR支援繁中英與PDF/TIFF/JPG,辨識準確率依專家小組會議決議標準(待釐清Q1);單頁≤5秒、100頁批次≤10分鐘", 0)
    p.assoc("n3", "a5")
    p.add("n4", "note", "RFP限制因素(工項M4-03):應具工作階段保留,重新登入可銜接前次作業,免重跑批次辨識", 0)
    p.assoc("n4", "a4")

    p.flow("s", "a1"); p.flow("a1", "a2"); p.flow("a2", "a3")
    p.flow("a3", "a4"); p.flow("a4", "a5"); p.flow("a5", "a5b")
    p.flow("a5b", "a5c"); p.flow("a5c", "a5d"); p.flow("a5d", "a6")
    p.flow("a6", "a7"); p.flow("a7", "gw")
    p.flow("gw", "a9", "符合→是")
    p.flow("gw", "a8", "符合→否")
    p.flow("a8", "a9")
    p.flow("a9", "a10")
    p.flow("a10", "e")
    return p


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    emit(build(), outdir, fmt="drawio", src=__file__,
         change="依RFP工項M2補充:卷證類型辨識、標題摘要、頁數判讀三系統任務與證據清單產出;加OCR準確率、工作階段保留註解",
         change_kind="結構", change_source="RFP工項拆解-v1.md")
    print("done ->", os.path.abspath(outdir))
