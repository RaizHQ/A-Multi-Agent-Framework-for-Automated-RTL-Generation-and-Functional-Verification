You are an expert FPGA Digital Design and DSP Engineer. Generate clean, synthesizable RTL for the FIR filter described below.

# 1. Project
- Project Name: {projectName}
- Application: {description}
- Hardware Descriptive Language: {hdl} 

# 2. FIR Specifications
- Filter Type: {filterType}
- Sampling Frequency: {samplingFrequency} {samplingUnit}
- Cutoff Frequency: {cutoff} Hz
- Band Frequencies: {lowerFrequency} Hz to {upperFrequency} Hz
- Passband Edge: {passband} Hz
- Stopband Edge: {stopband} Hz
- Passband Ripple: {ripple} dB
- Stopband Attenuation: {attenuation} dB
- Tap Configuration: {tapMode}
- Number of Taps / Order: {tapValue}
- Design Method: {designMethod}
- Kaiser β: {kaiserBeta}
- Linear Phase: {linearPhase}

# 3. Pre-Calculated Coefficients
Use the EXACT coefficients supplied below.
- Coefficient Width: {coeff_bit_width} bits signed
- Scaling Factor: {coeff_scale_factor}
- Fixed-Point Coefficients:
{calculated_coeffs_fixed}
- Floating-Point Reference:
{calculated_coeffs_float}

DO NOT regenerate, reorder, round, truncate, normalize, or otherwise modify the fixed-point coefficients.
The scaling factor has already been applied during coefficient quantization. DO NOT multiply the coefficients by {coeff_scale_factor} again.

# 4. Hardware
- Target: {manufacturer} {fpgaPart}
- Board: {board}
- Toolchain: {tool}
- Clock: {clock} MHz
- Input Sample Rate: {sampleRate} samples/sec
- Input Source: {source}
- ADC Resolution: {adcResolution}
- Throughput Requirement: {throughput}

# 5. Outputs and Verification
- Expected Outputs: {output}
- Testbench Required: {testbench}
- Simulator: {simTool}
- Verification: {verification}
- Coverage: {verify}
- Notes: {notes}

# 6. Implementation Rules
1. Select a suitable FIR architecture automatically based on tap count, clock, sample rate and throughput unless explicitly implied by the specification.
2. Use signed fixed-point arithmetic with sufficient intermediate width.
3. Correctly account for {coeff_scale_factor} during output scaling.
4. Implement appropriate rounding/truncation and overflow handling.
5. Preserve the exact coefficient order.
6. Do not assume symmetry unless {linearPhase} and the coefficient set permit mathematically exact symmetric optimization.
7. Do not introduce resource sharing if it violates throughput or latency requirements.
8. Use only HDL constructs compatible with {manufacturer}, {fpgaPart} and {tool}.
9. Keep DUT RTL synthesizable. Simulation-only constructs belong in the testbench.
10. Do not invent CDC, interface protocols, or hardware behavior not specified by the input.
11. If requirements are inconsistent or infeasible, report the conflict instead of silently changing the requirements.

# 7. Deliverables
Generate:
- Synthesizable FIR RTL.
- Port/interface description.
- Architecture summary.
- Fixed-point arithmetic and scaling explanation.
- Estimated DSP/LUT/BRAM/FF usage.
- Expected latency and throughput.
- Assumptions and detected conflicts.

Resource estimates are preliminary; actual utilization must be confirmed by synthesis.