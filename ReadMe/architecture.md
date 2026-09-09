requirements.json
      │
      ▼
┌──────────────────────┐
│ Specification Agent  │
│ validate + Automatic │
│ default resolution   │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ FIR/DSP Agent        │
│ taps + coefficients  │
│ fixed-point design   │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Architecture Agent   │
│ DSP/LUT/FF/timing    │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ RTL Generator Agent  │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Verification Agent   │
│ TB + Python golden   │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Simulation Agent     │
│ actual headless run  │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Quartus Agent        │
│ synthesis + timing   │
└──────────┬───────────┘
           │
       FAIL ▼
┌──────────────────────┐
│ Diagnosis/Router     │
│ bounded repair loop  │
└──────────────────────┘







requirements.json
       ↓
Specification Agent
       ↓
validated_spec.json
       ↓
DSP/FIR Agent
       ↓
coefficients.json
fixed_point_spec.json
       ↓
Architecture Agent
       ↓
architecture.json
interface_spec.json
       ↓
RTL Agent
       ↓
rtl/
       ↓
Verification Environment Agent
       ↓
verification/
simulation_manifest.json
       ↓
Headless Simulation Agent
       ↓
execution_report.json
       ↓
       ┌─────────────┐
       │             │
      PASS          FAIL
       │             │
       ▼             ▼
   Quartus       Diagnosis
                   Agent
                     │
             ┌───────┼────────┐
             ▼       ▼        ▼
            RTL     DSP       TB