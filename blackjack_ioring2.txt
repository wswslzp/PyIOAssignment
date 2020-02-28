############################################################################################
#  IO description file for the BlackJack exercise
#
#  created:
#  09.02.2017 -- Michael Nydegger -- HuCE microLab -- BFH-TI
#  modified:
#  15.12.2017 -- Jonas GROSSENBACHER --HuCE microlab --BFH-TI
#  Note: This file describes the placement of the IO-cells building up the ASIC's IO ring.
#        For Cadence GPDK045
#        The "offset" field corresponds to the y-coorinate of the cells lower border for
#        both the left and right column and the x-coordinate of the cells left border for
#        both the top and bottom row.
#        Instances that do not exist in the source netlist will be created from the celltype
#        given in the "cell" field.
#        To prevent DRC-Errors there are placed spacing cells between the bonding-pads.
#
############################################################################################

(globals
  version = 3
  io_order = default
)
(iopad
  (topright
    (inst name="CORNER1"        cell="padIORINGCORNER"  orientation=R180  )
  )
  (top
    (inst name="IO_FINISHED"	                                ) 
    (inst name="FEED10u1"	cell="padIORINGFEED10"		)
    (inst name="IO_LOST"	                                )
    (inst name="FEED10u2"	cell="padIORINGFEED10"		)
    (inst name="IO_NEWCARD"	                                )
    (inst name="FEED10u3"	cell="padIORINGFEED10"		)
    (inst name="IO_CARDREADY"                                   )
    (inst name="FEED10u4"	cell="padIORINGFEED10"		)
    (inst name="IO_CLK"                                         )
     
  )
  (topleft
    (inst name="CORNER3"        cell="padIORINGCORNER"  orientation=R270 )
  )
  (left
    (inst name="IO_CARDVALUE_0"                   orientation=MX90 )
    (inst name="FEED10u5"	cell="padIORINGFEED10"		)
    (inst name="IO_CARDVALUE_1"                                    )
    (inst name="FEED10u6"	cell="padIORINGFEED10"		)
    (inst name="IO_CARDVALUE_2"                   orientation=MX90 )
    (inst name="FEED10u7"	cell="padIORINGFEED10"		)
    (inst name="IO_CARDVALUE_3"                                    )
    (inst name="FEED10u8"	cell="padIORINGFEED10"		)
    (inst name="IO_START"                         orientation=MX90 )
  )
  (bottomleft
    (inst name="CORNER4"        cell="padIORINGCORNER"  orientation=R0 )
  )
  (bottom
    (inst name="VSS_CORE"       cell="PADVSS"                    )
    (inst name="FEED10u9"	cell="padIORINGFEED10"		)
    (inst name="VDD_CORE"       cell="PADVDD"                    )
    (inst name="FEED10u10"	cell="padIORINGFEED10"		)
    (inst name="VSS_IOR"       cell="PADVSSIOR"                 )
    (inst name="FEED10u11"	cell="padIORINGFEED10"		)
    (inst name="VDD_IOR"       cell="PADVDDIOR"                 )
    (inst name="FEED10u12"	cell="padIORINGFEED10"		)
    (inst name="VDD_BUFFER"     cell="PADVDD25"                 ) 
  

 )
  (bottomright
    (inst name="CORNER2"        cell="padIORINGCORNER"  orientation=R90   )
  )
  (right
    (inst name="IO_SCORE_0"                                     )
    (inst name="FEED10u15"	cell="padIORINGFEED10"		)
    (inst name="IO_SCORE_1"                                     )
    (inst name="FEED10u16"	cell="padIORINGFEED10"		)
    (inst name="IO_SCORE_2"                                     )
    (inst name="FEED10u17"	cell="padIORINGFEED10"		)
    (inst name="IO_SCORE_3"                                     )
    (inst name="FEED10u18"	cell="padIORINGFEED10"		)
    (inst name="IO_SCORE_4"                                     )
  )

)
