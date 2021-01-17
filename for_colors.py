import colorsys
ranges = {'red': [range(20), range(341, 361)], 'orange': [range(21, 41)],
          'yellow': [range(41, 81)], 'poisonous-green': [range(81, 101)],
          'green': [range(101, 141)], 'aquamarine': [range(141, 161)],
          'turquoise': [range(161, 201)], 'light-blue': [range(201, 221)],
          'blue': [range(221, 261)], 'violet': [range(261, 281)],
          'magenta': [range(281, 320)], 'fuchsia': [range(321, 341)]}
v = 50


def func_area2(area, f, s, t, v, main_color):
    '''
    исходя из показателя флага определяем, по какой формуле цвет сдвигается
    по цветовому кругу
    '''
    if area == 'red':
        f_c, s_c = (f, s, t + v), (f, s + v, t)
    elif area == 'orange':
        f_c, s_c = (f, s - v, t), (f, s + v, t)
    elif area == 'yellow':
        f_c, s_c = (f, s - v, t), (f - v, s, t)
    elif area == 'poisonous-green':
        f_c, s_c = (f + v, s, t), (f - v, s, t)
    elif area == 'green':
        f_c, s_c = (f + v, s, t), (f, s, t + v)
    elif area == 'aquamarine':
        f_c, s_c = (f, s, t - v), (f, s, t + v)
    elif area == 'turquoise':
        f_c, s_c = (f, s - v, t), (f, s, t - v)
    elif area == 'light-blue':
        f_c, s_c = (f, s + v, t), (f, s - v, t)
    elif area == 'blue':
        f_c, s_c = (f + v, s, t), (f, s + v, t)
    elif area == 'violet':
        f_c, s_c = (f + v, s, t), (f - v, s, t)
    elif area == 'magenta':
        f_c, s_c = (f, s, t - v), (f - v, s, t)
    elif area == 'fuchsia':
        f_c, s_c = (f, s, t + v), (f, s, t - v)
    else:
        # если цвет является полностью белым или черным
        f_c, s_c = main_color, main_color
    return [f_c, s_c]


def func_for_analog(f_orig, s_orig):
    # устранение ошибок
    f_orig, s_orig = list(f_orig), list(s_orig)
    for i in range(3):
        if f_orig[i] > 255:
            f_orig[i] = 255
        elif f_orig[i] < 0:
            f_orig[i] = 0

        if s_orig[i] > 255:
            s_orig[i] = 255
        elif s_orig[i] < 0:
            s_orig[i] = 0
    return [tuple(f_orig), tuple(s_orig)] # чтобы преобразовать в hex: '#' + '%02x%02x%02x' % i


def rngs(hue, saturation, value):
    flag = ''
    for key, value2 in ranges.items():
        for i in value2:
            if hue in i:
                if value != 0:
                    flag = key
                elif hue == 0 and saturation == 0 and value == 25500:
                    flag = 'white'
                else:
                    flag = 'black'
    return flag


def defining_color_area(f, s, t):
    hsv = colorsys.rgb_to_hsv(f, s, t)
    hue, saturation, value = hsv
    hue, saturation, value = hue * 360, saturation * 100, value * 100

    flag = rngs(hue, saturation, value)
    if flag == '':
        hue = int(round(hue))
        flag = rngs(hue, saturation, value)
    return flag
