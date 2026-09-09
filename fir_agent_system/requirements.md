# FIR Filter Specification Document

## Important!
* **Language:** Verilog-2001
* **Critical:** Do not use system verilog. Do not use any other HDL.
* **FPGA:** ALTERA Cyclone II EP2C5T144

## 1. Filter Application & Type
* **Application:** Smoothing raw digital sensor data in real-time embedded systems.
* **Filter Type:** 8-tap Moving Average Low-pass filter.
* **Phase Characteristic:** Linear phase achieved through symmetric coefficients.

## 2. Data Format & Bit-Widths
* **Input Data:** 12-bit unsigned integer raw samples.
* **Coefficients:** 8 static taps, all conceptually equal to $1/8$.
* **Internal Accumulator:** 15-bit unsigned register to accommodate 3 growth bits and prevent overflow during summation.
* **Output Data:** 12-bit unsigned integer truncated output.

## 3. Hardware Architecture Constraints
* **Multiplier-Free Logic:** The design must use zero DSP multiplier slices; the division by 8 must be implemented as a logical right-shift by 3 bits (`>>> 3`).
* **Architecture Style:** Fully parallel pipeline utilizing a shift register (delay line) to process multiple computations simultaneously.
* **Latency:** The filter operation will divide into sequential stages, causing a calculated number of clock cycle delays between the input raw sample and the corresponding processed output.

## 4. System Interface Signals
* **Clocking (`clk`):** 1:1 System clock to sample rate (e.g., 100 MHz), where one raw sample enters and one filtered sample exits on every active clock edge.
* **Reset (`rst`):** An initialization signal (active-high or active-low) to clear all internal shift registers and the accumulator to 0 before the filter starts responding to input.
* **Data Valid:** Handshake signals to identify when input data is ready and when the output pipeline contains valid filtered data.
