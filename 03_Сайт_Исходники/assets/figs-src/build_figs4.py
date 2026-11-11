#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Иллюстрации вместо микрофотографий + схемы двух новых статей."""

import os, re, sys
import cairosvg

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_figs3 import (C, T, B, S, M, marker, svg, panel, esc)

OUT = os.path.dirname(os.path.abspath(__file__))

DARK = "#131A16"
DARK2 = "#1B241E"


# =====================================================================
# KZ1 · КЛЕТКИ ПОД ФЛУОРЕСЦЕНТНЫМ МИКРОСКОПОМ (иллюстрация)
# =====================================================================
def kz_fluorescence():
    W, H = 940, 600

    defs = '''
    <radialGradient id="kzGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#8FD9A8" stop-opacity=".55"/>
      <stop offset="60%" stop-color="#4E9E76" stop-opacity=".22"/>
      <stop offset="100%" stop-color="#2A5A44" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="kzNuc" cx="40%" cy="35%" r="60%">
      <stop offset="0" stop-color="#A9C8FF"/><stop offset="100%" stop-color="#4C6FD1"/></radialGradient>
    <filter id="kzBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="6"/></filter>
    '''

    cells = [
        (150, 170, 78, 0.06), (330, 130, 66, 0.10), (520, 168, 84, 0.14),
        (720, 128, 70, 0.18), (200, 330, 88, 0.24), (420, 296, 74, 0.30),
        (610, 330, 92, 0.35), (790, 268, 66, 0.40), (280, 470, 72, 0.46),
        (500, 470, 84, 0.50), (700, 470, 76, 0.55),
    ]

    o = []
    o.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="16" fill="{DARK}"/>')
    # лёгкая текстура фона
    for i in range(26):
        x = 40 + (i * 137) % 860
        y = 30 + (i * 211) % 540
        o.append(f'<circle cx="{x}" cy="{y}" r="2" fill="#2E4438" opacity=".5"/>')

    for cx, cy, r, at in cells:
        o.append(f'<g data-at="{at}">')
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r*1.25}" fill="url(#kzGlow)"/>')
        # тело клетки — неровный овал
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r*0.72}" ry="{r*0.56}" fill="#3E7A5C" '
                 f'opacity=".28" stroke="#6FBF92" stroke-width="1.1"/>')
        # отростки
        for ang, ln in ((-40, r*0.9), (35, r*0.8), (150, r*0.75), (215, r*0.85)):
            import math
            a = math.radians(ang)
            x2 = cx + math.cos(a) * ln
            y2 = cy + math.sin(a) * ln * 0.7
            o.append(f'<path d="M{cx},{cy} Q{(cx+x2)/2 + 6},{(cy+y2)/2 - 8} {x2:.0f},{y2:.0f}" '
                     f'fill="none" stroke="#63B98A" stroke-width="1.6" opacity=".75"/>')
        # ядро
        o.append(f'<ellipse cx="{cx-3}" cy="{cy-2}" rx="{r*0.26}" ry="{r*0.22}" fill="url(#kzNuc)"/>')
        o.append('</g>')

    # подписи
    o.append(f'<g data-at="0.66">{M(46, 40, "ИЛЛЮСТРАЦИЯ · ФЛУОРЕСЦЕНТНАЯ МИКРОСКОПИЯ — СХЕМА, А НЕ СНИМОК", 8.5, fill="#7FBFA0")}</g>')
    o.append(f'<g data-at="0.70"><line x1="188" y1="176" x2="250" y2="212" stroke="#7FBFA0" '
             f'stroke-width="1" stroke-dasharray="3 3"/>'
             f'{M(258, 216, "ЯДРО КЛЕТКИ", 8.5, fill="#BBD9EE")}</g>')
    o.append(f'<g data-at="0.74"><line x1="404" y1="352" x2="356" y2="400" stroke="#7FBFA0" '
             f'stroke-width="1" stroke-dasharray="3 3"/>'
             f'{M(268, 406, "ОТРОСТКИ — КАРКАС", 8.5, fill="#BBD9EE")}</g>')
    o.append(f'<g data-at="0.78"><line x1="612" y1="374" x2="660" y2="412" stroke="#7FBFA0" '
             f'stroke-width="1" stroke-dasharray="3 3"/>'
             f'{M(668, 418, "КОЛОНИЯ КЛЕТОК", 8.5, fill="#BBD9EE")}</g>')

    o.append(f'<g data-at="0.84">{S(46, 556, "Так клетки выглядели бы под микроскопом: зелёный цитоскелет держит форму, "
                                            "синее ядро хранит программу.", 10, fill="#9FC4B2")}</g>')
    return svg(W, H, "".join(o), defs)


# =====================================================================
# KZ2 · КЛЕТКИ НА КОЛЛАГЕНОВОЙ СЕТИ (иллюстрация)
# =====================================================================
def kz_sem():
    W, H = 940, 520

    defs = '''
    <linearGradient id="kzFiber" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#E3D6C0"/><stop offset="1" stop-color="#CBBBA0"/></linearGradient>
    <linearGradient id="kzCell" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F0CDB9"/><stop offset="1" stop-color="#D9A98F"/></linearGradient>
    '''

    o = []
    o.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="16" fill="#F4F1E9"/>')

    # коллагеновые волокна
    fibers = [
        "M40,140 C220,96 420,180 640,132 C760,108 850,140 900,126",
        "M30,250 C200,214 400,286 620,240 C760,212 860,250 910,238",
        "M36,366 C210,330 410,404 630,356 C770,326 862,364 906,352",
        "M60,84 C150,200 120,330 190,460",
        "M420,60 C400,180 470,300 440,470",
        "M760,66 C740,190 800,320 770,462",
    ]
    for i, d in enumerate(fibers):
        o.append(f'<path d="{d}" fill="none" stroke="url(#kzFiber)" stroke-width="{9 - i*0.4:.1f}" '
                 f'stroke-linecap="round" data-at="{0.06 + i*0.045}" data-draw="1"/>')

    cells = [
        (250, 214, 1.0, 0.36), (560, 300, 1.15, 0.44), (700, 168, 0.85, 0.52),
    ]
    for cx, cy, k, at in cells:
        o.append(f'<g data-at="{at}">')
        # тело
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{52*k:.0f}" ry="{34*k:.0f}" fill="url(#kzCell)" '
                 f'stroke="#B98B72" stroke-width="1.3"/>')
        # отростки, цепляющиеся за волокна
        for dx, dy in ((-70, -34), (74, -26), (-58, 40), (62, 36), (0, -52), (4, 52)):
            o.append(f'<path d="M{cx},{cy} Q{cx+dx*0.6:.0f},{cy+dy*0.6:.0f} {cx+dx*k:.0f},{cy+dy*k:.0f}" '
                     f'fill="none" stroke="#C99B81" stroke-width="{2.4*k:.1f}" stroke-linecap="round"/>')
        # ядро
        o.append(f'<ellipse cx="{cx-4}" cy="{cy-3}" rx="{17*k:.0f}" ry="{12*k:.0f}" fill="#A97357" opacity=".72"/>')
        o.append(f'<ellipse cx="{cx-8}" cy="{cy-6}" rx="{6*k:.0f}" ry="{4*k:.0f}" fill="#F3DED2" opacity=".6"/>')
        o.append('</g>')

    o.append(f'<g data-at="0.62">{M(40, 38, "ИЛЛЮСТРАЦИЯ · КЛЕТКИ НА СЕТИ ВОЛОКОН", 8.5, fill=C["muted"])}</g>')
    o.append(f'<g data-at="0.66"><line x1="286" y1="196" x2="330" y2="150" stroke="{C["muted"]}" '
             f'stroke-width="1" stroke-dasharray="3 3"/>{M(338, 148, "ФИБРОБЛАСТ", 8.5)}</g>')
    o.append(f'<g data-at="0.70"><line x1="470" y1="120" x2="470" y2="86" stroke="{C["muted"]}" '
             f'stroke-width="1" stroke-dasharray="3 3"/>{M(480, 92, "ВОЛОКНА КОЛЛАГЕНА", 8.5)}</g>')
    o.append(f'<g data-at="0.74">{S(40, 480, "Клетка натянута отростками между волокнами, как гамак: она не лежит в матриксе, "
                                            "а держится за него.", 10)}</g>')
    return svg(W, H, "".join(o), defs)


# =====================================================================
# B1 · ПЯТЬ СЛОЁВ И 28 ДНЕЙ
# =====================================================================
def br_layers():
    W, H = 940, 560
    X0, X1 = 90, 600

    layers = [
        ("РОГОВОЙ", "мёртвые чешуйки, кератин", 372, 92, "#E8DFD0", 0.10),
        ("БЛЕСТЯЩИЙ", "только на ладонях и стопах", 340, 32, "#F1E9DB", 0.18),
        ("ЗЕРНИСТЫЙ", "клетки теряют ядро", 300, 40, "#EADFCB", 0.26),
        ("ШИПОВАТЫЙ", "клетки сцеплены мостиками", 240, 60, "#F0DED2", 0.34),
        ("БАЗАЛЬНЫЙ", "здесь клетки делятся", 200, 40, "#E5C9B8", 0.42),
    ]

    o = []
    o.append(f'<g data-at="0.02">{M(40, 44, "ПЯТЬ СЛОЁВ · ОДИН ПУТЬ НАВЕРХ", 9, fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.04">{S(40, 66, "Эпидермис обновляется целиком: клетка рождается внизу и умирает наверху.", 10.5)}</g>')

    # базальная мембрана
    o.append(f'<g data-at="0.08"><rect x="{X0}" y="428" width="{X1-X0}" height="12" rx="5" '
             f'fill="#C9A78C"/></g>')
    o.append(f'<g data-at="0.10">{M(X0, 458, "БАЗАЛЬНАЯ МЕМБРАНА — ГРАНИЦА С ДЕРМОЙ", 8.5)}</g>')

    for name, sub, y, h, col, at in layers:
        o.append(f'<g data-at="{at}"><rect x="{X0}" y="{y}" width="{X1-X0}" height="{h}" '
                 f'fill="{col}" stroke="#D3B29C" stroke-width=".9"/></g>')
        o.append(f'<g data-at="{at+0.03}">{M(X0+16, y+h/2+3, name, 8.5)}</g>')
        o.append(f'<g data-at="{at+0.04}">{S(X0+16, y+h/2+19, sub, 9.5)}</g>')

    # клетки: чем выше, тем площе
    import random
    random.seed(3)
    for k in range(9):
        x = X0 + 60 + k * 52
        o.append(f'<g data-at="{0.46+k*0.02}">'
                 f'<ellipse cx="{x}" cy="218" rx="13" ry="12" fill="#C99B81" opacity=".85"/>'
                 f'<ellipse cx="{x}" cy="266" rx="15" ry="9" fill="#C99B81" opacity=".6"/>'
                 f'<ellipse cx="{x}" cy="318" rx="17" ry="7" fill="#B8907A" opacity=".45"/>'
                 f'<rect x="{x-18}" y="{386}" width="36" height="10" rx="4" fill="#C9BBA3" opacity=".8"/>'
                 f'</g>')

    # стрелка пути
    o.append(f'<g data-at="0.56"><path d="M660,420 L660,220" stroke="{C["accent"]}" stroke-width="2" '
             f'marker-end="url(#brArr)" data-draw="1"/>'
             f'{M(676, 404, "РОЖДЕНИЕ", 8.5, fill=C["accent"])}'
             f'{M(676, 244, "СЛУЩИВАНИЕ", 8.5, fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.62"><rect x="700" y="286" width="196" height="88" rx="12" '
             f'fill="{C["stone"]}" stroke="{C["border"]}"/>'
             f'{B(718, 316, "28 дней", 22, fill=C["brand"])}'
             f'{M(718, 340, "ПОЛНЫЙ ЦИКЛ", 8.5)}'
             f'{S(718, 358, "от деления до слущивания", 9)}</g>')

    o.append(f'<g data-at="0.72">{S(40, 510, "Пока клетка поднимается, она теряет ядро и органеллы и превращается в плоскую "
                                            "чешуйку, заполненную кератином.", 10.5)}</g>')
    o.append(f'<g data-at="0.76">{S(40, 532, "Отсюда простой вывод: всё, что мы видим на поверхности, — уже мёртвая ткань.", 10.5)}</g>')
    return svg(W, H, "".join(o), marker("brArr", C["accent"]))


# =====================================================================
# B2 · КИРПИЧИ И ЦЕМЕНТ
# =====================================================================
def br_barrier():
    W, H = 940, 470
    X0, Y0, BW, BH = 120, 190, 84, 34

    o = []
    o.append(f'<g data-at="0.02">{M(40, 44, "КИРПИЧИ И ЦЕМЕНТ · КАК УСТРОЕН БАРЬЕР", 9, fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.04">{S(40, 66, "Роговой слой — это не плёнка, а кладка: плоские клетки, скреплённые липидным «раствором».", 10.5)}</g>')

    # кладка
    for row in range(4):
        y = Y0 + row * BH
        offset = (row % 2) * (BW // 2)
        for col in range(6):
            x = X0 + offset + col * BW
            if x + BW > 640:
                continue
            o.append(f'<g data-at="{0.08 + row*0.04 + col*0.008}">'
                     f'<rect x="{x}" y="{y}" width="{BW-6}" height="{BH-6}" rx="5" '
                     f'fill="#EFE3D2" stroke="#CDBBA2" stroke-width="1"/>'
                     f'<ellipse cx="{x+(BW-6)/2}" cy="{y+(BH-6)/2}" rx="18" ry="7" fill="#E3D2BB"/></g>')

    o.append(f'<g data-at="0.34"><rect x="{X0-10}" y="{Y0-10}" width="520" height="150" rx="10" '
             f'fill="none" stroke="{C["border"]}" stroke-dasharray="5 5"/>'
             f'{M(X0-10, Y0-22, "ЛИПИДЫ МЕЖДУ КЛЕТКАМИ — «РАСТВОР»", 8.5)}</g>')

    # вода выходит
    o.append(f'<g data-at="0.44"><path d="M300,178 L300,140" stroke="{C["gel_d"]}" stroke-width="1.8" '
             f'marker-end="url(#brArr2)"/>{M(312, 148, "ВОДА УХОДИТ", 8.5, fill=C["gel_d"])}</g>')

    # вещество снаружи не проходит
    o.append(f'<g data-at="0.52"><circle cx="470" cy="112" r="9" fill="{C["accent"]}" opacity=".85"/>'
             f'<path d="M470,126 L470,170" stroke="{C["accent"]}" stroke-width="1.6" stroke-dasharray="4 3"/>'
             f'<path d="M462,162 L470,176 L478,162" fill="none" stroke="{C["warn"]}" stroke-width="1.6"/>'
             f'{M(486, 106, "МОЛЕКУЛА СНАРУЖИ", 8.5, fill=C["accent"])}'
             f'{S(486, 122, "почти не проходит", 9.5)}</g>')

    # три вывода
    cards = [
        ("ПОВЕРХНОСТЬ", "уход работает здесь:\nвлага, защита, отшелушивание", 0.62),
        ("ГЛУБЖЕ", "сюда нужно доставлять:\nиначе активное вещество\nостанется снаружи", 0.68),
        ("ДЕРМА", "клетки, которые строят\nколлаген, живут глубоко", 0.74),
    ]
    for i, (title, sub, at) in enumerate(cards):
        x = 120 + i * 250
        o.append(f'<g data-at="{at}"><rect x="{x}" y="376" width="230" height="76" rx="10" '
                 f'fill="{C["stone"]}" stroke="{C["border"]}"/>'
                 f'{M(x+16, 398, title, 8.5, fill=C["brand"])}</g>')
        for k, line in enumerate(sub.split("\n")):
            o.append(f'<g data-at="{at+0.02}">{S(x+16, 418+k*14, line, 9.5)}</g>')

    return svg(W, H, "".join(o), marker("brArr2", C["gel_d"]))


# =====================================================================
# B3 · ГЛУБИНА: ГДЕ ЧТО РАБОТАЕТ
# =====================================================================
def br_depth():
    W, H = 940, 500
    X0, X1 = 180, 720
    SURF = 150

    o = []
    o.append(f'<g data-at="0.02">{M(40, 44, "ОДИН СРЕЗ · ТРИ РАЗНЫЕ ГЛУБИНЫ", 9, fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.04">{S(40, 66, "Чем глубже цель, тем важнее способ доставки. Крем и игла решают разные задачи.", 10.5)}</g>')

    # слои
    o.append(f'<g data-at="0.08"><rect x="{X0}" y="{SURF}" width="{X1-X0}" height="62" fill="#EFE3D2" '
             f'stroke="#CDBBA2"/></g>')
    o.append(f'<g data-at="0.12"><rect x="{X0}" y="{SURF+62}" width="{X1-X0}" height="180" fill="#F0DED2" '
             f'stroke="#D3B29C"/></g>')
    o.append(f'<g data-at="0.16"><rect x="{X0}" y="{SURF+242}" width="{X1-X0}" height="94" fill="#F4E6C6" '
             f'stroke="{C["fat_d"]}"/></g>')

    o.append(f'<g data-at="0.20">{M(X0+14, SURF+26, "ЭПИДЕРМИС", 8.5)}'
             f'{S(X0+14, SURF+44, "здесь нет сосудов и нет фибробластов", 9.5)}</g>')
    o.append(f'<g data-at="0.24">{M(X0+14, SURF+92, "ДЕРМА", 8.5)}'
             f'{S(X0+14, SURF+110, "коллаген, эластин, фибробласты", 9.5)}</g>')
    o.append(f'<g data-at="0.28">{M(X0+14, SURF+272, "ГИПОДЕРМА", 8.5)}'
             f'{S(X0+14, SURF+290, "жир, крупные сосуды, нервы", 9.5)}</g>')

    # фибробласты в дерме
    for i, (fx, fy) in enumerate(((300, 250), (420, 300), (540, 232), (610, 316))):
        o.append(f'<g data-at="{0.34+i*0.03}">'
                 f'<ellipse cx="{fx}" cy="{fy}" rx="13" ry="8" fill="#C99B81"/>'
                 f'<path d="M{fx-20},{fy} L{fx-13},{fy}" stroke="#C99B81" stroke-width="1.6"/>'
                 f'<path d="M{fx+13},{fy} L{fx+20},{fy}" stroke="#C99B81" stroke-width="1.6"/></g>')

    # крем сверху
    o.append(f'<g data-at="0.44"><ellipse cx="250" cy="{SURF-6}" rx="46" ry="12" fill="{C["gel"]}" '
             f'stroke="{C["gel_d"]}" stroke-width="1.2"/>'
             f'{M(250, SURF-30, "КРЕМ", 8.5, anchor="middle", fill=C["gel_d"])}'
             f'{S(250, SURF-14, "остаётся наверху", 9, anchor="middle")}</g>')

    # игла в дерму
    o.append(f'<g data-at="0.54"><path d="M540,60 L540,286" stroke="{C["brand"]}" stroke-width="2.4"/>'
             f'<path d="M534,284 L540,298 L546,284" fill="{C["brand"]}"/>'
             f'{M(556, 74, "ИНЪЕКЦИЯ", 8.5, fill=C["brand"])}'
             f'{S(556, 90, "доставляет в дерму", 9.5)}</g>')

    # линия поверхности
    o.append(f'<g data-at="0.60"><line x1="{X0-20}" y1="{SURF}" x2="{X1+20}" y2="{SURF}" '
             f'stroke="{C["muted"]}" stroke-width="1.4"/>'
             f'{M(X1+26, SURF+4, "ПОВЕРХНОСТЬ", 8)}</g>')

    o.append(f'<g data-at="0.70">{S(40, 460, "Фибробласты живут в дерме и на границе с гиподермой. Если активное вещество "
                                            "осталось в роговом слое, оно просто не встретится с ними.", 10.5)}</g>')
    return svg(W, H, "".join(o))


# =====================================================================
# S1 · КАК РАЗРУШАЕТСЯ ГЕМОГЛОБИН
# =====================================================================
def sn_chain():
    W, H = 940, 420
    steps = [
        ("ОКСИГЕМОГЛОБИН", "ярко-красный", "#D8412F", "сразу после травмы"),
        ("ДЕЗОКСИГЕМОГЛОБИН", "сине-багровый", "#7C4A8C", "1–2 дня"),
        ("МЕТГЕМОГЛОБИН", "зеленоватый", "#5E7A4A", "3–5 дней"),
        ("БИЛИВЕРДИН", "тёмно-зелёный", "#3F6B3A", "5–7 дней"),
        ("БИЛИРУБИН", "жёлтый", "#C9A227", "7–14 дней"),
    ]
    BW, GAP, TOP = 156, 22, 150

    o = []
    o.append(f'<g data-at="0.02">{M(40, 44, "ЦВЕТ СИНЯКА — ЭТО ХИМИЯ, А НЕ «СТАДИЯ ЗАЖИВЛЕНИЯ»", 9, fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.04">{S(40, 66, "Гемоглобин распадается постепенно, и на каждом шаге меняет цвет. Отсюда радуга на коже.", 10.5)}</g>')

    for i, (name, col_name, col, when) in enumerate(steps):
        x = 40 + i * (BW + GAP)
        o.append(f'<g data-at="{0.10+i*0.09}">')
        o.append(f'<rect x="{x}" y="{TOP-26}" width="{BW}" height="132" rx="12" fill="{C["stone"]}" '
                 f'stroke="{C["border"]}"/>')
        o.append(f'<circle cx="{x+BW/2}" cy="{TOP+22}" r="26" fill="{col}"/>')
        o.append(f'{M(x+BW/2, TOP+62, name, 7.5, anchor="middle")}')
        o.append(f'{B(x+BW/2, TOP+84, col_name, 10, anchor="middle")}')
        o.append(f'{S(x+BW/2, TOP+102, when, 9, anchor="middle")}')
        o.append('</g>')
        if i < len(steps) - 1:
            o.append(f'<g data-at="{0.14+i*0.09}"><path d="M{x+BW+3},{TOP+20} L{x+BW+GAP-5},{TOP+20}" '
                     f'stroke="{C["muted"]}" stroke-width="1.4" marker-end="url(#snArr)"/></g>')

    o.append(f'<g data-at="0.62"><rect x="40" y="300" width="860" height="72" rx="12" fill="#FBF3E6" '
             f'stroke="{C["border"]}"/>'
             f'{M(58, 322, "ГДЕ ЭТО ПРОИСХОДИТ", 8.5, fill=C["accent"])}'
             f'{S(58, 344, "В дерме и подкожном жире. Глубокий синяк первые дни может быть не виден:", 10)}'
             f'{S(58, 360, "кожа над ним выглядит обычно, а «проявляется» он позже — когда продукты распада поднимаются выше.", 10)}</g>')

    return svg(W, H, "".join(o), marker("snArr", C["muted"]))


# =====================================================================
# S2 · КАЛЕНДАРЬ СИНЯКА
# =====================================================================
def sn_stages():
    W, H = 940, 390
    PW, GAP, TOP = 204, 20, 104

    stages = [
        ("0 день", "красный", "#D8412F", "свежая кровь", 0.10),
        ("1–2 дня", "сине-багровый", "#7C4A8C", "кислород ушёл", 0.26),
        ("5–7 дней", "зеленоватый", "#5E7A4A", "распад клеток", 0.42),
        ("10–14 дней", "жёлто-бурый", "#C9A227", "финал распада", 0.58),
    ]

    o = []
    o.append(f'<g data-at="0.02">{M(40, 44, "ПРИМЕРНЫЙ КАЛЕНДАРЬ · СРОКИ ИНДИВИДУАЛЬНЫ", 9, fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.04">{S(40, 66, "Цвет меняется не по расписанию: влияют глубина, объём крови и особенности ткани.", 10.5)}</g>')

    for i, (day, name, col, note, at) in enumerate(stages):
        x = 40 + i * (PW + GAP)
        o.append(f'<g data-at="{at}"><rect x="{x}" y="{TOP}" width="{PW}" height="150" rx="12" '
                 f'fill="#FAF1EA" stroke="{C["border"]}"/></g>')
        # пятно
        o.append(f'<g data-at="{at+0.04}"><ellipse cx="{x+PW/2}" cy="{TOP+68}" rx="62" ry="34" '
                 f'fill="{col}" opacity=".72"/>'
                 f'<ellipse cx="{x+PW/2}" cy="{TOP+68}" rx="86" ry="46" fill="{col}" opacity=".16"/></g>')
        o.append(f'<g data-at="{at+0.08}">{B(x+PW/2, TOP+130, day, 12, anchor="middle")}</g>')
        o.append(f'<g data-at="{at+0.10}">{S(x+PW/2, TOP+176, name, 10, anchor="middle", fill=col)}</g>')
        o.append(f'<g data-at="{at+0.12}">{S(x+PW/2, TOP+192, note, 9, anchor="middle")}</g>')

    o.append(f'<g data-at="0.74">{S(40, 340, "Петехии — точечные следы от прокола — проходят сами за несколько дней.", 10.5)}</g>')
    o.append(f'<g data-at="0.78">{S(40, 360, "Крупная разлитая гематома ведёт себя иначе: она требует контроля, а не «подождать».", 10.5)}</g>')
    return svg(W, H, "".join(o))


# =====================================================================
# S3 · ЗОНЫ РИСКА
# =====================================================================
def sn_zones():
    W, H = 940, 560
    CX, CY = 330, 270

    o = []
    o.append(f'<g data-at="0.02">{M(40, 44, "ГДЕ СИНЯКИ ПОЯВЛЯЮТСЯ ЧАЩЕ ВСЕГО", 9, fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.04">{S(40, 66, "Чем тоньше кожа и богаче сосудистая сеть, тем заметнее любая капля крови.", 10.5)}</g>')

    face = (f'M{CX},{CY-200} C{CX+112},{CY-200} {CX+160},{CY-92} {CX+160},{CY+6} '
            f'C{CX+160},{CY+116} {CX+108},{CY+210} {CX},{CY+230} '
            f'C{CX-108},{CY+210} {CX-160},{CY+116} {CX-160},{CY+6} '
            f'C{CX-160},{CY-92} {CX-112},{CY-200} {CX},{CY-200} Z')
    o.append(f'<g data-at="0.06"><path d="{face}" fill="#FAF1EA" stroke="{C["skin_d"]}" stroke-width="1.4"/></g>')

    # глаза, нос, губы
    o.append(f'<g data-at="0.10"><ellipse cx="{CX-58}" cy="{CY-56}" rx="30" ry="15" fill="none" '
             f'stroke="{C["musc_d"]}" stroke-width="1.2"/>'
             f'<ellipse cx="{CX+58}" cy="{CY-56}" rx="30" ry="15" fill="none" stroke="{C["musc_d"]}" stroke-width="1.2"/>'
             f'<path d="M{CX},{CY-30} L{CX-10},{CY+34} Q{CX},{CY+44} {CX+12},{CY+34}" fill="none" '
             f'stroke="{C["musc_d"]}" stroke-width="1.1"/>'
             f'<path d="M{CX-34},{CY+96} Q{CX},{CY+86} {CX+34},{CY+96} Q{CX},{CY+124} {CX-34},{CY+96}" '
             f'fill="#E3B9AE" stroke="{C["musc_d"]}" stroke-width="1"/></g>')

    zones = [
        ("ПЕРИОРБИТАЛЬНАЯ", "тонкая кожа, рыхлая клетчатка:\nкапля крови растекается широко", CX-118, CY-92, 0.18),
        ("МЕЖБРОВЬЕ", "сосуды близко к поверхности", CX, CY-118, 0.26),
        ("ГУБЫ И УГЛЫ РТА", "плотная сеть сосудов", CX, CY+104, 0.34),
        ("ЛОБ", "сосуды сращены с надкостницей", CX, CY-152, 0.42),
    ]
    for name, sub, zx, zy, at in zones:
        o.append(f'<g data-at="{at}"><circle cx="{zx}" cy="{zy}" r="30" fill="{C["warn"]}" opacity=".16"/>'
                 f'<circle cx="{zx}" cy="{zy}" r="17" fill="{C["warn"]}" opacity=".26"/></g>')

    labels = [
        ("Периорбитальная зона", "самая частая и самая заметная", CY - 70, 0.50),
        ("Межбровье и лоб", "сосуды у самой поверхности", CY - 118, 0.56),
        ("Губы и углы рта", "обильное кровоснабжение", CY + 110, 0.62),
        ("Подкожный жир", "глубокий синяк всплывает позже", CY + 176, 0.68),
    ]
    for title, sub, ly, at in labels:
        o.append(f'<g data-at="{at}"><line x1="{CX+168}" y1="{ly-6}" x2="600" y2="{ly-6}" '
                 f'stroke="{C["border"]}" stroke-dasharray="3 4"/>'
                 f'{B(614, ly, title, 11)}</g>')
        o.append(f'<g data-at="{at+0.02}">{S(614, ly+16, sub, 9.5)}</g>')

    o.append(f'<g data-at="0.76">{S(40, 528, "Это не «плохие зоны», а просто анатомия. Знание помогает не удивляться "
                                            "и не считать синяк ошибкой врача.", 10.5)}</g>')
    return svg(W, H, "".join(o))


FIGURES = {
    "kz-fluorescence": kz_fluorescence,
    "kz-sem": kz_sem,
    "br-layers": br_layers,
    "br-barrier": br_barrier,
    "br-depth": br_depth,
    "sn-chain": sn_chain,
    "sn-stages": sn_stages,
    "sn-zones": sn_zones,
}


def validate(name, text):
    vb = re.search(r'viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"', text)
    if not vb:
        return [f"{name}: нет viewBox"]
    W, H = float(vb.group(1)), float(vb.group(2))
    probs, boxes = [], []
    for m in re.finditer(r'<text ([^>]*)>(.*?)</text>', text, re.S):
        attrs, content = m.group(1), m.group(2)
        gx = re.search(r'x="([-\d.]+)"', attrs)
        gy = re.search(r'y="([-\d.]+)"', attrs)
        gs = re.search(r'font-size="([\d.]+)"', attrs)
        ga = re.search(r'text-anchor="(\w+)"', attrs)
        if not (gx and gy):
            continue
        x, y = float(gx.group(1)), float(gy.group(1))
        size = float(gs.group(1)) if gs else 13
        anchor = ga.group(1) if ga else "start"
        w = len(content) * size * 0.57
        left = x if anchor == "start" else (x - w if anchor == "end" else x - w / 2)
        if left < -4 or left + w > W + 4:
            probs.append(f"{name}: «{content[:32]}» x={left:.0f}..{left+w:.0f} (W={W:.0f})")
        if y < 6 or y > H - 2:
            probs.append(f"{name}: «{content[:32]}» y={y} (H={H:.0f})")
        boxes.append((content[:22], left, y - size * 0.8, left + w, y + size * 0.25))
    for i, a in enumerate(boxes):
        for b in boxes[i + 1:]:
            if min(a[3], b[3]) - max(a[1], b[1]) > 3 and min(a[4], b[4]) - max(a[2], b[2]) > 2.5:
                probs.append(f"{name}: наложение «{a[0]}» и «{b[0]}»")
    return probs


if __name__ == "__main__":
    allp = []
    for name, fn in FIGURES.items():
        s = fn()
        open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8").write(s)
        cairosvg.svg2png(bytestring=s.encode(), write_to=os.path.join(OUT, name + ".png"),
                         output_width=1200, background_color="#FAF7F2")
        p = validate(name, s)
        allp += p
        print(f"{name:16} {len(s)/1024:5.1f} КБ  {'OK' if not p else str(len(p)) + ' замеч.'}")
    if allp:
        print("\nЗАМЕЧАНИЯ:")
        for x in allp:
            print("  •", x)
        sys.exit(1)
    print("\nВсе подписи в пределах холста, наложений нет.")
