"""Original editorial artwork. Pillow + the URW Base35 fonts are build-time only."""
from functools import lru_cache
from math import cos, pi, sin
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

S = 3
SIZE = 1024
PAPER, INK, CORAL = '#faf2df', '#172826', '#ff805b'
CREAM, TEAL, GOLD = '#fff2d4', '#20544e', '#f5b941'
SERIF, SANS, BOLD = 'NimbusRoman-Bold', 'NimbusSans-Regular', 'NimbusSans-Bold'
FONT_DIR = Path('/usr/share/fonts/opentype/urw-base35')
canvas = Image.new('RGB', (SIZE * S, SIZE * S), PAPER)
d = ImageDraw.Draw(canvas)


@lru_cache(maxsize=None)
def font(face, size):
    return ImageFont.truetype(str(FONT_DIR / f'{face}.otf'), size * S)


def coords(*numbers):
    return tuple(round(n * S) for n in numbers)


def box(x, y, w, h, fill):
    d.rectangle(coords(x, y, x + w, y + h), fill=fill)


def disk(x, y, r, fill, outline=None, width=1):
    d.ellipse(coords(x-r, y-r, x+r, y+r), fill=fill, outline=outline, width=width*S)


def poly(points, color):
    d.polygon([coords(x, y) for x, y in points], fill=color)


def pen(points, color, width=1):
    d.line([coords(x, y) for x, y in points], fill=color, width=width*S, joint='curve')


def text(x, y, value, size, face=BOLD, fill=INK, anchor='ls', fit=None):
    f = font(face, size)
    while fit is not None and f.getlength(value) > fit*S:
        size -= 1
        f = font(face, size)
    d.text(coords(x, y), value, font=f, fill=fill, anchor=anchor)


def orbit(x, y, width, height, color, start, end, weight=2):
    d.arc(coords(x, y, x+width, y+height), start, end, fill=color, width=weight*S)


def star(x, y, r, fill, points=4):
    poly([(x + cos(i*pi/points-pi/2)*r*(1 if i%2==0 else .26),
           y + sin(i*pi/points-pi/2)*r*(1 if i%2==0 else .26))
          for i in range(2*points)], fill)


def print_mark(x, y):
    disk(x, y, 16, None, INK, 2)
    d.ellipse(coords(x-7, y-16, x+7, y+16), outline=INK, width=2*S)
    pen([(x-16, y), (x+16, y)], INK, 2)


def masthead():
    print_mark(57, 46)
    text(87, 53, 'THE ILLUSTRATED DAILY', 25)
    text(39, 135, 'World Desk', 105, SERIF)
    pen([(722, 36), (722, 132)], '#9a9881', 1)
    text(984, 60, 'TUESDAY  /  2026', 26, BOLD, INK, 'rs')
    text(986, 127, '24 NOV', 69, SERIF, INK, 'rs')


def city():
    # A symbolic street elevation, not a reconstruction of the strike site.
    night, wall, side, shadow = '#172c3a', '#477487', '#26495e', '#0b2231'
    box(40, 155, 944, 229, night)
    sun_x, sun_y = 787, 265
    disk(sun_x, sun_y, 92, '#294a55')
    disk(sun_x, sun_y, 79, None, '#6d9191', 1)
    for xx, yy, rr in [(655, 196, 6), (910, 216, 7), (946, 250, 4), (690, 180, 3), (889, 182, 4)]:
        star(xx, yy, rr, '#bed0c3')
    for i, (x, y, w) in enumerate([(636, 300, 62), (691, 281, 38), (838, 274, 63), (899, 307, 53)]):
        box(x, y, w, 365-y, ['#325464', '#274552'][i%2])
        for xx in range(x+8, x+w-6, 13):
            for yy in range(y+9, 351, 15):
                if (xx+yy)%4:
                    box(xx, yy, 4, 5, '#719491')
    poly([(712, 245), (745, 222), (775, 228), (803, 216), (844, 229), (860, 247), (839, 361), (712, 361)], wall)
    poly([(844, 229), (866, 240), (888, 253), (885, 358), (839, 361)], side)
    for row in range(5):
        yy = 250 + row*20
        for col in range(6):
            xx = 723 + 19*col
            box(xx, yy, 11, 11, GOLD if (row*7+col)%5 in (1, 2) else shadow)
        for xx in (851, 868):
            box(xx, yy+3, 7, 8, shadow)
    poly([(774, 225), (811, 218), (807, 246), (794, 250), (803, 267), (787, 267), (790, 283), (778, 278), (766, 292), (768, 268), (758, 249)], night)
    for x, y, r in [(777, 259, 4), (806, 290, 3), (763, 285, 3), (790, 301, 4)]:
        star(x, y, r, CORAL)
    poly([(622, 367), (659, 351), (701, 364), (730, 351), (751, 364), (789, 354),
          (826, 367), (884, 359), (921, 366), (961, 357), (984, 365), (984, 384), (622, 384)], shadow)
    box(62, 182, 38, 4, CORAL)
    text(111, 192, 'UKRAINE  /  WAR', 23, BOLD, '#ffad89')
    text(62, 253, 'Strike toll rises', 59, SERIF, CREAM)
    text(62, 310, 'in Zaporizhzhia', 64, SERIF, CREAM)
    text(64, 357, 'Russian attack: 2 killed, 48 wounded', 31, SANS, CREAM)


def chip(x, y):
    disk(x, y, 63, '#f2ca87')
    for zz in range(-24, 26, 12):
        pen([(x+zz, y-34), (x+zz, y-51)], INK, 4)
        pen([(x+zz, y+34), (x+zz, y+51)], INK, 4)
        pen([(x-34, y+zz), (x-51, y+zz)], INK, 4)
        pen([(x+34, y+zz), (x+51, y+zz)], INK, 4)
    box(x-35, y-35, 70, 70, INK)
    box(x-27, y-27, 54, 54, '#ad4a36')
    # The balanced scales distinguish a verdict from a product announcement.
    pen([(x-20, y-9), (x+20, y-9)], CREAM, 3)
    pen([(x, y-17), (x, y+17)], CREAM, 4)
    pen([(x-10, y+17), (x+10, y+17)], CREAM, 3)
    for side in (-1, 1):
        a = x + side*14
        poly([(a,y-8), (a-9,y+9), (a+9,y+9)], CREAM)


def strait(x, y):
    disk(x, y, 63, '#c1d8c5')
    for i in range(5):
        yy = y+24+i*6
        pen([(x-44+i*5, yy), (x+44-i*5, yy)], '#4b8177', 2)
    poly([(x-49, y+12), (x-28, y+29), (x+37,y+29), (x+53,y+11)], TEAL)
    box(x-29, y-4, 22, 13, '#c2583e')
    box(x-5, y-4, 23, 13, '#dea746')
    box(x-29, y-19, 22, 13, '#daa03d')
    box(x+20, y-12, 22, 21, CREAM)
    box(x+26, y-22, 5, 10, TEAL)
    pen([(x-38, y-13), (x-38, y-43)], TEAL, 3)
    poly([(x-38,y-43), (x-12,y-37), (x-38,y-31)], '#ba513c')


def helmet(x, y):
    disk(x, y, 63, '#203c51')
    for dx, dy in [(-42, -26), (40, -29), (51, 2), (-48, 17)]:
        star(x+dx, y+dy, 5, '#e8ba6a')
    orbit(x-53, y+11, 106, 32, '#658996', 12, 170)
    poly([(x-44,y+41),(x-35,y+25),(x+35,y+25),(x+44,y+41)], '#adc4bc')
    disk(x, y-4, 36, CREAM)
    d.rounded_rectangle(coords(x-29, y-24, x+29, y+12), radius=15*S, fill='#3d687b')
    poly([(x-21,y-16), (x-5,y-19), (x-13,y+5), (x-23,y+3)], '#a6c2c4')
    box(x-22, y+30, 44, 6, '#c75540')


def medic(x, y):
    disk(x, y, 63, '#edd6b5')
    for i, w in enumerate((74, 93, 100, 101, 90)):
        yy = y+29+i*5
        pen([(x-w/2, yy), (x+w/2, yy)], '#bd987c', 1)
    poly([(x-51,y-15),(x+12,y-15),(x+12,y-7),(x+34,y-7),
          (x+50,y+10),(x+50,y+26),(x-51,y+26)], TEAL)
    poly([(x+19,y-2),(x+32,y-2),(x+43,y+11),(x+19,y+11)], '#b1d3c7')
    disk(x-31,y+24,11,INK)
    disk(x+32,y+24,11,INK)
    disk(x-31,y+24,4,CREAM)
    disk(x+32,y+24,4,CREAM)
    box(x-29,y-8,9,26,CREAM)
    box(x-37,y,25,9,CREAM)
    for offset in (0, 7, 14):
        pen([(x-22+offset,y-23-offset//3), (x-25+offset,y-32-offset//3)], '#b85e47', 2)


def cup(x, y):
    disk(x, y, 63, '#d7e4c2')
    orbit(x-41,y-28,34,34,TEAL,55,280,5)
    orbit(x+7,y-28,34,34,TEAL,270,125,5)
    poly([(x-27,y-35),(x+27,y-35),(x+19,y-5),(x+11,y+6),
          (x+5,y+12),(x+5,y+27),(x+22,y+34),(x-22,y+34),
          (x-5,y+27),(x-5,y+12),(x-15,y+5),(x-21,y-7)], '#b87524')
    poly([(x-26,y-34),(x+13,y-34),(x+9,y-8),(x+2,y+8),(x-9,y+7),(x-19,y-7)], GOLD)
    star(x, y-17, 11, CREAM, 5)
    box(x-25,y+34,50,9,TEAL)


def accord(x, y):
    disk(x, y, 63, '#efc8b3')
    poly([(x-47,y-22),(x-3,y-40),(x+29,y-15),(x+20,y+38),(x-20,y+48)], '#a04e40')
    poly([(x-40,y-20),(x-3,y-34),(x+22,y-14),(x+13,y+33),(x-16,y+40)], CREAM)
    poly([(x-3,y-34),(x+22,y-14),(x+1,y-10)], '#dcc6a2')
    pen([(x-29,y-9),(x-9,y-16)], '#666958', 2)
    pen([(x-25,y+1),(x+12,y-10)], '#666958', 2)
    pen([(x-22,y+11),(x+5,y+3)], '#666958', 2)
    pen([(x-17,y+25),(x-12,y+17),(x-8,y+22),(x-2,y+14),(x+3,y+16)], TEAL, 2)
    poly([(x+0,y+29),(x+6,y+14),(x+38,y-27),(x+47,y-20),(x+16,y+20)], TEAL)
    poly([(x+0,y+29),(x+6,y+14),(x+16,y+20)], '#b97d3d')


STORIES = [
    ('U.S. / CHINA', ('Huawei found', 'guilty in U.S.'), ('Iran sanctions violations', 'and bank fraud'), chip),
    ('YEMEN', ('UK sanctions', 'the Houthis'), ('Group and 4 officials', 'targeted after attacks'), strait),
    ('CHINA / PAKISTAN', ('Shenzhou-24', 'crew unveiled'), ('Ali set to be Tiangong’s', 'first foreign astronaut'), helmet),
    ('DR CONGO', ('Ebola team', 'evacuated'), ('WHO, local staff leave', 'Akwe amid fighting'), medic),
    ('SENEGAL / MOROCCO', ('Senegal regains', 'AFCON title'), ('Sports court reinstates', '2025 tournament win'), cup),
    ('COLOMBIA', ('FARC peace deal', 'turns 10'), ('UN urges Colombia to', 'carry out the full accord'), accord),
]


def briefing():
    gutter = '#bfbbaa'
    pen([(512, 404), (512, 959)], gutter)
    for i, (region, title, summary, illustration) in enumerate(STORIES):
        x, y = 42+(i%2)*489, 410+(i//2)*188
        text(x, y+18, region, 23, BOLD, TEAL)
        illustration(x+388, y+80)
        for j, line in enumerate(title):
            text(x, y+62+j*42, line, 42, BOLD, fit=313)
        for j, line in enumerate(summary):
            text(x, y+138+j*27, line, 26, SANS, fit=316)
        if i%2 == 0 and i < 4:
            pen([(42, y+178), (982, y+178)], gutter)
    pen([(42, 975), (982, 975)], INK, 2)
    text(42, 1002, '24 NOVEMBER 2026', 19, BOLD, TEAL)
    text(982, 1002, 'ORIGINAL EDITORIAL ILLUSTRATIONS', 19, BOLD, TEAL, 'rs')


if __name__ == '__main__':
    masthead()
    city()
    briefing()
    output = Path(__file__).with_name('entry.png')
    canvas.resize((SIZE, SIZE), Image.Resampling.LANCZOS).save(output, optimize=True)
