from utils.utils import line_resize, poly
THRESHOLD_SPEED = 4
DISTANCE = 10

# LINE1 = [[220, 455], [242, 480], [350, 489], [325, 455]]
LINE2 = [[253, 490], [253, 494], [351, 494], [351, 490]]
LINE3 = [[272, 516], [272, 520], [391, 520], [391, 516]]
LINE4 = [[300, 546], [300, 550], [440, 550], [440, 546]]
LINE5 = [[345, 595], [345, 599], [506, 599], [506, 595]]
LINE6 = [[398, 650], [398, 659], [590, 659], [590, 650]]

LINE7 = [[477, 727], [477, 731], [712, 731], [712, 727]]

# POLY1 = [220,455,251,488,349,488,295,455]
POLY2 = [253,490,270,514,389,514,351,490]
POLY3 = [272,516,298,544,438,544,391,516]
POLY4 = [300,546,343,593,504,593,440,546]
POLY5 = [345,595,396,648,588,648,506,595]
POLY6 = [398,650,475,725,710,725,590,650]
POLY7 = [477,727,480,735,715,735,712,727]


# line1_value = line_resize(LINE1)
line2_value = line_resize(LINE2)
line3_value = line_resize(LINE3)
line4_value = line_resize(LINE4)
line5_value = line_resize(LINE5)
line6_value = line_resize(LINE6)
line7_value = line_resize(LINE7)

# poly1 = poly(POLY1)
poly2 = poly(POLY2)
poly3 = poly(POLY3)
poly4 = poly(POLY4)
poly5 = poly(POLY5)
poly6 = poly(POLY6)
poly7 = poly(POLY7)
