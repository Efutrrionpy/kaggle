"""Policy-facing observation boundary. No evaluator, replay, or seed API."""
from copy import deepcopy

CONFIG_FIELDS = ('episodeSteps','actTimeout','runTimeout','boardSize','startingMoney',
                 'maxMarketOrdersPerTurn','turnsPerDay','shedCapacity','weedSpawnChance',
                 'townShopUnlockInterval','townShopSellInterval','townCenterSellInterval',
                 'farmHandCostMult','marketParams')
FARM_FIELDS = ('farmer','hands','hires_today','money','tiles','unlocked_quadrants')
TILE_FIELDS = ('kind','crop','planted_day','watered_today','consecutive_unwatered',
               'yield_units','max_lifespan_step','fertilized_until_day','animal',
               'placed_day','consecutive_unfed','fed_today','cared_today',
               'fertilizer_available','pending_care_bonus')


def pick(value, names):
    return {name:deepcopy(value[name]) for name in names if name in value}


def legal_input(observation, configuration):
    cfg = pick(configuration, CONFIG_FIELDS)
    obs = pick(observation, ('player','day','hour','remainingOverageTime'))
    obs['step'] = int(obs['day'])*int(cfg['turnsPerDay'])+int(obs['hour'])
    if 'step' in observation and observation['step'] != obs['step']:
        raise ValueError('Inconsistent public clock')
    obs['farms'] = []
    for raw in observation['farms']:
        farm = pick(raw, FARM_FIELDS)
        farm['tiles'] = [[pick(tile,TILE_FIELDS) if isinstance(tile,dict) else tile for tile in row]
                         for row in raw['tiles']]
        obs['farms'].append(farm)
    obs['private'] = pick(observation['private'], ('inventories','shed','seeds'))
    obs['market'] = pick(observation['market'], ('inventory','prices','params'))
    obs['town'] = pick(observation['town'], ('unlocked_shops',))
    return obs,cfg


class IdentityMacro:
    """No-op reference for subsequently implemented feedback macros."""
    def act(self, observation, configuration, parent_action):
        return deepcopy(parent_action)


class MacroPolicy:
    def __init__(self, parent, macro=None):
        self.parent=parent
        self.macro=IdentityMacro() if macro is None else macro

    def __call__(self, observation, configuration):
        obs,cfg=legal_input(observation,configuration)
        parent=self.parent(deepcopy(obs),deepcopy(cfg))
        return self.macro.act(obs,cfg,parent)


def service_index(visits):
    result={}
    for row in visits:
        key=(int(row['step']),int(row['actor']))
        if key in result:
            raise ValueError(('Duplicate actor service',key))
        result[key]=deepcopy(row)
    return result
