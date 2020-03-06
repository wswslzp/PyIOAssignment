(globals 
	version = 3
	io_order = clockwise
	total_edge = 4
)
(iopad 
	(top 
		(inst name = "MDSDUSX16_osci_clk_inst" cell = "MDSDUSX16" ) 
		(inst name = "IO_VCCK_0" cell = "VDD2DGZS" ) 
		(inst name = "IO_GNDK_1" cell = "VSS2DGZS" ) 
		(inst name = "CORE_VCCK_2" cell = "VDD1DGZS" ) 
		(inst name = "CORE_GNDK_3" cell = "VSS1DGZS" ) 
		(inst name = "IO_VCCK_4" cell = "VDD2DGZS" ) 
		(inst name = "IO_GNDK_5" cell = "VSS2DGZS" ) 
		(inst name = "MDSDUSX16_rst_n_inst" cell = "MDSDUSX16" ) 

	) 
	(left 
		(inst name = "MDSDUSX16_test_ctl_inst" cell = "MDSDUSX16" ) 
		(inst name = "IO_VCCK_6" cell = "VDD2DGZS" ) 
		(inst name = "IO_GNDK_7" cell = "VSS2DGZS" ) 
		(inst name = "CORE_VCCK_8" cell = "VDD1DGZS" ) 
		(inst name = "CORE_GNDK_9" cell = "VSS1DGZS" ) 
		(inst name = "IO_VCCK_10" cell = "VDD2DGZS" ) 
		(inst name = "IO_GNDK_11" cell = "VSS2DGZS" ) 
		(inst name = "MDSDUSX16_test_clk_inst" cell = "MDSDUSX16" ) 

	) 
	(right 
		(inst name = "MDSDUSX16_int_clk_o_inst" cell = "MDSDUSX16" ) 
		(inst name = "IO_VCCK_12" cell = "VDD2DGZS" ) 
		(inst name = "IO_GNDK_13" cell = "VSS2DGZS" ) 
		(inst name = "CORE_VCCK_14" cell = "VDD1DGZS" ) 
		(inst name = "CORE_GNDK_15" cell = "VSS1DGZS" ) 
		(inst name = "IO_VCCK_16" cell = "VDD2DGZS" ) 
		(inst name = "IO_GNDK_17" cell = "VSS2DGZS" ) 
		(inst name = "MDSDUSX16_int_clk_inst" cell = "MDSDUSX16" ) 

	) 
	(bottom 
		(inst name = "IO_VCCK_18" cell = "VDD2DGZS" ) 
		(inst name = "IO_GNDK_19" cell = "VSS2DGZS" ) 
		(inst name = "CORE_VCCK_20" cell = "VDD1DGZS" ) 
		(inst name = "CORE_GNDK_21" cell = "VSS1DGZS" ) 
		(inst name = "IO_VCCK_22" cell = "VDD2DGZS" ) 
		(inst name = "IO_GNDK_23" cell = "VSS2DGZS" ) 

	) 
	(topleft 
		(inst name = "TL_CORNER" cell = "MCORNERS" orientation = R270 ) 

	) 
	(topright 
		(inst name = "TR_CORNER" cell = "MCORNERS" orientation = R180 ) 

	) 
	(bottomleft 
		(inst name = "BL_CORNER" cell = "MCORNERS" orientation = R0 ) 

	) 
	(bottomright 
		(inst name = "BR_CORNER" cell = "MCORNERS" orientation = R90 ) 

	) 

)