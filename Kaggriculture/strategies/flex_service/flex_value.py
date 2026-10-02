"""Conditional exact animal biology plus nonlinear competitive sale forecasts."""
from collections import Counter,defaultdict
from copy import deepcopy
from own_worker_projection import engine
from fourth_economic import timeline,asset_supply

ITEMS=('EGG','MILK','WOOL')

def geometry(obs,cfg,tape,targets):
    events=timeline(obs,cfg,tape,targets);by_site=defaultdict(list)
    for t,row in events:
        for actor,pos,c,grain in row:
            if c[0] not in ('PASS','NORTH','SOUTH','EAST','WEST'):
                by_site[tuple(pos)].append((t,actor,c))
    return by_site

def production(tile,events,start,extra=(),delivery=None):
    """Existing animal, actual current flags; future native service conditional.

    No fictitious future actor calls. Native harvest delivered next dawn; helper
    harvest uses its explicit depot turn. No terminal-night phantom revenue.
    """
    state=deepcopy(tile);commands=defaultdict(list);flow=Counter();product=engine.ANIMALS[tile['animal']]['product']
    for t,actor,c in events:commands[t].append((False,c))
    for t,c in extra:commands[t].append((True,c))
    for t in range(start,719):
        if not state.get('animal'):break
        for added,c in commands[t]:
            if c[0] in ('PLANT','TILL','BUILD_COOP','BUILD_PASTURE') or c[0]=='PLACE' and c[1] in engine.ANIMALS:
                return dict(product=product,sales=dict(flow),stopped=t)
            if c[0]=='FEED':state['fed_today']=True
            elif c[0]=='CARE':state['cared_today']=True
            elif c[0]=='HARVEST':
                when=delivery if added else (t//24+1)*24
                if when is not None and when<719:flow[when]+=state.get('yield_units',0)
                state['yield_units']=0
        if t%24==23:
            f={'tiles':[[state]]};engine._daily_refresh_animals(f,t//24);state=f['tiles'][0][0]
    return dict(product=product,sales=dict(flow),stopped=719)

def supplies(obs,events):
    own=defaultdict(Counter);profiles={}
    for y,row in enumerate(obs['farms'][obs['player']]['tiles']):
        for x,tile in enumerate(row):
            if isinstance(tile,dict) and tile.get('animal'):
                profile=production(tile,events[(x,y)],obs['step']);profiles[(x,y)]=profile
                for t,n in profile['sales'].items():own[t][profile['product']]+=n
    for product in ITEMS:
        own[obs['step']][product]+=obs['private']['shed'].get(product,0)
        t=(obs['step']//24+1)*24
        if t<719:own[t][product]+=sum(inv.get(product,0) for inv in obs['private']['inventories'])
    rival=asset_supply(obs['farms'][1-obs['player']],obs['step'])
    return own,rival,profiles

def market_paths(obs,cfg,own,rival,extra=None):
    """Enumerate next unseen shop; later draws use public expectation.

    Nonlinear quotes inside each scenario. Own intended receipts conditional;
    rival existing assets ideal-service, future investments omitted. Not a win
    predictor, perfect-information rollout, or exact financing certificate.
    """
    extra=extra or {};known=Counter();average=Counter()
    for shop in obs['town']['unlocked_shops']:
        for p in engine.SHOPS[shop]:known[p]+=2 if len(engine.SHOPS[shop])==1 else 1
    for products in engine.SHOPS.values():
        for p in products:average[p]+=(2 if len(products)==1 else 1)/len(engine.SHOPS)
    seen=len(obs['town']['unlocked_shops']);scenarios=list(engine.SHOPS) if seen<engine.MAX_SHOP_INSTANCES else [None]
    results=[]
    for next_shop in scenarios:
        inv={p:float(obs['market']['inventory'][p]) for p in ITEMS};cash=[0.,0.]
        for t in range(obs['step'],719):
            for p in ITEMS:
                n0=int(own.get(t,{}).get(p,0)+extra.get(t,{}).get(p,0));n1=int(rival.get(t,{}).get(p,0))
                assert n0>=0 and n1>=0
                for i in range(max(n0,n1)):
                    q=engine.market_price(p,inv[p],obs['market'].get('params'));a=i<n0;b=i<n1
                    cash[0]+=q*a;cash[1]+=q*b
                    if q>1:inv[p]+=a+b
            if t%cfg['townShopSellInterval']==0:
                count=max(0,min(engine.MAX_SHOP_INSTANCES,t//(cfg['townShopUnlockInterval']*24))-seen)
                for p in ITEMS:
                    first=(2 if len(engine.SHOPS[next_shop])==1 else 1) if count and next_shop and p in engine.SHOPS[next_shop] else 0
                    inv[p]-=known[p]+first+max(0,count-1)*average[p]
            if t%cfg['townCenterSellInterval']==0:
                for p in ITEMS:inv[p]-=1
        results.append(cash)
    return results

def delta_profile(tile,events,start,extra,delivery,baseline):
    changed=production(tile,events,start,extra,delivery);p=changed['product']
    delta={t:Counter({p:changed['sales'].get(t,0)-baseline['sales'].get(t,0)})
           for t in changed['sales'].keys()|baseline['sales'].keys()
           if changed['sales'].get(t,0)!=baseline['sales'].get(t,0)}
    return delta
