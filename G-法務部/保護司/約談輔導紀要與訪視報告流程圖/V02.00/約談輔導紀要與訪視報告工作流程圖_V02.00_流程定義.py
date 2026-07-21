# -*- coding: utf-8 -*-
"""約談輔導紀要與訪視報告工作流程圖(保護司/AI觀護助理系統)
角色:觀護人、被觀護人
對應工項(工項拆解-v1.md):M5-02 錄音控制面板、M5-03 報告智慧編輯器、
M6-01 語音辨識(STT)、M7-02 Prompt模板(約談輔導紀要、訪視報告、風險評估與
處遇建議)、M7-03 抗幻覺、M9 異質系統資料介接、M12-01 報告雙向同步回寫
跨系統自動介接之連線以紅色標示(emit 後後處理 .drawio/.svg/檢視器)。
執行: python 本檔 [輸出資料夾]
"""
import io, sys, os, re
sys.path.insert(0, r"C:\Users\User\.claude\plugins\marketplaces\lancelot-skills\plugins\geo-bpmn-flow-builder\skills\geo-bpmn-flow-builder\scripts")
from bpmn_builder import Proc, emit

VERSION = "V02.00"
# 跨系統自動介接連線(上紅色):(source, target)
RED_FLOWS = [
    ("query", "load"),   # 受保護管束人再犯風險評估智慧輔助系統 → AI觀護助理系統(帶入個案資料)
    ("gw2",   "wb"),     # AI觀護助理系統 → 受保護管束人再犯風險評估智慧輔助系統(回填存檔)
    ("wb",    "sync"),   # 受保護管束人再犯風險評估智慧輔助系統 → 觀護案件管理作業系統(回存)
]
RED = "#cc0000"


def build():
    p = Proc("約談輔導紀要與訪視報告工作流程圖",
             "約談輔導紀要與訪視報告工作流程圖",
             ["觀護人", "被觀護人"],
             version=VERSION)

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
    p.add("plan",  "task",    "產出風險評估與\n處遇建議(M7-02)",   0, kind="system")
    p.add("pdoc",  "output",  "風險評估與\n處遇建議",             0)
    p.add("n1",    "note",    "M7-02 標準Prompt模板:約談輔導紀要、\n訪視報告、風險評估與處遇建議", 1, 8)
    p.add("rev",   "task",    "觀護人審閱報告與處遇建議",          0, kind="user")
    p.add("gw2",   "gateway", "無誤?",                          0)
    p.add("edit",  "task",    "以報告智慧編輯器修改(M5-03)",       0, kind="user")
    p.add("wb",    "task",    "回填受保護管束人再犯風險評估\n智慧輔助系統存檔(M12-01)", 0, kind="system")
    p.add("sync",  "task",    "回存至觀護案件管理作業系統(M12-01)", 0, kind="system")
    p.add("e",     "end",     "結束本次訪談",                     0)

    p.assoc("itv", "rec")
    p.assoc("gen", "doc")
    p.assoc("plan", "pdoc")
    p.assoc("n1", "plan")

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


def _read(path):
    return io.open(path, encoding="utf-8").read()


def _write(path, s):
    io.open(path, "w", encoding="utf-8").write(s)


def paint_red(p, vdir, stem):
    """後處理:把 RED_FLOWS 對應連線改紅(drawio 依 source/target;
    SVG/檢視器依順序流輸出順序 = p.flows 定義順序)。"""
    from bpmn_builder import _ncname
    red_pairs = {(_ncname(a), _ncname(b)) for a, b in RED_FLOWS}
    red_idx = [i for i, (fid, s_, t_, lbl, rt) in enumerate(p.flows)
               if (s_, t_) in red_pairs]
    assert len(red_idx) == len(RED_FLOWS), "RED_FLOWS 有未對應到的連線"

    # .drawio:依 source/target 屬性改 strokeColor
    dpath = os.path.join(vdir, stem + ".drawio")
    d = _read(dpath)
    n = 0
    def repl(m):
        nonlocal n
        cell = m.group(0)
        src = re.search(r'source="([^"]+)"', cell)
        tgt = re.search(r'target="([^"]+)"', cell)
        if src and tgt and (src.group(1), tgt.group(1)) in red_pairs and 'edge="1"' in cell:
            n += 1
            return cell.replace("strokeColor=#3a4a59", "strokeColor=" + RED)
        return cell
    d = re.sub(r"<mxCell [^>]*edge=\"1\"[^>]*>", repl, d)
    assert n == len(RED_FLOWS), "drawio 紅線數不符:%d" % n
    _write(dpath, d)

    # .svg 與 _檢視器.html:順序流箭頭路徑依定義順序;加紅色箭頭 marker
    for fname in (stem + ".svg", stem + "_檢視器.html"):
        fpath = os.path.join(vdir, fname)
        if not os.path.exists(fpath):
            continue
        s = _read(fpath)
        s = s.replace(
            '<marker id="arr"',
            '<marker id="arrred" markerWidth="9" markerHeight="9" refX="7" refY="3" '
            'orient="auto" markerUnits="strokeWidth">'
            '<path d="M0,0 L8,3 L0,6 Z" fill="%s"/></marker><marker id="arr"' % RED)
        parts = s.split('stroke="#5a6b7b" stroke-width="1.6" marker-end="url(#arr)"')
        assert len(parts) - 1 == len(p.flows), "SVG 順序流數不符:%d" % (len(parts) - 1)
        out = parts[0]
        for i in range(1, len(parts)):
            sep = ('stroke="%s" stroke-width="1.6" marker-end="url(#arrred)"' % RED) \
                if (i - 1) in red_idx else \
                'stroke="#5a6b7b" stroke-width="1.6" marker-end="url(#arr)"'
            out += sep + parts[i]
        _write(fpath, out)


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    p = build()
    emit(p, outdir, fmt="drawio", src=__file__,
         xml=True, svg=True, viewer=True,
         change="跨系統自動介接連線標紅(帶入個案資料、回填存檔、回存案管);"
                "補 M7-02 標準Prompt模板註解(約談輔導紀要、訪視報告、風險評估與處遇建議);"
                "產出任務更名含風險評估",
         change_kind="結構", change_source="口頭指示")
    paint_red(p, os.path.join(outdir, VERSION), "約談輔導紀要與訪視報告工作流程圖_" + VERSION)
    print("done ->", os.path.abspath(outdir))
