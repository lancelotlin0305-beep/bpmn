# -*- coding: utf-8 -*-
"""統計標籤判斷工作流程圖(多頁):頁1 偵查類(含介接說明)、頁2 執行類(含介接說明)
V10.00:4頁併為2頁——
  將原獨立的兩頁介接說明併入偵查類/執行類主流程頁(介接註解直接掛在對應任務),
  刪除獨立介接說明兩頁;介接註解移除RFP工項編號,僅保留「RFP工項」字樣;
  流程末端閘道「符合?」改為「引用?」,分支改為 引用→是 / 引用→否。
執行: python 統計標籤判斷_流程定義.py [輸出資料夾]
"""
import sys, os
sys.path.insert(0, r"C:\Users\User\.claude\plugins\marketplaces\lancelot-skills\plugins\geo-bpmn-flow-builder\skills\geo-bpmn-flow-builder\scripts")
from bpmn_builder import Proc, emit_multi


def build_pretrial():
    """頁1:偵查類(觸發點=檢察官於書類生成系統列印/儲存書類→PDF拋轉SFTP→AI批次撈取)。"""
    p = Proc("統計標籤判斷_偵查類_工作流程圖", "統計標籤判斷(偵查類)工作流程圖",
             ["檢察官", "刑案管理系統使用者"],
             bands=[("書類生成系統", ["a_s", "a_1", "a_2", "a_2b", "a_sftpin"]),
                    ("AI智慧輔助系統", ["a_3", "a_4", "a_5"]),
                    ("刑案管理系統", ["a_sftp", "a_6", "a_7", "a_8", "a_9",
                                      "a_10", "a_gw", "a_11", "a_e", "a_n1"])])
    p.add("a_s",    "start",   "開始", 0)
    p.add("a_1",    "task",    "完成起訴書或不起訴書", 0, kind="user")
    p.add("a_2",    "task",    "執行列印或儲存", 0, kind="user")
    p.add("a_2b",   "task",    "產製書類PDF並拋轉至SFTP", 0, kind="system")
    p.add("a_sftpin","database","SFTP(書類PDF)", 0)
    p.add("a_3",    "task",    "批次撈取SFTP之書類PDF", 0, kind="system")
    p.add("a_4",    "task",    "AI智慧輔助系統判讀五類統計欄位", 0, kind="system")
    p.add("a_5",    "task",    "整理判讀結果並呼叫刑案管理系統API存入暫存檔", 0, kind="system")
    p.add("a_sftp", "database","刑案管理系統暫存區", 1)
    p.add("a_6",    "task",    "登入刑案管理系統", 1, kind="user")
    p.add("a_7",    "task",    "進入偵查類案件查詢個案", 1, kind="user")
    p.add("a_8",    "task",    "點選「AI引用」按鈕", 1, kind="user")
    p.add("a_9",    "task",    "自暫存區讀取AI判讀結果", 1, kind="system")
    p.add("a_10",   "task",    "檢視判讀資料是否符合需求", 1, kind="user")
    p.add("a_gw",   "gateway", "引用?", 1)
    p.add("a_11",   "task",    "點選引用,欄位資訊存入刑案管理系統", 1, kind="user")
    p.add("a_e",    "end",     "結束", 1)

    p.add("a_d1", "input",  "起訴書/不起訴書PDF", 0)
    p.add("a_d2", "output", "欄位判讀結果", 0)
    p.add("a_n1", "note",   "引用→否時:後續由統計處收集不符資訊,回饋進行判讀邏輯調整", 1, 17)
    p.assoc("a_d1", "a_2b"); p.assoc("a_5", "a_d2"); p.assoc("a_n1", ("a_gw", "a_e"))

    p.add("a_n2", "note",
          "檢察官執行列印/儲存時,由書類生成系統產製書類PDF拋轉至SFTP;AI智慧輔助系統再以批次方式定時撈取判讀(非即時呼叫)", 0)
    p.add("a_n3", "note",
          "AI智慧輔助系統判讀完個案欄位屬性後,直接呼叫刑案管理系統API將判讀結果寫入暫存區;使用者於刑案管理系統點選AI引用時,由系統自暫存區讀取(RFP工項要求API整合)", 0)
    p.assoc("a_n2", "a_2b"); p.assoc("a_n3", "a_5")

    p.flow("a_s", "a_1"); p.flow("a_1", "a_2"); p.flow("a_2", "a_2b")
    p.flow("a_2b", "a_sftpin"); p.flow("a_sftpin", "a_3")
    p.flow("a_3", "a_4"); p.flow("a_4", "a_5"); p.flow("a_5", "a_sftp")
    p.flow("a_sftp", "a_6"); p.flow("a_6", "a_7"); p.flow("a_7", "a_8")
    p.flow("a_8", "a_9"); p.flow("a_9", "a_10"); p.flow("a_10", "a_gw")
    p.flow("a_gw", "a_11", "引用→是")
    p.flow("a_gw", "a_e", "引用→否")
    p.flow("a_11", "a_e")
    return p


def build_execution():
    """頁2:執行類(觸發點=AI智慧輔助系統每日排程撈取司法院新增裁判書)。"""
    p = Proc("統計標籤判斷_執行類_工作流程圖", "統計標籤判斷(執行類)工作流程圖",
             ["刑案管理系統使用者"],
             bands=[("AI智慧輔助系統", ["b_s", "b_1", "b_2", "b_3"]),
                    ("刑案管理系統", ["b_sftp", "b_4", "b_5", "b_6", "b_7",
                                      "b_8", "b_gw", "b_9", "b_e", "b_n1"])])
    p.add("b_s",   "timer",   "每日排程", 0)
    p.add("b_1",   "task",    "至司法院裁判書系統撈取新增裁判書", 0, kind="system")
    p.add("b_2",   "task",    "AI智慧輔助系統判讀裁判書七項欄位", 0, kind="system")
    p.add("b_3",   "task",    "整理判讀結果並呼叫刑案管理系統API存入暫存檔", 0, kind="system")
    p.add("b_sftp","database","刑案管理系統暫存區", 0)
    p.add("b_4",   "task",    "登入刑案管理系統", 0, kind="user")
    p.add("b_5",   "task",    "進入執行類案件查詢個案", 0, kind="user")
    p.add("b_6",   "task",    "點選「AI引用」按鈕", 0, kind="user")
    p.add("b_7",   "task",    "自暫存區讀取AI判讀結果", 0, kind="system")
    p.add("b_8",   "task",    "檢視判讀資料是否符合需求", 0, kind="user")
    p.add("b_gw",  "gateway", "引用?", 0)
    p.add("b_9",   "task",    "點選引用,欄位資訊存入刑案管理系統", 0, kind="user")
    p.add("b_e",   "end",     "結束", 0)

    p.add("b_d1", "input",  "新增裁判書", 0)
    p.add("b_d2", "output", "欄位判讀結果", 0)
    p.add("b_n1", "note",   "引用→否時:後續由統計處收集不符資訊,回饋進行判讀邏輯調整", 0, 13)
    p.assoc("b_d1", "b_1"); p.assoc("b_3", "b_d2"); p.assoc("b_n1", ("b_gw", "b_e"))

    p.add("b_n3", "note",
          "AI智慧輔助系統判讀完個案欄位屬性後,直接呼叫刑案管理系統API將判讀結果寫入暫存區;使用者於刑案管理系統點選AI引用時,由系統自暫存區讀取(RFP工項要求API整合)", 0)
    p.add("b_n4", "note",
          "RFP工項:裁判書API判讀七項欄位(正確率80%)", 0)
    p.assoc("b_n3", "b_3"); p.assoc("b_n4", "b_1")

    p.flow("b_s", "b_1"); p.flow("b_1", "b_2"); p.flow("b_2", "b_3")
    p.flow("b_3", "b_sftp"); p.flow("b_sftp", "b_4"); p.flow("b_4", "b_5")
    p.flow("b_5", "b_6"); p.flow("b_6", "b_7"); p.flow("b_7", "b_8")
    p.flow("b_8", "b_gw")
    p.flow("b_gw", "b_9", "引用→是")
    p.flow("b_gw", "b_e", "引用→否")
    p.flow("b_9", "b_e")
    return p


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    emit_multi([build_pretrial(), build_execution()], "統計標籤判斷",
               outdir, version="V10.00", src=__file__,
               change="4頁併為2頁:介接說明併入偵查類/執行類主流程頁,刪除獨立介接說明兩頁;註解移除RFP工項編號(僅留「RFP工項」);閘道「符合?」改為「引用?」、分支改引用→是/引用→否",
               change_kind="結構", change_source="口頭指示")

    # ---- 後處理:跨系統自動介接連線標紅(builder 不支援線色,於輸出檔後製) ----
    import io, re
    from bpmn_builder import _git_mode
    RED = "#FF0000"
    # git 版控模式:輸出不建版號子目錄、檔名不帶版號
    GIT = _git_mode(outdir)
    SUF = "" if GIT else "_V10.00"
    vdir = outdir if GIT else os.path.join(outdir, "V10.00")
    red_edges = {  # pid → [(source, target, flow定義順序索引)]
        "統計標籤判斷_偵查類_工作流程圖": [("a_2b", "a_sftpin", 3), ("a_sftpin", "a_3", 4),
                                          ("a_5", "a_sftp", 7)],
        "統計標籤判斷_執行類_工作流程圖": [("b_3", "b_sftp", 3)],
    }

    # 1) .drawio:依 source/target 精準改 style(順序流原色 #3a4a59)
    dpath = os.path.join(vdir, "統計標籤判斷%s.drawio" % SUF)
    t = io.open(dpath, encoding="utf-8").read()
    n = 0
    for pairs in red_edges.values():
        for s, g, _ in pairs:
            pat = re.compile(r'(<mxCell[^>]*style=")([^"]*)("[^>]*source="%s" target="%s")' % (s, g))
            t, k = pat.subn(lambda m: m.group(1)
                            + m.group(2).replace("strokeColor=#3a4a59",
                                                 "strokeColor=%s;strokeWidth=2" % RED)
                            + m.group(3), t)
            n += k
    io.open(dpath, "w", encoding="utf-8").write(t)
    print("drawio 標紅連線:", n, "(預期 4)")

    # 2) .svg:順序流 path 無 id,依 flow() 定義順序取第 idx 條;箭頭改紅色 marker
    FLOW_TAG = re.compile(r'<path d="([^"]+)" fill="none" stroke="#5a6b7b" stroke-width="1.6" marker-end="url\(#(arr)\)"\s*/>')
    MARKER = re.compile(r'<marker id="arr"(.*?)</marker>', re.S)
    red_ds = []
    for pid, pairs in red_edges.items():
        spath = os.path.join(vdir, "%s%s.svg" % (pid, SUF))
        st = io.open(spath, encoding="utf-8").read()
        # 加紅色箭頭 marker(複製 #arr → #arrR)
        st = MARKER.sub(lambda m: m.group(0) + '<marker id="arrR"'
                        + m.group(1).replace("#5a6b7b", RED) + "</marker>", st, count=1)
        tags = list(FLOW_TAG.finditer(st))
        for s, g, idx in pairs:
            m = tags[idx]
            new = ('<path d="%s" fill="none" stroke="%s" stroke-width="2" '
                   'marker-end="url(#arrR)"/>' % (m.group(1), RED))
            st = st.replace(m.group(0), new)
            red_ds.append(m.group(1))
            print("svg 標紅 %s→%s: d=%s" % (s, g, m.group(1)))
        io.open(spath, "w", encoding="utf-8").write(st)

    # 3) 檢視器 html:內嵌 SVG 的 marker id 帶頁前綴(pN_arr),以 d 字串比對同步標紅
    hpath = os.path.join(vdir, "統計標籤判斷%s_檢視器.html" % SUF)
    ht = io.open(hpath, encoding="utf-8").read()
    ht = re.sub(r'<marker id="(p\d+_arr)"(.*?)</marker>',
                lambda m: m.group(0) + '<marker id="%sR"' % m.group(1)
                + m.group(2).replace("#5a6b7b", RED) + "</marker>", ht, flags=re.S)
    for d in red_ds:
        ht = re.sub(r'<path d="%s" fill="none" stroke="#5a6b7b" stroke-width="1.6" marker-end="url\(#(p\d+_arr)\)"\s*/>' % re.escape(d),
                    lambda m: '<path d="%s" fill="none" stroke="%s" stroke-width="2" marker-end="url(#%sR)"/>' % (d, RED, m.group(1)), ht)
    io.open(hpath, "w", encoding="utf-8").write(ht)
    print("檢視器同步標紅完成")
    print("done ->", os.path.abspath(outdir))
