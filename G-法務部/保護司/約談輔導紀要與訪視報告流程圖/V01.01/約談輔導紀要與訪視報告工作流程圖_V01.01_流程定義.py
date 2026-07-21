# -*- coding: utf-8 -*-
"""約談輔導紀要與訪視報告工作流程圖(保護司/AI觀護助理系統)
角色:觀護人、被觀護人
對應工項(工項拆解-v1.md):M5-02 錄音控制面板、M5-03 報告智慧編輯器、
M6-01 語音辨識(STT)、M7-02 Prompt模板、M7-03 抗幻覺、M9 異質系統資料介接、
M12-01 報告雙向同步回寫
執行: python 本檔 [輸出資料夾]
"""
import sys, os
sys.path.insert(0, r"C:\Users\User\.claude\plugins\marketplaces\lancelot-skills\plugins\geo-bpmn-flow-builder\skills\geo-bpmn-flow-builder\scripts")
from bpmn_builder import Proc, emit


def build():
    p = Proc("約談輔導紀要與訪視報告工作流程圖",
             "約談輔導紀要與訪視報告工作流程圖",
             ["觀護人", "被觀護人"],
             version="V01.01")

    p.add("s",     "start",   "開始",                          0)
    p.add("open",  "task",    "開啟觀護案件管理作業系統",          0, kind="user")
    p.add("query", "task",    "於受保護管束人再犯風險評估\n智慧輔助系統查詢個案資料", 0, kind="user")
    p.add("load",  "task",    "導引至AI觀護助理系統\n帶入個案資料(含獄政等資料)(M9)", 0, kind="system")
    p.add("gw1",   "gateway", "訪談方式",                       0)
    p.add("come",  "task",    "至地檢接受約談",                  1)
    p.add("visit", "task",    "出訪至被觀護人所在地",             0, kind="user")
    p.add("recv",  "task",    "於所在地接受訪視",                1)
    p.add("itv",   "task",    "進行訪談並全程錄音(M5-02)",        0, kind="user")
    p.add("rec",   "output",  "錄音檔",                         0)
    p.add("up",    "task",    "上傳錄音檔至\nAI觀護助理系統(M5-02)", 0, kind="user")
    p.add("stt",   "task",    "語音轉逐字稿(M6-01)",             0, kind="system")
    p.add("fix",   "task",    "AI順稿(M7-02)",                  0, kind="system")
    p.add("gen",   "task",    "生成約談輔導紀要\n或訪視報告(M7-02/M7-03)", 0, kind="system")
    p.add("doc",   "output",  "約談輔導紀要/\n訪視報告",          1, 7)
    p.add("plan",  "task",    "產出處遇計畫建議(M7-02)",          0, kind="system")
    p.add("pdoc",  "output",  "處遇計畫",                        0)
    p.add("rev",   "task",    "觀護人審閱報告與處遇計畫",          0, kind="user")
    p.add("gw2",   "gateway", "無誤?",                          0)
    p.add("edit",  "task",    "以報告智慧編輯器修改(M5-03)",       0, kind="user")
    p.add("wb",    "task",    "回填受保護管束人再犯風險評估\n智慧輔助系統存檔(M12-01)", 0, kind="system")
    p.add("sync",  "task",    "回存至觀護案件管理作業系統(M12-01)", 0, kind="system")
    p.add("e",     "end",     "結束本次訪談",                     0)

    p.assoc("itv", "rec")
    p.assoc("gen", "doc")
    p.assoc("plan", "pdoc")

    p.flow("s", "open")
    p.flow("open", "query")
    p.flow("query", "load")
    p.flow("load", "gw1")
    p.flow("gw1", "come",  "被觀護人到地檢")
    p.flow("gw1", "visit", "觀護人出訪")
    p.flow("visit", "recv")
    p.flow("come", "itv")
    p.flow("recv", "itv")
    p.flow("itv", "up")
    p.flow("up", "stt")
    p.flow("stt", "fix")
    p.flow("fix", "gen")
    p.flow("gen", "plan")
    p.flow("plan", "rev")
    p.flow("rev", "gw2")
    p.flow("gw2", "edit", "否")
    p.flow("gw2", "wb",   "是")
    p.flow("edit", "rev", route="backLoop")
    p.flow("wb", "sync")
    p.flow("sync", "e")
    return p


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    emit(build(), outdir, fmt="drawio", src=__file__,
         xml=True, svg=True, viewer=True,
         change="系統名稱更正:觀護案件管理作業系統、受保護管束人再犯風險評估智慧輔助系統、AI觀護助理系統",
         change_kind="文字", change_source="口頭指示")
    print("done ->", os.path.abspath(outdir))
