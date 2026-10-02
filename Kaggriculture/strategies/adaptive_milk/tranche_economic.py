"""Unfitted later-asset proposal: dated production and public inventory economics.

Conditional forecast, not a resource certificate or hidden-future reconstruction.
All inputs are the reached legal root and already-frozen intended programmes.
"""
from collections import Counter, defaultdict
from copy import deepcopy
from own_worker_projection import engine

MOVES={'NORTH':(0,-1),'SOUTH':(0,1),'WEST':(-1,0),'EAST':(1,0)}
ITEMS=('EGG','MILK','WOOL')


def timeline(obs,cfg,tape,targets):
    farm=obs['farms'][obs['player']];positions=deepcopy([farm['farmer'],*farm['hands']])
    grain=[i.get('WHEAT',0) for i in obs['private']['inventories']]
    h=cfg['boardSize']//2;access=[(h-1,h-1),(h,h-1),(h-1,h),(h,h)]
    out=[]
    for t in range(198,719):
        row=[]
        for i,c in enumerate([tape[t]['farmer'],*tape[t]['hands']]):
            if i>=len(positions):continue
            pos=positions[i];row.append((i,list(pos),list(c),grain[i]))
            if c[0] in MOVES:
                dx,dy=MOVES[c[0]];x,y=pos
                if 0<=x+dx<cfg['boardSize'] and 0<=y+dy<cfg['boardSize']:positions[i]=[x+dx,y+dy]
            elif c[:2]==['PICKUP','WHEAT'] and tuple(pos) in access:grain[i]+=c[2]
            elif c[0]=='FEED' and grain[i]>0:grain[i]-=1
            elif c[0]=='DROP' and tuple(pos) in access:grain[i]=0
            elif c[:2]==['PLACE','WHEAT'] and tuple(pos) in access:grain[i]=max(0,grain[i]-c[2])
        out.append((t,row))
        if (t+1)%cfg['turnsPerDay']==0:
            positions=[[h-1,h-1]];grain=[0]
        elif targets[t] is not None:
            for _ in range(max(0,targets[t]['hands']-len(positions)+1)):
                site=min(access,key=lambda s:sum(tuple(p)==s for p in positions))
                positions.append(list(site));grain.append(0)
    return out


def cohort(species,events,cfg):
    """First new asset at203/(3,5), exact species biology under intended service.

    Delivery conservatively occurs at actual DROP or nightly inventory deposit;
    omit optional PLACE EGG remapping so mixed cargo cannot manufacture receipts.
    Future hires/feed pickups remain conditional. No future observed states.
    """
    state=None;cargo=Counter();sales=Counter();feed=0;harvest=0
    h=cfg['boardSize']//2;access={(h-1,h-1),(h,h-1),(h-1,h),(h,h)}
    for t,row in events:
        if t==203:state=engine._new_animal(species,t//cfg['turnsPerDay'])
        if t<204:continue
        for actor,pos,c,grain in row:
            if pos==[3,5] and state and state.get('animal'):
                if c[0]=='FEED' and grain>0 and not state['fed_today']:state['fed_today']=True;feed+=1
                elif c[0]=='CARE':state['cared_today']=True
                elif c[0]=='HARVEST':
                    cargo[actor]+=state['yield_units'];harvest+=state['yield_units'];state['yield_units']=0
            if c[0]=='DROP' and tuple(pos) in access:
                sales[t]+=cargo.pop(actor,0)
        if (t+1)%cfg['turnsPerDay']==0:
            # Night deposit is after market, hence next turn is first sale slot.
            if t+1<719:sales[t+1]+=sum(cargo.values())
            cargo.clear()
            f={'tiles':[[state]]};engine._daily_refresh_animals(f,t//cfg['turnsPerDay']);state=f['tiles'][0][0]
    return dict(sales={t:q for t,q in sales.items() if q},feed=feed,harvest=harvest,
                final_tile=state,product=engine.ANIMALS[species]['product'])


def asset_supply(farm,start=198):
    """Public existing animal ages; continued daily care/feed is an explicit model.

    Unknown future rival investment, feed failures, cargo delay are not invented.
    Model production is harvested/sold at dawn; use as uncertain background only.
    """
    animals=[deepcopy(t) for row in farm['tiles'] for t in row if isinstance(t,dict) and t.get('animal')]
    flow=defaultdict(Counter)
    for tile in animals:
        p=engine.ANIMALS[tile['animal']]['product']
        flow[start+1][p]+=tile.get('yield_units',0);tile['yield_units']=0
        for day in range(start//24,30):
            t=(day+1)*24
            if t>=719:break
            tile['fed_today']=True;tile['cared_today']=True
            f={'tiles':[[tile]]};engine._daily_refresh_animals(f,day);tile=f['tiles'][0][0]
            flow[t][p]+=tile['yield_units'];tile['yield_units']=0
    return flow


def score(obs,cfg,profiles,species):
    own=asset_supply(obs['farms'][obs['player']]);rival=asset_supply(obs['farms'][1-obs['player']])
    inv={p:float(obs['market']['inventory'][p]) for p in ITEMS}
    known=Counter()
    for shop in obs['town']['unlocked_shops']:
        for p in engine.SHOPS[shop]:known[p]+=2 if len(engine.SHOPS[shop])==1 else 1
    expected=Counter()
    for products in engine.SHOPS.values():
        for p in products:expected[p]+=(2 if len(products)==1 else 1)/len(engine.SHOPS)
    receipt=[0.,0.]
    for t in range(199,719):
        amounts=[Counter(own[t]),Counter(rival[t])]
        amounts[0][profiles[species]['product']]+=profiles[species]['sales'].get(t,0)
        # Rival and own units are quoted against the same pre-unit inventory.
        for p in ITEMS:
            n0,n1=int(amounts[0][p]),int(amounts[1][p])
            for i in range(max(n0,n1)):
                price=engine.market_price(p,inv[p]);s0=i<n0;s1=i<n1
                receipt[0]+=price*s0;receipt[1]+=price*s1
                if price>1:inv[p]+=s0+s1
        if t%cfg['townShopSellInterval']==0:
            # Public unlock law, expected unrevealed draws, no actual future list.
            unlocked=min(engine.MAX_SHOP_INSTANCES,t//(cfg['townShopUnlockInterval']*24))
            future=max(0,unlocked-len(obs['town']['unlocked_shops']))
            for p in ITEMS:inv[p]-=known[p]+future*expected[p]
        if t%cfg['townCenterSellInterval']==0:
            for p in ITEMS:inv[p]-=1
    return dict(own_receipts=receipt[0],rival_receipts=receipt[1],
                cash_margin=receipt[0]-receipt[1]-engine.ANIMALS[species]['cost'],
                final_inventory=inv)


def choose(obs,cfg,tape,targets):
    events=timeline(obs,cfg,tape,targets)
    profiles={s:cohort(s,events,cfg) for s in ('GOOSE','COW','SHEEP')}
    estimates={s:score(obs,cfg,profiles,s) for s in profiles}
    chosen=max(estimates,key=lambda s:estimates[s]['cash_margin'])
    return dict(selected=chosen,estimates=estimates,profiles=profiles,
        limitations=['Forecast assumes affordable intended hires and feed pickups.',
            'Existing public animals assumed continuously serviced; future rival investments omitted.',
            'Other unplaced own animals omitted from background supply; price exposure can be biased.',
            'Unrevealed shops use mean distribution, not realised random draws or private seed.',
            'No exact financing certificate, win calibration, or future observation input.'])
