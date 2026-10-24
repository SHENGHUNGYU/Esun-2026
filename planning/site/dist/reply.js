'use strict';
// Drafts live only in this page's memory; no storage, requests or status writes.
const replyDrafts=new Map();
const preparationStates=['待準備','已備妥','受阻','不適用'];
const listDecisions={unspecified:'本次未提供新的清單確認（不變更既有授權）',confirm:'我確認本單元列出的 Codex／機器工作清單，依前置依賴執行',discuss:'需先討論或調整清單，修改內容見補充'};
const acceptanceDecisions={unspecified:'本次未提供驗收結論',pass:'我確認本單元驗收通過，請核對必要證據後記錄',fail:'驗收未通過，需要延續本單元',partial:'部分已驗證，仍有缺項，暫不標為完成'};
const listDecisionLabels={unspecified:'本次不新增清單確認',confirm:'確認本單元清單',discuss:'先討論或調整清單'};
const acceptanceDecisionLabels={unspecified:'本次不提交驗收結論',pass:'確認驗收通過',fail:'驗收未通過，延續本單元',partial:'部分通過，仍有缺項'};
function getReplyDraft(t){
 if(!replyDrafts.has(t.id))replyDrafts.set(t.id,{preparation:{},answers:{},listDecision:'unspecified',acceptanceDecision:'unspecified',notes:'',generated:false});
 return replyDrafts.get(t.id);
}
function composeDailyReply(t,draft){
 const lineBlock=(text)=>String(text).trim().replace(/\r\n?/g,'\n').split('\n').map(x=>'  '+x).join('\n');
 const out=[`# 每日回覆｜${t.id} ${t.title}`,'',`- 對照狀態：${t.status}（來自每日 TODO；填表不會改變狀態）`,`- 前置單元：${t.deps.join('、')||'無'}`,'','## 準備材料'];
 t.preparation.forEach((item,i)=>{out.push(`- [${preparationStates.includes(draft.preparation?.[i])?draft.preparation[i]:'待準備'}] ${item}`)});
 out.push('','## 逐項回答');
 t.reply_fields.forEach((f,i)=>{const answer=String(draft.answers?.[f.key]||'').trim();out.push(`\n### ${i+1}. ${f.label}`,answer?lineBlock(answer):'  待補／待確認')});
 out.push('','## 本次確認',`- 清單確認：${listDecisions[draft.listDecision]||listDecisions.unspecified}`,`- 驗收結果：${acceptanceDecisions[draft.acceptanceDecision]||acceptanceDecisions.unspecified}`,'','## 補充、阻礙與希望討論的事項',String(draft.notes||'').trim()?lineBlock(draft.notes):'  無新增補充','', '本回覆由我填寫後複製；未填或待確認的資訊不視為已具備。表單不代送官方文件、不自動修改進度；確認與驗收只按上方明確選擇處理。');
 return out.join('\n');
}
function replyPanel(t){
 const d=getReplyDraft(t);const filled=t.reply_fields.filter(f=>String(d.answers[f.key]||'').trim()).length;
 return `<div class="reply-intro"><div class="panel-label">填寫後複製回聊天</div><h4>你需要準備什麼、回答什麼</h4><p>可分次提供，未知項填「待確認」。材料用檔案位置或可查閱連結說明，這裡不會上傳檔案。</p><p class="draft-notice">草稿僅留在這次開啟的頁面中，切換單元會保留；重新整理或關閉頁面會清除。不要填密碼、API key、私鑰或受限全文。</p></div><form id="daily-reply-form"><fieldset class="reply-fieldset"><legend><span>01</span> 需要準備給我的材料</legend><p class="field-group-hint">標記準備狀態；檔案位置、證據或尚缺的內容可填在下方回答及補充中。</p><div class="preparation-list">${t.preparation.map((item,i)=>`<div class="preparation-row"><label for="prep-${i}">${esc(item)}</label><select id="prep-${i}" data-preparation="${i}">${preparationStates.map(s=>`<option ${s===(d.preparation[i]||'待準備')?'selected':''}>${s}</option>`).join('')}</select></div>`).join('')}</div></fieldset><fieldset class="reply-fieldset"><legend><span>02</span> 需要你回答的問題</legend><p class="field-group-hint">提示說明回答範圍；可用條列、檔案位置或「待 Codex 產出」作答。空白會在回覆中標為待補。</p><div class="answer-fields">${t.reply_fields.map((f,i)=>`<div class="answer-field"><label for="answer-${f.key}"><span>${String(i+1).padStart(2,'0')}</span>${esc(f.label)}</label><p id="hint-${f.key}" class="answer-hint">${esc(f.hint)}</p><textarea id="answer-${f.key}" data-answer="${f.key}" aria-describedby="hint-${f.key}" rows="3" placeholder="填入你的回答；未知時可填待確認">${esc(d.answers[f.key]||'')}</textarea></div>`).join('')}</div></fieldset><fieldset class="reply-fieldset"><legend><span>03</span> 本次確認與補充</legend><p class="field-group-hint">提供資料與確認清單／驗收是不同動作；以下不會替你預選確認。選擇後也須複製回聊天，我才會依內容處理。</p><div class="reply-decisions"><label for="reply-list-decision">清單確認<select id="reply-list-decision">${Object.entries(listDecisions).map(([key,value])=>`<option value="${key}" ${key===d.listDecision?'selected':''}>${esc(listDecisionLabels[key])}</option>`).join('')}</select></label><label for="reply-acceptance-decision">驗收結果<select id="reply-acceptance-decision">${Object.entries(acceptanceDecisions).map(([key,value])=>`<option value="${key}" ${key===d.acceptanceDecision?'selected':''}>${esc(acceptanceDecisionLabels[key])}</option>`).join('')}</select></label></div><label class="notes-label" for="reply-notes">補充、阻礙、負責人／預計時間、希望討論的事項</label><textarea id="reply-notes" rows="3" placeholder="例如：M3 週五才能接通，由我處理；希望先討論新聞來源。">${esc(d.notes)}</textarea></fieldset><div class="reply-actions"><span id="reply-filled">已回答 ${filled} / ${t.reply_fields.length} 題</span><button type="button" id="generate-reply" class="primary-link">產生格式化回覆</button><button type="button" id="copy-reply" class="quiet" ${d.generated?'':'disabled'}>複製回覆</button></div><div id="reply-message" class="reply-message" role="status" aria-live="polite"></div><section id="reply-preview" class="reply-preview" ${d.generated?'':'hidden'}><label for="formatted-reply">格式化回覆預覽</label><p>核對內容後複製，貼回與我的聊天。仍有空白也可產生，會保留待補標記。</p><textarea id="formatted-reply" rows="14" readonly>${d.generated?esc(composeDailyReply(t,d)):''}</textarea></section></form>`;
}
function bindReplyForm(t){
 const form=document.getElementById('daily-reply-form');if(!form)return;
 const d=getReplyDraft(t);const message=document.getElementById('reply-message');
 const refresh=()=>{
  const count=t.reply_fields.filter(f=>String(d.answers[f.key]||'').trim()).length;
  document.getElementById('reply-filled').textContent=`已回答 ${count} / ${t.reply_fields.length} 題`;
  if(d.generated)document.getElementById('formatted-reply').value=composeDailyReply(t,d);
  message.textContent='';
 };
 form.onsubmit=e=>e.preventDefault();
 form.querySelectorAll('[data-answer]').forEach(el=>el.oninput=()=>{d.answers[el.dataset.answer]=el.value;refresh()});
 form.querySelectorAll('[data-preparation]').forEach(el=>el.onchange=()=>{d.preparation[el.dataset.preparation]=el.value;refresh()});
 document.getElementById('reply-list-decision').onchange=e=>{d.listDecision=e.target.value;refresh()};
 document.getElementById('reply-acceptance-decision').onchange=e=>{d.acceptanceDecision=e.target.value;refresh()};
 document.getElementById('reply-notes').oninput=e=>{d.notes=e.target.value;refresh()};
 document.getElementById('generate-reply').onclick=()=>{
  d.generated=true;document.getElementById('reply-preview').hidden=false;
  document.getElementById('formatted-reply').value=composeDailyReply(t,d);
  document.getElementById('copy-reply').disabled=false;
  message.textContent='回覆已產生；未填內容會標為待補。尚未傳送或修改進度。';
 };
 document.getElementById('copy-reply').onclick=async()=>{
  const output=document.getElementById('formatted-reply');output.value=composeDailyReply(t,d);
  try{await navigator.clipboard.writeText(output.value);message.textContent='已複製回覆。請貼回聊天，讓我依你的資訊繼續處理。'}
  catch{output.focus();output.select();message.textContent='瀏覽器未允許自動複製，已選取文字，請手動複製後貼回聊天。'}
 };
}
if(typeof module!=='undefined'&&module.exports)module.exports={composeDailyReply,getReplyDraft,listDecisions,acceptanceDecisions};
