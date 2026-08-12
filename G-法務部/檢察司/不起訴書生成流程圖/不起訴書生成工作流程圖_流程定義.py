# -*- coding: utf-8 -*-
"""檢察官不起訴書生成工作流程圖(多頁):
頁1 現行工作流程(未導入AI)、頁2 主流程(AI,含介接說明)
V10.00:頁序與頁數調整——現行(未導入AI)移至頁1;原頁1(AI主流程)與
  原頁2(AI主流程+介接說明)整合為單一頁,保留含介接說明版(為前者之超集)。
V10.01:介接說明備註移除工項編號(RFP工項M1-05/M1-06 前綴),僅留說明文字。
執行: python 不起訴書生成工作流程圖_流程定義.py [輸出資料夾]
"""
import sys, os
sys.path.insert(0, r"C:\Users\User\.claude\plugins\marketplaces\lancelot-skills\plugins\geo-bpmn-flow-builder\skills\geo-bpmn-flow-builder\scripts")
from bpmn_builder import Proc, Collab, emit_multi


def build(prefix, cid, name, with_notes=False):
    """含介接說明的 AI 主流程:只把 AI智慧輔助系統獨立成一個 pool,
    書類生成系統與漢書系統留在同一個 pool(檢察官單泳道,避免斜階交疊);
    pool 間以訊息流銜接(書類系統→AI 傳個案資料、AI→漢書 回傳草稿)。"""
    q = lambda i: prefix + i
    c = Collab(cid, name)

    # Pool 1:書類生成暨漢書系統(檢察官操作,單一泳道)
    p1 = c.add_pool(Proc(prefix + "pool_doc", "書類生成暨漢書系統", ["檢察官"]))
    p1.add(q("s"),   "start", "開始", 0, 0)
    p1.add(q("t0"),  "task",  "登錄書類生成系統", 0, 1, kind="user")
    p1.add(q("t1"),  "task",  "查詢並點開個案", 0, 2, kind="user")
    p1.add(q("t1b"), "task",  "由書類生成系統連線AI智慧輔助系統", 0, 3, kind="system")
    p1.add(q("x1"),  "end",   "轉AI智慧輔助系統", 0, 4)
    p1.flow(q("s"), q("t0")); p1.flow(q("t0"), q("t1")); p1.flow(q("t1"), q("t1b"))
    p1.flow(q("t1b"), q("x1"))
    # 同泳道下半段:AI 回傳草稿後匯入漢書系統定稿
    p1.add(q("r1"),  "start", "AI回傳草稿", 0, 22)
    p1.add(q("t9"),  "task",  "複製內文或下載後匯入漢書系統", 0, 23, kind="user")
    p1.add(q("e"),   "end",   "完成", 0, 24)
    p1.add(q("d5"),  "output", "不起訴書(定稿)", 0)
    p1.assoc(q("t9"), q("d5"))
    p1.flow(q("r1"), q("t9")); p1.flow(q("t9"), q("e"))

    # Pool 2:AI智慧輔助系統(獨立)
    p2 = c.add_pool(Proc(prefix + "pool_ai", "AI智慧輔助系統", ["AI智慧輔助系統"]))
    p2.add(q("a0"),  "start", "接收書類系統個案資料", 0, 5)
    p2.add(q("t3"),  "task",  "匯入卷證資料、移送書、偵訊筆錄與警詢筆錄", 0, 8, kind="user")
    p2.add(q("t2"),  "task",  "明確指定書類類型(不起訴書)", 0, 11, kind="user")
    p2.add(q("t2b"), "task",  "依案件類型自動選用書類範本", 0, 12, kind="system")
    p2.add(q("t4"),  "task",  "AI智慧輔助系統主動詢問不起訴原因", 0, 13, kind="system")
    p2.add(q("t5"),  "task",  "輸入不起訴原因", 0, 14, kind="user")
    p2.add(q("t5b"), "task",  "AI智慧輔助系統詢問適用法規條款(條/款)", 0, 15, kind="system")
    p2.add(q("t5c"), "task",  "選擇適用法規條款", 0, 16, kind="user")
    p2.add(q("t6"),  "task",  "AI智慧輔助系統生成不起訴書草稿", 0, 17, kind="system")
    p2.add(q("t7"),  "task",  "檢視草稿內容", 0, 18, kind="user")
    p2.add(q("t8"),  "task",  "直接調整草稿內文", 0, 19, kind="user")
    p2.add(q("a9"),  "end",   "回傳漢書系統", 0, 20)
    p2.add(q("d3"),  "output", "不起訴書草稿", 0)
    p2.assoc(q("t6"), q("d3"))
    p2.add(q("d1"),  "input", "移送書", 0)
    p2.add(q("d2"),  "input", "偵訊筆錄", 0)
    p2.add(q("d4"),  "input", "警詢筆錄", 0)
    p2.assoc(q("d1"), q("t3")); p2.assoc(q("d2"), q("t3")); p2.assoc(q("d4"), q("t3"))
    p2.flow(q("a0"), q("t3")); p2.flow(q("t3"), q("t2")); p2.flow(q("t2"), q("t2b"))
    p2.flow(q("t2b"), q("t4")); p2.flow(q("t4"), q("t5")); p2.flow(q("t5"), q("t5b"))
    p2.flow(q("t5b"), q("t5c")); p2.flow(q("t5c"), q("t6")); p2.flow(q("t6"), q("t7"))
    p2.flow(q("t7"), q("t8")); p2.flow(q("t8"), q("a9"))

    # 跨 pool 訊息流(端點取各段起訖事件,走線乾淨)
    c.message(q("x1"), q("a0"), "個案資料/案號")
    c.message(q("a9"), q("r1"), "不起訴書草稿內文")

    if with_notes:
        p1.add(q("n1"), "note",
              "書類生成系統須與AI智慧輔助系統完成帳號驗證,並同時傳遞個案資料與個案案號至AI智慧輔助系統", 0)
        p1.assoc(q("n1"), q("t1b"))
        p2.add(q("n2"), "note",
              "檢視與調整之編修結果應回饋自動Fine-tuning機制,持續優化模型", 0)
        p2.assoc(q("n2"), q("t8"))
        p1.add(q("n3"), "note",
              "應以標準化介接直接匯入書類系統(現行人工匯入)", 0)
        p1.assoc(q("n3"), q("e"))
    return c


def build_cur():
    """現行工作流程(未導入AI):書類生成系統查案→漢書系統人工登打不起訴書。"""
    p = Proc("不起訴書生成現行工作流程圖",
             "檢察官不起訴書生成現行工作流程圖(未導入AI)",
             ["書類生成系統", "書類生成系統-漢書系統"])
    p.add("c_s",  "start", "開始", 0, 0)
    p.add("c_t0", "task",  "登錄書類生成系統", 0, 1, kind="user")
    p.add("c_t1", "task",  "查詢並點開個案", 0, 2, kind="user")
    p.add("c_t1r", "task", "人工閱讀卷證資料、移送書、\n偵訊筆錄與警詢筆錄", 0, 3, kind="user")
    p.add("c_t2", "task",  "開啟漢書系統書類編輯介面", 1, 5, kind="user")
    p.add("c_t3", "task",  "登打不起訴書", 1, 6, kind="user")
    p.add("c_e",  "end",   "完成", 1, 7)

    p.add("c_d1", "output", "不起訴書", 1)
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
    emit_multi([build_cur(),
                build("a_", "不起訴書生成工作流程圖", "檢察官不起訴書生成工作流程圖(含介接說明)",
                      with_notes=True)],
               "不起訴書生成工作流程圖", outdir, version="V12.00", src=__file__,
               change="頁2含介接說明AI主流程:將AI智慧輔助系統獨立為一個 pool,書類生成系統與漢書系統留在同一 pool(檢察官單泳道),pool 間以訊息流銜接(書類系統→AI 傳個案資料、AI→漢書 回傳草稿)",
               change_kind="結構", change_source="口頭指示")
    print("done ->", os.path.abspath(outdir))
