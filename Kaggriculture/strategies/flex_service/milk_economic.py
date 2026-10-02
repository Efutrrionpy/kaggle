from collections import Counter
from own_worker_projection import engine
from fourth_economic import timeline,cohort
from late_milk import compile_late_cows
def choose(obs,cfg,tape,targets):
    compiled,error=compile_late_cows(obs,cfg,tape,targets)
    if error:return dict(selected='COW',reason=error)
    events=timeline(obs,cfg,tape,targets)
    future=[]
    for t,row in events:
        if t<=219:continue
        for actor,pos,c,grain in row:
            if len(c)>1 and c[0]=='PLACE' and c[1] in engine.ANIMALS:
                future.append(dict(step=t,place=t,actor=actor,site=pos,species=c[1]))
    pickups=sum(int(c[2]) for a in tape[220:] for c in [a['farmer'],*a['hands']] if c[:2]==['PICKUP','COW'])
    assert pickups>=len(compiled['placements'])
    # score() expects a single profile; summing each product independently below
    # preserves common future geese/sheep instead of adding them as the choice.
    profiles={};estimates={}
    for option in ('COW','GOOSE','SHEEP'):
        per_product={k:Counter() for k in ('EGG','MILK','WOOL')}
        cohorts=[]
        for placement in future:
            species=option if placement['species']=='COW' else placement['species']
            flow=cohort(species,events,cfg,placement)
            per_product[flow['product']].update(flow['sales'])
            cohorts.append(dict(placement=placement,species=species,profile=flow))
        # Reuse the accepted public biology/town model, with all future own
        # profiles represented as part of the own background cashflow.
        from fourth_economic import asset_supply,ITEMS
        own=asset_supply(obs['farms'][obs['player']],obs['step'])
        rival=asset_supply(obs['farms'][1-obs['player']],obs['step'])
        for item,sales in per_product.items():
            for t,n in sales.items():own[t][item]+=n
        known=Counter()
        for shop in obs['town']['unlocked_shops']:
            for item in engine.SHOPS[shop]:known[item]+=2 if len(engine.SHOPS[shop])==1 else 1
        expected=Counter()
        for products in engine.SHOPS.values():
            for item in products:expected[item]+=(2 if len(products)==1 else 1)/len(engine.SHOPS)
        inv={item:float(obs['market']['inventory'][item]) for item in ITEMS};cash=[0.,0.]
        for t in range(220,719):
            for item in ITEMS:
                n0,n1=int(own[t][item]),int(rival[t][item])
                for i in range(max(n0,n1)):
                    price=engine.market_price(item,inv[item],obs['market'].get('params'))
                    s0,s1=i<n0,i<n1;cash[0]+=price*s0;cash[1]+=price*s1
                    if price>1:inv[item]+=s0+s1
            if t%cfg['townShopSellInterval']==0:
                unlocked=min(engine.MAX_SHOP_INSTANCES,t//(cfg['townShopUnlockInterval']*24))
                future_count=max(0,unlocked-len(obs['town']['unlocked_shops']))
                for item in ITEMS:inv[item]-=known[item]+future_count*expected[item]
            if t%cfg['townCenterSellInterval']==0:
                for item in ITEMS:inv[item]-=1
        estimates[option]=dict(own_receipts=cash[0],rival_receipts=cash[1],planned_cow_pickup_units=pickups,
            option_procurement_cost=pickups*engine.ANIMALS[option]['cost'],
            cash_margin=cash[0]-cash[1]-pickups*engine.ANIMALS[option]['cost'])
        profiles[option]=cohorts
    return dict(selected=max(estimates,key=lambda s:estimates[s]['cash_margin']),estimates=estimates,profiles=profiles,
        limitations='Conditional service/feed/hires and procurement; no funding guarantee. Future own animal placements included, future rival investment omitted. Existing public animals assumed continuously serviced; market timing approximate. Unrevealed shops use expectation, not realised draw. No seed or future observation.')
