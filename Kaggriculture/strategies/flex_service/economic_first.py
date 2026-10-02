from copy import deepcopy
from types import SimpleNamespace
from late_flock import LateFlock
from tranche_economic import choose
MOVES={'NORTH':(0,-1),'SOUTH':(0,1),'EAST':(1,0),'WEST':(-1,0)}
class Bank:
    def __init__(self,plan,arm):
        self.source=SimpleNamespace(_POLICY=LateFlock(plan))
    def __call__(self,obs,cfg):
        return self.source._POLICY(obs,cfg)
    def receipt(self):
        return self.source._POLICY.receipt()


def compile_tranche(tape, targets, obs, cfg):
    """Future locations from fixed movement commands, not future observations."""
    farm = obs['farms'][obs['player']]
    positions = deepcopy([farm['farmer'], *farm['hands']])
    h=cfg['boardSize']//2
    access=[(h-1,h-1),(h,h-1),(h-1,h),(h,h)]
    placements, builds, animal_commands = [], [], []
    for t in range(198, 719):
        a = tape[t]
        for actor, c in enumerate([a['farmer'], *a['hands']]):
            if actor >= len(positions):
                if c != ['PASS']:return None, 'future_missing_actor'
                continue
            if t > 198 and c[:2] == ['PLACE', 'GOOSE']:
                placements.append(dict(step=t, actor=actor, site=list(positions[actor])))
            if t > 198 and c == ['BUILD_COOP']:
                builds.append(dict(step=t, actor=actor, site=list(positions[actor])))
            if c[0] in MOVES:
                dx, dy = MOVES[c[0]];x,y = positions[actor]
                if 0 <= x+dx < cfg['boardSize'] and 0 <= y+dy < cfg['boardSize']:
                    positions[actor] = [x+dx,y+dy]
        if t > 198:
            for actor, c in enumerate([a['farmer'], *a['hands'], *a['market']]):
                if len(c)>1 and c[1]=='GOOSE' and c[0] in ('BUY_ANIMAL','PICKUP','PLACE'):
                    animal_commands.append(dict(step=t, index=actor, command=c))
        # Pinned mechanics dismiss all hands/reset the farmer each night.
        # Targets specify desired hires, not a claim they will be affordable.
        if (t+1)%cfg['turnsPerDay']==0:
            positions=[[h-1,h-1]]
        elif targets[t] is not None:
            for _ in range(max(0,targets[t]['hands']-(len(positions)-1))):
                site=min(access,key=lambda s:sum(tuple(p)==s for p in positions))
                positions.append(list(site))
    sites = {tuple(e['site']) for e in placements}
    if not sites:return None, 'no_later_placements'
    unchanged_builds=[b for b in builds if tuple(b['site']) not in sites]
    builds=[b for b in builds if tuple(b['site']) in sites]
    for p in placements:
        if not any(b['site']==p['site'] and b['step']<p['step'] for b in builds):
            return None, 'placement_without_new_structure'
        x,y=p['site'];tile=farm['tiles'][y][x]
        if isinstance(tile,dict) and tile.get('animal'):return None, 'existing_animal_at_site'
    return dict(placements=placements, builds=builds, unchanged_builds=unchanged_builds,
                animal_commands=animal_commands), None

class Tranche(Bank):
    def __init__(self, source, species, enabled=True):
        super().__init__(source, 'accepted_late')
        assert species in ('COW','SHEEP')
        self.species, self.enabled = species, enabled
        self.tranche = None
        self.decision198 = None
        self.deposits = []
        self.placement_attempts = []

    def __call__(self, obs, cfg):
        t=obs['step'];ctl=getattr(self.source,'_POLICY',None)
        if self.tranche and t>198:
            a=deepcopy(ctl.donor.tape[t]);farm=obs['farms'][obs['player']]
            positions=[farm['farmer'],*farm['hands']];half=cfg['boardSize']//2
            access={(half-1,half-1),(half,half-1),(half-1,half),(half,half)}
            product={'COW':'MILK','SHEEP':'WOOL'}[self.species]
            for actor,c in enumerate([a['farmer'],*a['hands']]):
                if actor>=len(positions):continue
                held=obs['private']['inventories'][actor]
                if c[:2]==['PLACE','EGG'] and tuple(positions[actor]) in access:
                    if held.get('EGG',0)==0 and held.get(product,0)>0:
                        self.deposits.append(dict(step=t,actor=actor,held=deepcopy(held),command_before=list(c)))
                        c[1]=product
                if c[:2]==['PLACE',self.species] and (t,actor) in self.tranche['placement_keys']:
                    x,y=positions[actor]
                    self.placement_attempts.append(dict(step=t,actor=actor,site=[x,y],held=held.get(self.species,0),tile=deepcopy(farm['tiles'][y][x])))
            ctl.donor.tape[t]=a
        action=super().__call__(obs,cfg)
        if t==198:
            ctl=self.source._POLICY
            self.decision198=dict(donor=ctl.arm,active=ctl.active,enabled=self.enabled,
                species=self.species,legal_root=deepcopy(obs),applied=False)
            if not self.enabled or not ctl.active or ctl.arm=='episode_114453315':
                self.decision198['reason']='disabled_or_inactive_or_existing_yarn_branch'
                return action
            private=obs['private']
            if private['shed'].get('GOOSE',0) or any(i.get('GOOSE',0) for i in private['inventories']):
                self.decision198['reason']='already_committed_goose_cargo';return action
            if any(len(c)>1 and c[1]=='GOOSE' and c[0] in ('BUY_ANIMAL','PICKUP','PLACE') for c in [action['farmer'],*action['hands'],*action['market']]):
                self.decision198['reason']='decision_turn_goose_commitment';return action
            compiled,error=compile_tranche(ctl.donor.tape,ctl.donor.targets,obs,cfg)
            if error:self.decision198['reason']=error;return action
            build_keys={(e['step'],e['actor']) for e in compiled['builds']}
            for u in range(199,719):
                a=ctl.donor.tape[u]
                for actor,c in enumerate([a['farmer'],*a['hands']]):
                    if (u,actor) in build_keys:
                        assert c==['BUILD_COOP'];c[0]='BUILD_PASTURE'
                for c in [a['farmer'],*a['hands'],*a['market']]:
                    if len(c)>1 and c[1]=='GOOSE' and c[0] in ('BUY_ANIMAL','PICKUP','PLACE'):c[1]=self.species
                target=ctl.donor.targets[u]
                if target is not None:
                    n=target['shed'].pop('GOOSE',0)
                    if n:target['shed'][self.species]=target['shed'].get(self.species,0)+n
            self.tranche=dict(compiled,placement_keys={(e['step'],e['actor']) for e in compiled['placements']})
            self.decision198.update(applied=True,reason='uncommitted_tranche',compiled=compiled)
        return action

    def receipt(self):
        return dict(super().receipt(),tranche_decision=self.decision198,tranche_deposits=self.deposits,
            tranche_placement_attempts=self.placement_attempts,
            scope_tranche='Exact accepted0..198 and router. Non-Yarn later uncommitted goose procurement/retained animal input/placement/new structures map to one species. Existing animals and product targets unchanged. Deposit substitution only at shed with no actual EGG and actual new product. Mixed cargo retains original EGG deposit; residue follows actual later/night deposit. No money injection, future observation or post-commitment fallback. Feasibility and economics measured in full games.')

class FirstTranche(Tranche):
    def __call__(self,obs,cfg):
        ctl=getattr(self.source,'_POLICY',None)
        before=None
        if obs['step']==198 and ctl is not None and ctl.active and ctl.arm!='episode_114453315':
            before=(deepcopy(ctl.donor.tape),deepcopy(ctl.donor.targets))
        action=super().__call__(obs,cfg)
        if obs['step']==198 and self.tranche:
            tape,targets=before
            # These are the common first new-asset dependency chain on all3
            # non-Yarn donors, verified from compiled locations and saved paths.
            placement=self.tranche['placements'][0]
            assert placement['step']==203 and placement['actor']==4
            assert tape[200]['hands'][3]==['PICKUP','GOOSE',1]
            assert tape[202]['hands'][3]==['BUILD_COOP']
            assert tape[203]['hands'][3]==['PLACE','GOOSE',1]
            assert targets[199]['shed'].get('GOOSE')==1
            assert targets[200]['shed'].get('GOOSE')==1
            tape[200]['hands'][3][1]=self.species
            tape[202]['hands'][3]=['BUILD_PASTURE']
            tape[203]['hands'][3][1]=self.species
            for c in tape[199]['market']:
                if c[:2]==['BUY_ANIMAL','GOOSE']:c[1]=self.species
            targets[199]['shed'].pop('GOOSE')
            targets[199]['shed'][self.species]=targets[199]['shed'].get(self.species,0)+1
            ctl.donor.tape,ctl.donor.targets=tape,targets
            self.tranche['placement_keys']={(203,4)}
            self.decision198.update(first_animal_only=True,
                additional_purchase_cost={'COW':100,'SHEEP':200}[self.species],
                scope_correction='Only199first animal procurement/retained target,200pickup,202structure,203placement change. All other GOOSE targets/commands and later structures restored byte-exact. No capital injection or route rescheduling.')
        return action

class EconomicFirst(FirstTranche):
    def __init__(self,source):
        super().__init__(source,'SHEEP')
        self.economic_decision=None

    def __call__(self,obs,cfg):
        if obs['step']==198:
            ctl=self.source._POLICY
            if ctl.active and ctl.arm!='episode_114453315':
                self.economic_decision=choose(obs,cfg,ctl.donor.tape,ctl.donor.targets)
                selected=self.economic_decision['selected']
                self.enabled=selected!='GOOSE'
                if self.enabled:self.species=selected
        return super().__call__(obs,cfg)

    def receipt(self):
        return dict(super().receipt(),economic_decision=self.economic_decision,
            scope_economic='Unfitted, frozen conditional dated first-animal projection and public existing-animal/market model. Unknown future shop draws use public expectation, no seed/source future/rival private state. Full limitations retained; no win-probability claim or midgame incompatible fallback.')
