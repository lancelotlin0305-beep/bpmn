# -*- coding: utf-8 -*-
"""數位卷證標籤製作工作流程圖(多頁):
頁1 AI智慧輔助系統流程(沿用 V02.02)、頁2 現行工作流程(未導入AI)
V03.00:新增頁2 現行工作流程——以列印PDF方式下載產生卷證PDF檔,
  人工於PDF編輯器編輯數位標籤,完成後交由檢察官使用辦理案件。
執行: python 數位卷證標籤製作工作流程圖_V03.00_流程定義.py [輸出資料夾]
"""
import sys, os
sys.path.insert(0, r"C:\Users\User\.claude\plugins\marketplaces\lancelot-skills\plugins\geo-bpmn-flow-builder\skills\geo-bpmn-flow-builder\scripts")
from bpmn_builder import Proc, emit_multi

VERSION = "V03.00"


def build_ai():
    p = Proc("數位卷證標籤製作工作流程圖", "數位卷證標籤製作工作流程圖(AI智慧輔助)",
             ["檢察事務官", "檢察官"], version=VERSION,
             bands=[("數位卷證系統", ["s", "a1", "a2", "a3"]),
                    ("AI智慧輔助系統", ["a4", "a5", "a5b", "a5c", "a5d",
                                    "a6", "a7", "gw", "a8", "a9"]),
                    ("卷證交付", ["a10", "e"])])
    p.add("s",  "start",   "開始", 0)
    p.add("a1", "task",    "登入數位卷證系統查詢數位卷證", 0, kind="user")
    p.add("a2", "task",    "開啟數位卷證PDF", 0, kind="user")
    p.add("a3", "task",    "以列印PDF方式下載產生卷證PDF檔", 0, kind="user")
    p.add("a4", "task",    "將卷證PDF匯入AI智慧輔助系統", 0, kind="user")
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
    p.add("n3", "note", "RFP工項M2-01:OCR支援繁中英與PDF/TIFF/JPG,辨識準確率依專家小組會議決議標準;單頁≤5秒、100頁批次≤10分鐘", 0)
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


def build_cur():
    """現行工作流程(未導入AI):下載卷證PDF後於PDF編輯器人工編輯數位標籤。"""
    p = Proc("數位卷證標籤製作現行工作流程圖",
             "數位卷證標籤製作現行工作流程圖(未導入AI)",
             ["檢察事務官", "檢察官"], version=VERSION,
             bands=[("數位卷證系統", ["c_s", "c_a1", "c_a2", "c_a3"]),
                    ("PDF編輯器",   ["c_a4", "c_a5"]),
                    ("卷證交付",     ["c_a6", "c_e"])])
    p.add("c_s",  "start", "開始", 0)
    p.add("c_a1", "task",  "登入數位卷證系統查詢數位卷證", 0, kind="user")
    p.add("c_a2", "task",  "開啟數位卷證PDF", 0, kind="user")
    p.add("c_a3", "task",  "以列印PDF方式下載產生卷證PDF檔", 0, kind="user")
    p.add("c_a4", "task",  "以PDF編輯器開啟卷證PDF檔", 0, kind="user")
    p.add("c_a5", "task",  "人工編輯數位標籤", 0, kind="user")
    p.add("c_a6", "task",  "使用帶標籤卷證PDF辦理案件", 1, kind="user")
    p.add("c_e",  "end",   "結束", 1)

    p.add("c_d1", "output", "卷證PDF檔", 0)
    p.add("c_d2", "output", "帶標籤卷證PDF檔", 0)
    p.assoc("c_a3", "c_d1"); p.assoc("c_a5", "c_d2")

    p.flow("c_s", "c_a1"); p.flow("c_a1", "c_a2"); p.flow("c_a2", "c_a3")
    p.flow("c_a3", "c_a4"); p.flow("c_a4", "c_a5"); p.flow("c_a5", "c_a6")
    p.flow("c_a6", "c_e")
    return p


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    emit_multi([build_ai(), build_cur()],
               "數位卷證標籤製作工作流程圖", outdir, version=VERSION, src=__file__,
               change="新增頁2「現行工作流程(未導入AI)」:以列印PDF方式下載產生"
                      "卷證PDF檔,人工於PDF編輯器編輯數位標籤,完成後交由檢察官"
                      "使用辦理案件;既有AI流程改為多頁專案頁1",
               change_kind="結構", change_source="口頭指示")
    print("done ->", os.path.abspath(outdir))
