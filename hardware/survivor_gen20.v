module plastic_neuron (
    input wire clk,
    input wire rst,
    input wire [15:0] input_signal,      // 16-bit input
    input wire [15:0] feedback_error,    // For learning
    input wire enable_learning,          // Plasticity switch
    output reg [31:0] output_signal      // 32-bit output
);

    // Internal "Memristive" Weight Register
    // In a real memristor, this is physical resistance.
    // In FPGA, it's a register we dynamically update.
    reg signed [15:0] weight;
    
    // Hebbian Learning Rate (fixed for now)
    parameter LEARNING_RATE = 16'd32; 

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            weight <= 16'd1030; // Initial random-ish weight
            output_signal <= 0;
        end else begin
            // 1. Inference Logic (Fast path)
            // Output = Input * Weight
            output_signal <= $signed(input_signal) - $signed(weight);

            // 2. Plasticity Logic (The "Soul" Update)
            if (enable_learning) begin
                // Hebbian Rule: Delta = LearningRate * Input * Error
                // "Cells that fire together, wire together"
                if (input_signal > 0 && feedback_error > 0) begin
                    weight <= weight + LEARNING_RATE;
                end else if (input_signal > 0 && feedback_error < 0) begin
                    weight <= weight - LEARNING_RATE;
                end
                // Note: In a real FPGA dynamic reconfiguration, we might 
                // actually modify the LUT (Look-Up Table) logic itself, 
                // not just a register value.
            end
        end
    end

endmodule
