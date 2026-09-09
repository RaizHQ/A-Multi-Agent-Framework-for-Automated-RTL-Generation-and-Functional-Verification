// 8-Tap Moving Average (Boxcar) FIR Filter
// Standard Verilog-2001 Implementation
// Multiplier-free architecture optimized for FPGA Logic Elements (LUTs)

module fir_boxcar_8tap (
    input  wire        clk,       // System clock
    input  wire        rst_n,     // Active-low asynchronous reset
    input  wire        en,        // Input enable / valid signal
    input  wire [11:0] data_in,   // 12-bit unsigned input sample
    output reg         valid_out, // Output data valid qualifier
    output reg  [11:0] data_out   // 12-bit filtered output sample (>> 3)
);

    // =========================================================================
    // Stage 1: Delay Line (8-tap shift register)
    // =========================================================================
    reg [11:0] tap [0:7];
    integer i;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (i = 0; i < 8; i = i + 1) begin
                tap[i] <= 12'd0;
            end
        end else if (en) begin
            tap[0] <= data_in;
            for (i = 1; i < 8; i = i + 1) begin
                tap[i] <= tap[i - 1];
            end
        end
    end

    // =========================================================================
    // Stage 2: Pipelined Binary Adder Tree
    // =========================================================================
    
    // Adder Tree Level 1: 4 x 13-bit sums (Latency: 1 cycle after tap register)
    reg [12:0] sum_l1_0;
    reg [12:0] sum_l1_1;
    reg [12:0] sum_l1_2;
    reg [12:0] sum_l1_3;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sum_l1_0 <= 13'd0;
            sum_l1_1 <= 13'd0;
            sum_l1_2 <= 13'd0;
            sum_l1_3 <= 13'd0;
        end else if (en) begin
            sum_l1_0 <= {1'b0, tap[0]} + {1'b0, tap[1]};
            sum_l1_1 <= {1'b0, tap[2]} + {1'b0, tap[3]};
            sum_l1_2 <= {1'b0, tap[4]} + {1'b0, tap[5]};
            sum_l1_3 <= {1'b0, tap[6]} + {1'b0, tap[7]};
        end
    end

    // Adder Tree Level 2: 2 x 14-bit sums (Latency: +1 cycle)
    reg [13:0] sum_l2_0;
    reg [13:0] sum_l2_1;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sum_l2_0 <= 14'd0;
            sum_l2_1 <= 14'd0;
        end else if (en) begin
            sum_l2_0 <= {1'b0, sum_l1_0} + {1'b0, sum_l1_1};
            sum_l2_1 <= {1'b0, sum_l1_2} + {1'b0, sum_l1_3};
        end
    end

    // Adder Tree Level 3 & Output Stage: 1 x 15-bit sum / Truncation (Latency: +1 cycle)
    // Division by 8 is achieved via bit slice [14:3]
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            data_out <= 12'd0;
        end else if (en) begin
            data_out <= ({1'b0, sum_l2_0} + {1'b0, sum_l2_1}) >> 3;
        end
    end

    // =========================================================================
    // Pipeline Valid Handshake
    // =========================================================================
    // Total pipeline latency through the adder tree: 3 clock cycles
    reg [2:0] valid_pipe;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            valid_pipe <= 3'b000;
            valid_out  <= 1'b0;
        end else begin
            valid_pipe <= {valid_pipe[1:0], en};
            valid_out  <= valid_pipe[2] & en;
        end
    end

endmodule