"""Reusable competition PDF outputs and a hash-verified local handoff bundle."""
import io
import json
import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape
from pydantic import BaseModel, ConfigDict, Field
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .store import digest,encoded,immutable
from .operations import candidate_bundle

class StrategyDescription(BaseModel):
    model_config=ConfigDict(extra='forbid')
    etf_name: str = Field(min_length=3,max_length=20,pattern=r'^主動[\u3400-\u9fffA-Za-z ]+$')
    theme: str = Field(min_length=1,max_length=50)
    philosophy: str = Field(min_length=100,max_length=300)


def font():
    if 'NotoTC' not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont('NotoTC',str(Path(__file__).parent/'assets/NotoSansTC-Regular.ttf')))
    return 'NotoTC'

def pdf(body):
    buffer=io.BytesIO();family=font()
    styles={
        'title':ParagraphStyle('title',fontName=family,fontSize=19,leading=29,spaceAfter=17,textColor=colors.black,wordWrap='CJK'),
        'heading':ParagraphStyle('heading',fontName=family,fontSize=12,leading=19,spaceBefore=17,spaceAfter=8,textColor=colors.black,wordWrap='CJK',keepWithNext=True),
        'body':ParagraphStyle('body',fontName=family,fontSize=10.5,leading=19,spaceAfter=10,textColor=colors.black,wordWrap='CJK',allowWidows=0,allowOrphans=0),
        'small':ParagraphStyle('small',fontName=family,fontSize=9,leading=16,spaceAfter=9,textColor=colors.HexColor('#555555'),wordWrap='CJK')}
    story=[]
    for kind,text in body:
        if kind=='break':story.append(PageBreak());continue
        story.append(Paragraph(escape(text).replace('\n','<br/>'),styles[kind]))
    def footer(canvas,doc):
        canvas.setFont(family,8);canvas.setFillColor(colors.HexColor('#666666'));canvas.drawRightString(A4[0]-52,32,str(doc.page))
    SimpleDocTemplate(buffer,pagesize=A4,rightMargin=52,leftMargin=52,topMargin=49,bottomMargin=49,title=body[0][1],author='Agent',invariant=1).build(story,onFirstPage=footer,onLaterPages=footer)
    return buffer.getvalue()

def strategy_pdf(description):
    description=StrategyDescription.model_validate(description)
    return pdf([('title','ETF 投資策略說明'),('small','玉山人工智慧公開挑戰賽 Agent 基金經理人'),
        ('heading','ETF 名稱'),('body',description.etf_name),('heading','ETF 投資主題'),('body',description.theme),
        ('heading','ETF 投資理念'),('body',description.philosophy)])

def strategy_description(engine='baseline'):
    name='strategy-description-agent.json' if engine=='llm_agent' else 'strategy-description.json'
    return json.loads((Path(__file__).resolve().parents[2]/'config'/name).read_bytes())

def operating_guide_pdf(engine='baseline'):
    body=[
        ('title','Agent 操作與繳交手冊'),
        ('body','這份手冊供參賽操作人員每日使用。工作台負責資料檢查、自主配置、本地模型推論與文件產出；正式收件結果仍以官方後台及資料包為準。'),
        ('heading','一 啟動與資料準備'),
        ('body','在專案目錄執行 uv sync，依交付說明建立本機模型 SSH 通道，再啟動 uv run esun-agent --root artifacts/live-20261024。工作台只綁定本機，瀏覽器開啟 http://127.0.0.1:8766。勿對網際網路公開帳戶工作台。'),
        ('body','從官方後台下載最新 DataPack 原始 JSON，在今日工作匯入。首日有效全現金與結算尚未產生是不同情況；若資料包顯示缺結算、缺收盤價或未知成交結果，停止產生委託，等待官方新資料。'),
        ('heading','二 更新與自主產出'),
        ('body','更新官方資料，核對來源狀態及行情基準。首日交易 2026/10/27 依目前封存公告使用 2026/10/22；一般日期使用官方資料包 as_of_date。更晚公告的交易事件可以影響交易日，但不代替指定基準價格。'),
        ('body','啟用本地 LLM 後執行 Agent。模型固定版本雜湊，只產生有引用的理由與反證；股數、權重、現金及交易限制由程式核對。模型失敗不會假裝成功，錯誤輸出最多修正一次。'),
        ('heading','三 檢視候選'),
        ('body','在候選與報告選擇本次執行版本，閱讀本地錯誤、發布阻礙、事件檢查、Active Share 及預估配置。確認文件與策略說明一致。資料不足或未驗收項目仍是阻礙，不能把本地通過當成官方通過。'),
        ('body','完整持股 benchmark 必須覆蓋指定全部三十檔 ETF。PCF 適用日與持股評價日不可混用，海外原股與 ADR 不任意合併。內部雙口徑比較不是官方認證，缺資料時不判全數通過。'),
        ('heading','四 官方繳交與證據'),
        ('body','先下載本次 D-Plan JSON 及策略 PDF，在官方後台上傳檢核並閱讀所有結果。上傳或檢核通過不等於已繳交，還需明確送出，再核對歷史紀錄及當日委託。最後送出版本、文件雜湊、時間與回執應一致。'),
        ('body','送出逾時或狀態未知時，先查官方歷史及當日委託，再決定是否重送。工作台的繳交紀錄只保存你已完成操作的證據，不會替你上傳、按送出或更改官方狀態。策略 PDF 亦須在官方標示期限內完成繳交。'),
        ('break',''),('heading','五 結算與恢復'),
        ('body','取得次日官方 DataPack 後，在繳交紀錄與對帳選擇前次候選並上傳新資料包。executed 仍可能有個別 excluded_codes；voided 應核對整批作廢原因。正式帳戶與庫存以官方資料為真值，本地模擬只作差異核對。'),
        ('body','violations 是官方累計違規天數，notices 與 warn 提示分開。股票股數差異須檢查公司行動與官方成交結果，不能擅自把本地預估覆寫成正式庫存。中斷後先核對工作程序及封存版本，使用 resume-dplan 恢復；程式或政策已改版就建立新 run。'),
        ('heading','六 備份與尚待外部驗收'),
        ('body','備份完整 artifacts 資料目錄，包含 objects、SQLite 索引、checkpoint、候選及回執。只保留報告無法重建。金鑰與密碼不放入備份交付包、程式庫或網站。'),
        ('body','目前已確認試繳成功，來源為使用者於 2026/10/26 的確認；尚未獨立讀取後台回執。完整 ETF 持股、官方 Active Share 日期與正規化、完整公司行動、官方費用取整、正式收件與結算及長時間穩定性仍須依最新驗收紀錄確認，不可自行勾選完成。')]
    if engine=='llm_agent':
        body[0]=('title','LLM 主導研究版操作與繳交手冊')
        body[3]=('body','以 Python 3.12 或 3.13 執行 uv sync --frozen，再以 ESUN_DATA_ROOT 指定私人資料目錄，執行 scripts/start-agent.sh。開啟 http://127.0.0.1:8766。來源與模型版本須符合 config，私人 DataPack 與快照不隨 Git 提供。')
        body[7]=('body','先更新決策與研究消息來源，在資料與持股建立指定行情基準日的研究因子，再選 LLM 主導模式執行。模型自行查詢基本面、技術、籌碼及消息，提出至少兩個不同方案、比較修訂後自主選擇；程式核對成本、權重、整張股數與硬限制。受阻時不靜默改用基線。')
        body[9]=('body','候選頁保留策略比較、引用、模型與工具紀錄，須閱讀本地錯誤、外部阻礙、事件、Active Share 與配置。恢復使用同一 run 的凍結輸入與 checkpoint；更改程式、模型或資料須新 run。策略 PDF 為新草案，若已繳舊版，先核對可否變更及主題一致性。')
    return pdf(body)

def create_documents(folder,description):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);description=StrategyDescription.model_validate(description)
    outputs={'ETF_strategy.pdf':strategy_pdf(description.model_dump()),'Operator_guide.pdf':operating_guide_pdf(),
        'strategy-description.json':encoded(description.model_dump()),'document-checks.json':encoded({'etf_name_characters':len(description.etf_name),'theme_characters':len(description.theme),'philosophy_characters':len(description.philosophy),
            'name_prefix_valid':description.etf_name.startswith('主動'),'content_review_scope':'Character constraints checked; the strategy narrative must be compared with actual implemented policy.','visual_review_required':True})}
    for name,body in outputs.items():(folder/name).write_bytes(body)
    return outputs

def handoff_zip(store,run_id,documents):
    folder,manifest=candidate_bundle(store,run_id);buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w',zipfile.ZIP_DEFLATED) as archive:
        allow=['report.md','validation.json','active-share.json','trading-risk.json','policy.json','llm-review.json',
            'agent-research.json','strategy-comparison.md','agent-call-evidence.json']
        allow += [n for n in manifest['artifacts'] if n.startswith('D-Plan_')]
        contents={n:(folder/n).read_bytes() for n in allow if n in manifest['artifacts']}
        contents.update(documents)
        for name,body in contents.items():archive.writestr(name,body)
        archive.writestr('handoff-manifest.json',encoded({'run_id':run_id,'candidate_status':manifest['status'],'files':{n:digest(b) for n,b in contents.items()},
            'submission_performed':False,'note':'Local review package. External blockers in validation.json remain in force.'}))
    return buffer.getvalue()
