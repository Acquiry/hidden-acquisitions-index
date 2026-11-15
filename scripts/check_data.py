"""Accuracy checks for deals.json. Usage: python3 check_data.py deals.json"""
import json,sys,re,collections
d=json.load(open(sys.argv[1]));D=d['deals']
ND={'not disclosed','',None,'n/a','none known'}
BANNED=r'\b(evad\w*|evasion|avoid\w*|dodg\w*|sidestep\w*|circumvent\w*|bypass\w*|loophole\w*|secret\w*|covert\w*|stealth|disguis\w*|sham|hollow\w*|gutted|raid\w*|poach\w*|strip(ped|ping)?|killer|collaps\w*|failed|wiped out|forced out|below the radar|regulatory arbitrage|zombie\w*|shadow|illegal\w*|unlawful\w*|anticompetitive|husk)\b'
FACT_FIELDS=['remainder_valuation_after_usd','remainder_after','founder_retention','disclosed_value_usd','equity_stake_pct','staff_moved','target_last_valuation_usd','investor_outcome','employee_outcome','licence_exclusive','target_status_after','regulatory_review','voting_board_seat','board_observer_or_committee','veto_or_reserved_matters','exclusivity','right_of_first_refusal','contractual_consultation_rights','cloud_compute_spending_commitment','licence_exclusive_confirmed','remainder_6m','remainder_12m','remainder_24m','payout_detail','lead_investors','company_rationale','total_funding_raised_usd']
issues=collections.defaultdict(list)
for x in D:
    did=x['deal_id'];src=x.get('sources',[])
    supported=collections.defaultdict(set)
    for s in src:
        for f in s.get('supports',[]): supported[f].add(s.get('grade'))
    if not src: issues['no sources at all'].append(did)
    if not any(s.get('grade') in('A','B') for s in src): issues['no A/B source for the deal existing'].append(did)
    for f in FACT_FIELDS:
        val=x.get(f)
        if val in ND or (isinstance(val,str) and val.lower().startswith('not disclosed')): continue
        g=supported.get(f)
        if not g: issues[f'{f} filled but no source linked to it'].append(did)
        elif g<= {'C'}: issues[f'{f} backed only by grade C'].append(did)
    if x.get('target_status_after')=='wound down' and not supported.get('target_status_after'):
        issues['"wound down" without a linked source'].append(did)
    if x.get('disclosed_value_usd') not in ND and x.get('value_source_grade') in ND:
        issues['value present but value_source_grade blank'].append(did)
    for s in src:
        if s.get('quote') and len(str(s['quote']).split())>20: issues['quote over 20 words'].append(f"{did} #{s.get('n')}")
        if not str(s.get('url','')).startswith('http'): issues['source without valid URL'].append(f"{did} #{s.get('n')}")
    text=' '.join(str(x.get(k,'')) for k in ['notes','value_note','target_status_note','regulatory_detail','target_focus','structure_facts','remainder_after','payout_detail','conflict','value_scope','investor_outcome','employee_outcome','staff_moved','evidence_status','company_rationale','tier_reason','deal_stage','wind_down_notice','founder_retention'])
    for m in set(mm.group(0) for mm in re.finditer(BANNED,text,re.I)): issues[f'banned wording: "{m.lower()}"'].append(did)
    if not re.match(r'^\d{4}(-\d{2})?(-\d{2})?$',str(x.get('announce_date',''))): issues['bad date format'].append(did)
ids=[x['deal_id'] for x in D]
dup=[i for i,c in collections.Counter(ids).items() if c>1]
if dup: issues['duplicate deal_id']+=dup
print(f"{len(D)} deals checked")
if not issues: print('ALL CHECKS PASS')
for k,v in sorted(issues.items(),key=lambda kv:-len(kv[1])):
    print(f"\n[{len(v)}] {k}\n   "+', '.join(v[:15])+(' ...' if len(v)>15 else ''))
sys.exit(1 if issues else 0)
