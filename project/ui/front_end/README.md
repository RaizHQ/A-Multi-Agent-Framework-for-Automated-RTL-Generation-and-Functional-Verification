# FPGA FIR Filter Generator – Questionnaire UI

Files:
- index.html — questionnaire structure
- styles.css — responsive styling
- script.js — conditional questions, progress tracking, and JSON export

Open `index.html` in a browser.

The form currently works as a standalone front-end prototype. On submission it downloads
`fir-design-request.json`. A backend can later consume this JSON and generate MATLAB/Python
filter coefficients, fixed-point parameters, Verilog/VHDL, testbenches, and reports.
