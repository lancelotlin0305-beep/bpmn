# -*- coding: utf-8 -*-
"""數位卷證標籤製作工作流程圖(多頁):
頁1 現行工作流程(未導入AI)、頁2 AI智慧輔助系統流程(現況規劃)、
頁3 沿用數位卷證系統OCR・省算力方案、頁4 資安優先方案
V08.00:頁4資安優先方案重構——數位卷證系統初步取得數位卷證後,將卷證PDF傳送AI智慧
  輔助系統進行OCR與標籤識別;AI識別完回傳數位卷證系統,由檢察事務官於系統內檢視標籤
  是否符合、不符則人工調整;不再另產出帶標籤卷證PDF檔,直接於數位卷證系統存檔;另由
  檢察官於數位卷證系統執行下載。
V07.00:頁4資安優先方案之待確認項目均已確認完成,移除全部待確認標示(待確認①虛線框
  容器、待確認①/②備註),頁名去除「含待確認流程」;並套用使用者手動調整——頁3移除
  「換頁速度過慢」「不含回傳」兩則備註、頁4精簡資安備註措辭。
執行: python 數位卷證標籤製作工作流程圖_流程定義.py [輸出資料夾]
"""
import sys, os
sys.path.insert(0, r"C:\Users\User\.claude\plugins\marketplaces\lancelot-skills\plugins\geo-bpmn-flow-builder\skills\geo-bpmn-flow-builder\scripts")
from bpmn_builder import Proc, Collab, emit_multi

VERSION = "V09.00"


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
    p.add("n3", "note", "OCR辨識由AI智慧輔助系統執行:支援繁中英與PDF/TIFF/JPG,辨識準確率依專家小組會議決議標準;單頁≤5秒、100頁批次≤10分鐘", 0)
    p.assoc("n3", "a5")
    p.add("n4", "note", "應具工作階段保留,重新登入可銜接前次作業,免重跑批次辨識", 0)
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


def build_reuse():
    """頁3:沿用數位卷證系統OCR・省算力方案——數位卷證系統已完成OCR,
    直接下載加密卷證PDF匯入AI,略過OCR辨識,其餘同頁2。"""
    p = Proc("數位卷證標籤製作沿用OCR方案工作流程圖",
             "數位卷證標籤製作工作流程圖(沿用數位卷證系統OCR・省算力方案)",
             ["檢察事務官", "檢察官"], version=VERSION,
             bands=[("數位卷證系統", ["r_s", "r_a1", "r_a2", "r_a3"]),
                    ("AI智慧輔助系統", ["r_a4", "r_a5b", "r_a5c", "r_a5d",
                                    "r_a6", "r_a7", "r_gw", "r_a8", "r_a9"]),
                    ("卷證交付", ["r_a10", "r_e"])])
    p.add("r_s",  "start",   "開始", 0)
    p.add("r_a1", "task",    "登入數位卷證系統查詢數位卷證", 0, kind="user")
    p.add("r_a2", "task",    "開啟數位卷證PDF", 0, kind="user")
    p.add("r_a3", "task",    "直接下載具數位金鑰加密之卷證PDF檔", 0, kind="user")
    p.add("r_a4", "task",    "將卷證PDF匯入AI智慧輔助系統", 0, kind="user")
    p.add("r_a5b","task",    "卷證類型辨識與關鍵資訊擷取", 0, kind="system")
    p.add("r_a5c","task",    "證據標題自動摘要", 0, kind="system")
    p.add("r_a5d","task",    "頁數起迄判讀與分段標記", 0, kind="system")
    p.add("r_a6", "task",    "數位標籤識別與製作", 0, kind="system")
    p.add("r_a7", "task",    "檢視標籤是否符合需求", 0, kind="user")
    p.add("r_gw", "gateway", "符合?", 0)
    p.add("r_a8", "task",    "人工調整標籤", 0, kind="user")
    p.add("r_a9", "task",    "產出帶標籤之卷證PDF檔", 0, kind="system")
    p.add("r_a10","task",    "使用帶標籤卷證PDF辦理案件", 1, kind="user")
    p.add("r_e",  "end",     "結束", 1)

    p.add("r_d1", "output", "加密卷證PDF檔", 0)
    p.add("r_d2", "output", "帶標籤卷證PDF檔", 0)
    p.add("r_d3", "output", "證據清單", 0)
    p.assoc("r_a3", "r_d1"); p.assoc("r_a9", "r_d2"); p.assoc("r_a5d", "r_d3")

    p.add("rn2", "note", "數位卷證系統之卷證PDF已完成OCR,為節省算力,匯入後免重跑OCR辨識,直接做卷證類型辨識與關鍵資訊擷取", 0)
    p.assoc("rn2", "r_a5b")

    p.flow("r_s", "r_a1"); p.flow("r_a1", "r_a2"); p.flow("r_a2", "r_a3")
    p.flow("r_a3", "r_a4"); p.flow("r_a4", "r_a5b")
    p.flow("r_a5b", "r_a5c"); p.flow("r_a5c", "r_a5d"); p.flow("r_a5d", "r_a6")
    p.flow("r_a6", "r_a7"); p.flow("r_a7", "r_gw")
    p.flow("r_gw", "r_a9", "符合→是")
    p.flow("r_gw", "r_a8", "符合→否")
    p.flow("r_a8", "r_a9")
    p.flow("r_a9", "r_a10")
    p.flow("r_a10", "r_e")
    return p


def build_alt():
    """頁4:資安優先方案——3 系統各為獨立 pool 協作圖:數位卷證系統(取得PDF→傳AI,
    AI回傳後檢視/調整/存檔)、AI智慧輔助系統(OCR與標籤識別)、卷證交付(檢察官下載);
    數位卷證系統↔AI 來回、數位卷證系統→卷證交付 皆以訊息流銜接。"""
    c = Collab("數位卷證標籤製作調整方案工作流程圖",
               "數位卷證標籤製作工作流程圖(資安優先方案)", version=VERSION)

    # 階梯式列位(數位卷證段1:0-3、AI:4-11、數位卷證段2:12-17、卷證交付:18-20)
    # Pool 1:數位卷證系統(檢察事務官;含去AI繞一圈的兩段)
    pDoc = c.add_pool(Proc("alt_pDoc", "數位卷證系統", ["檢察事務官"]))
    pDoc.lane_subs = [2]
    pDoc.add("b_s",  "start", "開始", 0, 0)
    pDoc.add("b_a1", "task",  "取得新上傳之數位卷證PDF", 0, 1, kind="system")
    pDoc.add("b_a3", "task",  "將卷證PDF傳送至AI智慧輔助系統", 0, 2, kind="system")
    pDoc.add("b_x1", "end",   "送AI進行OCR與標籤識別", 0, 3)
    pDoc.add("bn0", "note",
             "前段全自動、無人工介入:當其他使用者上傳數位卷證,數位卷證系統取得新卷證時"
             "即自動將PDF送AI智慧輔助系統進行OCR與標籤識別;結果回傳後標籤直接回存數位"
             "卷證系統,不另產出外部帶標籤PDF檔;卷證由檢察官於數位卷證系統內下載", 0)
    pDoc.assoc("bn0", "b_a1")
    pDoc.flow("b_s", "b_a1"); pDoc.flow("b_a1", "b_a3"); pDoc.flow("b_a3", "b_x1")
    pDoc.add("b_rs", "start", "AI回傳標籤識別結果", 0, 12)
    pDoc.add("b_a7", "task",  "檢視標籤是否符合需求", 0, 13, kind="user")
    pDoc.add("b_gw", "gateway", "符合?", 0, 14)
    pDoc.add("b_save","task", "於數位卷證系統將檔案存檔", 0, 16, kind="system")
    pDoc.add("b_x2", "end",   "標籤存檔完成", 0, 17)
    pDoc.add("b_a8", "task",  "人工調整標籤", 0, 15, kind="user")
    pDoc.nodes["b_a8"]["sub"] = 1   # 符合→否 分支旁置右子欄
    pDoc.flow("b_rs", "b_a7"); pDoc.flow("b_a7", "b_gw")
    pDoc.flow("b_gw", "b_save", "符合→是", route="sideLeft")
    pDoc.flow("b_gw", "b_a8", "符合→否", route="outRight")
    pDoc.flow("b_a8", "b_save"); pDoc.flow("b_save", "b_x2")

    # Pool 2:AI智慧輔助系統
    pAI = c.add_pool(Proc("alt_pAI", "AI智慧輔助系統", ["系統"]))
    pAI.add("b_bs", "start", "接收卷證PDF", 0, 4)
    pAI.add("b_ocr","task",  "執行OCR辨識", 0, 5, kind="system")
    pAI.add("b_a5b","task",  "卷證類型辨識與關鍵資訊擷取", 0, 6, kind="system")
    pAI.add("b_a5c","task",  "證據標題自動摘要", 0, 7, kind="system")
    pAI.add("b_a5d","task",  "頁數起迄判讀與分段標記", 0, 8, kind="system")
    pAI.add("b_a6", "task",  "數位標籤識別與製作", 0, 9, kind="system")
    pAI.add("b_ret","task",  "將標籤識別結果回傳數位卷證系統", 0, 10, kind="system")
    pAI.add("b_be", "end",   "回傳完成", 0, 11)
    pAI.add("b_d3", "output", "證據清單", 0)
    pAI.assoc("b_a5d", "b_d3")
    pAI.flow("b_bs", "b_ocr"); pAI.flow("b_ocr", "b_a5b"); pAI.flow("b_a5b", "b_a5c")
    pAI.flow("b_a5c", "b_a5d"); pAI.flow("b_a5d", "b_a6"); pAI.flow("b_a6", "b_ret")
    pAI.flow("b_ret", "b_be")

    # Pool 3:卷證交付
    pDel = c.add_pool(Proc("alt_pDel", "卷證交付", ["檢察官"]))
    pDel.add("b_cs", "start", "收到已存檔卷證", 0, 18)
    pDel.add("b_dl", "task",  "於數位卷證系統下載卷證", 0, 19, kind="user")
    pDel.add("b_e",  "end",   "結束", 0, 20)
    pDel.flow("b_cs", "b_dl"); pDel.flow("b_dl", "b_e")

    # 跨 pool 訊息流
    c.message("b_x1", "b_bs", "卷證PDF送AI進行OCR與標籤識別")
    c.message("b_be", "b_rs", "標籤識別結果回傳數位卷證系統")
    c.message("b_x2", "b_cs", "卷證已存檔,通知可下載")
    return c


def build_cur():
    """頁3:現行工作流程(未導入AI)——下載卷證PDF後於PDF編輯器人工編輯數位標籤。"""
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
    emit_multi([build_cur(), build_ai(), build_reuse(), build_alt()],
               "數位卷證標籤製作工作流程圖", outdir, version=VERSION, src=__file__,
               change="頁4資安優先方案:原 4 個系統分區(bands)改為 3 個獨立 pool"
                      "——數位卷證系統(合併原前後兩段、含去AI來回)/AI智慧輔助系統/"
                      "卷證交付(檢察官下載);數位卷證系統↔AI 來回、數位卷證系統→卷證交付"
                      "皆以訊息流銜接;閘道「符合?」否分支旁置右子欄",
               change_kind="結構", change_source="口頭指示")
    print("done ->", os.path.abspath(outdir))
