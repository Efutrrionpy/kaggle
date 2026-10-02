"""Recompute score tables from published synthetic experiment outcome rows."""
from collections import defaultdict
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def stats(rows):
    valid=[r for r in rows if r['valid'] and all(isinstance(v,(int,float)) for v in r['rewards'])]
    margins=[r['rewards'][r['seat']]-r['rewards'][1-r['seat']] for r in valid]
    return dict(games=len(rows),valid_games=len(valid),invalid_games=len(rows)-len(valid),
                independent_worlds=len({r['seed'] for r in rows}),wins=sum(x>0 for x in margins),
                draws=sum(x==0 for x in margins),losses=sum(x<0 for x in margins),
                points=sum(1 if x>0 else .5 if x==0 else 0 for x in margins),
                mean_margin=sum(margins)/len(margins) if margins else None)

def grouped(rows):
    result={}
    for field in ('arm','seed','opponent','seat'):
        groups=defaultdict(list)
        for row in rows:
            key=str(row['arm']) if field=='arm' else str(row['arm'])+' | '+str(row[field])
            groups[key].append(row)
        result[field]={k:stats(v) for k,v in sorted(groups.items())}
    return result

if __name__=='__main__':
    checked=[]
    for p in sorted((ROOT/'results').glob('*_cells.json')):
        q=json.loads(p.read_text());actual=grouped(q['rows'])
        expected=json.loads(p.with_name(p.name.replace('_cells.json','_groups.json')).read_text())
        assert actual==expected,p.name
        checked.append(dict(experiment=q['experiment'],cells=len(q['rows'])))
    print(json.dumps(dict(status='PASS',checked=checked,scope='Arithmetic reconstruction only; no new simulations and no claim of gold calibration.'),indent=2))
