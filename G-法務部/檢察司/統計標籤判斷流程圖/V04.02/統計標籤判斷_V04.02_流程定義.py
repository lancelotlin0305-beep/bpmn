# -*- coding: utf-8 -*-
"""統計標籤判斷工作流程圖(多頁):頁1 偵查類、頁2 執行類
執行: python 統計標籤判斷_V04.02_流程定義.py [輸出資料夾]
"""
import sys, os
sys.path.insert(0, r"C:\Users\User\.claude\plugins\cache\lancelot-skills\bpmn-flow-builder\20260710.16\skills\bpmn-flow-builder\scripts")
from bpmn_builder import Proc, emit_multi


def build_pretrial():
    """頁1:偵查類(觸發點=檢察官於書類生成系統列印/儲存書類)。"""
    p = Proc("統計標籤判斷_偵查類_工作流程圖", "統計標籤判斷(偵查類)工作流程圖",
             ["檢察官", "刑案管理系統使用者"],
             bands=[("書類生成系統", ["a_s", "a_1", "a_2"]),
                    ("波特玩系統", ["a_3", "a_4", "a_5"]),
                    ("刑案管理系統", ["a_sftp", "a_6", "a_7", "a_8", "a_9",
                                      "a_10", "a_gw", "a_11", "a_e"])])
    p.add("a_s",   "start",   "開始", 0)
    p.add("a_1",   "task",    "完成起訴書或不起訴書", 0, kind="user")
    p.add("a_2",   "task",    "執行列印或儲存", 0, kind="user")
    p.add("a_3",   "task",    "呼叫波特玩智慧判斷並傳送書類內文", 0, kind="system")
    p.add("a_4",   "task",    "波特玩判讀個案欄位", 0, kind="system")
    p.add("a_5",   "task",    "整理判讀結果並拋轉至SFTP", 0, kind="system")
    p.add("a_sftp","database","SFTP", 1)
    p.add("a_6",   "task",    "登入刑案管理系統", 1, kind="user")
    p.add("a_7",   "task",    "進入偵查類案件查詢個案", 1, kind="user")
    p.add("a_8",   "task",    "點選「AI引用」按鈕", 1, kind="user")
    p.add("a_9",   "task",    "帶出SFTP判讀資料", 1, kind="system")
    p.add("a_10",  "task",    "檢視判讀資料是否符合需求", 1, kind="user")
    p.add("a_gw",  "gateway", "符合?", 1)
    p.add("a_11",  "task",    "點選引用,欄位資訊存入刑案管理系統", 1, kind="user")
    p.add("a_e",   "end",     "結束", 1)

    p.add("a_d1", "input",  "起訴書/不起訴書內文", 0)
    p.add("a_d2", "output", "欄位判讀結果", 0)
    p.add("a_n1", "note",   "符合→否時:後續由統計處收集不符資訊,回饋進行判讀邏輯調整", 1)
    p.assoc("a_d1", "a_3"); p.assoc("a_5", "a_d2"); p.assoc("a_n1", ("a_gw", "a_e"))

    p.flow("a_s", "a_1"); p.flow("a_1", "a_2"); p.flow("a_2", "a_3")
    p.flow("a_3", "a_4"); p.flow("a_4", "a_5"); p.flow("a_5", "a_sftp")
    p.flow("a_sftp", "a_6"); p.flow("a_6", "a_7"); p.flow("a_7", "a_8")
    p.flow("a_8", "a_9"); p.flow("a_9", "a_10"); p.flow("a_10", "a_gw")
    p.flow("a_gw", "a_11", "符合→是")
    p.flow("a_gw", "a_e", "符合→否(不引用)")
    p.flow("a_11", "a_e")
    return p


def build_execution():
    """頁2:執行類(觸發點=波特玩每日排程撈取司法院新增裁判書)。"""
    p = Proc("統計標籤判斷_執行類_工作流程圖", "統計標籤判斷(執行類)工作流程圖",
             ["刑案管理系統使用者"],
             bands=[("波特玩系統", ["b_s", "b_1", "b_2", "b_3"]),
                    ("刑案管理系統", ["b_sftp", "b_4", "b_5", "b_6", "b_7",
                                      "b_8", "b_gw", "b_9", "b_e"])])
    p.add("b_s",   "timer",   "每日排程", 0)
    p.add("b_1",   "task",    "至司法院裁判書系統撈取新增裁判書", 0, kind="system")
    p.add("b_2",   "task",    "波特玩判讀個案欄位", 0, kind="system")
    p.add("b_3",   "task",    "整理判讀結果並拋轉至SFTP", 0, kind="system")
    p.add("b_sftp","database","SFTP", 0)
    p.add("b_4",   "task",    "登入刑案管理系統", 0, kind="user")
    p.add("b_5",   "task",    "進入執行類案件查詢個案", 0, kind="user")
    p.add("b_6",   "task",    "點選「AI引用」按鈕", 0, kind="user")
    p.add("b_7",   "task",    "帶出SFTP判讀資料", 0, kind="system")
    p.add("b_8",   "task",    "檢視判讀資料是否符合需求", 0, kind="user")
    p.add("b_gw",  "gateway", "符合?", 0)
    p.add("b_9",   "task",    "點選引用,欄位資訊存入刑案管理系統", 0, kind="user")
    p.add("b_e",   "end",     "結束", 0)

    p.add("b_d1", "input",  "新增裁判書", 0)
    p.add("b_d2", "output", "欄位判讀結果", 0)
    p.add("b_n1", "note",   "符合→否時:後續由統計處收集不符資訊,回饋進行判讀邏輯調整", 0)
    p.assoc("b_d1", "b_1"); p.assoc("b_3", "b_d2"); p.assoc("b_n1", ("b_gw", "b_e"))

    p.flow("b_s", "b_1"); p.flow("b_1", "b_2"); p.flow("b_2", "b_3")
    p.flow("b_3", "b_sftp"); p.flow("b_sftp", "b_4"); p.flow("b_4", "b_5")
    p.flow("b_5", "b_6"); p.flow("b_6", "b_7"); p.flow("b_7", "b_8")
    p.flow("b_8", "b_gw")
    p.flow("b_gw", "b_9", "符合→是")
    p.flow("b_gw", "b_e", "符合→否(不引用)")
    p.flow("b_9", "b_e")
    return p


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    emit_multi([build_pretrial(), build_execution()], "統計標籤判斷",
               outdir, version="V04.02", src=__file__,
               change="註解改括號+文字雙元件錯開;錨定線路徑點顯式寫入防draw.io重佈",
               change_kind="文字", change_source="口頭指示")
    print("done ->", os.path.abspath(outdir))
