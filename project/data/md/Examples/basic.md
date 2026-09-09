You are an expert FPGA Digital Design and DSP Engineer. Your task is to generate a complete, synthesizable RTL design and a verification testbench based on the following specific requirements.

# Project Context
- **Project Name:** Test
- **Experience Level/Complexity:** basic
- **Application Description:** N/A

# Filter Specifications (DSP Requirements)
- **Filter Type:** Low-pass
- **Sampling Frequency:** 3432 Hz
- **Cutoff Frequency (Low/High-pass):** 22 Hz
- **Band Frequencies (Band-pass/stop):** N/A Hz (Lower) to N/A Hz (Upper)
- **Passband Edge:** N/A Hz
- **Stopband Edge:** N/A Hz
- **Passband Ripple:** N/A dB
- **Stopband Attenuation:** 22 dB
- **Tap Configuration:** auto
- **Number of Taps / Order:** N/A
- **Filter Design Method:** Automatic
- **Kaiser Window β (if applicable):** N/A
- **Linear Phase Required:** Yes

# Pre-Calculated Filter Coefficients (SciPy Generated)
The DSP math and coefficient quantization have already been executed via Python. Use the EXACT Fixed-Point integers provided below for your RTL implementation.
- **Coefficient Bit Width:** 16-bit signed
- **Scaling Factor applied:** multiplied by 32767

**Fixed-Point Coefficients (RTL Implementation Array):**
[
    153,
    174,
    233,
    328,
    457,
    613,
    791,
    983,
    1180,
    1373,
    1555,
    1716,
    1850,
    1950,
    2012,
    2033,
    2012,
    1950,
    1850,
    1716,
    1555,
    1373,
    1180,
    983,
    791,
    613,
    457,
    328,
    233,
    174,
    153
]

*(Reference Only) Original Floating-Point Coefficients:*
[
    0.0046669486,
    0.0052956859,
    0.0070959059,
    0.0100132837,
    0.0139396471,
    0.0187174729,
    0.0241468453,
    0.0299945520,
    0.0360048900,
    0.0419116556,
    0.0474507360,
    0.0523726821,
    0.0564546400,
    0.0595110504,
    0.0614025811,
    0.0620428468,
    0.0614025811,
    0.0595110504,
    0.0564546400,
    0.0523726821,
    0.0474507360,
    0.0419116556,
    0.0360048900,
    0.0299945520,
    0.0241468453,
    0.0187174729,
    0.0139396471,
    0.0100132837,
    0.0070959059,
    0.0052956859,
    0.0046669486
]

# Hardware & Platform Constraints
- **Target Architecture:** Intel/Altera -
- **Target Board:** N/A
- **Synthesis Toolchain:** Automatic
- **System Clock Frequency:** 122 MHz
- **Input Sample Rate:** 1212 samples/sec
- **Input Source:** ADC
- **ADC Resolution (if applicable):** 12-bit
- **Throughput Requirement:** Automatic

# Deliverables & Verification
- **Expected Outputs:** Verilog RTL, FIR coefficients, Testbench
- **Testbench Required:** Yes (Target Simulator: QuestaSim)
- **Verification Models Needed:** Python
- **Verification Coverage:** Frequency response, Random input comparison, Throughput verification
- **Additional Engineering Notes:** N/A

# Tasks to Execute:
1. **RTL Implementation:** Write the Verilog RTL, FIR coefficients, Testbench (preferably Verilog/SystemVerilog unless otherwise specified). Use the pre-calculated 16-bit fixed-point coefficients provided above. The architecture must meet the `Automatic` requirement while running at a `122` MHz system clock. Implement an efficient Multiply-Accumulate (MAC) pipeline, taking into account the multiplication by the 32767 scaling factor to prevent overflow.
2. **Interface Design:** Provide standard clock, synchronous reset, and data valid handshake signals suitable for interfacing with the specified input source (ADC).
3. **Testbench Generation:** If `Yes` is "Yes", generate a standard testbench compatible with `QuestaSim` that stimulates the filter to verify `Frequency response, Random input comparison, Throughput verification`.
4. **Resource Estimation:** Provide a brief summary estimating the required DSP slices and block RAMs based on the `Intel/Altera` architecture.

Ensure the generated code is clean, well-commented, and follows industry best practices for synchronous digital design.