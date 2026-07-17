# -*- coding: utf-8 -*-
"""統計標籤判斷工作流程圖(多頁):頁1 偵查類、頁2 執行類、頁3 偵查類(含介接說明)、頁4 執行類(含介接說明)
執行: python 統計標籤判斷_V06.00_流程定義.py [輸出資料夾]
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
                                      "a_10", "a_gw", "a_11", "a_e", "a_n1"])])
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
    p.add("a_n1", "note",   "符合→否時:後續由統計處收集不符資訊,回饋進行判讀邏輯調整", 1, 15)
    p.assoc("a_d1", "a_3"); p.assoc("a_5", "a_d2"); p.assoc("a_n1", ("a_gw", "a_e"))

    p.flow("a_s", "a_1"); p.flow("a_1", "a_2"); p.flow("a_2", "a_3")
    p.flow("a_3", "a_4"); p.flow("a_4", "a_5"); p.flow("a_5", "a_sftp")
    p.flow("a_sftp", "a_6"); p.flow("a_6", "a_7"); p.flow("a_7", "a_8")
    p.flow("a_8", "a_9"); p.flow("a_9", "a_10"); p.flow("a_10", "a_gw")
    p.flow("a_gw", "a_11", "符合→是")
    p.flow("a_gw", "a_e", "符合→否(不引用)")
    p.flow("a_11", "a_e")
    return p


def build_pretrial_notes():
    """頁3:偵查類(含介接說明)。"""
    p = Proc("統計標籤判斷_偵查類_介接說明", "統計標籤判斷(偵查類)工作流程圖(含介接說明)",
             ["檢察官", "刑案管理系統使用者"],
             bands=[("書類生成系統", ["c_s", "c_1", "c_2"]),
                    ("波特玩系統", ["c_3", "c_4", "c_5"]),
                    ("刑案管理系統", ["c_sftp", "c_6", "c_7", "c_8", "c_9",
                                      "c_10", "c_gw", "c_11", "c_e", "c_n1"])])
    p.add("c_s",   "start",   "開始", 0)
    p.add("c_1",   "task",    "完成起訴書或不起訴書", 0, kind="user")
    p.add("c_2",   "task",    "執行列印或儲存", 0, kind="user")
    p.add("c_3",   "task",    "呼叫波特玩智慧判斷並傳送書類內文", 0, kind="system")
    p.add("c_4",   "task",    "波特玩判讀個案欄位", 0, kind="system")
    p.add("c_5",   "task",    "整理判讀結果並拋轉至SFTP", 0, kind="system")
    p.add("c_sftp","database","SFTP", 1)
    p.add("c_6",   "task",    "登入刑案管理系統", 1, kind="user")
    p.add("c_7",   "task",    "進入偵查類案件查詢個案", 1, kind="user")
    p.add("c_8",   "task",    "點選「AI引用」按鈕", 1, kind="user")
    p.add("c_9",   "task",    "帶出SFTP判讀資料", 1, kind="system")
    p.add("c_10",  "task",    "檢視判讀資料是否符合需求", 1, kind="user")
    p.add("c_gw",  "gateway", "符合?", 1)
    p.add("c_11",  "task",    "點選引用,欄位資訊存入刑案管理系統", 1, kind="user")
    p.add("c_e",   "end",     "結束", 1)

    p.add("c_d1", "input",  "起訴書/不起訴書內文", 0)
    p.add("c_d2", "output", "欄位判讀結果", 0)
    p.add("c_n1", "note",   "符合→否時:後續由統計處收集不符資訊,回饋進行判讀邏輯調整", 1, 15)
    p.assoc("c_d1", "c_3"); p.assoc("c_5", "c_d2"); p.assoc("c_n1", ("c_gw", "c_e"))

    p.add("c_n2", "note",
          "由書類生成系統觸發呼叫波特玩,並傳遞起訴書/不起訴書之書類資訊", 0)
    p.add("c_n3", "note",
          "波特玩判讀完個案欄位屬性後,將判讀結果拋轉至刑案管理系統之SFTP資料夾,後續由刑案管理系統讀取", 0)
    p.assoc("c_n2", "c_3"); p.assoc("c_n3", "c_5")

    p.flow("c_s", "c_1"); p.flow("c_1", "c_2"); p.flow("c_2", "c_3")
    p.flow("c_3", "c_4"); p.flow("c_4", "c_5"); p.flow("c_5", "c_sftp")
    p.flow("c_sftp", "c_6"); p.flow("c_6", "c_7"); p.flow("c_7", "c_8")
    p.flow("c_8", "c_9"); p.flow("c_9", "c_10"); p.flow("c_10", "c_gw")
    p.flow("c_gw", "c_11", "符合→是")
    p.flow("c_gw", "c_e", "符合→否(不引用)")
    p.flow("c_11", "c_e")
    return p


def build_execution():
    """頁2:執行類(觸發點=波特玩每日排程撈取司法院新增裁判書)。"""
    p = Proc("統計標籤判斷_執行類_工作流程圖", "統計標籤判斷(執行類)工作流程圖",
             ["刑案管理系統使用者"],
             bands=[("波特玩系統", ["b_s", "b_1", "b_2", "b_3"]),
                    ("刑案管理系統", ["b_sftp", "b_4", "b_5", "b_6", "b_7",
                                      "b_8", "b_gw", "b_9", "b_e", "b_n1"])])
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
    p.add("b_n1", "note",   "符合→否時:後續由統計處收集不符資訊,回饋進行判讀邏輯調整", 0, 13)
    p.assoc("b_d1", "b_1"); p.assoc("b_3", "b_d2"); p.assoc("b_n1", ("b_gw", "b_e"))

    p.flow("b_s", "b_1"); p.flow("b_1", "b_2"); p.flow("b_2", "b_3")
    p.flow("b_3", "b_sftp"); p.flow("b_sftp", "b_4"); p.flow("b_4", "b_5")
    p.flow("b_5", "b_6"); p.flow("b_6", "b_7"); p.flow("b_7", "b_8")
    p.flow("b_8", "b_gw")
    p.flow("b_gw", "b_9", "符合→是")
    p.flow("b_gw", "b_e", "符合→否(不引用)")
    p.flow("b_9", "b_e")
    return p


def build_execution_notes():
    """頁4:執行類(含介接說明)。"""
    p = Proc("統計標籤判斷_執行類_介接說明", "統計標籤判斷(執行類)工作流程圖(含介接說明)",
             ["刑案管理系統使用者"],
             bands=[("波特玩系統", ["e_s", "e_1", "e_2", "e_3"]),
                    ("刑案管理系統", ["e_sftp", "e_4", "e_5", "e_6", "e_7",
                                      "e_8", "e_gw", "e_9", "e_e", "e_n1"])])
    p.add("e_s",   "timer",   "每日排程", 0)
    p.add("e_1",   "task",    "至司法院裁判書系統撈取新增裁判書", 0, kind="system")
    p.add("e_2",   "task",    "波特玩判讀個案欄位", 0, kind="system")
    p.add("e_3",   "task",    "整理判讀結果並拋轉至SFTP", 0, kind="system")
    p.add("e_sftp","database","SFTP", 0)
    p.add("e_4",   "task",    "登入刑案管理系統", 0, kind="user")
    p.add("e_5",   "task",    "進入執行類案件查詢個案", 0, kind="user")
    p.add("e_6",   "task",    "點選「AI引用」按鈕", 0, kind="user")
    p.add("e_7",   "task",    "帶出SFTP判讀資料", 0, kind="system")
    p.add("e_8",   "task",    "檢視判讀資料是否符合需求", 0, kind="user")
    p.add("e_gw",  "gateway", "符合?", 0)
    p.add("e_9",   "task",    "點選引用,欄位資訊存入刑案管理系統", 0, kind="user")
    p.add("e_e",   "end",     "結束", 0)

    p.add("e_d1", "input",  "新增裁判書", 0)
    p.add("e_d2", "output", "欄位判讀結果", 0)
    p.add("e_n1", "note",   "符合→否時:後續由統計處收集不符資訊,回饋進行判讀邏輯調整", 0, 13)
    p.assoc("e_d1", "e_1"); p.assoc("e_3", "e_d2"); p.assoc("e_n1", ("e_gw", "e_e"))

    p.add("e_n3", "note",
          "波特玩判讀完個案欄位屬性後,將判讀結果拋轉至刑案管理系統之SFTP資料夾,後續由刑案管理系統讀取", 0)
    p.assoc("e_n3", "e_3")

    p.flow("e_s", "e_1"); p.flow("e_1", "e_2"); p.flow("e_2", "e_3")
    p.flow("e_3", "e_sftp"); p.flow("e_sftp", "e_4"); p.flow("e_4", "e_5")
    p.flow("e_5", "e_6"); p.flow("e_6", "e_7"); p.flow("e_7", "e_8")
    p.flow("e_8", "e_gw")
    p.flow("e_gw", "e_9", "符合→是")
    p.flow("e_gw", "e_e", "符合→否(不引用)")
    p.flow("e_9", "e_e")
    return p


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    emit_multi([build_pretrial(), build_execution(), build_pretrial_notes(), build_execution_notes()], "統計標籤判斷",
               outdir, version="V06.00", src=__file__,
               change="新增頁4:執行類介接說明(SFTP拋轉與讀取)",
               change_kind="文字", change_source="口頭指示")
    print("done ->", os.path.abspath(outdir))
