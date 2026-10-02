from copy import deepcopy
from adaptive_milk import AdaptiveMilk
class CombinedFeedback:
    def __init__(self, native, compose=None):
        object.__setattr__(self,'native',native)
        object.__setattr__(self,'compose',compose)
        object.__setattr__(self,'hook_calls',0)

    def __getattr__(self,name):return getattr(self.native,name)

    def __setattr__(self,name,value):
        if name in ('native','compose','hook_calls'):object.__setattr__(self,name,value)
        else:setattr(self.native,name,value)

    def __call__(self,obs,cfg):
        self.hook_calls+=1
        if self.compose is None:return self.native(obs,cfg)
        t=obs['step'];row=self.native.tape[t];target=self.native.targets[t]
        action,reservation=self.compose(obs,cfg,deepcopy(row),deepcopy(target))
        assert isinstance(action,dict) and all(k in action for k in ('farmer','hands','market'))
        if target is None:
            # End-day targets mix later deposit with market fills. Until an
            # explicit final-turn closure exists, no fabricated reservations.
            assert reservation is None,'No implicit reservation at end-day target=None'
            assert action['market']==row['market'],'End-day market edits need explicit closure'
        else:
            assert isinstance(reservation,dict)
            assert all(k in reservation for k in ('hands','land','shed','seeds'))
            assert reservation['hands']>=target['hands'] and reservation['land']>=target['land']
            assert all(reservation[k].get(item,0)>=n for k in ('shed','seeds') for item,n in target[k].items()),'Native obligations cannot be spent by supplemental work'
        self.native.tape[t],self.native.targets[t]=action,reservation
        try:
            # Existing Demonstration projects complete current native+service
            # actor commands before ResourceFeedback generates market orders.
            return self.native(obs,cfg)
        finally:self.native.tape[t],self.native.targets[t]=row,target

    def receipt(self):
        return dict(self.native.receipt(),combined_feedback_calls=self.hook_calls)

class FlexBoundary(AdaptiveMilk):
    def __init__(self,source,compose=None):
        super().__init__(source);self.composer=compose;self.boundary=None

    def __call__(self,obs,cfg):
        # Install after all accepted early policy choices, without replacing
        # or replaying those choices. Native remains the owner of its state.
        ctl=self.source._POLICY
        if obs['step']>=240 and ctl.active and self.boundary is None:
            self.boundary=CombinedFeedback(ctl.donor,self.composer)
            ctl.donor=self.boundary
        return super().__call__(obs,cfg)

    def receipt(self):
        return dict(super().receipt(),combined_boundary_calls=self.boundary.hook_calls if self.boundary else 0,
            scope_boundary='One native call; compose physical actions and nondecreasing native reservations before original stock projection/market closure. Current row and target restored; accepted source unchanged. No service planner/performance claim.')
