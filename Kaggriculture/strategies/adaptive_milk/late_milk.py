from copy import deepcopy
from economic_first import EconomicFirst
MOVES={'NORTH':(0,-1),'SOUTH':(0,1),'WEST':(-1,0),'EAST':(1,0)}
def compile_late_cows(obs,cfg,tape,targets):
    farm=obs['farms'][obs['player']];pos=deepcopy([farm['farmer'],*farm['hands']])
    h=cfg['boardSize']//2;access=[(h-1,h-1),(h,h-1),(h-1,h),(h,h)]
    placements=[];builds=[]
    for t in range(219,719):
        for actor,c in enumerate([tape[t]['farmer'],*tape[t]['hands']]):
            if actor>=len(pos):
                if c!=['PASS']:return None,'missing_planned_actor'
                continue
            if t>219 and c[:2]==['PLACE','COW']:
                placements.append(dict(step=t,actor=actor,site=list(pos[actor])))
            if t>219 and c==['BUILD_PASTURE']:
                builds.append(dict(step=t,actor=actor,site=list(pos[actor])))
            if c[0] in MOVES:
                dx,dy=MOVES[c[0]];x,y=pos[actor]
                if 0<=x+dx<cfg['boardSize'] and 0<=y+dy<cfg['boardSize']:pos[actor]=[x+dx,y+dy]
        if (t+1)%cfg['turnsPerDay']==0:pos=[[h-1,h-1]]
        elif targets[t] is not None:
            for _ in range(max(0,targets[t]['hands']-len(pos)+1)):
                pos.append(list(min(access,key=lambda s:sum(tuple(p)==s for p in pos))))
    sites={tuple(e['site']) for e in placements}
    if not sites:return None,'no_uncommitted_cow_placement'
    selected=[e for e in builds if tuple(e['site']) in sites]
    for e in placements:
        x,y=e['site'];tile=farm['tiles'][y][x]
        if isinstance(tile,dict) and tile.get('animal'):return None,'existing_animal_at_future_site'
        if not any(b['site']==e['site'] and b['step']<e['step'] for b in selected):
            return None,'missing_future_structure'
    return dict(placements=placements,builds=selected),None

class LateMilk(EconomicFirst):
    def __init__(self,source,species,enabled=True):
        super().__init__(source)
        assert species in ('GOOSE','SHEEP')
        self.milk_species=species;self.milk_enabled=enabled;self.milk_decision=None
        self.milk_applied=False;self.milk_placements=[];self.milk_deposits=[]

    def __call__(self,obs,cfg):
        t=obs['step'];ctl=getattr(self.source,'_POLICY',None)
        if self.milk_applied and t>219:
            a=deepcopy(ctl.donor.tape[t]);f=obs['farms'][obs['player']]
            positions=[f['farmer'],*f['hands']];h=cfg['boardSize']//2
            access={(h-1,h-1),(h,h-1),(h-1,h),(h,h)}
            product={'GOOSE':'EGG','SHEEP':'WOOL'}[self.milk_species]
            keys={(e['step'],e['actor']) for e in self.milk_decision['compiled']['placements']}
            for actor,c in enumerate([a['farmer'],*a['hands']]):
                if actor>=len(positions):continue
                held=obs['private']['inventories'][actor]
                if c[:2]==['PLACE','MILK'] and tuple(positions[actor]) in access:
                    if not held.get('MILK',0) and held.get(product,0)>0:
                        c[1]=product;self.milk_deposits.append(dict(step=t,actor=actor,held=deepcopy(held)))
                if (t,actor) in keys:
                    x,y=positions[actor]
                    self.milk_placements.append(dict(step=t,actor=actor,site=[x,y],held=held.get(self.milk_species,0),tile=deepcopy(f['tiles'][y][x])))
            ctl.donor.tape[t]=a
        action=super().__call__(obs,cfg)
        if t!=219:return action
        ctl=self.source._POLICY
        self.milk_decision=dict(donor=ctl.arm,species=self.milk_species,enabled=self.milk_enabled,applied=False,legal_root=deepcopy(obs))
        if not self.milk_enabled or not ctl.active:
            self.milk_decision['reason']='disabled_or_inactive';return action
        private=obs['private']
        if private['shed'].get('COW',0) or any(i.get('COW',0) for i in private['inventories']):
            self.milk_decision['reason']='already_committed_cow_cargo';return action
        if any(len(c)>1 and c[1]=='COW' and c[0] in ('BUY_ANIMAL','PICKUP','PLACE') for c in [action['farmer'],*action['hands'],*action['market']]):
            self.milk_decision['reason']='root_turn_cow_commitment';return action
        compiled,error=compile_late_cows(obs,cfg,ctl.donor.tape,ctl.donor.targets)
        if error:self.milk_decision['reason']=error;return action
        buildkeys={(e['step'],e['actor']) for e in compiled['builds']}
        for u in range(220,719):
            a=ctl.donor.tape[u]
            for actor,c in enumerate([a['farmer'],*a['hands']]):
                if (u,actor) in buildkeys and self.milk_species=='GOOSE':
                    assert c==['BUILD_PASTURE'];c[0]='BUILD_COOP'
            for c in [a['farmer'],*a['hands'],*a['market']]:
                if len(c)>1 and c[1]=='COW' and c[0] in ('BUY_ANIMAL','PICKUP','PLACE'):c[1]=self.milk_species
            target=ctl.donor.targets[u]
            if target is not None:
                n=target['shed'].pop('COW',0)
                if n:target['shed'][self.milk_species]=target['shed'].get(self.milk_species,0)+n
        self.milk_applied=True
        self.milk_decision.update(applied=True,reason='uncommitted_late_milk',compiled=compiled)
        return action

    def receipt(self):
        return dict(super().receipt(),milk_decision=self.milk_decision,milk_placements=self.milk_placements,milk_deposits=self.milk_deposits,
            scope_milk='Exact acceptedEconomicFirst through219. Existinganimalassets and first198selection retained; only uncommitted futureCOW purchase/targets/cargo/placement and matchingnewpasture sites converted. ExistingMILK deposits retain priority; substituted product uses otherwiseemptyMILKslot oractualnightdeposit. No freecash or incompatiblemidgamefallback. All workers/routes/GOOSE/SHEEP commitments otherwise unchanged; fullgame includes cargo competition.')
