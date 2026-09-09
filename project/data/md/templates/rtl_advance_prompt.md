You are an expert FPGA Digital Design and DSP Engineer. Generate production-quality synthesizable FIR RTL from the following specification.

# 1. Project
- Project Name: {projectName}
- Application: {description}
- Hardware Descriptive Language: {hdl}

# 2. FIR Specifications
- Filter Type: {filterType}
- Sampling Frequency: {samplingFrequency} {samplingUnit}
- Cutoff Frequency: {cutoff} Hz
- Passband: {passband} Hz
- Stopband: {stopband} Hz
- Passband Ripple: {ripple} dB
- Stopband Attenuation: {attenuation} dB
- Tap Configuration: {tapMode}
- Design Method: {designMethod}
- Linear Phase: {linearPhase}

# 3. Fixed-Point Architecture
- Input: {inputWidth} bits, {inputFormat}, Q{inputQ}
- Coefficients: {coeff_bit_width} bits, Q{coeffQ}
- Accumulator: {accWidth} bits
- Output: {outputWidth} bits
- Rounding: {rounding}
- Overflow: {overflow}

# 4. Hardware Architecture
- Target: {manufacturer} {fpgaPart}
- Board: {board}
- Tool: {tool}
- FIR Architecture: {architecture}
- Processing Mode: {processing}
- Symmetric Optimization: {symmetric}
- Optimization Priority: {optimization}
- Clock Domains: {clockDomains}
- System Clock: {clock} MHz
- FIR Clock: {firClock} MHz
- Latency Target: {latency}
- Throughput Target: {timingThroughput}
- Pipelining: {pipelining}

# 5. Interface
- Protocol: {interface}
- Input Source: {source}
- Input Rate: {sampleRate} samples/sec
- Input Handshake: {inputHandshake}
- Output Handshake: {outputHandshake}
- Reset: {resetType}, {resetPolarity}
- Clock Enable: {clockEnable}

# 6. Pre-Calculated Coefficients
Use the EXACT fixed-point coefficient array:
{calculated_coeffs_fixed}

Floating-point reference:
{calculated_coeffs_float}

Coefficient Width: {coeff_bit_width} bits
Quantization Scale: {coeff_scale_factor}

The coefficients are immutable. Do not regenerate, reorder, round, truncate, normalize or modify them.
The scaling factor has already been applied during coefficient generation. DO NOT multiply the coefficients by {coeff_scale_factor} again.

# 7. Verification
- Outputs: {output}
- Testbench Required: {testbench}
- Simulator: {simTool}
- Verification Models: {verification}
- Coverage: {verify}
- Notes: {notes}

# 8. Engineering Rules
1. Follow explicitly specified architecture, processing mode, protocol, latency, throughput and optimization settings.
2. Use mathematically correct signed fixed-point arithmetic and sufficient intermediate widths.
3. Apply {rounding} and {overflow} exactly as specified.
4. Preserve coefficient ordering and numerical meaning.
5. Symmetric optimization is allowed only when mathematically exact for the supplied coefficients.
6. Verify architecture feasibility against clock, throughput and latency before implementation.
7. Do not introduce time-multiplexing/resource sharing if it violates throughput or latency.
8. Do not invent CDC logic. If multiple clock domains require an unspecified CDC mechanism, report the requirement as unresolved.
9. Use only constructs compatible with {manufacturer}, {fpgaPart} and {tool}.
10. DUT RTL must be synthesizable; simulation-only code belongs in the testbench.
11. Never silently change a user requirement. Report conflicts or infeasibility explicitly.

# 9. Deliverables
Generate:
- Synthesizable FIR RTL.
- Interface/port definition.
- Architecture description.
- Pipeline and latency description.
- Fixed-point arithmetic/scaling description.
- Preliminary resource estimate.
- Timing/throughput analysis.
- Assumptions, conflicts and feasibility status.