const test=require('node:test');const assert=require('node:assert/strict');const path=require('node:path');
const {composeDailyReply,getReplyDraft}=require('../site/dist/reply.js');
const plan=require('../plan.json').tasks;
test('all 14 units have distinct preparation and reply fields reflected in output',()=>{
 assert.equal(plan.length,14);
 for(const t of plan){assert.ok(t.preparation.length>=3);assert.ok(t.reply_fields.length>=4);const out=composeDailyReply(t,getReplyDraft(t));for(const f of t.reply_fields)assert.ok(out.includes(f.label));for(const p of t.preparation)assert.ok(out.includes(p));}
});
test('empty draft does not imply preparation, approval or acceptance',()=>{
 const out=composeDailyReply(plan[0],{answers:{},preparation:{}});
 assert.ok(out.includes('[待準備]'));assert.ok(out.includes('待補／待確認'));assert.ok(out.includes('本次未提供新的清單確認'));assert.ok(out.includes('本次未提供驗收結論'));assert.ok(!out.includes('我確認本單元驗收通過'));
});
test('multiline answers, notes and explicit decisions preserve content without changing status',()=>{
 const t=plan[0],before=JSON.stringify(t);const out=composeDailyReply(t,{answers:{team:'TEAM_X\r\n報名待確認'},preparation:{0:'已備妥'},notes:'檔案路徑：/tmp/資料.md',listDecision:'confirm',acceptanceDecision:'partial'});
 assert.ok(out.includes('  TEAM_X\n  報名待確認'));assert.ok(out.includes('[已備妥]'));assert.ok(out.includes('暫不標為完成'));assert.ok(out.includes('/tmp/資料.md'));assert.equal(JSON.stringify(t),before);
});
test('drafts are isolated by unit and switching units retains the same draft',()=>{
 const a=getReplyDraft(plan[0]),b=getReplyDraft(plan[1]);a.answers.team='TEST';assert.equal(getReplyDraft(plan[0]).answers.team,'TEST');assert.equal(b.answers.team,undefined);
});
