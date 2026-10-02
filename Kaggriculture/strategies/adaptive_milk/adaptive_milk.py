import json
from pathlib import Path
from late_milk import LateMilk
from milk_economic import choose
class AdaptiveMilk(LateMilk):
    def __init__(self,source):
        super().__init__(source,'GOOSE')
        self.template_dir=Path(__file__).resolve().parent;self.milk_economic=None

    def __call__(self,obs,cfg):
        if obs['step']==219:
            ctl=self.source._POLICY
            if ctl.active:
                # Immutable public schedule inputs exactly match the frozen
                # predictor; do not substitute a mutated runtime tape.
                actions=json.loads((self.template_dir/f'{ctl.arm}_actions.json').read_text())['actions']
                targets=json.loads((self.template_dir/f'{ctl.arm}_targets.json').read_text())['targets']
                self.milk_economic=choose(obs,cfg,actions,targets)
                selected=self.milk_economic['selected']
                self.milk_enabled=selected!='COW'
                if self.milk_enabled:self.milk_species=selected
        return super().__call__(obs,cfg)

    def receipt(self):
        return dict(super().receipt(),milk_economic=self.milk_economic,
            scope_adaptive_milk='Exact unfitted proposal frozen before fixed-option results. Allrootguards remain; rejectedorKEEP paths retain acceptedprimary. No outcome-fitted decision, futuredata, or postcommitment rollback.')
