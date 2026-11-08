import json
from esun_research.store import Store
from esun_research.research_board import run_board


def test_board_bounded_and_resume_does_not_recall_model(tmp_path):
    s=Store(tmp_path);context={'cutoff_at':'2026-11-04T07:00:00+08:00','sources':[{'id':'CBC-USDTWD','status':'ok'}],
      'observations':[{'source_id':'CBC-USDTWD','observed_date':'2026-11-03','evidence_id':'Wfx','values':{'USDTWD':'31'}}]}
    class Model:
        calls=0
        def complete(self,messages,schema):
            self.calls+=1
            return {'value':{'claims':[],'gaps':['沒有足夠證據建立個股因果與績效優勢。']}}
    from esun_research.llm import ModelConfig
    config=ModelConfig.model_validate_json(open('config/llm-local.json').read())
    model=Model();r=run_board(s,'board-test',context,model=model,config=config)
    calls=model.calls;assert calls==1 and r['production_authorized'] is False
    assert r['status']=='PARTIAL_REVIEW'
    again=run_board(s,'board-test',context,model=model,config=config)
    assert again==r and model.calls==calls


def test_board_rejects_invented_refs(tmp_path):
    s=Store(tmp_path);context={'cutoff_at':'2026-11-04T07:00:00+08:00','sources':[{'id':'CBC-USDTWD','status':'ok'}],
      'observations':[{'source_id':'CBC-USDTWD','observed_date':'2026-11-03','evidence_id':'Wfx','values':{'USDTWD':'31'}}]}
    class Model:
        def complete(self,messages,schema):
            return {'value':{'claims':[{'hypothesis':'可能存在匯率與產業風險的關聯。','mechanism':'匯率透過收入換算影響公司。','evidence_refs':['FAKE'],'counter_evidence':'公司可能已進行避險操作。','uncertainty':'尚缺公司實際外幣曝險資料。'}],'gaps':['尚無公司曝險資料。']}}
    r=run_board(s,'bad-ref',context,model=Model())
    assert r['results']['macro']['status']=='FAILED' and not r['results']['macro']['claims']
