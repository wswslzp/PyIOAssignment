( globals
    version = 3
    space = 0
    io_order = default
)

( row_margin
    ( top
        ( io_row ring_number = 1 margin = 0)
        ( io_row ring_number = 2 margin = 630)
        ( io_row ring_number = 3 margin = 830)
    )
    ( bottom
        ( io_row ring_number = 1 margin = 0)
        ( io_row ring_number = 4 margin = 0)
        ( io_row ring_number = 5 margin = 0)
    )
    ( left
        ( io_row ring_number = 1 margin = 0)
        ( io_row ring_number = 6 margin = 200)
        ( io_row ring_number = 7 margin = 0)
    )
    ( right
        ( io_row ring_number = 1 margin = 0)
        ( io_row ring_number = 8 margin = 200)
    )
)

( iopad
    ( topleft
        (locals ring_number = 1)
        ( inst name="ins_0")
    )
    ( left
        ( locals ring_number = 6)
        ( inst name="ins_5" offset = 5896.2 )
        ( inst name="ins_7" space = 5)
        ( inst name="ins_9" place_status = placed)
        ( inst name="ins_10" orientation = R0)
        ( inst name="ins_11" )
        ( inst name="ins_12" )
        ( inst name="ins_14" space = 0)
        ( locals ring_number = 7)
        ( inst name="ins_6" offset = 5826.4 )
        ( inst name="ins_8" )
        ( inst name="ins_13" )
        ( inst name="ins_15" )
        ( inst name="ins_17" )
        ( inst name="ins_19" )
        ( inst name="ins_21" )
        ( inst name="ins_23" )
        ( inst name="ins_25" )
    )
    ( bottomleft
        (locals ring_number = 1)
        ( inst name="ins_1")
    )
    ( bottom
        ( locals ring_number = 4 )
        ( inst name="ins_167" offset = 3946.8)
        ( inst name="ins_168" )
        ( inst name="ins_169" space = 5)
        ( inst name="ins_170" )
        ( inst name="ins_171" )
        ( inst name="ins_172" space = 0)
        ( inst name="ins_173" )
        ( inst name="ins_174" )
        ( inst name="ins_175" )
        ( inst name="ins_176" )
        ( locals ring_number = 5)
        ( inst name="ins_261" offset = 11812.3 )
        ( inst name="ins_262" )
        ( inst name="ins_263" )
        ( inst name="ins_264" )
        ( inst name="ins_265" )
        ( inst name="ins_266" )
        ( inst name="ins_267" )
    )
    ( bottomright
        (locals ring_number = 1)
        ( inst name="ins_2" orientation=R0 )
    )
    ( right
        ( locals ring_number = 8 )
        ( inst name="ins_313" offset = 200 )
        ( inst name="ins_315" )
        ( inst name="ins_316" )
        ( inst name="ins_318" )
        ( inst name="ins_320" )
        ( inst name="ins_322" )
        ( inst name="ins_324" )
        ( inst name="ins_326" )
        ( inst name="ins_328" )
        ( inst name="ins_330" )
        ( inst name="ins_332" )
        ( inst name="ins_334" )
        ( inst name="ins_336" )
        ( inst name="ins_337" )
        ( inst name="ins_338" )
        ( inst name="ins_339" )
        ( inst name="ins_341" )
        ( inst name="ins_343" )
        ( inst name="ins_344" )
    )
    ( topright
        (locals ring_number = 1)
        ( inst name="ins_3")
    )
    ( top
        ( locals ring_number = 2 )
        ( inst name="ins_610" offset = 100 )
        ( locals ring_number = 3)
        ( inst name="ins_611" offset = 200 )
        ( inst name="ins_612" )
        ( inst name="ins_614" )
        ( inst name="ins_616" )
        ( inst name="ins_617" )
        ( inst name="ins_619" )
    )
)

(iopin
    (top | north | edge num = 0
        (locals
            space = 1.2
        )
        (pin name = address[14] N
            layer = 3
            width = 0.28
            depth = 0.28
            offset = 19.4700
            place_status = fixed
        )
        (pin name = address[14] N
            layer = 4
            width = 0.38
            depth = 0.38
            offset = 39.2700
            place_status = fixed
        )
    )
)