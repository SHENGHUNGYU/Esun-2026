"""Deterministic progress contracts for autonomous research, never portfolio choices."""
from collections import Counter
from .decision_review import primary_proposal


def evaluation_contract(evaluations,revisions,settings,probe_missing=False):
    primary={k:v for k,v in evaluations.items() if primary_proposal(k)}
    distinct=len({e['economic_hash'] for e in primary.values()})
    excluded=[k for k in primary if revisions.get(k,0)>=settings.maximum_revisions]
    # A second description of the same hypothesis does not fill a research slot.
    create=distinct<settings.minimum_compared_strategies
    if create and len(primary)>=settings.maximum_strategies:
        raise ValueError('independent_strategy_capacity_exhausted')
    eligible=[k for k in primary if k not in excluded]
    if not create and not eligible and len(primary)>=settings.maximum_strategies:
        raise ValueError('strategy_revision_capacity_exhausted')
    return {'operation':'create' if create else 'create_or_revise',
        'new_id_required':create,'forbidden_revision_ids':excluded,
        'revisable_ids':[] if create else eligible,
        'existing_primary_ids':list(primary),'distinct_primary_count':distinct,
        'minimum_distinct_primary_count':settings.minimum_compared_strategies,
        'suggested_new_id':next('HYP_'+str(i).zfill(2) for i in range(1,100) if 'HYP_'+str(i).zfill(2) not in evaluations),
        'required_mode':'cash_probe' if probe_missing else None,
        'note':'BASE_/ALT_ do not fill new hypothesis slots. Create a new economic hypothesis; renaming alone is rejected. Portfolio content remains the model decision.'}


def check_proposal_contract(proposal,contract,evaluations):
    pid=proposal.proposal_id
    if not primary_proposal(pid):raise ValueError('reserved_comparison_cannot_be_modified')
    if contract['new_id_required'] and pid in evaluations:raise ValueError('new_independent_proposal_required')
    if pid in contract['forbidden_revision_ids']:raise ValueError('proposal_revision_not_available')
    if pid in evaluations and pid not in contract['revisable_ids']:raise ValueError('proposal_revision_not_available')
    if contract['required_mode'] and proposal.mode!=contract['required_mode']:raise ValueError('cash_probe_comparison_required')


def phase_counts(trace):
    return dict(Counter(t['action']['tool'] for t in trace if not t['action']['tool'].startswith('automatic_')))


def stalled_error(trace,start_index,limit=2):
    """Count unchanged failures only in this continuation, not its archived prefix."""
    recent=trace[start_index:]
    if len(recent)<limit:return None
    errors=[r.get('error') for r in recent[-limit:]]
    return errors[0] if errors[0] and len(set(errors))==1 else None
