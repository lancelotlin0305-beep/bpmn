# -*- coding: utf-8 -*-
"""統計標籤判斷工作流程圖(多頁):頁1 偵查類(含介接說明)、頁2 執行類(含介接說明)
V11.00:執行類重構——
  觸發點由「AI每日排程」改為「使用者於案件管理系統執行分案」:分案時傳送
  執行案號+確認案號+被告姓名+身分證號給AI智慧輔助系統;AI依確認案號更新確認號,
  至司法院裁判書系統撈取裁判書並判讀七項欄位;新增閘道「上訴駁回?」——
  是:取原案(上一審)確認案號重查裁判書(迴圈);否:以確認案號+被告姓名取得欄位、
  整理判讀結果;最後以執行案號+被告姓名+身分證號回傳,呼叫刑案管理系統API存暫存。
  新增第三道泳道「案件管理系統」;刑案管理系統後段(登入→查詢→AI引用→引用?)沿用。
執行: python 統計標籤判斷_流程定義.py [輸出資料夾]
"""
import sys, os
sys.path.insert(0, r"D:\claude-skills-marketplace\plugins\geo-bpmn-flow-builder\skills\geo-bpmn-flow-builder\scripts")
from bpmn_builder import Proc, Collab, emit_multi


def build_pretrial():
    """頁1:偵查類——3 系統各為獨立 pool 的協作圖(檢察書類製作系統→AI智慧輔助系統
    →刑案管理系統,單向接力鏈:書類PDF經SFTP批次撈取、判讀結果經API寫入暫存區)。"""
    c = Collab("統計標籤判斷_偵查類_工作流程圖", "統計標籤判斷(偵查類)工作流程圖")

    # 訊息流端點拉齊同列(慣例 20260817.01):書類系統 0-4、小腦/AI 對齊、
    # 刑案 7-15;跨 pool 訊息流走水平直線、不降階
    # Pool 1:檢察書類製作系統
    pA = c.add_pool(Proc("pre_pA", "檢察書類製作系統", ["檢察官"]))
    pA.add("a_s",  "start", "開始", 0, 0)
    pA.add("a_1",  "task",  "完成起訴書或不起訴書", 0, 1, kind="user")
    pA.add("a_2",  "task",  "執行列印或儲存\n(書類列印+核章欄)", 0, 2, kind="user")
    pA.add("a_2b", "task",  "產製書類PDF並拋轉至SFTP", 0, 3, kind="system")
    pA.add("a_ae", "end",   "書類PDF拋轉SFTP", 0, 4)
    pA.add("a_d1", "input", "起訴書/不起訴書PDF", 0)
    pA.assoc("a_d1", "a_2b")
    pA.add("a_n2", "note",
           "檢察官執行列印/儲存時,由書類系統產製書類PDF拋轉至SFTP;AI智慧輔助系統再以批次方式定時撈取判讀(非即時呼叫)", 0)
    pA.assoc("a_n2", "a_2b")
    pA.flow("a_s", "a_1"); pA.flow("a_1", "a_2"); pA.flow("a_2", "a_2b"); pA.flow("a_2b", "a_ae")

    # Pool 小腦:書類系統拋轉之書類PDF暫存於此 SFTP,供 AI 排程撈取(被動來源)
    pXn = c.add_pool(Proc("pre_pXn", "小腦", ["SFTP"]))
    pXn.add("a_xndb", "database", "書類PDF", 0, 4)   # 與 a_ae 同列:訊息流水平
    pXn.add("a_xnote", "note",
            "書類系統拋轉;檔名：包含偵字案號>>需要請宏碁提供標號邏輯", 0, 5)
    pXn.assoc("a_xnote", "a_xndb")

    # Pool 2:AI智慧輔助系統
    pB = c.add_pool(Proc("pre_pB", "AI智慧輔助系統", ["系統"]))
    pB.add("a_bs", "timer", "定時批次排程", 0, 3)
    pB.add("a_3",  "task",  "批次撈取小腦SFTP之書類PDF", 0, 4, kind="system")  # 與 a_xndb 同列
    pB.add("a_4",  "task",  "AI智慧輔助系統判讀五類統計欄位", 0, 5, kind="system")
    pB.add("a_5",  "task",  "整理判讀結果並呼叫刑案管理系統API存入暫存檔", 0, 6, kind="system")
    pB.add("a_ae2","end",   "判讀結果寫入暫存區", 0, 7)
    pB.add("a_d2", "output", "欄位判讀結果", 0)
    pB.assoc("a_5", "a_d2")
    pB.add("a_n3", "note",
           "AI智慧輔助系統判讀完個案欄位屬性後,直接呼叫刑案管理系統API將判讀結果寫入暫存區;使用者於刑案管理系統點選AI引用時,由系統自暫存區讀取(RFP工項要求API整合)", 0)
    pB.assoc("a_n3", "a_5")
    pB.flow("a_bs", "a_3"); pB.flow("a_3", "a_4"); pB.flow("a_4", "a_5"); pB.flow("a_5", "a_ae2")
    # AI 每日排程:自大腦SFTP下載部頒代碼表與法條對照表(供判讀套用),置主流程上方獨立小流程
    pB.add("a_dls", "timer", "每日排程", 0, 0)
    pB.add("a_dl",  "task",  "至大腦SFTP下載部頒代碼表與法條對照表", 0, 1, kind="system")
    pB.add("a_dle", "end",   "完成", 0, 2)
    pB.flow("a_dls", "a_dl"); pB.flow("a_dl", "a_dle")

    # Pool 大腦:部頒代碼表與法條對照表原存於此(SFTP),供 AI 每日下載(被動來源)
    pBr = c.add_pool(Proc("pre_pBr", "大腦", ["SFTP"]))
    pBr.add("a_brdb", "database", "部頒代碼表、法條對照表", 0, 1)   # 與 a_dl 同列

    # Pool 3:刑案管理系統
    pC = c.add_pool(Proc("pre_pC", "刑案管理系統", ["使用者"]))
    pC.lane_subs = [2]
    pC.add("a_cs", "start", "AI判讀結果已寫入暫存區", 0, 7)   # 與 a_ae2 同列:訊息流水平
    pC.add("a_6",  "task",  "登入刑案管理系統", 0, 8, kind="user")
    pC.add("a_7",  "task",  "進入偵查類案件查詢個案", 0, 9, kind="user")
    pC.add("a_8",  "task",  "點選「AI引用」按鈕", 0, 10, kind="user")
    pC.add("a_9",  "task",  "自暫存區讀取AI判讀結果", 0, 11, kind="system")
    pC.add("a_10", "task",  "檢視判讀資料是否符合需求", 0, 12, kind="user")
    pC.add("a_gw", "gateway","引用?", 0, 13)
    pC.add("a_e",  "end",   "結束", 0, 15)
    pC.add("a_11", "task",  "點選引用,欄位資訊存入刑案管理系統", 0, 14, kind="user")
    pC.nodes["a_11"]["sub"] = 1   # 是-分支旁置右子欄,不擋 gw→a_e 直下
    pC.add("a_n1", "note", "引用→否時:後續由統計處收集不符資訊,回饋進行判讀邏輯調整", 0)
    pC.assoc("a_n1", "a_gw")
    pC.flow("a_cs", "a_6"); pC.flow("a_6", "a_7"); pC.flow("a_7", "a_8")
    pC.flow("a_8", "a_9"); pC.flow("a_9", "a_10"); pC.flow("a_10", "a_gw")
    pC.flow("a_gw", "a_e", "引用→否", route="sideLeft")
    pC.flow("a_gw", "a_11", "引用→是", route="outRight")
    pC.flow("a_11", "a_e", route="enterRight")  # 自結束事件右側接入,減少轉折(使用者指示)

    # 跨 pool 訊息流(單向接力)
    c.message("a_ae", "a_xndb", "書類PDF拋轉至SFTP")          # 書類系統→小腦:上傳書類PDF
    c.message("a_xndb", "a_3", "AI排程撈取、下載書類PDF")     # 小腦→AI:批次下載書類PDF
    c.message("a_ae2", "a_cs", "判讀結果寫入刑案管理系統暫存區")
    # 大腦(SFTP)→AI 下載任務:AI 每日下載部頒代碼表與法條對照表
    c.message("a_brdb", "a_dl", "部頒代碼表、法條對照表")
    return c


def build_execution():
    """頁2:執行類——3 個系統各為獨立 pool 的協作圖(單向接力鏈:
    案件管理系統(使用者分案傳資料)→ AI智慧輔助系統(撈判裁判書七欄位)
    → 刑案管理系統(使用者引用),pool 間以訊息流銜接。"""
    c = Collab("統計標籤判斷_執行類_工作流程圖", "統計標籤判斷(執行類)工作流程圖")

    # 訊息流端點拉齊同列(慣例 20260817.01):A 0-3、B 對齊 3-9、C 9-17;
    # 跨 pool 訊息流走水平直線、不降階
    # Pool A:案件管理系統
    pA = c.add_pool(Proc("exec_pA", "案件管理系統", ["地檢署分案室"]))
    pA.add("b_s",  "start", "開始", 0, 0)
    pA.add("b_1",  "task",  "執行分案", 0, 1, kind="user")
    pA.add("b_2",  "task",  "傳送執行案號、確認案號(院方)、被告姓名、身分證號至AI智慧輔助系統", 0, 2, kind="system")
    pA.add("b_ae", "end",   "轉AI智慧輔助系統", 0, 3)
    pA.add("b_n2", "note",
           "使用者於案件管理系統執行分案時,將執行案號、確認案號、被告姓名、身分證號傳給AI智慧輔助系統作為撈取判讀依據", 0)
    pA.assoc("b_n2", "b_2")
    pA.flow("b_s", "b_1"); pA.flow("b_1", "b_2"); pA.flow("b_2", "b_ae")

    # Pool B:AI智慧輔助系統(單泳道加寬至 2 子欄,供閘道 是-分支旁置)
    pB = c.add_pool(Proc("exec_pB", "AI智慧輔助系統", ["系統"]))
    pB.lane_subs = [2]
    pB.add("b_bs", "start", "接收案件資料", 0, 3)   # 與 b_ae 同列:訊息流水平
    pB.add("b_4",  "task",  "依確認案號至司法院裁判書系統查詢下載裁判書", 0, 4, kind="system")
    pB.add("b_5",  "task",  "AI判讀裁判書七項欄位", 0, 5, kind="system")
    pB.add("b_gw1","gateway","駁回?", 0, 6)
    pB.add("b_7",  "task",  "以確認案號+被告姓名取得相關欄位資訊,整理判讀結果", 0, 7, kind="system")
    pB.add("b_8",  "task",  "以執行案號+被告姓名+身分證號回傳,呼叫刑案管理系統API存入暫存檔", 0, 8, kind="system")
    pB.add("b_be", "end",   "回傳刑案管理系統", 0, 9)
    pB.add("b_6",  "task",  "取原案(上一審)確認案號,重查取得上一審裁判書", 0, 7, kind="system")
    pB.nodes["b_6"]["sub"] = 1   # 是-分支旁置右子欄,不擋 gw1→b_7 直下
    pB.add("b_d2", "output", "欄位判讀結果", 0)
    pB.assoc("b_7", "b_d2")   # b_d1(司法院裁判書)已移除:b_4 標籤已含,且讓右通道供重查迴圈走線
    pB.add("b_n5", "note",
           "RFP工項:裁判書API判讀七項欄位(正確率80%);駁回?→是取原案(上一審)確認案號重查上一審裁判書,→否即有裁判結果以此版本分辨", 0)
    pB.add("b_n3", "note",
           "AI判讀完個案欄位屬性後,以執行案號+被告姓名+身分證號呼叫刑案管理系統API將判讀結果寫入暫存區;使用者點選AI引用時由系統自暫存區讀取(RFP工項要求API整合)", 0)
    pB.assoc("b_n5", "b_gw1"); pB.assoc("b_n3", "b_8")  # b_n5 改掛閘道(內容含駁回?邏輯),讓 b_5 給大腦訊息
    pB.flow("b_bs", "b_4"); pB.flow("b_4", "b_5"); pB.flow("b_5", "b_gw1")
    pB.flow("b_gw1", "b_7", "上訴駁回→否")           # 否:主線直下
    pB.flow("b_gw1", "b_6", "上訴駁回→是", route="outRight")  # 是:旁置右子欄
    pB.flow("b_6", "b_4", "重查", route="sideRight")  # 重查:走右通道上回 b_4(b_d1 已移除、右通道淨空)
    pB.flow("b_7", "b_8"); pB.flow("b_8", "b_be")
    # AI 每日排程:自大腦SFTP下載部頒代碼表與法條對照表(供判讀套用),置主流程上方獨立小流程
    pB.add("b_dls", "timer", "每日排程", 0, 0)
    pB.add("b_dl",  "task",  "至大腦SFTP下載部頒代碼表與法條對照表", 0, 1, kind="system")
    pB.add("b_dle", "end",   "完成", 0, 2)
    pB.flow("b_dls", "b_dl"); pB.flow("b_dl", "b_dle")

    # Pool 大腦:部頒代碼表與法條對照表原存於此(SFTP),供 AI 每日下載(被動來源)
    pBr = c.add_pool(Proc("exec_pBr", "大腦", ["SFTP"]))
    pBr.add("b_brdb", "database", "部頒代碼表、法條對照表", 0, 1)   # 與 b_dl 同列

    # Pool C:刑案管理系統(單泳道加寬至 2 子欄,供閘道 是-分支旁置)
    pC = c.add_pool(Proc("exec_pC", "刑案管理系統", ["使用者"]))
    pC.lane_subs = [2]
    pC.add("b_cs", "start", "AI判讀結果已寫入暫存區", 0, 9)   # 與 b_be 同列:訊息流水平
    pC.add("b_9",  "task",  "登入刑案管理系統", 0, 10, kind="user")
    pC.add("b_10", "task",  "進入執行類案件查詢個案", 0, 11, kind="user")
    pC.add("b_11", "task",  "點選「AI引用」按鈕", 0, 12, kind="user")
    pC.add("b_12", "task",  "自暫存區讀取AI判讀結果", 0, 13, kind="system")
    pC.add("b_13", "task",  "檢視判讀資料是否符合需求", 0, 14, kind="user")
    pC.add("b_gw2","gateway","引用?", 0, 15)
    pC.add("b_e",  "end",   "結束", 0, 17)
    pC.add("b_14", "task",  "點選引用,欄位資訊存入刑案管理系統", 0, 16, kind="user")
    pC.nodes["b_14"]["sub"] = 1   # 是-分支旁置右子欄,不擋 gw2→b_e 直下
    pC.add("b_n6", "note", "引用→否時由統計處收集不符資訊,回饋進行判讀邏輯調整", 0)
    pC.assoc("b_n6", "b_gw2")
    pC.flow("b_cs", "b_9"); pC.flow("b_9", "b_10"); pC.flow("b_10", "b_11")
    pC.flow("b_11", "b_12"); pC.flow("b_12", "b_13"); pC.flow("b_13", "b_gw2")
    pC.flow("b_gw2", "b_e", "引用→否", route="sideLeft")  # 否:走左側接入 b_e(與 b_14→b_e 分埠)
    pC.flow("b_gw2", "b_14", "引用→是", route="outRight")  # 是:旁置右子欄
    pC.flow("b_14", "b_e", route="enterRight")  # 自結束事件右側接入,減少轉折(使用者指示)

    # 跨 pool 訊息流(單向接力)
    c.message("b_ae", "b_bs", "案件資料:案號/被告姓名/身分證號")
    c.message("b_be", "b_cs", "AI判讀結果寫入刑案管理系統暫存區")
    # 大腦(SFTP)→AI 下載任務:AI 每日下載部頒代碼表與法條對照表
    c.message("b_brdb", "b_dl", "部頒代碼表、法條對照表")
    return c


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    emit_multi([build_pretrial(), build_execution()], "統計標籤判斷",
               outdir, version="V17.04", src=__file__,
               change="兩頁訊息流端點拉齊同列走水平直線、不降階(舊階梯式列位改正):"
                      "偵查類壓縮3列、執行類壓縮2列;每日排程小流程與大腦同步上移;"
                      "偵查類「小腦訊息流左移」後製隨拉平失效移除",
               change_kind="文字", change_source="口頭指示")

    # ---- 後處理:跨系統自動介接連線標紅(builder 不支援線色,於輸出檔後製) ----
    import io, re
    from bpmn_builder import _git_mode
    RED = "#FF0000"
    # git 版控模式:輸出不建版號子目錄、檔名不帶版號
    GIT = _git_mode(outdir)
    SUF = "" if GIT else "_V11.00"
    vdir = outdir if GIT else os.path.join(outdir, "V11.00")
    red_edges = {  # pid → [(source, target, flow定義順序索引)]
        # 偵查類、執行類皆已改 3-pool 協作圖:跨系統連線成訊息流(本就虛線),不再標紅
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
    print("drawio 標紅連線:", n, "(預期 0:兩頁皆改訊息流)")

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

    # (V17.04 拉平後訊息流走水平直線,原「小腦訊息流左移」後製失效移除)
    print("done ->", os.path.abspath(outdir))
