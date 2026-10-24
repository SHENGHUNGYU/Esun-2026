'use strict';
let apiMode='catalog',apiExchange='all',apiPriority='all',apiCategory='all',apiSearch='',apiPage=1;
const API_PAGE_SIZE=30;
function exchangeApis(){
 const c=EXCHANGE_APIS,core=c.items.filter(x=>['P0','P1'].includes(x.priority)).length;
 view.innerHTML=title('OFFICIAL API INVENTORY','TWSE／TPEx 官方端點','完整 Swagger 盤點，對照參賽資料需求。每個端點可展開方法、欄位、用途與限制。')+`
 <div class="api-overview"><div><strong>${c.items.length}</strong><span>全部 GET 端點</span></div>${c.sources.map(s=>`<div><strong>${s.count}</strong><span>${s.exchange} · ${s.oas}</span></div>`).join('')}<div><strong>${core}</strong><span>P0＋P1 優先候選</span></div></div>
 <div class="note">盤點 ${c.updated} · 9 個代表端點已唯讀探測，其餘已核對規格。<b>全部端點未宣告查詢參數</b>；名稱含「歷史」不保證指定日期或多年資料。Beta／技術指標仍需足夠歷史原料自行計算。</div>
 <div class="data-mode" role="group" aria-label="API頁內容"><button data-api-mode="catalog" aria-pressed="${apiMode==='catalog'}">端點與欄位</button><button data-api-mode="guide" aria-pressed="${apiMode==='guide'}">接入指南・實測・缺口</button></div>
 <div id="api-body"></div>`;
 view.querySelectorAll('[data-api-mode]').forEach(b=>b.onclick=()=>{apiMode=b.dataset.apiMode;view.querySelectorAll('[data-api-mode]').forEach(x=>x.setAttribute('aria-pressed',x.dataset.apiMode===apiMode));renderApiBody()});renderApiBody();
}
function renderApiBody(){
 const c=EXCHANGE_APIS,body=document.getElementById('api-body');
 if(apiMode==='guide'){body.innerHTML=`<div class="page-links api-downloads"><a class="link-button" href="documents/11-openapi-guide.md" download>下載接入指南</a><a class="link-button" href="#data">決策資料地圖 →</a></div><article class="reader">${DOCS.find(x=>x.id==='11-openapi-guide.md').html}</article>`;body.querySelectorAll('a[href^="https:"]').forEach(a=>{a.target='_blank';a.rel='noopener'});return}
 body.innerHTML=`<div class="api-downloads page-links"><a class="link-button" href="api-specs/exchange-apis.json" download>完整端點 JSON ↓</a>${c.sources.map(s=>`<a class="link-button" href="documents/${s.exchange==='TWSE'?'12-twse':'13-tpex'}-endpoints.md" download>${s.exchange} 全欄位 Markdown ↓</a>`).join('')}</div>
 <div class="api-controls"><label class="api-search" for="api-search">搜尋端點、欄位或需求編號<input id="api-search" type="search" placeholder="例如：營收、TradeValue、D25、STOCK_DAY" value="${esc(apiSearch)}"></label><label for="api-exchange">交易所<select id="api-exchange">${[['all','全部交易所'],['TWSE','TWSE 上市'],['TPEx','TPEx 上櫃']].map(([k,v])=>`<option value="${k}" ${apiExchange===k?'selected':''}>${v}</option>`).join('')}</select></label><label for="api-priority">優先序<select id="api-priority"><option value="all">全部端點</option><option value="core" ${apiPriority==='core'?'selected':''}>兩週核心 P0＋P1</option>${Object.entries(c.priorities).map(([k,v])=>`<option value="${k}" ${apiPriority===k?'selected':''}>${k} ${esc(v)}</option>`).join('')}</select></label><label for="api-category">決策面向<select id="api-category"><option value="all">全部面向</option>${c.categories.map(x=>`<option value="${x.id}" ${apiCategory===x.id?'selected':''}>${esc(x.title)}</option>`).join('')}</select></label></div>
 <div class="data-result-bar"><span id="api-count" role="status" aria-live="polite"></span><button id="api-core" class="quiet">只看兩週核心</button><button id="api-reset" class="quiet">全部端點／清除篩選</button></div><p class="data-caption">優先序與需求關聯為本計畫的判斷；欄位與 Path 依官方規格。關聯表示可支持的部分原料，須再驗證單位、日期、覆蓋與完整性。</p>
 <div id="api-results"></div><div id="api-pager" class="api-pager" aria-label="端點列表分頁"></div>
 <details class="api-source-summary"><summary>官方來源、規格快照與下載</summary>${c.sources.map(s=>`<section><h3>${s.exchange}</h3><p><a href="${s.entry_url}" target="_blank" rel="noopener">官方 Swagger UI ↗</a> · <a href="${s.spec_url}" target="_blank" rel="noopener">官方 JSON 規格 ↗</a> · <a href="api-specs/${s.exchange.toLowerCase()}-swagger.json" download>本次完整快照 ↓</a></p><p>Base URL <code>${esc(s.base_url)}</code> · 服務版號 ${s.info_version}</p><p class="api-hash">SHA-256 ${s.sha256}</p></section>`).join('')}</details>`;
 const update=()=>{apiPage=1;renderApiResults()};
 document.getElementById('api-search').oninput=e=>{apiSearch=e.target.value;update()};
 document.getElementById('api-exchange').onchange=e=>{apiExchange=e.target.value;update()};
 document.getElementById('api-priority').onchange=e=>{apiPriority=e.target.value;update()};
 document.getElementById('api-category').onchange=e=>{apiCategory=e.target.value;update()};
 document.getElementById('api-core').onclick=()=>{apiPriority='core';document.getElementById('api-priority').value='core';update()};
 document.getElementById('api-reset').onclick=()=>{apiSearch='';apiExchange=apiPriority=apiCategory='all';document.getElementById('api-search').value='';['exchange','priority','category'].forEach(k=>document.getElementById('api-'+k).value='all');update()};renderApiResults();
}
function renderApiResults(){
 const c=EXCHANGE_APIS,q=apiSearch.trim().toLocaleLowerCase();
 const rows=c.items.filter(x=>(apiExchange==='all'||x.exchange===apiExchange)&&(apiCategory==='all'||x.category===apiCategory)&&(apiPriority==='all'||(apiPriority==='core'?['P0','P1'].includes(x.priority):x.priority===apiPriority))&&(!q||[x.id,x.path,x.summary,x.use,x.caveat,...x.tags,...x.data_refs,...x.fields.map(f=>f.name+' '+f.description)].join(' ').toLocaleLowerCase().includes(q)));
 const pages=Math.max(1,Math.ceil(rows.length/API_PAGE_SIZE));apiPage=Math.min(apiPage,pages);
 document.getElementById('api-count').textContent=`符合 ${rows.length} / ${c.items.length} 個端點${rows.length?` · 第 ${apiPage} / ${pages} 頁`:''}`;
 const shown=rows.slice((apiPage-1)*API_PAGE_SIZE,apiPage*API_PAGE_SIZE);
 document.getElementById('api-results').innerHTML=shown.length?shown.map(apiCard).join(''):'<div class="data-empty"><h3>沒有符合的端點</h3><p>可清除篩選或查看接入指南。T86、ETF完整持股與CFO等部分需求，需要另服務補足。</p></div>';
 document.getElementById('api-pager').innerHTML=rows.length?`<button class="quiet" data-api-page="${apiPage-1}" ${apiPage===1?'disabled':''}>← 上一頁</button><label for="api-page">頁碼<select id="api-page">${Array.from({length:pages},(_,i)=>`<option value="${i+1}" ${apiPage===i+1?'selected':''}>${i+1} / ${pages}</option>`).join('')}</select></label><button class="quiet" data-api-page="${apiPage+1}" ${apiPage===pages?'disabled':''}>下一頁 →</button>`:'';
 view.querySelectorAll('[data-api-page]').forEach(b=>b.onclick=()=>{apiPage=Number(b.dataset.apiPage);renderApiResults();document.getElementById('api-results').scrollIntoView({block:'start'})});
 const picker=document.getElementById('api-page');if(picker)picker.onchange=e=>{apiPage=Number(e.target.value);renderApiResults();document.getElementById('api-results').scrollIntoView({block:'start'})};
 view.querySelectorAll('[data-api-copy]').forEach(b=>b.onclick=async()=>{try{await navigator.clipboard.writeText(b.dataset.apiCopy);b.textContent='已複製 URL'}catch{b.textContent='請選取上方 URL 複製'}});
}
function apiCard(x){
 const probe=x.probe;
 return `<details class="api-item"><summary><span class="api-item-meta"><span class="tag">${esc(x.exchange)}</span><span class="data-tier ${x.priority.toLowerCase()}">${esc(x.priority)}</span><span>${esc(x.verification)}</span></span><span class="api-item-title">${esc(x.summary)}</span><span class="api-path"><b>${x.method}</b> ${esc(x.path)}</span><span class="api-brief">${esc(x.use)}</span><span class="data-expand">${x.fields.length} 個欄位 · 展開完整定義與接入限制 <span aria-hidden="true">＋</span></span></summary><div class="api-item-body"><div class="api-url"><a href="${esc(x.url)}" target="_blank" rel="noopener">${esc(x.url)}</a><button class="quiet" data-api-copy="${esc(x.url)}">複製 URL</button></div><dl><dt>官方分類／可支持需求</dt><dd>${esc(x.tags.join('、'))} · ${esc(x.data_refs.join('、')||'非目前主線')}</dd><dt>查詢參數與歷史</dt><dd>${x.parameters.length?esc(JSON.stringify(x.parameters)):'Swagger 未宣告查詢參數（日期、代號、分頁皆無文件化保證）。'} ${esc(x.history)}</dd><dt>回應與授權設定</dt><dd>規格根型別 ${esc(x.response_shape)}；${esc(x.media_types.join('／'))}；${x.security.length?'另見原始 security 設定':'未宣告 security'}。精確更新時間、配額與 SLA 仍待確認。</dd><dt>接入注意</dt><dd class="api-caveat">${esc(x.caveat)}</dd></dl>${probe?`<div class="api-probe"><strong>代表探測</strong><p>HTTP ${probe.http_status} · ${probe.rows??'未知'} 列 · 實際根結構 ${esc(probe.actual_shape||'未知')}<br>取得時間 ${esc(probe.fetched_at)}<br>資料日期 ${esc(JSON.stringify(probe.date_ranges||{}))}</p><small>只代表該次觀測，完整證據見端點 JSON。</small></div>`:''}<h4>全部官方欄位</h4>${table(['原始名稱（含空白）','型別','官方描述'],x.fields.map(f=>[`<code>${esc(JSON.stringify(f.name))}</code>`,esc(f.type),esc(f.description)]))}<a class="link-button" href="${x.spec_url}" target="_blank" rel="noopener">官方原始 Swagger ↗</a></div></details>`;
}
