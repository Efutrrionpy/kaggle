"""Research adapter: exact current-turn own worker effects using pinned engine.

Inputs deliberately exclude market history, opponent private state and seed.
Not a multi-turn forecast or a standalone Kaggle package.
"""
from collections import Counter
from copy import deepcopy
import engine_core as engine


def project(farm, private, action, *, step, configuration):
    farm, private = deepcopy(farm), deepcopy(private)
    commands = [action.get('farmer', ['PASS']), *action.get('hands', [])]
    demand = Counter(c[1] for c in commands if len(c) >= 2 and c[0] == 'PLANT')
    blocked = {crop for crop, count in demand.items() if count > private['seeds'].get(crop, 0)}
    ledger = []
    for actor, command in enumerate(commands):
        effective = ['PASS'] if len(command) >= 2 and command[0] == 'PLANT' and command[1] in blocked else command
        before_shed = Counter(private['shed'])
        before_carried = Counter(private['inventories'][actor]) if actor < len(private['inventories']) else Counter()
        engine._apply_unit_action(farm, private, actor, effective, configuration['boardSize'],
                                  step // configuration['turnsPerDay'], configuration['turnsPerDay'],
                                  configuration['shedCapacity'])
        after_shed = Counter(private['shed'])
        after_carried = Counter(private['inventories'][actor]) if actor < len(private['inventories']) else Counter()
        delta = lambda a, b: {i: b[i] - a[i] for i in a.keys() | b.keys() if b[i] != a[i]}
        ledger.append({'actor': actor, 'requested': command, 'effective': effective,
                       'shed_delta': delta(before_shed, after_shed),
                       'carried_delta': delta(before_carried, after_carried)})
    return {'farm': farm, 'private': private, 'ledger': ledger}


def deposit_after_market(private, *, capacity):
    """Call only after executing market, and only on a real endday boundary."""
    private = deepcopy(private)
    engine._drop_inventories_to_shed(private, capacity)
    return private
