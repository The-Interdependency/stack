# ratios: loc_comments=0:13 imports_exports=0:0 calls_definitions=0:0


"""Post-calibration integration/demo line.

One thin integration package that combines, without modifying any frozen
calibration build:

- the DeepCode playable implementation (`ahbg/deepseek/`) for the engine:
  world + turn loop + move/build mechanics + persistence + deterministic
  replay, with the energy layer available for live-provider mode;
- Grok's cross-driver viewer surface (`ahbg/grok/bridges/common.py`) for
  tile naming and hex geometry, reused read-only for headless frames and the
  interactive window.

Only mechanics with earned standing are demonstrated: observe -> choose ->
move/build -> encounter adversarial tile context -> refuse injection ->
persist -> deterministic replay. War stays fail-closed and visibly ``hmmm``.
"""
# ratios: loc_comments=0:13 imports_exports=0:0 calls_definitions=0:0
