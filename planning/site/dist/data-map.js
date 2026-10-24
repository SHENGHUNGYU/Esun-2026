'use strict';
// The catalog and its downloadable Markdown share decision-data.json.
let dataMode='catalog',dataCategory='all',dataPriority='all',dataQuery='';
function dataSourceLink(s){return `<a href="${esc(s.url)}" ${s.url.startsWith('https:')?'target="_blank" rel="noopener"':''}>${esc(s.title)}${s.url.startsWith('https:')?' ↗':''}</a>`}
function decisionData(){
 const c=DATA_CATALOG;
 view.innerHTML=`<div class="data-heading"><div><div class="eyebrow">DECISION DATA ATLAS</div><h2>決策資料地圖</h2><p class="subtitle">先確定要回答的投資問題，再決定需要哪些資料。</p></div><a class="link-button" href="documents/10-data-catalog.md" download>下載完整清單 ↓</a></div>
 <section class="data-thesis"><span class="small-label">根據這場比賽，我的建議</span><h3>品質建立假說，趨勢與事件驗證，<br>風險決定配置。</h3><p>以成本後期末 NAV 為目標，保留合規、自主與可追溯的完整流程。先接通少量可靠資料，再驗證籌碼、新聞與模型能否帶來增量。</p><div class="data-totals"><span><strong>${c.categories.length}</strong> 決策面向</span><span><strong>${c.items.length}</strong> 資料群</span><span><strong>4</strong> 優先層級</span><span>盤點更新 ${c.updated}</span></div></section>
 <div class="data-start"><h3>兩週的起點</h3><ol><li><b>先能參賽</b><span>名單、價量、帳本、ETF 持股與回執</span></li><li><b>建立持有理由</b><span>營收、品質、趨勢與法人交易</span></li><li><b>控制共同風險</b><span>Beta、相關性、產業與重大事件</span></li></ol></div>
 <div class="data-mode" role="group" aria-label="資料頁內容"><button data-mode="catalog" aria-pressed="${dataMode==='catalog'}">資料目錄</button><button data-mode="method" aria-pressed="${dataMode==='method'}">決策方法・Beta・資料時點</button></div>
 <div class="page-links api-data-link"><a class="link-button" href="#apis">查看 TWSE／TPEx 全部官方端點 →</a></div><div id="data-body"></div>`;
 view.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>{dataMode=b.dataset.mode;view.querySelectorAll('[data-mode]').forEach(x=>x.setAttribute('aria-pressed',x.dataset.mode===dataMode));renderDataBody()});
 renderDataBody();
}
function renderDataBody(){
 const c=DATA_CATALOG,body=document.getElementById('data-body');
 if(dataMode==='method'){
  body.innerHTML=`<div class="data-method-links"><a class="link-button" href="documents/09-decision-data.md" download>下載決策方法 ↓</a><span>研究建議與待確認事項，非實測績效。</span></div><article class="reader">${DOCS.find(x=>x.id==='09-decision-data.md').html}</article>`;
  body.querySelectorAll('a[href^="https:"]').forEach(a=>{a.target='_blank';a.rel='noopener'});return;
 }
 body.innerHTML=`<div class="data-priorities">${Object.entries(c.priorities).map(([p,label])=>`<button data-priority="${p}" aria-pressed="${dataPriority===p}"><b>${p}</b><span>${esc(label)}</span><small>${c.items.filter(x=>x.priority===p).length} 組</small></button>`).join('')}</div>
 <p class="data-caption">這是候選需求清單，<strong>不代表已串接</strong>。P1 每群先選少數代表；P2／P3 須有樣本外增量才採用。展開項目查看欄位、來源與限制。</p>
 <div class="data-controls"><label class="data-search">搜尋資料<input type="search" id="data-search" placeholder="例如：Beta、籌碼、新聞、營收" value="${esc(dataQuery)}"></label><label>決策面向<select id="data-category"><option value="all">全部 12 類</option>${c.categories.map(x=>`<option value="${x.id}" ${dataCategory===x.id?'selected':''}>${esc(x.title)}</option>`).join('')}</select></label><label>優先序<select id="data-priority"><option value="all">全部優先序</option><option value="core" ${dataPriority==='core'?'selected':''}>兩週核心 P0＋P1</option>${Object.entries(c.priorities).map(([k,v])=>`<option value="${k}" ${dataPriority===k?'selected':''}>${k} ${esc(v)}</option>`).join('')}</select></label></div>
 <div class="data-result-bar"><span id="data-count" role="status" aria-live="polite"></span><button id="data-core" class="quiet">只看兩週核心</button><button id="data-reset" class="quiet">清除篩選</button></div><div id="data-results"></div>
 <details class="data-sources"><summary>來源與取得現況說明 · ${c.sources.length} 項</summary><p>公開來源入口不等於已取得帳號授權或完整歷史；競賽規則以專案原始文件與官方答覆為準。</p><ul>${c.sources.map(s=>`<li>${dataSourceLink(s)}<p>${esc(s.note)}</p></li>`).join('')}</ul></details>`;
 document.getElementById('data-search').oninput=e=>{dataQuery=e.target.value;renderDataResults()};
 document.getElementById('data-category').onchange=e=>{dataCategory=e.target.value;renderDataResults()};
 document.getElementById('data-priority').onchange=e=>{dataPriority=e.target.value;renderDataResults()};
 body.querySelectorAll('[data-priority]').forEach(b=>b.onclick=()=>{dataPriority=dataPriority===b.dataset.priority?'all':b.dataset.priority;document.getElementById('data-priority').value=dataPriority;renderDataResults()});
 document.getElementById('data-core').onclick=()=>{dataPriority='core';document.getElementById('data-priority').value='core';renderDataResults()};
 document.getElementById('data-reset').onclick=()=>{dataQuery='';dataCategory='all';dataPriority='all';document.getElementById('data-search').value='';document.getElementById('data-category').value='all';document.getElementById('data-priority').value='all';renderDataResults()};
 renderDataResults();
}
function renderDataResults(){
 const c=DATA_CATALOG,q=dataQuery.trim().toLocaleLowerCase(),bySource=Object.fromEntries(c.sources.map(s=>[s.id,s])),byCat=Object.fromEntries(c.categories.map(s=>[s.id,s]));
 const items=c.items.filter(x=>(dataCategory==='all'||dataCategory===x.category)&&(dataPriority==='all'||(dataPriority==='core'?['P0','P1'].includes(x.priority):x.priority===dataPriority))&&(!q||[x.id,x.name,x.fields,x.use,x.caveat,x.status,x.cadence,byCat[x.category].title,...x.sources.map(s=>bySource[s].title)].join(' ').toLocaleLowerCase().includes(q)));
 document.getElementById('data-count').textContent=`顯示 ${items.length} / ${c.items.length} 組資料`;
 view.querySelectorAll('[data-priority]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.priority===dataPriority));
 const target=document.getElementById('data-results');
 if(!items.length){target.innerHTML='<div class="data-empty"><h3>沒有符合的資料</h3><p>試試「Beta」、「新聞」或清除篩選，回到完整目錄。</p></div>';return}
 target.innerHTML=c.categories.map(cat=>{
  const rows=items.filter(x=>x.category===cat.id);if(!rows.length)return '';
  return `<section class="data-group"><div class="data-group-heading"><div><h3>${esc(cat.title)} <small>${rows.length} 組</small></h3><p>${esc(cat.question)}</p></div></div><div class="data-cards">${rows.map(x=>`<details class="data-item"><summary><span class="data-item-top"><span class="data-code">${x.id}</span><span class="data-tier ${x.priority.toLowerCase()}">${x.priority} · ${esc(c.priorities[x.priority])}</span></span><span class="data-item-name">${esc(x.name)}</span><span class="data-item-use">${esc(x.use)}</span><span class="data-expand">查看欄位、來源與限制 <span aria-hidden="true">＋</span></span></summary><dl><dt>欄位與候選指標</dt><dd>${esc(x.fields)}</dd><dt>更新頻率與歷史需求</dt><dd>${esc(x.cadence)}</dd><dt>目前取得狀態</dt><dd class="data-availability">${esc(x.status)}</dd><dt>限制與回測偏誤</dt><dd>${esc(x.caveat)}</dd><dt>候選來源</dt><dd class="data-source-links">${x.sources.map(s=>dataSourceLink(bySource[s])).join(' · ')}</dd></dl></details>`).join('')}</div></section>`;
 }).join('');
}
