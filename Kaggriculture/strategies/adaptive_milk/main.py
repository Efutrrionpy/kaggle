import json
import sys
from pathlib import Path
_POLICY=None
_DEFAULTS=None
def agent(observation,configuration=None):
    global _POLICY,_DEFAULTS
    folder=Path(agent.__code__.co_filename).resolve().parent
    if _POLICY is None or observation.get('step',-1)==0 or (observation.get('day')==0 and observation.get('hour')==0):
        if str(folder) not in sys.path:sys.path.insert(0,str(folder))
        from adaptive_milk import AdaptiveMilk as ProgrammeRouter
        _DEFAULTS=json.loads((folder/'defaults.json').read_text())
        _POLICY=ProgrammeRouter(json.loads((folder/'policy.json').read_text()))
    cfg=dict(_DEFAULTS)
    if configuration is not None:cfg.update(configuration)
    action=_POLICY(observation,cfg)
    if observation.get('step')==0:
        orders=action['market']
        grain=[c for c in orders if c[:2]==['BUY_PRODUCT','WHEAT']]
        other=[c for c in orders if c[:2]!=['BUY_PRODUCT','WHEAT']]
        if grain and grain+other!=orders:
            action=dict(action,market=grain+other)
    return action
if __name__=='__main__':
    for line in sys.stdin:
        request=json.loads(line)
        print(json.dumps(agent(request['observation'],request.get('configuration')),separators=(',',':')),flush=True)
