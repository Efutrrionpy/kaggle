from collections import Counter,defaultdict
from copy import deepcopy
import json,time
from flex_boundary import FlexBoundary
from flex_value import geometry,supplies,production,delta_profile,market_paths
from service_route import route
from own_worker_projection import project,engine
class FlexService(FlexBoundary):
    def __init__(self,source,mode='economic'):
        assert mode in ('none','reference','economic')
        super().__init__(source,None if mode=='none' else self.compose)
        self.mode=mode;self.day=None;self.tour=None;self.decisions=[];self.issued=[]
        self.attempted=False;self.service_geometry=None;self.last=0;self.maximum=0

    def prepare(self,obs,cfg):
        d=obs['step']//24;self.day=d;self.tour=None;self.attempted=False
        owner=self.boundary.native
        targets=[(t,owner.targets[t]) for t in range(d*24,min(d*24+24,719)) if owner.targets[t] is not None]
        self.maximum=max(r['hands'] for t,r in targets)
        self.last=max(t for t,r in targets if any(c==['HIRE'] for c in owner.tape[t]['market'])) if any(any(c==['HIRE'] for c in owner.tape[t]['market']) for t,r in targets) else d*24
        self.last=max(self.last,min(t for t,r in targets if r['hands']==self.maximum))

    def plan(self,obs,cfg,action,target):
        start=time.monotonic();t=obs['step'];farm=obs['farms'][obs['player']]
        owner=self.boundary.native;self.service_geometry=geometry(obs,cfg,owner.tape,owner.targets)
        own,rival,profiles=supplies(obs,self.service_geometry)
        after=project(farm,obs['private'],action,step=t,configuration=cfg)
        af=after['farm'];access=[(cfg['boardSize']//2-1,cfg['boardSize']//2-1),(cfg['boardSize']//2,cfg['boardSize']//2-1),
            (cfg['boardSize']//2-1,cfg['boardSize']//2),(cfg['boardSize']//2,cfg['boardSize']//2)]
        actor=len(farm['hands'])+1;spawn=tuple(engine._spawn_hand(af,cfg['boardSize']))
        wage=engine._hire_cost(farm['hires_today'],cfg.get('farmHandCostMult',1));end=min((t//24+1)*24-2,718)
        jobs=[]
        for site,base in profiles.items():
            x,y=site;tile=farm['tiles'][y][x];future=self.service_geometry[site]
            today=[c[0] for u,a,c in future if u//24==t//24]
            feed_days=[u//24 for u,a,c in future if c[0]=='FEED']
            todo=[]
            # Respect original retirement: never add a feed after final native
            # intended feed day; also prohibit any upcoming same-day site reuse.
            reuse=any(u//24==t//24 and c[0] in ('PLANT','TILL','BUILD_COOP','BUILD_PASTURE') for u,a,c in future)
            if reuse:continue
            if not tile['fed_today'] and 'FEED' not in today and feed_days and t//24<=max(feed_days):todo.append('FEED')
            if not tile['cared_today'] and 'CARE' not in today and (tile['fed_today'] or 'FEED' in today or 'FEED' in todo):todo.append('CARE')
            if tile.get('yield_units',0)>0 and 'HARVEST' not in today:todo.append('HARVEST')
            if not todo:continue
            jobs.append(dict(site=site,tile=tile,commands=[[c] for c in todo],base=base))
        proposals=[]
        # Each possible first site starts a nearest incremental-benefit tour;
        # every complete prefix is evaluated with ONE real marginal wage.
        for first in range(len(jobs)):
            remaining=list(range(len(jobs)));order=[];pos=spawn;clock=t+2;commands=[['PICKUP','WHEAT',0]]
            while remaining:
                candidates=[]
                for i in remaining:
                    j=jobs[i];path=route(farm['tiles'],pos,j['site'])
                    if path is None:continue
                    if not order and i!=first:continue
                    back=min((route(farm['tiles'],j['site'],q) for q in access),key=lambda p:999 if p is None else len(p))
                    if back is None or clock+len(path)+len(j['commands'])+len(back)>end:continue
                    hypothetical=[(clock+len(path)+k,c) for k,c in enumerate(j['commands'])]
                    dd=delta_profile(j['tile'],self.service_geometry[j['site']],t,hypothetical,end,j['base'])
                    value=sum(n*obs['market']['prices'][p] for f in dd.values() for p,n in f.items())-obs['market']['prices']['WHEAT']*(['FEED'] in j['commands'])
                    if value>0:candidates.append((value/(len(path)+len(j['commands'])),i,path))
                if not candidates:break
                _,i,path=max(candidates,key=lambda q:(q[0],-q[1]));j=jobs[i];remaining.remove(i)
                commands+=path+j['commands'];clock+=len(path)+len(j['commands']);pos=j['site'];order.append(i)
                back=min((route(farm['tiles'],pos,q) for q in access),key=lambda p:999 if p is None else len(p))
                cmds=deepcopy(commands+back+[['DROP']]);grain=sum(['FEED'] in jobs[k]['commands'] for k in order);cmds[0]=['PICKUP','WHEAT',grain] if grain else ['PASS']
                delivery=t+len(cmds);assert delivery<=end
                pos2=spawn;extra=defaultdict(list)
                moves={'NORTH':(0,-1),'SOUTH':(0,1),'WEST':(-1,0),'EAST':(1,0)}
                for u,c in enumerate(cmds,t+1):
                    if c[0] in moves:dx,dy=moves[c[0]];pos2=(pos2[0]+dx,pos2[1]+dy)
                    elif c[0] in ('FEED','CARE','HARVEST'):extra[pos2].append((u,c))
                delta=defaultdict(Counter)
                for k in order:
                    s=jobs[k]['site'];dd=delta_profile(jobs[k]['tile'],self.service_geometry[s],t,extra[s],delivery,jobs[k]['base'])
                    for u,flow in dd.items():delta[u].update(flow)
                cost=wage+sum(engine.market_price('WHEAT',obs['market']['inventory']['WHEAT']-q,obs['market'].get('params')) for q in range(grain))
                base_value=sum(n*(obs['market'].get('params') or engine.MARKET_PARAMS)[p]['base'] for f in delta.values() for p,n in f.items())-cost
                # Cash is not a safety-confidence gate; reserve native planned
                # purchases before an optional worker consumes today's money.
                native_cost=sum(max(0,target['shed'].get(a,0)-after['private']['shed'].get(a,0))*engine.ANIMALS[a]['cost'] for a in engine.ANIMALS)
                native_cost+=sum(max(0,target['seeds'].get(c,0)-after['private']['seeds'].get(c,0))*engine.CROPS[c]['seed'] for c in engine.CROPS)
                native_cost+=sum(max(0,target['shed'].get(c,0)-after['private']['shed'].get(c,0))*obs['market']['prices'][c] for c in ('WHEAT','FERTILIZER'))
                if target['land']>len(af['unlocked_quadrants']):continue
                if af['money']<cost+native_cost:continue
                proposals.append(dict(commands=cmds,grain=grain,wage=wage,cost=cost,delta=dict(delta),reference=base_value,sites=[list(jobs[k]['site']) for k in order],delivery=delivery))
        unique={json.dumps(r['commands']):r for r in proposals}
        shortlist=sorted(unique.values(),key=lambda r:r['reference'],reverse=True)[:8]
        baseline=market_paths(obs,cfg,own,rival) if self.mode=='economic' and shortlist else None
        for r in shortlist:
            if self.mode=='economic':
                values=market_paths(obs,cfg,own,rival,r['delta'])
                r['scenario_margin_deltas']=[(a-b)-(c-d)-r['cost'] for (a,b),(c,d) in zip(values,baseline)]
                r['value']=sum(r['scenario_margin_deltas'])/len(values)
            else:r['value']=r['reference']
        best=max(shortlist,key=lambda r:r['value']) if shortlist else None
        record=dict(step=t,mode=self.mode,worker=actor,native_hands=len(farm['hands']),proposals=len(unique),shortlist=shortlist,
            selected=best if best and best['value']>0 else None,seconds=time.monotonic()-start)
        self.decisions.append(record)
        if record['selected']:
            self.tour=dict(record['selected'],actor=actor,issued_hire=t,position=0,picked=False,spawn=list(spawn))

    def compose(self,obs,cfg,action,target):
        t=obs['step'];farm=obs['farms'][obs['player']]
        if self.day!=t//24:self.prepare(obs,cfg)
        if target is not None and not self.attempted and t>self.last and len(farm['hands'])==self.maximum:
            self.attempted=True;self.plan(obs,cfg,action,target)
        tour=self.tour
        if tour is None:return action,target
        if target is not None:
            target['hands']=max(target['hands'],tour['actor'])
            if not tour['picked']:target['shed']['WHEAT']=target['shed'].get('WHEAT',0)+tour['grain']
        actor=tour['actor']
        if len(farm['hands'])<actor:return action,target
        if tour['position']>=len(tour['commands']):return action,target
        command=deepcopy(tour['commands'][tour['position']])
        # Extra actor follows originals, so project those actions first for
        # actual shared stock. Never consume the native retained grain reserve.
        action['hands']=action['hands'][:len(farm['hands'])]+[['PASS'] for _ in range(max(0,len(farm['hands'])-len(action['hands'])))]
        action['hands'][actor-1]=['PASS']
        after=project(farm,obs['private'],action,step=t,configuration=cfg)
        if tour['position']==0:
            native=self.boundary.native.targets[t]
            reserve=native['shed'].get('WHEAT',0) if native is not None else 0
            if after['private']['shed'].get('WHEAT',0)<tour['grain']+reserve:return action,target
            tour['picked']=True
            if target is not None:target['shed']['WHEAT']-=tour['grain']
        if t+len(tour['commands'])-tour['position']-1>min((t//24+1)*24-2,718):
            # Real funding delay can invalidate a planned route. No teleport or
            # imaginary completion; idle remainder is charged and recorded.
            self.issued.append(dict(step=t,event='late_funding_abandon',actor=actor));tour['position']=len(tour['commands']);return action,target
        action['hands'][actor-1]=command;tour['position']+=1
        self.issued.append(dict(step=t,actor=actor,command=command,site=after['farm']['hands'][actor-1],held=deepcopy(after['private']['inventories'][actor])))
        return action,target

    def receipt(self):
        return dict(super().receipt(),flex_mode=self.mode,flex_decisions=self.decisions,flex_issued=self.issued,
            flex_limits='One optional extra crew tour/day after native hires, fromday10. Exactbiology and intendedfutureevents conditional on nativefunding/feed; nightdelivery approximation for baseline, explicithelperdepot. Native retirement bounded by finalfeedday. Currentassets only in marketbackground, futureinvestments omitted; nextshop enumerated/latermean. Top8 reference shortlist, not optimum. Realcosts/errors/fullgame decide.')
