translation = {"height":5,
               "width":5,
               "pixels":[0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0,
                        1, 0, 0, 0, 0,
                        0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0]}

identity = {"height":3,
               "width":3,
               "pixels":[0,0,0,
                         0,1,0,
                         0,0,0]}

average = {"height":3,
               "width":3,
               "pixels":[0,0.2,  0,
                         0.2,0.2,0.2,
                         0,0.2,  0]}

gaussian_blur_Kernel = {"height":3,
               "width":3,
               "pixels":[1,2,1,
                         2,4,2,
                         1,2,1]}

edge_detection = {"height":3,
               "width":3,
               "pixels":[-1,-1,-1,
                         -1,8,-1,
                         -1,-1,-1]}


edge_detection_1 = {"height":3,
               "width":3,
               "pixels":[0,-1,0,
                         -1,4,-1,
                         0,-1,0]}

bottom_sobel_filter = {"height":3,
               "width":3,
               "pixels":[-1,-2,-1,
                         0, 0, 0,
                         1,2, 1]}

bottom_sobel_filter = {"height":3,
               "width":3,
               "pixels":[1,2, 1,
                         0, 0, 0,
                         -1,-2,-1]}