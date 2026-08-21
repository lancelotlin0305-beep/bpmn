# -*- coding: utf-8 -*-
"""約談輔導紀要與訪視報告工作流程圖(保護司)— 多頁專案 V04.01
頁籤1:AI觀護助理流程,雙 pool 協作——受保護管束人再犯風險評估智慧輔助系統/
       AI觀護助理系統,觀護人為兩 pool 內之操作者泳道(pool=系統、lane=角色);
       被觀護人泳道移除(訪談方式分支標籤保留其語意),工項編號全數移除。
頁籤2:現行工作流程(未導入AI):訪談不錄音,訪談後回觀護案件管理作業系統
       登打約談輔導紀要/訪視報告並建立處遇建議
執行: python 本檔 [輸出資料夾]
"""
import sys, os
sys.path.insert(0, r"D:\claude-skills-marketplace\plugins\geo-bpmn-flow-builder\skills\geo-bpmn-flow-builder\scripts")
from bpmn_builder import Proc, Collab, emit_multi

VERSION = "V04.01"
PROJECT = "約談輔導紀要與訪視報告工作流程圖"


def build_ai():
    """雙 pool 協作,全手動列:
    風評系統 pool [觀護人|系統]、AI觀護助理系統 pool [系統|觀護人]——
    兩系統泳道相鄰,跨 pool 訊息流(個案資料/個案報告資料)端點同列走水平直線;
    pool 內跨泳道以一般順序流銜接,無需訊息流接力事件。"""
    c = Collab(PROJECT, "約談輔導紀要與訪視報告工作流程圖(AI觀護助理)",
               version=VERSION)

    # Pool 1:受保護管束人再犯風險評估智慧輔助系統(單一觀護人泳道,
    # 系統自動任務以藍色 kind=system 標示,不另設系統泳道——pool 名即系統)
    pr = c.add_pool(Proc("pool_risk", "受保護管束人再犯風險評估智慧輔助系統",
                         ["觀護人"]))
    pr.add("s",     "start", "開始",                              0, 0)
    pr.add("open",  "task",  "開啟觀護案件管理作業系統",             0, 1, kind="user")
    pr.add("query", "task",  "於受保護管束人再犯風險評估\n智慧輔助系統查詢個案資料", 0, 2, kind="user")
    pr.add("b1",    "task",  "導引至AI觀護助理系統\n帶入個案資料(含獄政等資料)", 0, 3, kind="system")
    pr.add("x1",    "end",   "轉AI觀護助理系統",                   0, 4)
    pr.add("b3",    "start", "接收個案報告資料",                   0, 17)  # 與 a9 同列
    pr.add("b4",    "task",  "個案報告存檔",                       0, 18, kind="system")
    pr.add("b5",    "task",  "自動回存至\n個案管理作業系統",          0, 19, kind="system")
    pr.add("b6",    "end",   "完成",                              0, 20)

    pr.flow("s", "open")
    pr.flow("open", "query")
    pr.flow("query", "b1")
    pr.flow("b1", "x1")
    pr.flow("b3", "b4")
    pr.flow("b4", "b5")
    pr.flow("b5", "b6")

    # Pool 2:AI觀護助理系統(單一觀護人泳道,系統自動任務藍色標示)
    pa = c.add_pool(Proc("pool_ai", "AI觀護助理系統", ["觀護人"]))
    pa.add("a0",  "start",   "接收個案資料\n(含獄政等資料)",        0, 4)   # 與 x1 同列
    pa.add("gw1", "gateway", "訪談方式",                          0, 5)
    pa.add("visit", "task",  "出訪至被觀護人所在地",                0, 6, kind="user")
    pa.add("itv", "task",    "進行訪談並全程錄音",                 0, 7, kind="user")
    pa.add("rec", "output",  "錄音檔",                            0)
    pa.add("up",  "task",    "上傳錄音檔至\nAI觀護助理系統",         0, 8, kind="user")
    pa.add("a2",  "task",    "語音轉逐字稿",                       0, 9,  kind="system")
    pa.add("a3",  "task",    "AI順稿",                            0, 10, kind="system")
    pa.add("a4",  "task",    "生成約談輔導紀要\n或訪視報告",         0, 11, kind="system")
    pa.add("doc", "output",  "約談輔導紀要/\n訪視報告",             0)
    pa.add("a5",  "task",    "產出風險評估與\n處遇建議",             0, 12, kind="system")
    pa.add("pdoc", "output", "風險評估與\n處遇建議",               0)
    pa.add("n1",  "note",    "標準Prompt模板:約談輔導紀要、\n訪視報告、風險評估與處遇建議", 0)
    pa.add("rev", "task",    "觀護人審閱報告與處遇建議",             0, 13, kind="user")
    pa.add("gw2", "gateway", "無誤?",                             0, 14)
    pa.add("edit", "task",   "以報告智慧編輯器修改",                0, 15, kind="user")
    pa.nodes["edit"]["sub"] = 1   # 修改旁置右子欄(泳道已因工件加寬):迴圈就近、不擋主線直下
    pa.add("a8",  "task",    "回填受保護管束人再犯風險評估\n智慧輔助系統存檔", 0, 16, kind="system")
    pa.add("a9",  "end",     "轉風險評估智慧輔助系統",              0, 17)

    pa.assoc("itv", "rec")
    pa.assoc("a4", "doc")
    pa.assoc("a5", "pdoc")
    pa.assoc("n1", "a5")

    pa.flow("a0", "gw1")
    pa.flow("gw1", "visit", "觀護人出訪")                      # 主線直下
    pa.flow("gw1", "itv",   "被觀護人到地檢", route="sideLeft")  # 走泳道左通道,不壓出訪任務
    pa.flow("visit", "itv")
    pa.flow("itv", "up")
    pa.flow("up", "a2")
    pa.flow("a2", "a3")
    pa.flow("a3", "a4")
    pa.flow("a4", "a5")
    pa.flow("a5", "rev")
    pa.flow("rev", "gw2")
    pa.flow("gw2", "edit", "否", route="outRight")             # 修改分支旁置右子欄
    pa.flow("edit", "rev", route="sideLeft")                   # 迴圈走左通道接回審閱(右側有備註)
    pa.flow("gw2", "a8",   "是")                               # 主線直下回填
    pa.flow("a8", "a9")

    # 跨 pool 訊息流(端點同列,兩系統泳道相鄰,走水平直線)
    c.message("x1", "a0", "個案資料")
    c.message("a9", "b3", "個案報告資料")
    return c


def build_cur():
    """現行工作流程(未導入AI):不錄音,訪談後回案管系統登打與建立處遇建議。"""
    p = Proc("約談輔導紀要與訪視報告現行工作流程圖",
             "約談輔導紀要與訪視報告現行工作流程圖(未導入AI)",
             ["觀護人", "被觀護人"],
             version=VERSION)

    p.add("c_s",     "start",   "開始",                              0)
    p.add("c_open",  "task",    "開啟觀護案件管理作業系統\n查詢個案資料", 0, kind="user")
    p.add("c_gw1",   "gateway", "訪談方式",                          0)
    p.add("c_come",  "task",    "至地檢接受約談",                     1)
    p.add("c_visit", "task",    "出訪至被觀護人所在地",                0, kind="user")
    p.add("c_recv",  "task",    "於所在地接受訪視",                   1)
    p.add("c_itv",   "task",    "進行訪談(現行不錄音)",               0, kind="user")
    p.add("c_log",   "task",    "於受保護管束人再犯風險評估\n智慧輔助系統登打約談輔導紀要\n或訪視報告", 0, kind="user")
    p.add("c_doc",   "output",  "約談輔導紀要/\n訪視報告",             0)
    p.add("c_plan",  "task",    "於受保護管束人再犯風險評估\n智慧輔助系統建立處遇建議",  0, kind="user")
    p.add("c_pdoc",  "output",  "處遇建議",                           0)
    p.add("c_sync",  "task",    "自動回存至\n觀護案件管理作業系統",      0, kind="system")
    p.add("c_e",     "end",     "結束本次訪談",                       0)

    p.assoc("c_log", "c_doc")
    p.assoc("c_plan", "c_pdoc")

    p.flow("c_s", "c_open")
    p.flow("c_open", "c_gw1")
    p.flow("c_gw1", "c_come",  "被觀護人到地檢")
    p.flow("c_gw1", "c_visit", "觀護人出訪")
    p.flow("c_visit", "c_recv")
    p.flow("c_come", "c_itv")
    p.flow("c_recv", "c_itv")
    p.flow("c_itv", "c_log")
    p.flow("c_log", "c_plan")
    p.flow("c_plan", "c_sync")
    p.flow("c_sync", "c_e")
    return p


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    emit_multi([build_ai(), build_cur()], PROJECT, outdir, version=VERSION,
               src=__file__, xml=True, svg=True, viewer=True,
               change="頁1自動回存任務改「自動回存至個案管理作業系統」"
                      "(原:觀護案件管理作業系統;使用者於 .drawio 修改後回灌)",
               change_kind="文字", change_source="使用者修改 .drawio")
    print("done ->", os.path.abspath(outdir))
