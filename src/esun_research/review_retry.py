"""Retry failed prose without repeating or silently changing an LLM decision."""
import json
import sqlite3
import re
from .store import encoded,digest,immutable


def validate_research_continuation(store,continuation,request):
    from .operations import candidate_bundle
    folder,manifest=candidate_bundle(store,continuation['source_run'])
    old=json.loads((folder/'request.json').read_bytes())['request']
    if digest((folder/'request.json').read_bytes())!=continuation['source_request_sha256']:raise ValueError('continuation_source_request_mismatch')
    if manifest['artifacts']['agent-research.json']!=continuation['source_research_sha256']:raise ValueError('continuation_research_hash_mismatch')
    source=json.loads((folder/'agent-research.json').read_bytes())
    resumable={'agent_research_budget_exhausted','agent_context_budget_exceeded','agent_exploration_budget_exhausted','agent_review_budget_exhausted','agent_selection_budget_exhausted'}
    if not source['errors'] or not all(e in resumable or e.startswith(('agent_research_stalled:','agent_action_contract_failed:')) for e in source['errors']) or source.get('selection'):raise ValueError('continuation_requires_capacity_blocked_unselected_research')
    exempt={'run_id','code_hash','research_continuation_ref'}
    if any(old.get(k)!=request.get(k) for k in set(old)|set(request) if k not in exempt):raise ValueError('continuation_inputs_changed')
    seed=continuation['state']
    if seed.get('selection') or seed['trace']!=source['trace'] or seed['evaluations']!=source['evaluations']:raise ValueError('continuation_journal_mismatch')
    for r in seed.get('reviews',{}).values():
        if r['tool_id'] not in {t['tool_id'] for t in seed['trace'] if r['value']['review_id'] in store.json(t['result_ref']).get('reviewed',[])}:
            raise ValueError('continuation_review_not_verified_in_trace')
        packet=store.json(r['input_ref'])
        if digest(encoded({k:v for k,v in packet.items() if k!='input_hash'}))!=r['input_hash']:raise ValueError('continuation_review_input_hash_mismatch')
    # JSON serializes object keys canonically. Restore the source packet's
    # evaluation order so a harmless map reorder does not invalidate reviews.
    order=['BASE_HOLD','BASE_REPAIR','BASE_PREVIOUS']
    packet=next((store.json(r['input_ref']) for r in seed.get('reviews',{}).values() if r['value']['review_id'].startswith('H')),None)
    if packet:order += [a['proposal_id'] for a in packet.get('alternatives',[])]
    order=list(dict.fromkeys([*order,*seed['evaluations']]))
    seed={**seed,'evaluations':{k:seed['evaluations'][k] for k in order if k in seed['evaluations']}}
    return {**seed,'errors':[]}


def retry_research(store,source_run,run_id,model=None):
    from .candidate import DecisionRequest,generate_candidate
    from .cli import candidate_sources,settings,code_hash
    from .operations import candidate_bundle
    from langgraph.checkpoint.sqlite import SqliteSaver
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}',run_id):raise ValueError('invalid_run_id')
    folder,manifest=candidate_bundle(store,source_run)
    old=json.loads((folder/'request.json').read_bytes())
    with sqlite3.connect(store.root/'strategy-agent-checkpoints.sqlite',check_same_thread=False) as connection:
        checkpoint=SqliteSaver(connection).get_tuple({'configurable':{'thread_id':source_run}})
    if not checkpoint:raise ValueError('missing_research_checkpoint')
    from .strategy_agent import ResearchState
    seed={k:v for k,v in checkpoint.checkpoint['channel_values'].items() if k in ResearchState.__annotations__}
    seed.pop('action',None)
    continuation={'source_run':source_run,'source_request_sha256':digest((folder/'request.json').read_bytes()),
        'source_research_sha256':manifest['artifacts']['agent-research.json'],'source_code_hash':old['request']['code_hash'],
        'scope':'Continue frozen context/step-capacity-blocked research with a bounded allowance; retain trace, evaluations and verified reviews.','state':seed}
    request=DecisionRequest.model_validate({**old['request'],'run_id':run_id,'code_hash':code_hash(),
        'research_continuation_ref':store.put_json(continuation)})
    validate_research_continuation(store,continuation,request.model_dump(mode='json'))
    sources=candidate_sources(True);_,universe=settings()
    frozen=store.freeze(request,sources,namespace='candidates')
    if frozen['captures']!=old['captures']:raise ValueError('continuation_capture_mismatch')
    return generate_candidate(store,request,sources,universe,model=model)


def retry_review(store,source_run,run_id,model=None):
    from .candidate import DecisionRequest,graph_for,export_dplan
    from .cli import candidate_sources,settings,code_hash
    from .operations import candidate_bundle
    from .datapack import load_datapack
    from .portfolio import Policy
    from langgraph.checkpoint.sqlite import SqliteSaver
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}',run_id):raise ValueError('invalid_run_id')
    folder,manifest=candidate_bundle(store,source_run)
    validation=json.loads((folder/'validation.json').read_bytes())
    errors=validation['errors']
    if not errors or any(not e.startswith('llm_review_failed:') for e in errors):
        raise ValueError('only_failed_prose_review_can_be_retried')
    research=json.loads((folder/'agent-research.json').read_bytes())
    if research['status']!='SELECTED':raise ValueError('requires_completed_autonomous_selection')
    if (store.root/'candidates'/run_id).exists():raise ValueError('retry_requires_new_run_id')
    old=json.loads((folder/'request.json').read_bytes())
    request=DecisionRequest.model_validate({**old['request'],'run_id':run_id,'code_hash':code_hash()})
    sources=candidate_sources(True);_,universe=settings()
    if digest(encoded([s.model_dump() for s in sources]))!=request.registry_hash or digest(encoded(universe))!=request.universe_hash:
        raise ValueError('retry_source_registry_changed')
    frozen=store.freeze(request,sources,namespace='candidates')
    if frozen['captures']!=old['captures']:raise ValueError('retry_must_preserve_exact_captures')
    origin={'source_run':source_run,'source_request_sha256':digest((folder/'request.json').read_bytes()),
        'source_research_sha256':manifest['artifacts']['agent-research.json'],
        'source_code_hash':old['request']['code_hash'],'current_code_hash':request.code_hash,
        'scope':'Reuse the frozen autonomous decision; retry prose only; recompute selected portfolio and all hard checks.'}
    research['decision_origin']=origin
    immutable(store.root/'candidates'/run_id/'decision-origin.json',encoded(origin))
    pack=load_datapack(store.read(request.datapack_ref),request.team_id,request.trade_date)
    policy=Policy.model_validate(store.json(request.policy_ref));schema=store.json(request.schema_ref)
    seed={'snapshot':store.put((folder/'snapshot.json').read_bytes()),
        'features':store.put((folder/'ranking.json').read_bytes()),'agent_research':store.put_json(research),'errors':[]}
    with sqlite3.connect(store.root/'candidate-checkpoints.sqlite',check_same_thread=False) as connection:
        graph=graph_for(store,request,sources,universe,frozen,pack,policy,schema,SqliteSaver(connection),model=model)
        cfg={'configurable':{'thread_id':run_id},'recursion_limit':20}
        graph.update_state(cfg,seed,as_node='rank')
        result=graph.invoke(None,cfg)
    export_dplan(store,run_id)
    return result


def retry_validation(store,source_run,run_id):
    """Revalidate a selected, fully explained checkpoint without any new inference.

    Exact factual inputs to the cached prose must match the rebuilt document;
    only code/run audit metadata may differ. All hard checks run again.
    """
    from .candidate import DecisionRequest,graph_for,compile_document,export_dplan
    from .cli import candidate_sources,settings,code_hash
    from .datapack import load_datapack
    from .portfolio import Policy,decimal
    from langgraph.checkpoint.sqlite import SqliteSaver
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}',run_id):raise ValueError('invalid_run_id')
    source=store.root/'candidates'/source_run
    if (source/'manifest.json').exists():raise ValueError('validation_retry_requires_unpublished_checkpoint')
    if (store.root/'candidates'/run_id).exists():raise ValueError('retry_requires_new_run_id')
    old=json.loads((source/'request.json').read_bytes())
    with sqlite3.connect(store.root/'candidate-checkpoints.sqlite',check_same_thread=False) as connection:
        checkpoint=SqliteSaver(connection).get_tuple({'configurable':{'thread_id':source_run}})
    if not checkpoint or checkpoint.checkpoint['channel_values'].get('errors'):raise ValueError('validation_retry_requires_clean_checkpoint')
    channels=checkpoint.checkpoint['channel_values']
    seed={k:channels[k] for k in ['snapshot','features','allocation','agent_research']}
    for ref in [*seed.values(),channels.get('llm_review'),channels.get('plan')]:
        if not ref:raise ValueError('validation_retry_requires_completed_decision_and_prose')
        if digest(store.read(ref))!=ref.split('/')[-1].split('.')[0]:raise ValueError('validation_retry_object_hash_mismatch')
    research=store.json(seed['agent_research'])
    if research.get('status')!='SELECTED' or not channels.get('llm_review'):raise ValueError('validation_retry_requires_completed_decision_and_prose')
    # Validate the old reviewed bundle against its immutable prose checkpoint.
    from .llm import apply_review
    review=store.json(channels['llm_review']);baseline=json.loads((source/'compiled.json').read_bytes())
    if apply_review(baseline['plan'],review)!=store.json(channels['plan'])['plan']:raise ValueError('validation_retry_prose_checkpoint_mismatch')
    request=DecisionRequest.model_validate({**old['request'],'run_id':run_id,'code_hash':code_hash()})
    sources=candidate_sources(True);_,universe=settings()
    if digest(encoded([s.model_dump() for s in sources]))!=request.registry_hash or digest(encoded(universe))!=request.universe_hash:raise ValueError('retry_source_registry_changed')
    frozen=store.freeze(request,sources,namespace='candidates')
    if frozen['captures']!=old['captures']:raise ValueError('retry_must_preserve_exact_captures')
    pack=load_datapack(store.read(request.datapack_ref),request.team_id,request.trade_date)
    policy=Policy.model_validate(research['selected_evaluation']['policy']);ranked=store.json(seed['features'])
    for row in ranked:row['score']=decimal(row['score'])
    rebuilt,_,_=compile_document(store.json(seed['snapshot']),ranked,store.json(seed['allocation']),pack,policy,request.model_dump(mode='json'),sources,research)
    if {k:v for k,v in rebuilt.items() if k!='agent_metadata'}!={k:v for k,v in baseline['plan'].items() if k!='agent_metadata'}:
        raise ValueError('validation_retry_explanation_inputs_changed')
    origin={'source_run':source_run,'source_request_sha256':digest((source/'request.json').read_bytes()),
        'source_research_ref':seed['agent_research'],'source_prose_ref':channels['llm_review'],
        'source_code_hash':old['request']['code_hash'],'current_code_hash':request.code_hash,
        'scope':'Reuse completed autonomous selection and exact-input prose; rerun all deterministic validation; no new model calls.'}
    research={**research,'decision_origin':origin};seed['agent_research']=store.put_json(research);seed['errors']=[]
    folder=store.root/'candidates'/run_id;immutable(folder/'llm-review.json',encoded(review))
    history=source/'research-agent/event-history.json'
    if history.exists():immutable(folder/'research-agent/event-history.json',history.read_bytes())
    class NoInference:
        def complete(self,*args,**kwargs):raise AssertionError('validation_retry_must_not_infer')
    with sqlite3.connect(store.root/'candidate-checkpoints.sqlite',check_same_thread=False) as connection:
        graph=graph_for(store,request,sources,universe,frozen,pack,Policy.model_validate(store.json(request.policy_ref)),store.json(request.schema_ref),SqliteSaver(connection),model=NoInference())
        cfg={'configurable':{'thread_id':run_id},'recursion_limit':20}
        graph.update_state(cfg,seed,as_node='allocate');result=graph.invoke(None,cfg)
    if result.get('status')=='CANDIDATE_BLOCKED_EXTERNAL_CHECKS':export_dplan(store,run_id)
    return result
