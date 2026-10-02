from copy import deepcopy
from programme_policy import BiologyEntry
class LateFlock(BiologyEntry):
    def __init__(self,plan,enabled=True):
        super().__init__(plan);self.late_flock_enabled=enabled;self.late_transform=None;self.cargo_events=[]
    def __call__(self,obs,cfg):
        t=obs['step']
        if self.late_transform and t>198:
            action=deepcopy(self.donor.tape[t]);farm=obs['farms'][obs['player']];half=cfg['boardSize']//2
            access={(half-1,half-1),(half,half-1),(half-1,half),(half,half)}
            for actor,c in enumerate([action['farmer'],*action['hands']]):
                if c[:2]!=['PLACE','EGG'] or actor>=len(obs['private']['inventories']):continue
                pos=[farm['farmer'],*farm['hands']][actor];held=obs['private']['inventories'][actor]
                if tuple(pos) in access and held.get('EGG',0)==0 and held.get('WOOL',0)>0:
                    c[1]='WOOL';self.cargo_events.append(dict(step=t,actor=actor,held_wool=held['WOOL']))
            self.donor.tape[t]=action
        action=super().__call__(obs,cfg)
        if t==198 and self.late_flock_enabled and self.active and self.arm=='episode_114453315':
            assert obs['private']['shed'].get('GOOSE',0)==0 and all(inv.get('GOOSE',0)==0 for inv in obs['private']['inventories'])
            assert not any(c[:2] in (['PICKUP','GOOSE'],['PLACE','GOOSE'],['BUY_ANIMAL','GOOSE']) for c in [action['farmer'],*action['hands'],*action['market']])
            counts={}
            for u in range(199,719):
                a=self.donor.tape[u]
                for c in [a['farmer'],*a['hands']]:
                    if c==['BUILD_COOP']:c[0]='BUILD_PASTURE';counts['construction']=counts.get('construction',0)+1
                for c in [a['farmer'],*a['hands'],*a['market']]:
                    if len(c)>1 and c[1]=='GOOSE' and c[0] in ('PICKUP','PLACE','BUY_ANIMAL'):
                        c[1]='SHEEP';counts['animal_commands']=counts.get('animal_commands',0)+1
                target=self.donor.targets[u]
                if target is not None:
                    amount=target['shed'].pop('GOOSE',0)
                    if amount:target['shed']['SHEEP']=target['shed'].get('SHEEP',0)+amount
            self.late_transform=dict(step=198,species='SHEEP',counts=counts)
        return action
    def receipt(self):
        return dict(super().receipt(),late_flock_enabled=self.late_flock_enabled,late_transform=self.late_transform,cargo_events=self.cargo_events,
            scope_late_flock='Keepfirstday6goose tranche andallactions0..198. OnlylaterGOOSEprocurement/stock/deliveryandCOOPbuildmaptoSHEEP/PASTURE. Existinggeesestaygeese. SourceEGGdepotcommand changes toWOOLonlywhenactualactorholdsWOOLandnoEGGatshedaccess; quantity/capacityreal. Existingproducttargets unchanged; ordinaryownfeedbacksellsactualsurplus. No cashinjection orunobservedreceipts.')
