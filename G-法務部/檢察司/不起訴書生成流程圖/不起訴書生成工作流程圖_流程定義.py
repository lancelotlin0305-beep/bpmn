# -*- coding: utf-8 -*-
"""檢察官不起訴書生成工作流程圖(多頁):
頁1 主流程(AI)、頁2 主流程+介接說明、頁3 現行工作流程(未導入AI)
V09.01:併入 V07.03 之分區更名——三頁分區「漢書系統」一律改為
  「書類生成系統-漢書系統」(任務文字維持簡短寫法);
  V08.00/V09.00 係自 V07.02 分支開發,未帶入該更名,於本版補齊。
執行: python 不起訴書生成工作流程圖_流程定義.py [輸出資料夾]
"""
import sys, os
sys.path.insert(0, r"C:\Users\User\.claude\plugins\marketplaces\lancelot-skills\plugins\geo-bpmn-flow-builder\skills\geo-bpmn-flow-builder\scripts")
from bpmn_builder import Proc, emit_multi


def build(prefix, pid, name, with_notes=False):
    q = lambda i: prefix + i
    p = Proc(pid, name, ["檢察官"],
             bands=[("書類生成系統", [q("s"), q("t0"), q("t1"), q("t1b")]),
                    ("AI智慧輔助系統", [q("t2"), q("t2b"), q("t3"), q("t4"), q("t5"),
                                    q("t5b"), q("t5c"), q("t6"), q("t7"), q("t8")]),
                    ("書類生成系統-漢書系統", [q("t9"), q("e")])])
    p.add(q("s"),   "start",   "開始", 0)
    p.add(q("t0"),  "task",    "登錄書類生成系統", 0, kind="user")
    p.add(q("t1"),  "task",    "查詢並點開個案", 0, kind="user")
    p.add(q("t1b"), "task",    "由書類生成系統連線AI智慧輔助系統", 0, kind="system")
    p.add(q("t3"),  "task",    "匯入卷證資料、移送書、偵訊筆錄與警詢筆錄", 0, kind="user")
    p.add(q("t2"),  "task",    "明確指定書類類型(不起訴書)", 0, kind="user")
    p.add(q("t2b"), "task",    "依案件類型自動選用書類範本", 0, kind="system")
    p.add(q("t4"),  "task",    "AI智慧輔助系統主動詢問不起訴原因", 0, kind="system")
    p.add(q("t5"),  "task",    "輸入不起訴原因", 0, kind="user")
    p.add(q("t5b"), "task",    "AI智慧輔助系統詢問適用法規條款(條/款)", 0, kind="system")
    p.add(q("t5c"), "task",    "選擇適用法規條款", 0, kind="user")
    p.add(q("t6"),  "task",    "AI智慧輔助系統生成不起訴書草稿", 0, kind="system")
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
              "書類生成系統須與AI智慧輔助系統完成帳號驗證,並同時傳遞個案資料與個案案號至AI智慧輔助系統", 0)
        p.assoc(q("n1"), q("t1b"))
        p.add(q("n2"), "note",
              "RFP工項M1-05:檢視與調整之編修結果應回饋自動Fine-tuning機制,持續優化模型", 0)
        p.assoc(q("n2"), q("t8"))
        p.add(q("n3"), "note",
              "RFP工項M1-06:應以標準化介接直接匯入書類系統(現行人工匯入)", 0)
        p.assoc(q("n3"), q("e"))

    p.flow(q("s"), q("t0")); p.flow(q("t0"), q("t1")); p.flow(q("t1"), q("t1b"))
    p.flow(q("t1b"), q("t3")); p.flow(q("t3"), q("t2")); p.flow(q("t2"), q("t2b"))
    p.flow(q("t2b"), q("t4"))
    p.flow(q("t4"), q("t5")); p.flow(q("t5"), q("t5b")); p.flow(q("t5b"), q("t5c"))
    p.flow(q("t5c"), q("t6")); p.flow(q("t6"), q("t7")); p.flow(q("t7"), q("t8"))
    p.flow(q("t8"), q("t9")); p.flow(q("t9"), q("e"))
    return p


def build_cur():
    """現行工作流程(未導入AI):書類生成系統查案→漢書系統人工登打不起訴書。"""
    p = Proc("不起訴書生成現行工作流程圖",
             "檢察官不起訴書生成現行工作流程圖(未導入AI)",
             ["檢察官"],
             bands=[("書類生成系統", ["c_s", "c_t0", "c_t1", "c_t1r"]),
                    ("書類生成系統-漢書系統", ["c_t2", "c_t3", "c_e"])])
    p.add("c_s",  "start", "開始", 0)
    p.add("c_t0", "task",  "登錄書類生成系統", 0, kind="user")
    p.add("c_t1", "task",  "查詢並點開個案", 0, kind="user")
    p.add("c_t1r", "task", "人工閱讀卷證資料、移送書、\n偵訊筆錄與警詢筆錄", 0, kind="user")
    p.add("c_t2", "task",  "開啟漢書系統書類編輯介面", 0, kind="user")
    p.add("c_t3", "task",  "登打不起訴書", 0, kind="user")
    p.add("c_e",  "end",   "完成", 0)

    p.add("c_d1", "output", "不起訴書", 0)
    p.assoc("c_t3", "c_d1")
    p.add("c_i1", "input", "移送書", 0)
    p.add("c_i2", "input", "偵訊筆錄", 0)
    p.add("c_i3", "input", "警詢筆錄", 0)
    p.assoc("c_i1", "c_t1r"); p.assoc("c_i2", "c_t1r"); p.assoc("c_i3", "c_t1r")

    p.flow("c_s", "c_t0"); p.flow("c_t0", "c_t1"); p.flow("c_t1", "c_t1r")
    p.flow("c_t1r", "c_t2"); p.flow("c_t2", "c_t3"); p.flow("c_t3", "c_e")
    return p


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    emit_multi([build("a_", "不起訴書生成工作流程圖", "檢察官不起訴書生成工作流程圖"),
                build("b_", "不起訴書生成工作流程圖_介接說明", "檢察官不起訴書生成工作流程圖(含介接說明)",
                      with_notes=True),
                build_cur()],
               "不起訴書生成工作流程圖", outdir, version="V09.01", src=__file__,
               change="併入V07.03分區更名:三頁分區「漢書系統」改為「書類生成系統-"
                      "漢書系統」(V08.00/V09.00自V07.02分支開發未帶入);"
                      "並改git版控模式產出",
               change_kind="文字", change_source="口頭指示")
    print("done ->", os.path.abspath(outdir))
