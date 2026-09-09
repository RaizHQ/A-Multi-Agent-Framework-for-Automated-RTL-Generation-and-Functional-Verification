You are an expert FPGA Digital Design and DSP Engineer. Your task is to generate a complete, synthesizable RTL design and a verification testbench based on the following advanced specification. 

# 1. Project Context
- **Project Name:** Test (basic level)
- **Application:** N/A

# 2. Filter Specifications (DSP Requirements)
- **Filter Type:** Low-pass
- **Sampling Frequency:** 3432 Hz
- **Cutoff Frequency:** 22 Hz (Passband: N/A Hz, Stopband: N/A Hz)
- **Passband Ripple:** N/A dB | **Stopband Attenuation:** 22 dB
- **Tap Configuration:** auto
- **Design Method:** Automatic | **Linear Phase:** Yes

# 3. Numerical Representation (Fixed-Point Architecture)
- **Input Data:** Automatic width, Signed two's complement, Q-Format: Automatic
- **Coefficients:** 16-bit width, Q-Format: Automatic
- **Accumulator:** Automatic width
- **Output Data:** Same as input width, Quantization: Automatic, Overflow Handling: Automatic

# 4. Hardware Architecture & Clocking
- **Target Platform:** Intel/Altera -, N/A (Synthesis Tool: Automatic)
- **FIR Architecture:** Automatic
- **Processing Mode:** Automatic (Symmetric Optimization: Automatic)
- **Optimization Priority:** Balanced
- **Clock Domains:** Same clock
- **System Clock:** 122 MHz | **FIR Processing Clock:** Same as System Clock (MHz)
- **Timing / Pipelining:** Latency: No specific requirement | Throughput Target: Automatic | Pipelining: Automatic

# 5. Interfaces & Control Logic
- **Interface Protocol:** Automatic
- **Input Source:** ADC (Input Sample Rate: 1212 samples/sec)
- **Handshaking:** Input: Automatic | Output: Automatic
- **Control Signals:** Reset: Automatic, Active High | Clock Enable: Automatic

# 6. Pre-Calculated Filter Coefficients (SciPy Generated)
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

# 7. Deliverables & Verification
- **Outputs to Generate:** Verilog RTL, FIR coefficients, Testbench
- **Testbench Required:** Yes (Target Simulator: QuestaSim)
- **Verification Coverage:** Frequency response, Random input comparison, Throughput verification (Models: Python)
- **Additional Notes:** N/A

# Tasks to Execute:
1. **RTL Implementation:** Write the requested Verilog RTL, FIR coefficients, Testbench using best practices for Intel/Altera FPGAs. Implement the Automatic with Automatic processing. Use the pre-calculated 16-bit fixed-point coefficients provided above.
2. **Data Path & Arithmetic:** Construct the MAC pipeline to prevent intermediate overflow using the Automatic specification. Implement Automatic quantization and Automatic logic at the output stage, taking into account the multiplication by the 32767 scaling factor.
3. **Clocking & Interfaces:** Implement the Automatic protocol using the specified Automatic and Automatic signaling. If Same clock requires separate clocks, safely handle clock domain crossing (CDC) between the 122 MHz system clock and the FIR Processing clock.
4. **Testbench Generation:** Create a self-checking testbench compatible with QuestaSim that stimulates the Automatic and verifies the Frequency response, Random input comparison, Throughput verification.

Ensure the code is fully synthesizable, well-commented, and free of latches or combinational loops.