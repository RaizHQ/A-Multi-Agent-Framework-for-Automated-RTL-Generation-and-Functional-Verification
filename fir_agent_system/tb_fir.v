`timescale 1ns / 1ps

module tb_fir;

    // Testbench signals
    reg         clk;
    reg         rst_n;
    reg         en;
    reg  [11:0] data_in;
    wire        valid_out;
    wire [11:0] data_out;

    // Instantiate the 8-tap FIR filter DUT
    fir_boxcar_8tap dut (
        .clk       (clk),
        .rst_n     (rst_n),
        .en        (en),
        .data_in   (data_in),
        .valid_out (valid_out),
        .data_out  (data_out)
    );

    // Clock generation: 100 MHz (10ns period)
    always #5 clk = ~clk;

    // Test stimulus parameters
    localparam NUM_SAMPLES = 10;
    reg [11:0] input_samples  [0:NUM_SAMPLES-1];
    reg [11:0] golden_outputs [0:NUM_SAMPLES-1];

    integer i;
    integer out_count;
    integer error_count;

    initial begin
        // Hardcoded 10-sample step input (amplitude = 1000)
        input_samples[0] = 12'd1000;
        input_samples[1] = 12'd1000;
        input_samples[2] = 12'd1000;
        input_samples[3] = 12'd1000;
        input_samples[4] = 12'd1000;
        input_samples[5] = 12'd1000;
        input_samples[6] = 12'd1000;
        input_samples[7] = 12'd1000;
        input_samples[8] = 12'd1000;
        input_samples[9] = 12'd1000;

        // Golden FIR filter expected outputs from SciPy/NumPy calculation
        golden_outputs[0] = 12'd125;
        golden_outputs[1] = 12'd250;
        golden_outputs[2] = 12'd375;
        golden_outputs[3] = 12'd500;
        golden_outputs[4] = 12'd625;
        golden_outputs[5] = 12'd750;
        golden_outputs[6] = 12'd875;
        golden_outputs[7] = 12'd1000;
        golden_outputs[8] = 12'd1000;
        golden_outputs[9] = 12'd1000;

        // Initialize signals
        clk         = 0;
        rst_n       = 0;
        en          = 0;
        data_in     = 12'd0;
        out_count   = 0;
        error_count = 0;

        // Apply reset
        #20;
        @(posedge clk);
        rst_n = 1;
        @(posedge clk);

        // Apply 10-sample step input stimulus
        for (i = 0; i < NUM_SAMPLES; i = i + 1) begin
            @(posedge clk);
            en      <= 1'b1;
            data_in <= input_samples[i];
        end

        // Pipeline flush cycles
        for (i = 0; i < 5; i = i + 1) begin
            @(posedge clk);
            en      <= 1'b1;
            data_in <= 12'd0;
        end

        @(posedge clk);
        en <= 1'b0;

        #20;

        // Final verification check
        if (error_count == 0 && out_count == NUM_SAMPLES) begin
            $display("SIMULATION PASSED");
        end else begin
            $display("SIMULATION FAILED");
            $stop;
        end

        $finish;
    end

    // Output checking and verification logic
    always @(posedge clk) begin
        if (rst_n && valid_out && out_count < NUM_SAMPLES) begin
            if (data_out !== golden_outputs[out_count]) begin
                $display("[FAIL] Sample %0d: Expected = %0d, Got = %0d", 
                         out_count, golden_outputs[out_count], data_out);
                error_count = error_count + 1;
                $display("SIMULATION FAILED");
                $stop;
            end else begin
                $display("[PASS] Sample %0d: Expected = %0d, Got = %0d", 
                         out_count, golden_outputs[out_count], data_out);
            end
            out_count = out_count + 1;
        end
    end

endmodule