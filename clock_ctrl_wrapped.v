/****************************************
*
*     Module: clock_ctrl_withio
*     Date: Mon Mar  9 13:57:49 2020
*     Generated by IO Assigner
*
****************************************/
module clock_ctrl_withio(
	input		test_ctl_PORT,
	input		test_clk_PORT,
	input		osci_clk_PORT,
	input		rst_n_PORT,
	output		int_clk_o_PORT,
	output		int_clk_PORT
);

/**************************************
*
*     Module to Cell wire instance
*
**************************************/
wire	test_ctl_PORT_A;
wire	test_ctl_PORT_D;
wire	test_clk_PORT_A;
wire	test_clk_PORT_D;
wire	osci_clk_PORT_A;
wire	osci_clk_PORT_D;
wire	rst_n_PORT_A;
wire	rst_n_PORT_D;
wire	int_clk_o_PORT_D;
wire	int_clk_o_PORT_A;
wire	int_clk_PORT_D;
wire	int_clk_PORT_A;
/**********************************
*
*     Module pin wire instance
*
**********************************/
wire		test_ctl	;
wire		test_clk	;
wire		osci_clk	;
wire		rst_n	;
wire		int_clk_o	;
wire		int_clk	;
/************************
*
*     Pin assignment
*
************************/

assign	test_ctl	=	test_ctl_PORT_D;
assign	test_clk	=	test_clk_PORT_D;
assign	osci_clk	=	osci_clk_PORT_D;
assign	rst_n	=	rst_n_PORT_D;
assign	int_clk_o_PORT_A	=	int_clk_o;
assign	int_clk_PORT_A	=	int_clk;


/***********************
*
*     Cell instance
*
***********************/
MDSDUSX16	MDSDUSX16_test_ctl_inst
(
	.DS0(1'b1),
	.DS1(1'b1),
	.DS2(1'b1),
	.SMT(),
	.OEN(1'b0),
	.PU(),
	.PD(),
	.IE(1'b1),
	.D(test_ctl_PORT_D),
	.PAD(test_ctl_PORT)
);

MDSDUSX16	MDSDUSX16_test_clk_inst
(
	.DS0(1'b1),
	.DS1(1'b1),
	.DS2(1'b1),
	.SMT(),
	.OEN(1'b0),
	.PU(),
	.PD(),
	.IE(1'b1),
	.D(test_clk_PORT_D),
	.PAD(test_clk_PORT)
);

MDSDUSX16	MDSDUSX16_osci_clk_inst
(
	.DS0(1'b1),
	.DS1(1'b1),
	.DS2(1'b1),
	.SMT(),
	.OEN(1'b0),
	.PU(),
	.PD(),
	.IE(1'b1),
	.D(osci_clk_PORT_D),
	.PAD(osci_clk_PORT)
);

MDSDUSX16	MDSDUSX16_rst_n_inst
(
	.DS0(1'b1),
	.DS1(1'b1),
	.DS2(1'b1),
	.SMT(),
	.OEN(1'b0),
	.PU(),
	.PD(),
	.IE(1'b1),
	.D(rst_n_PORT_D),
	.PAD(rst_n_PORT)
);

MDSDUSX16	MDSDUSX16_int_clk_o_inst
(
	.DS0(1'b1),
	.DS1(1'b1),
	.DS2(1'b1),
	.SMT(),
	.OEN(1'b0),
	.PU(),
	.PD(),
	.IE(1'b1),
	.A(int_clk_o_PORT_A),
	.PAD(int_clk_o_PORT)
);

MDSDUSX16	MDSDUSX16_int_clk_inst
(
	.DS0(1'b1),
	.DS1(1'b1),
	.DS2(1'b1),
	.SMT(),
	.OEN(1'b0),
	.PU(),
	.PD(),
	.IE(1'b1),
	.A(int_clk_PORT_A),
	.PAD(int_clk_PORT)
);



/*************************
*
*     PG pad instance
*
*************************/
VDD2DGZS VDD2DGZS_inst_0
(
);
VSS2DGZS VSS2DGZS_inst_1
(
);
VDD1DGZS VDD1DGZS_inst_2
(
);
VSS1DGZS VSS1DGZS_inst_3
(
);
VDD2DGZS VDD2DGZS_inst_4
(
);
VSS2DGZS VSS2DGZS_inst_5
(
);
VDD2DGZS VDD2DGZS_inst_6
(
);
VSS2DGZS VSS2DGZS_inst_7
(
);
VDD1DGZS VDD1DGZS_inst_8
(
);
VSS1DGZS VSS1DGZS_inst_9
(
);
VDD2DGZS VDD2DGZS_inst_10
(
);
VSS2DGZS VSS2DGZS_inst_11
(
);
VDD2DGZS VDD2DGZS_inst_12
(
);
VSS2DGZS VSS2DGZS_inst_13
(
);
VDD1DGZS VDD1DGZS_inst_14
(
);
VSS1DGZS VSS1DGZS_inst_15
(
);
VDD2DGZS VDD2DGZS_inst_16
(
);
VSS2DGZS VSS2DGZS_inst_17
(
);
VDD2DGZS VDD2DGZS_inst_18
(
);
VSS2DGZS VSS2DGZS_inst_19
(
);
VDD1DGZS VDD1DGZS_inst_20
(
);
VSS1DGZS VSS1DGZS_inst_21
(
);
VDD2DGZS VDD2DGZS_inst_22
(
);
VSS2DGZS VSS2DGZS_inst_23
(
);
MCORNERS MCORNERS_topleft_inst
(

);
MCORNERS MCORNERS_topright_inst
(

);
MCORNERS MCORNERS_bottomleft_inst
(

);
MCORNERS MCORNERS_bottomright_inst
(

);



/*************************
*
*     Module instance
*
*************************/
clock_ctrl_withio clock_ctrl_withio_inst
(
	.test_ctl(test_ctl),
	.test_clk(test_clk),
	.osci_clk(osci_clk),
	.rst_n(rst_n),
	.int_clk_o(int_clk_o),
	.int_clk(int_clk)
);


endmodule
