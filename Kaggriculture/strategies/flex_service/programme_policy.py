from copy import deepcopy
from collections import Counter
import json,hashlib
from pathlib import Path
from own_worker_projection import project,engine
from legal_macro_interface import legal_input
ROOT=Path(__file__).resolve().parent
class Demonstration:

    def __init__(self, path):
        self.tape = json.loads(path.read_text())['actions']
        assert len(self.tape) == 719
        self.calls = 0
        self.errors = []
        self.shape_changes = []

    def __call__(self, obs, cfg):
        self.calls += 1
        try:
            step = obs['step']
            action = deepcopy(self.tape[step])
            needed = len(obs['farms'][obs['player']]['hands'])
            old = len(action['hands'])
            action['hands'] = action['hands'][:needed] + [['PASS'] for _ in range(max(0, needed - old))]
            if old != needed:
                self.shape_changes.append(dict(step=step, original=old, actual=needed))
            return action
        except Exception as exc:
            self.errors.append(repr(exc))
            raise

    def receipt(self):
        return dict(calls=self.calls, errors=self.errors, reports={}, shape_changes=self.shape_changes, scope='Frozen action-only public tape, current legal step/own hand count. No responsive market adaptation or elite-strength claim.')
class ResourceFeedback(Demonstration):

    def __init__(self, actions_path, targets_path, enabled=True):
        super().__init__(actions_path)
        self.targets = json.loads(targets_path.read_text())['targets']
        assert len(self.targets) == len(self.tape)
        self.enabled = enabled
        self.events = []

    def __call__(self, observation, configuration):
        action = super().__call__(observation, configuration)
        if not self.enabled:
            return action
        obs, cfg = legal_input(observation, configuration)
        t = obs['step']
        target = self.targets[t]
        if target is None:
            return action
        after = project(obs['farms'][obs['player']], obs['private'], action, step=t, configuration=cfg)
        farm, private = (after['farm'], after['private'])
        shed = private['shed']
        sales = []
        for item in engine.PRODUCTS:
            excess = max(0, shed.get(item, 0) - target['shed'].get(item, 0))
            if excess:
                sales.append(['SELL', item, excess])
        sales.sort(key=lambda o: (-o[2] * obs['market']['prices'][o[1]], o[1]))
        buys = []
        for crop in engine.CROPS:
            need = target['seeds'].get(crop, 0) - private['seeds'].get(crop, 0)
            if need > 0:
                buys.append(['BUY_SEED', crop, need])
        for item in list(engine.ANIMALS) + ['WHEAT', 'FERTILIZER']:
            need = target['shed'].get(item, 0) - shed.get(item, 0)
            if need > 0:
                buys.append(['BUY_ANIMAL' if item in engine.ANIMALS else 'BUY_PRODUCT', item, need])
        hires = max(0, target['hands'] - len(farm['hands']))
        lands = max(0, target['land'] - len(farm['unlocked_quadrants']))
        atomic = [['HIRE'] for _ in range(hires)] + [['BUY_LAND'] for _ in range(lands)]
        limit = cfg['maxMarketOrdersPerTurn']
        proposed = sales[:1] + atomic + buys + sales[1:]
        orders = proposed[:limit]
        if orders != action['market']:
            self.events.append(dict(step=t, original=deepcopy(action['market']), issued=deepcopy(orders), omitted=deepcopy(proposed[limit:]), target=target, post_worker_shed=deepcopy(shed), post_worker_seeds=deepcopy(private['seeds']), money=farm['money']))
        return dict(action, market=orders)

    def receipt(self):
        return dict(super().receipt(), feedback_enabled=self.enabled, feedback_events=self.events, scope_feedback='Fixed complete public physical programme; after exact current own-worker projection, close deficits to demonstrated retained inputs/worker/land targets and sell observed surplus. Source targets exclude opponent-private data, money, rewards and seed. End-day market unchanged because deposit target is ambiguous. No claim of gold strength or reconstructed elite response.')
class CompactTelemetryFeedback(ResourceFeedback):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feedback_details = []

    def __call__(self, obs, cfg):
        action = super().__call__(obs, cfg)
        self.feedback_details.extend(self.events)
        self.events.clear()
        return action

    def receipt(self):
        return dict(super().receipt(), feedback_events=self.feedback_details, telemetry_storage='Full events in exclusive per-game candidate receipt, not duplicated in aggregate result rows.')
def contract(obs):
    f = deepcopy(obs['farms'][obs['player']])
    f.pop('money', None)
    return dict(farm=f, private=deepcopy(obs['private']))

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
class CatalogueProgramme:

    def __init__(self, plan, arm):
        self.arm = arm
        self.root = plan['root_step']
        self.entry = plan['entry_contract']
        spec = plan['base_prefix']
        donor = plan['demonstrations'][arm]
        self.prefix = CompactTelemetryFeedback(ROOT / spec['actions_path'], ROOT / spec['targets_path'])
        self.donor = CompactTelemetryFeedback(ROOT / donor['actions_path'], ROOT / donor['targets_path'])
        self.active = False
        self.decision = None
        self.root_observation = None
        self.calls = 0
        self.errors = []
        self.events = []

    def __call__(self, observation, configuration):
        self.calls += 1
        obs, cfg = legal_input(observation, configuration)
        if obs['step'] == self.root:
            current = contract(obs)
            self.active = current == self.entry
            self.root_observation = obs
            self.decision = dict(step=self.root, requested=self.arm, admitted=self.active, selected=self.arm if self.active else 'existing_a', entry_contract_sha256=digest(current))
        return (self.donor if self.active else self.prefix)(observation, configuration)

    def receipt(self):
        return dict(calls=self.calls, errors=self.errors, reports={}, decision=self.decision, root_observation=self.root_observation, prefix_receipt=self.prefix.receipt(), donor_receipt=self.donor.receipt(), scope='Same actually executed A opening through73. Full fixed donor continuation at74 only at matching own entry; no history/wealth injection. Full root and feedback saved in exclusive receipt,not duplicated in aggregate decision.')
class ProgrammeRouter(CatalogueProgramme):

    def __init__(self, plan):
        self.model = plan['router']
        self.specs = plan['demonstrations']
        super().__init__(plan, self.model['fallback'])

    def __call__(self, observation, configuration):
        obs, cfg = legal_input(observation, configuration)
        if obs['step'] == self.root:
            shop = '+'.join(obs['town']['unlocked_shops'])
            self.arm = self.model['routing'].get(shop, self.model['fallback'])
            spec = self.specs[self.arm]
            self.donor = CompactTelemetryFeedback(ROOT / spec['actions_path'], ROOT / spec['targets_path'])
        return super().__call__(observation, configuration)
def structural(value):
    q = deepcopy(value)
    for row in q['farm']['tiles']:
        for tile in row:
            if isinstance(tile, dict) and tile.get('animal'):
                for field in ('consecutive_unfed', 'pending_care_bonus'):
                    tile.pop(field, None)
    return q

class BiologyEntry(ProgrammeRouter):

    def __call__(self, observation, configuration):
        obs, cfg = legal_input(observation, configuration)
        relaxed = False
        if obs['step'] == self.root:
            current = contract(obs)
            relaxed = current != self.entry and structural(current) == structural(self.entry)
            if relaxed:
                self.entry = current
        action = super().__call__(observation, configuration)
        if obs['step'] == self.root:
            self.decision['biology_only_entry_relaxed'] = relaxed
        return action
