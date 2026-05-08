# FLD System Builder Project State  
  
## Current Status  
The FLD System Builder is a local Flask app running on port 5010 and temporarily shared through Cloudflare Tunnel.  
  
The app now includes:  
- Component Manager  
- Saved Projects / versioning  
- Pump Curve Manager  
- Pump curve import / validation / preview / export  
- Operating point overlay  
- Dynamic branch UI  
- Internal pipe diameter logic  
- Equivalent fitting length logic  
- Pump auto-select  
- Water storage auto-select  
- Design Direction  
- Design Readiness  
- Section Readiness  
- Guided Builder Summary  
- Auto Select Summary  
- Architecture Recommendations  
- Bottleneck Intelligence  
- Scenario / Operating Mode Comparison  
- Hydraulic Optimizer with minimum viable pipe logic and engineering reasoning  
  
## Current Direction  
We are building toward an interactive guided engineering design assistant, not live deployment automation.  
  
The tool should support:  
- Start from known pump/engine and suggest best zones/components  
- Start from known zones/sprinklers and suggest pump/engine/water/fuel/power  
- Leave fields on Auto Select  
- Use green/yellow/red readiness states  
- Suggest missing inputs  
- Allow section-by-section updating later  
  
## Current Phase  
Phase 2.1: Design Readiness Engine / Guided Builder Layer  
  
Recently added:  
- `section_readiness.py`  
- `build_section_readiness_html(primary)`  
- green/yellow/red section status styling  
- `build_guided_builder_summary_html(primary)`  
- `build_auto_select_summary_html(primary)`  
  
## Current Known Auto Select Behavior  
Working:  
- Pump auto-select  
- Water storage auto-select  
  
In progress / next:  
- Engine auto-select  
- Motor auto-select  
- Fuel storage auto-select  
- Battery auto-select  
- Generator auto-select  
- Pipe auto-select later  
- Section update buttons later  
  
## Current Restart Instructions  
Do NOT touch the Apple Terminal / Cloudflare window unless restarting the tunnel.  
  
To restart Flask in Cursor:  
1. Run:  
 ```bash  
 lsof -ti :5010