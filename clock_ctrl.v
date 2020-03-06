module clock_ctrl(
    input test_ctl,
    input test_clk,
    input osci_clk,
    input rst_n,

    output int_clk_o,
    output int_clk
);

CLKMUX2X6AR12 CLK_MUX_inst
(
    .I0(osci_clk),
    .I1(test_clk),
    .S(test_ctl),
    .O(int_clk)
);

reg [1:0] cnt;
reg int_clk_o_r;

assign int_clk_o = int_clk_o_r;

always @(posedge int_clk , negedge rst_n) begin
    if (~rst_n) begin
        cnt <= 2'b0;
    end else begin
        cnt <= cnt + 2'b1;
    end
end

always @(posedge int_clk, negedge rst_n) begin
    if (~rst_n) begin
        int_clk_o_r <= 1'b0;
    end else if (cnt == 2'b11) begin
        int_clk_o_r <= ~int_clk_o_r;
    end else begin
        int_clk_o_r <= int_clk_o_r;
    end
end


endmodule // clock_ctrl