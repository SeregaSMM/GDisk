#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Семь схем статьи «Кожа: архитектура, фибробласт и сборка коллагена».

Каждая схема управляется одним параметром p (0..1) через assets/app.js,
поэтому её можно и проиграть, и проскроллить ползунком.

В конце — валидатор: проверяет, что ни одна подпись не выходит за viewBox.
"""

import os, re, sys
import cairosvg

OUT = os.path.dirname(os.path.abspath(__file__))
SANS = "'Plus Jakarta Sans','DejaVu Sans',sans-serif"
MONO = "'JetBrains Mono','DejaVu Sans Mono',monospace"

C = dict(
    brand="#234233", brand_s="#2F5643", accent="#D96B43",
    text="#1C2420", muted="#5A655E", border="#E6E1D6", stone="#F2EFE9",
    epi="#E8DFD0", epi_d="#C9BBA3", der="#F0DED2", der_d="#D3B29C",
    hyp="#F5EBD6", hyp_d="#DCC49A",
    cell="#E7CDBD", cell_l="#C9A78C", nuc="#8A5A4A",
    art="#B4553A", vein="#4A6B5C", fat="#F4E6C6", fat_d="#DCC49A",
)


def _esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, t, size=13, weight=600, fill=None, anchor="start", mono=False, ls="0"):
    return (f'<text x="{x}" y="{y}" font-family="{MONO if mono else SANS}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill or C["text"]}" '
            f'text-anchor="{anchor}" letter-spacing="{ls}">{_esc(t)}</text>')


def B(x, y, t, size=13, anchor="start", fill=None):
    return text(x, y, t, size, 600, fill, anchor)


def S(x, y, t, size=11, anchor="start", fill=None):
    return text(x, y, t, size, 400, fill or C["muted"], anchor)


def M(x, y, t, size=9, anchor="start", fill=None):
    return text(x, y, t, size, 500, fill or C["muted"], anchor, mono=True, ls=".08em")


def lead(x1, y1, x2, y2, at, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{C["border"]}" '
            f'stroke-width="1" data-at="{at}"{d}/>')


def svg(w, h, body, defs=""):
    """pathLength="100" на каждом рисуемом элементе — чтобы прорисовка штриха
    не зависела от getTotalLength(): все браузеры нормализуют длину сами,
    и dashoffset считается в понятных 0..100.""" 
    body = body.replace('data-draw="1"', 'data-draw="1" pathLength="100"')
    return (f'<svg viewBox="0 0 {w} {h}" role="img" xmlns="http://www.w3.org/2000/svg">'
            f'<defs>{defs}</defs>{body}</svg>')


# =====================================================================
# 1 · ПОПЕРЕЧНЫЙ СРЕЗ КОЖИ
# =====================================================================
def fig_cross_section():
    W, H = 920, 580
    X0, X1 = 44, 620
    LX = 648
    EPI0, EPI1 = 92, 150
    DER1 = 384
    HYP1 = 470

    defs = '''
    <linearGradient id="cEpi" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#E7DCC8"/><stop offset="1" stop-color="#DCD0BA"/></linearGradient>
    <linearGradient id="cDer" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F2E1D5"/><stop offset="1" stop-color="#E6CCBC"/></linearGradient>
    <linearGradient id="cHyp" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F8EFDD"/><stop offset="1" stop-color="#EDDFC4"/></linearGradient>
    <marker id="cArr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5"
            orient="auto"><path d="M0,1 L9,5 L0,9 z" fill="#D96B43"/></marker>
    '''

    o = []
    o.append(f'<rect x="{X0}" y="{EPI0}" width="{X1-X0}" height="{EPI1-EPI0}" fill="url(#cEpi)" '
             f'stroke="{C["epi_d"]}" data-at="0.04"/>')
    o.append(f'<rect x="{X0}" y="{EPI1}" width="{X1-X0}" height="{DER1-EPI1}" fill="url(#cDer)" '
             f'stroke="{C["epi_d"]}" data-at="0.08"/>')
    o.append(f'<rect x="{X0}" y="{DER1}" width="{X1-X0}" height="{HYP1-DER1}" fill="url(#cHyp)" '
             f'stroke="{C["hyp_d"]}" data-at="0.12"/>')

    # эпидермис: три полосы
    for j, (y, op) in enumerate([(EPI0+18, .5), (EPI0+32, .45), (EPI0+44, .4)]):
        o.append(f'<line x1="{X0+4}" y1="{y}" x2="{X1-4}" y2="{y}" stroke="#C4B49A" '
                 f'stroke-width="1" opacity="{op}" data-at="{0.16+j*0.02}"/>')

    # сосочковая граница дермы
    st = (X1 - X0) / 11.0
    pap = f'M{X0},{EPI1} '
    for i in range(11):
        x = X0 + i * st
        pap += f'Q{x+st/2:.1f},{EPI1+34:.1f} {x+st:.1f},{EPI1} '
    o.append(f'<path d="{pap}" fill="none" stroke="{C["der_d"]}" stroke-width="1.3" data-at="0.18"/>')

    # коллагеновые волокна (сетчатый слой) — рисуются
    for k in range(7):
        y = 226 + k * 22
        o.append(f'<path d="M{X0+14},{y} Q{X0+150},{y-16} {X0+300},{y+8} '
                 f'T{X1-14},{y-4}" fill="none" stroke="{C["der_d"]}" stroke-width="2.2" '
                 f'stroke-linecap="round" opacity=".55" data-at="{0.26+k*0.03}" data-draw="1"/>')

    # капиллярные петли — только в сосочках
    for i in range(11):
        x = X0 + st/2 + i*st
        o.append(f'<path d="M{x:.1f},{EPI1+44:.1f} C{x-8:.1f},{EPI1+26:.1f} {x-8:.1f},{EPI1+8:.1f} '
                 f'{x:.1f},{EPI1-4:.1f} C{x+8:.1f},{EPI1+8:.1f} {x+8:.1f},{EPI1+26:.1f} '
                 f'{x:.1f},{EPI1+44:.1f}" fill="none" stroke="{C["art"]}" stroke-width="1.5" '
                 f'stroke-linecap="round" data-at="{0.36+i*0.014}" data-draw="1"/>')

    # мелкие сосуды в сетчатом слое
    for i in range(5):
        y = 250 + i * 26
        o.append(f'<path d="M{X0+30},{y} Q{X0+220},{y-14} {X1-30},{y+6}" fill="none" '
                 f'stroke="{C["vein"]}" stroke-width="1.2" opacity=".5" '
                 f'data-at="{0.40+i*0.02}"/>')

    # фибробласты в сетчатом слое
    for cx, cy, at in [(180, 320, 0.46), (420, 344, 0.50), (520, 300, 0.54)]:
        o.append(f'<g data-at="{at}"><ellipse cx="{cx}" cy="{cy}" rx="17" ry="8" '
                 f'fill="{C["cell_l"]}" stroke="#A9846B" stroke-width="1"/>'
                 f'<circle cx="{cx}" cy="{cy}" r="3" fill="{C["nuc"]}"/></g>')

    # жировые дольки
    for i in range(7):
        cx = X0 + 46 + i * 78
        cy = 410 + (i % 2) * 32
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="28" ry="17" fill="{C["fat"]}" '
                 f'stroke="{C["fat_d"]}" stroke-width="1" data-at="{0.30+i*0.02}"/>')

    # подписи справа
    rows = [
        (EPI1 - 30, 0.44, "Эпидермис", "сосудов нет · питание диффузией", 0.10),
        (236, 0.48, "Сосочковый слой", "капиллярные петли", 0.20),
        (330, 0.52, "Сетчатый слой", "коллаген, фибробласты", 0.90),
        (424, 0.58, "Гиподерма", "жировые дольки, амортизация", 1.60),
    ]
    for y, at, name, sub, depth in rows:
        o.append(lead(X1, y - 4, LX - 10, y - 4, at))
        o.append(f'<g data-at="{at}">{B(LX, y, name, 12.5)}{S(LX, y + 15, sub, 10.5)}</g>')
        o.append(f'<g data-at="{at}">{M(848, y, f"{depth:g} мм", 9, anchor="end")}</g>')

    # граница дерма/гиподерма
    o.append(f'<line x1="{X0}" y1="{DER1}" x2="{X1}" y2="{DER1}" stroke="{C["der_d"]}" '
             f'stroke-width="1.4" stroke-dasharray="7 5" data-at="0.56"/>')

    # крем на поверхности
    o.append(f'<g data-at="0.62"><path d="M{X0+120},{EPI0-2} q40,-22 96,-14 q60,8 100,-2" '
             f'fill="none" stroke="{C["accent"]}" stroke-width="2.6" stroke-linecap="round"/>'
             f'{M(X0+120, EPI0-26, "КРЕМ ОСТАЁТСЯ ЗДЕСЬ", 9, fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.66"><path d="M{X0+470},{EPI0-4} L{X0+470},{EPI1+6}" '
             f'stroke="{C["accent"]}" stroke-width="1.2" stroke-dasharray="4 4" '
             f'marker-end="url(#cArr)" opacity=".8"/>'
             f'{M(X0+300, EPI0-26, "ДАЛЬШЕ — НЕ ПРОХОДИТ", 9, fill=C["accent"])}</g>')

    # заголовок
    o.append(f'<g data-at="0.02">{M(X0, 34, "ГЛУБИНА ОТ ПОВЕРХНОСТИ · КОЖА ЛИЦА", 9)}</g>')

    return svg(W, H, "".join(o), defs)


# =====================================================================
# 2 · ЭПИДЕРМИС: СЛОИ И МИГРАЦИЯ
# =====================================================================
def fig_epidermis():
    W, H = 900, 640
    X0, X1 = 44, 606
    LX = 634
    TOP = 176

    defs = '''
    <linearGradient id="pCor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#E6DAC6"/><stop offset="1" stop-color="#DDCFB9"/></linearGradient>
    <linearGradient id="pGran" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#EADCC6"/><stop offset="1" stop-color="#E3D2BA"/></linearGradient>
    <linearGradient id="pSpin" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F0E4D3"/><stop offset="1" stop-color="#E9D9C6"/></linearGradient>
    <linearGradient id="pBas" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F3E6D6"/><stop offset="1" stop-color="#EBDAC9"/></linearGradient>
    <linearGradient id="pDer" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F1DFD3"/><stop offset="1" stop-color="#E8CEBE"/></linearGradient>
    <marker id="pArr" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5.5" markerHeight="5.5"
            orient="auto"><path d="M0,1 L9,5 L0,9 z" fill="#D96B43"/></marker>
    '''

    bands = [
        (176, 276, "url(#pCor)", "Роговой слой", "str. corneum · 15–20 рядов", 0.30),
        (276, 322, "url(#pGran)", "Зернистый слой", "str. granulosum · 3–5 рядов", 0.24),
        (322, 408, "url(#pSpin)", "Шиповатый слой", "str. spinosum · 5–10 рядов", 0.18),
        (408, 460, "url(#pBas)", "Базальный слой", "str. basale · 1 ряд", 0.12),
    ]

    o = [f'<rect x="{X0}" y="460" width="{X1-X0}" height="104" fill="url(#pDer)" '
         f'stroke="{C["epi_d"]}" data-at="0.02"/>']

    for y0, y1, fill, name, sub, at in bands:
        o.append(f'<g data-at="{at}"><rect x="{X0}" y="{y0}" width="{X1-X0}" '
                 f'height="{y1-y0}" fill="{fill}" stroke="{C["epi_d"]}"/></g>')

    # базальная мембрана + сосочки
    o.append(f'<path d="M{X0},460 L{X1},460" stroke="{C["brand"]}" stroke-width="2" data-at="0.34"/>')
    st = (X1 - X0) / 11.0
    pap = f'M{X0},460 '
    for i in range(11):
        x = X0 + i * st
        pap += f'Q{x+st/2:.1f},478 {x+st:.1f},460 '
    o.append(f'<path d="{pap}" fill="none" stroke="{C["brand"]}" stroke-width="1.1" '
             f'opacity=".45" data-at="0.36"/>')

    # рядность рогового слоя
    for j in range(5):
        y = 176 + 19 * (j + 1)
        o.append(f'<line x1="{X0+5}" y1="{y}" x2="{X1-5}" y2="{y}" stroke="#C4B49A" '
                 f'stroke-width=".8" opacity=".45" data-at="{0.34+j*0.015}"/>')

    # зернистые гранулы
    for i in range(18):
        gx = X0 + 20 + (i % 9) * 60
        gy = 288 + (i // 9) * 18
        if gx > X1 - 12:
            continue
        o.append(f'<circle cx="{gx}" cy="{gy}" r="1.9" fill="#B49B7A" opacity=".55" data-at="0.26"/>')

    # шиповатые и базальные клетки (минус место под мигрирующую)
    for i in range(9):
        cx = X0 + 34 + i * 62
        if abs(cx - 220) < 30:
            continue
        o.append(f'<ellipse cx="{cx}" cy="360" rx="13" ry="10" fill="{C["cell"]}" '
                 f'stroke="{C["cell_l"]}" stroke-width=".9" data-at="0.22"/>')
    for i in range(10):
        cx = X0 + 30 + i * 56
        if abs(cx - 220) < 30:
            continue
        o.append(f'<ellipse cx="{cx}" cy="434" rx="11" ry="9" fill="{C["cell"]}" '
                 f'stroke="{C["cell_l"]}" stroke-width=".9" data-at="0.16"/>')

    # меланоцит
    o.append(f'<g data-at="0.52"><ellipse cx="452" cy="434" rx="12" ry="8.5" '
             f'fill="{C["cell_l"]}" stroke="#A9846B"/>'
             f'<path d="M452,434 q-13,-17 -26,-21 M452,434 q13,-17 26,-21 '
             f'M452,434 q-5,-18 -8,-25" stroke="#A9846B" fill="none"/>'
             f'<circle cx="452" cy="434" r="3.3" fill="#6B4436"/></g>')

    # клетка Лангерганса
    o.append(f'<g data-at="0.56"><ellipse cx="348" cy="366" rx="10" ry="7.5" fill="#DCCAB6" '
             f'stroke="#B7A38C"/>'
             f'<path d="M348,366 q-15,-9 -23,-5 M348,366 q15,-9 23,-5 M348,366 q-6,10 -12,13 '
             f'M348,366 q6,10 12,13" stroke="#B7A38C" fill="none"/></g>')

    # миграция
    o.append(f'<g transform="translate(220 438)"><g data-ty="0,-244" data-scale="1,1,1.7,0.34">'
             f'<ellipse cx="0" cy="0" rx="11" ry="11" fill="{C["cell"]}" '
             f'stroke="{C["cell_l"]}" stroke-width="1.1"/>'
             f'<circle cx="0" cy="0" r="4.3" fill="{C["nuc"]}" data-out="0.72,0.92"/></g></g>')

    o.append(f'<path d="M182,412 L182,236" stroke="{C["accent"]}" stroke-width="1.2" opacity=".7" '
             f'marker-end="url(#pArr)" data-at="0.38"/>')

    # подписи слоёв
    for y0, y1, fill, name, sub, at in bands:
        yc = (y0 + y1) / 2 + 3
        o.append(lead(X1, yc - 4, LX - 10, yc - 4, at + 0.12))
        o.append(f'<g data-at="{at+0.12}">{B(LX, yc, name, 12.5)}{S(LX, yc + 15, sub, 10.5)}</g>')

    o.append(lead(X1, 500, LX - 10, 500, 0.62))
    o.append(f'<g data-at="0.62">{B(LX, 504, "Дерма", 12.5)}'
             f'{S(LX, 519, "сосочковый слой", 10.5)}</g>')

    # блестящий слой
    o.append(f'<line x1="{X0}" y1="264" x2="{X1}" y2="264" stroke="{C["muted"]}" '
             f'stroke-width="1" stroke-dasharray="5 4" data-at="0.58"/>')
    o.append(f'<g data-at="0.60">{M(X0+6, 259, "БЛЕСТЯЩИЙ СЛОЙ — ТОЛЬКО НА ЛАДОНЯХ И ПОДОШВАХ", 8)}</g>')

    # выноски
    o.append(f'<g data-at="0.64"><path d="M464,427 L566,404" stroke="{C["muted"]}"/>'
             f'{M(572, 400, "МЕЛАНОЦИТ", 9)}{S(572, 415, "остаётся на месте", 10.5)}</g>')
    o.append(f'<g data-at="0.66"><path d="M336,358 L272,332" stroke="{C["muted"]}"/>'
             f'{M(196, 328, "КЛЕТКА ЛАНГЕРГАНСА", 9)}{S(196, 343, "иммунный надзор", 10.5)}</g>')

    o.append(f'<g data-at="0.70">{M(140, 216, "28 СУТОК · ОДИН ЦИКЛ", 9, fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.72">{B(96, 108, "Кератиноцит поднимается и уплощается", 13)}'
             f'{S(96, 126, "Ядро и органеллы исчезают — так формируется", 11)}'
             f'{S(96, 141, "безъядерная чешуйка рогового слоя", 11)}</g>')

    return svg(W, H, "".join(o), defs)


# =====================================================================
# 3 · АНГИОАРХИТЕКТОНИКА
# =====================================================================
def fig_vessels():
    W, H = 920, 580
    X0, X1 = 52, 664
    LX = 692
    E0, E1 = 82, 152
    D1, H1 = 416, 508

    defs = '''
    <linearGradient id="aEpi" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#E9E0D1"/><stop offset="1" stop-color="#DFD3BF"/></linearGradient>
    <linearGradient id="aDer" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F4E3D7"/><stop offset="1" stop-color="#E9D3C2"/></linearGradient>
    <linearGradient id="aHyp" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F8EFDD"/><stop offset="1" stop-color="#EFE0C4"/></linearGradient>
    '''

    o = []
    o.append(f'<rect x="{X0}" y="{E0}" width="{X1-X0}" height="{E1-E0}" fill="url(#aEpi)" '
             f'stroke="{C["epi_d"]}" data-at="0.02"/>')
    o.append(f'<rect x="{X0}" y="{E1}" width="{X1-X0}" height="{D1-E1}" fill="url(#aDer)" '
             f'stroke="{C["epi_d"]}" data-at="0.06"/>')
    o.append(f'<rect x="{X0}" y="{D1}" width="{X1-X0}" height="{H1-D1}" fill="url(#aHyp)" '
             f'stroke="{C["hyp_d"]}" data-at="0.10"/>')

    n = 12
    st = (X1 - X0) / n
    pap = f'M{X0},{E1} '
    for i in range(n):
        x = X0 + i * st
        pap += f'Q{x+st/2:.1f},{E1+54:.1f} {x+st:.1f},{E1} '
    o.append(f'<path d="{pap}" fill="none" stroke="{C["der_d"]}" stroke-width="1.2" data-at="0.12"/>')

    # жировые дольки
    for i in range(8):
        cx = X0 + 40 + i * 76
        cy = 444 + (i % 2) * 34
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="27" ry="16" fill="{C["fat"]}" '
                 f'stroke="{C["fat_d"]}" stroke-width=".9" opacity=".8" data-at="0.14"/>')

    # глубокая сеть
    deep = f'M{X0+6},456 Q210,436 350,456 T{X1-6},448'
    o.append(f'<path d="{deep}" fill="none" stroke="{C["art"]}" stroke-width="3.2" '
             f'stroke-linecap="round" data-at="0.20" data-draw="1"/>')

    # восходящие сосуды
    for i in range(7):
        x = X0 + 46 + i * 88
        o.append(f'<path d="M{x},454 C{x-9},382 {x+11},330 {x},270 C{x-7},232 {x+5},200 '
                 f'{x},{E1+10}" fill="none" stroke="{C["art"]}" stroke-width="1.9" '
                 f'stroke-linecap="round" opacity=".88" data-at="{0.24+i*0.018}" data-draw="1"/>')
        o.append(f'<path d="M{x+10},454 C{x+2},382 {x+21},330 {x+10},270 C{x+5},232 {x+15},200 '
                 f'{x+10},{E1+10}" fill="none" stroke="{C["vein"]}" stroke-width="1.5" '
                 f'stroke-linecap="round" opacity=".68" data-at="{0.28+i*0.018}" data-draw="1"/>')

    # поверхностная сеть
    surf = f'M{X0+6},236 Q190,224 310,236 T{X1-6},228'
    o.append(f'<path d="{surf}" fill="none" stroke="{C["art"]}" stroke-width="2.3" '
             f'stroke-linecap="round" data-at="0.34" data-draw="1"/>')

    # капиллярные петли
    for i in range(n):
        x = X0 + st/2 + i*st
        o.append(f'<path d="M{x:.1f},236 C{x-10:.1f},214 {x-10:.1f},188 {x:.1f},{E1+14:.1f} '
                 f'C{x+10:.1f},188 {x+10:.1f},214 {x:.1f},236" fill="none" stroke="{C["art"]}" '
                 f'stroke-width="1.5" stroke-linecap="round" data-at="{0.40+i*0.012}" data-draw="1"/>')

    rows = [
        (116, 0.42, "Эпидермис", "сосудов нет"),
        (204, 0.48, "Поверхностная сеть", "питает эпидермис"),
        (312, 0.54, "Соединительные сосуды", "проходят дерму"),
        (448, 0.62, "Глубокая сеть", "на границе с гиподермой"),
        (494, 0.68, "Гиподерма", "жировые дольки"),
    ]
    for y, at, name, sub in rows:
        o.append(lead(X1, y - 4, LX - 10, y - 4, at))
        o.append(f'<g data-at="{at}">{B(LX, y, name, 12)}{S(LX, y + 15, sub, 10.5)}</g>')

    # легенда
    o.append(f'<g data-at="0.74">'
             f'<line x1="{X0}" y1="546" x2="{X0+34}" y2="546" stroke="{C["art"]}" '
             f'stroke-width="3.2" stroke-linecap="round"/>'
             f'{S(X0+44, 550, "артериальное звено", 11)}'
             f'<line x1="{X0+216}" y1="546" x2="{X0+250}" y2="546" stroke="{C["vein"]}" '
             f'stroke-width="2.4" stroke-linecap="round"/>'
             f'{S(X0+260, 550, "венозное звено", 11)}</g>')

    o.append(f'<g data-at="0.76">{M(X0, 62, "ГЛУБОКАЯ СЕТЬ → ПОВЕРХНОСТНАЯ → КАПИЛЛЯРНЫЕ ПЕТЛИ", 9, fill=C["accent"])}</g>')

    return svg(W, H, "".join(o), defs)


# =====================================================================
# 4 · ФИБРОБЛАСТ: ДВЕ ФУНКЦИИ
# =====================================================================
def fig_fibroblast():
    W, H = 980, 520
    CX, CY = 490, 250
    LEFT_X, RIGHT_X = 40, W - 40

    defs = '''
    <radialGradient id="fCell" cx="48%" cy="44%" r="62%">
      <stop offset="0" stop-color="#F4E4D6"/><stop offset="1" stop-color="#E8CFBE"/></radialGradient>
    <marker id="fG" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5"
            orient="auto"><path d="M0,1 L9,5 L0,9 z" fill="#234233"/></marker>
    <marker id="fT" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5"
            orient="auto"><path d="M0,1 L9,5 L0,9 z" fill="#D96B43"/></marker>
    '''

    o = []
    o.append(f'<g data-at="0.03">{M(LEFT_X, 54, "АНАБОЛИЗМ · СИНТЕЗ", 10, fill=C["brand"])}</g>')
    o.append(f'<g data-at="0.03">{M(RIGHT_X, 54, "КАТАБОЛИЗМ · РАЗРУШЕНИЕ", 10, anchor="end", fill=C["accent"])}</g>')

    # волокна по краям
    for i in range(4):
        yy = 150 + i * 62
        o.append(f'<path d="M{LEFT_X},{yy} q40,-14 84,2 q40,14 80,-4" fill="none" '
                 f'stroke="{C["der_d"]}" stroke-width="2.2" stroke-linecap="round" '
                 f'opacity=".4" data-at="0.08"/>')
        o.append(f'<path d="M{RIGHT_X-164},{yy} q40,-14 84,2 q40,14 80,-4" fill="none" '
                 f'stroke="{C["der_d"]}" stroke-width="2.2" stroke-linecap="round" '
                 f'opacity=".4" data-at="0.08"/>')

    # тело клетки
    body = (f'M{CX-152},{CY} C{CX-122},{CY-58} {CX-72},{CY-74} {CX},{CY-72} '
            f'C{CX+72},{CY-74} {CX+122},{CY-58} {CX+152},{CY} '
            f'C{CX+122},{CY+58} {CX+72},{CY+74} {CX},{CY+72} '
            f'C{CX-72},{CY+74} {CX-122},{CY+58} {CX-152},{CY} Z')
    o.append(f'<g data-at="0.06"><path d="{body}" fill="url(#fCell)" '
             f'stroke="{C["cell_l"]}" stroke-width="1.4"/></g>')

    # отростки
    o.append(f'<g data-at="0.12" stroke="{C["cell_l"]}" stroke-width="2" fill="none" '
             f'stroke-linecap="round" opacity=".85">'
             f'<path d="M{CX-148},{CY-16} Q{CX-176},{CY-42} {CX-196},{CY-34}"/>'
             f'<path d="M{CX-148},{CY+16} Q{CX-176},{CY+42} {CX-196},{CY+34}"/>'
             f'<path d="M{CX+148},{CY-16} Q{CX+176},{CY-42} {CX+196},{CY-34}"/>'
             f'<path d="M{CX+148},{CY+16} Q{CX+176},{CY+42} {CX+196},{CY+34}"/></g>')

    # ядро
    o.append(f'<g data-at="0.14"><ellipse cx="{CX}" cy="{CY-6}" rx="52" ry="40" '
             f'fill="#D9B9A4" stroke="#B8907A" stroke-width="1.2"/>'
             f'<ellipse cx="{CX}" cy="{CY-6}" rx="20" ry="16" fill="#A5745E" opacity=".5"/></g>')

    # ЭПС
    o.append(f'<g data-at="0.20" fill="none" stroke="#B8907A" stroke-width="1.3" opacity=".85">'
             f'<path d="M{CX-126},{CY-28} q14,-11 28,0 q14,11 28,0"/>'
             f'<path d="M{CX-126},{CY-10} q14,-11 28,0 q14,11 28,0"/>'
             f'<path d="M{CX-126},{CY+8} q14,-11 28,0 q14,11 28,0"/></g>')
    for i in range(9):
        o.append(f'<circle cx="{CX-118+i*11}" cy="{CY-33+(i%3)*18}" r="1.4" '
                 f'fill="#8A5A4A" opacity=".6" data-at="0.24"/>')

    # Гольджи
    o.append(f'<g data-at="0.26" fill="none" stroke="#B8907A" stroke-width="1.4" opacity=".85">'
             f'<path d="M{CX+52},{CY-20} q22,8 44,-2"/>'
             f'<path d="M{CX+52},{CY-6} q22,8 44,-2"/>'
             f'<path d="M{CX+52},{CY+8} q22,8 44,-2"/></g>')

    # подпись клетки
    o.append(f'<g data-at="0.30">{B(CX, CY+112, "ФИБРОБЛАСТ", 12.5, anchor="middle")}'
             f'{S(CX, CY+130, "резидентная клетка сетчатого слоя", 10.5, anchor="middle")}</g>')
    o.append(f'<g data-at="0.32">{M(CX-140, CY-94, "ЯДРО", 8, anchor="middle")}'
             f'{M(CX-74, CY+52, "ЭПС", 8, anchor="middle")}'
             f'{M(CX+74, CY+52, "ГОЛЬДЖИ", 8, anchor="middle")}</g>')
    o.append(f'<line x1="{CX-140}" y1="{CY-88}" x2="{CX-40}" y2="{CY-46}" '
             f'stroke="{C["border"]}" data-at="0.32"/>')

    # анаболизм
    anab = [("Коллаген I и III", 0.40), ("Эластин и фибриллин", 0.49),
            ("Гиалуронан", 0.58), ("Факторы роста", 0.67)]
    for i, (name, at) in enumerate(anab):
        y = 150 + i * 56
        o.append(f'<path d="M{CX-158},{CY-28+i*6} C{CX-212},{y+18} {CX-236},{y} {CX-266},{y}" '
                 f'fill="none" stroke="{C["brand"]}" stroke-width="1.6" opacity=".5" '
                 f'marker-end="url(#fG)" data-at="{at}" data-draw="1"/>')
        o.append(f'<g data-at="{at}">{B(LEFT_X, y + 4, name, 12)}</g>')

    # катаболизм
    catab = [("Коллагеназа MMP-1, -8, -13", 0.46), ("Желатиназы", 0.55),
             ("Эластаза", 0.63), ("Гиалуронидаза", 0.70)]
    for i, (name, at) in enumerate(catab):
        y = 150 + i * 56
        o.append(f'<path d="M{CX+158},{CY-28+i*6} C{CX+212},{y+18} {CX+236},{y} {CX+266},{y}" '
                 f'fill="none" stroke="{C["accent"]}" stroke-width="1.6" opacity=".55" '
                 f'marker-end="url(#fT)" data-at="{at}" data-draw="1"/>')
        o.append(f'<g data-at="{at}">{B(RIGHT_X, y + 4, name, 12, anchor="end")}</g>')

    o.append(f'<g data-at="0.76">{S(LEFT_X, 400, "Синтез и деградация идут", 11)}'
             f'{S(LEFT_X, 416, "одновременно и в одной клетке.", 11)}</g>')
    o.append(f'<g data-at="0.78">{S(RIGHT_X, 400, "Разрушение старых волокон — условие замены:", 11, anchor="end")}'
             f'{S(RIGHT_X, 416, "без него новый матрикс не встраивается.", 11, anchor="end")}</g>')

    return svg(W, H, "".join(o), defs)


# =====================================================================
# 5 · ПЯТЬ ПОРЯДКОВ СБОРКИ КОЛЛАГЕНА
# =====================================================================
def fig_collagen_orders():
    W, H = 980, 380
    Y = 200

    o = []
    stages = [
        (104, "1", "Тропоколлаген", "тройная спираль", "≈1,5 нм", 0.06),
        (296, "2", "Микрофибрилла", "спирали в пучок", "≈4 нм", 0.20),
        (490, "3", "Фибрилла", "с поперечной исчерченностью", "20–200 нм", 0.34),
        (684, "4", "Волокно", "пучок фибрилл", "1–20 мкм", 0.48),
        (880, "5", "Пучок", "волокна в связке", "до 100 мкм", 0.62),
    ]

    # соединяющие стрелки
    for i in range(4):
        x1 = stages[i][0] + 58
        x2 = stages[i + 1][0] - 62
        o.append(f'<path d="M{x1},{Y} L{x2},{Y}" stroke="{C["border"]}" stroke-width="1.4" '
                 f'stroke-linecap="round" marker-end="url(#coArr)" data-at="{stages[i][5]+0.10}"/>')

    # 1 — тройная спираль
    cx = stages[0][0]
    for k, dx in enumerate([-7, 0, 7]):
        o.append(f'<path d="M{cx+dx-22},{Y+16} q11,-12 22,0 q11,12 22,0 q11,-12 22,0" fill="none" '
                 f'stroke="{C["brand"]}" stroke-width="2.4" stroke-linecap="round" '
                 f'opacity="{0.9-k*0.18}" data-at="{stages[0][5]}" data-draw="1"/>')

    # 2 — микрофибрилла: пять спиралей
    cx = stages[1][0]
    for k in range(5):
        o.append(f'<path d="M{cx-48},{Y+14-k*7} q24,-10 48,0 q24,10 48,0" fill="none" '
                 f'stroke="{C["brand"]}" stroke-width="1.7" stroke-linecap="round" '
                 f'opacity="{0.85-k*0.1}" data-at="{stages[1][5]+k*0.015}" data-draw="1"/>')

    # 3 — фибрилла с исчерченностью
    cx = stages[2][0]
    o.append(f'<rect x="{cx-52}" y="{Y-14}" width="104" height="28" rx="6" '
             f'fill="#E9D9C6" stroke="{C["brand"]}" stroke-width="1.2" data-at="{stages[2][5]}"/>')
    for k in range(7):
        o.append(f'<line x1="{cx-44+k*14}" y1="{Y-12}" x2="{cx-44+k*14}" y2="{Y+12}" '
                 f'stroke="{C["brand"]}" stroke-width="1" opacity=".5" '
                 f'data-at="{stages[2][5]+0.03+k*0.01}"/>')

    # 4 — волокно: пучок фибрилл
    cx = stages[3][0]
    for k in range(6):
        o.append(f'<path d="M{cx-56},{Y-10+k*5} q28,-6 56,0 q28,6 56,0" fill="none" '
                 f'stroke="{C["brand"]}" stroke-width="1.5" opacity=".72" '
                 f'data-at="{stages[3][5]+k*0.012}"/>')

    # 5 — пучок
    cx = stages[4][0]
    for k in range(4):
        o.append(f'<path d="M{cx-62},{Y-24+k*14} q31,-12 62,0 q31,12 62,0" fill="none" '
                 f'stroke="{C["brand"]}" stroke-width="3.4" stroke-linecap="round" '
                 f'opacity="{0.9-k*0.1}" data-at="{stages[4][5]+k*0.02}" data-draw="1"/>')

    # подписи
    for x, num, name, desc, size, at in stages:
        o.append(f'<g data-at="{at+0.04}">{M(x, 96, num, 11, anchor="middle", fill=C["accent"])}</g>')
        o.append(f'<g data-at="{at+0.06}">{B(x, 286, name, 12, anchor="middle")}'
                 f'{S(x, 302, desc, 10, anchor="middle")}'
                 f'{M(x, 322, size, 9, anchor="middle")}</g>')

    # шкала
    o.append(f'<g data-at="0.80">{S(40, 360, "Масштаб намеренно не соблюдён между стадиями: ", 10)}'
             f'{S(296, 360, "от нанометров к микрометрам — два порядка разницы.", 10)}</g>')

    defs = ('<marker id="coArr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" '
            'markerHeight="5" orient="auto"><path d="M0,1 L9,5 L0,9 z" fill="#E6E1D6"/></marker>')
    return svg(W, H, "".join(o), defs)


# =====================================================================
# 6 · ТАЙМЛАЙН НЕОКОЛЛАГЕНОГЕНЕЗА
# =====================================================================
def fig_timeline():
    W, H = 940, 400
    AX0, AX1 = 70, 870
    AY = 210

    o = []
    o.append(f'<line x1="{AX0}" y1="{AY}" x2="{AX1}" y2="{AY}" stroke="{C["border"]}" '
             f'stroke-width="2" stroke-linecap="round" data-at="0.02"/>')

    phases = [
        (0.00, "0–3 дня", "Воспаление", "травма, отёк,\nмиграция клеток", C["accent"]),
        (0.26, "3 дня – 3 нед", "Пролиферация", "грануляции,\nранний коллаген III", "#C08457"),
        (0.55, "3 нед – 3 мес", "Ремоделирование", "замена III на I,\nуплотнение", C["brand_s"]),
        (0.82, "3–12 мес", "Созревание", "поперечные сшивки,\nфинальная плотность", C["brand"]),
    ]

    for i, (pos, span, name, desc, col) in enumerate(phases):
        at = 0.06 + i * 0.06
        x = AX0 + (AX1 - AX0) * pos
        # сегмент фазы
        nextpos = phases[i + 1][0] if i + 1 < len(phases) else 1.0
        x2 = AX0 + (AX1 - AX0) * nextpos
        o.append(f'<line x1="{x}" y1="{AY}" x2="{x2}" y2="{AY}" stroke="{col}" '
                 f'stroke-width="7" stroke-linecap="round" opacity=".85" data-at="{at}"/>')
        o.append(f'<circle cx="{x}" cy="{AY}" r="5" fill="#FAF7F2" stroke="{col}" '
                 f'stroke-width="2" data-at="{at}"/>')
        # подпись сверху
        o.append(f'<g data-at="{at+0.04}">{B(x, AY - 54, name, 12)}'
                 f'{M(x, AY - 36, span.upper(), 8.5, fill=col)}</g>')
        # описание снизу
        for k, line in enumerate(desc.split("\n")):
            o.append(f'<g data-at="{at+0.06}">{S(x, AY + 40 + k * 16, line, 10.5)}</g>')

    # «сегодня»
    o.append(f'<g data-at="0.76">'
             f'<line x1="{AX0+120}" y1="{AY-16}" x2="{AX0+120}" y2="{AY+16}" '
             f'stroke="{C["accent"]}" stroke-width="1.4" stroke-dasharray="3 3"/>'
             f'{M(AX0+120, AY-24, "ОЦЕНКА ПАЦИЕНТА", 8, anchor="middle", fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.80">{S(AX0, 340, "Границы фаз приблизительны и зависят от методики, зоны и индивидуального ответа.", 10.5)}</g>')

    # заголовок оси
    o.append(f'<g data-at="0.02">{M(AX0, 128, "ВРЕМЯ ОТ ПРОЦЕДУРЫ", 9)}</g>')

    return svg(W, H, "".join(o), '')


# =====================================================================
# 7 · ГИПОДЕРМА
# =====================================================================
def fig_hypodermis():
    W, H = 940, 480
    X0, X1 = 46, 894

    defs = '''
    <linearGradient id="hBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F9F0DE"/><stop offset="1" stop-color="#EFE0C3"/></linearGradient>
    '''

    o = []
    o.append(f'<rect x="{X0}" y="66" width="{X1-X0}" height="92" fill="{C["der"]}" '
             f'stroke="{C["der_d"]}" data-at="0.04"/>')
    o.append(f'<g data-at="0.06">{B(X0+22, 104, "Дерма", 12.5)}'
             f'{S(X0+22, 122, "сетчатый слой · коллаген и фибробласты", 10.5)}</g>')

    o.append(f'<rect x="{X0}" y="158" width="{X1-X0}" height="244" fill="url(#hBg)" '
             f'stroke="{C["hyp_d"]}" data-at="0.08"/>')

    sub = [(158, 244, "Поверхностный подслой", "мелкие дольки, много септ"),
           (244, 344, "Средний подслой", "крупные дольки, основная масса"),
           (344, 402, "Глубокий подслой", "слой скольжения над фасцией")]
    for y0, y1, name, d in sub:
        if y0 > 158:
            o.append(f'<line x1="{X0}" y1="{y0}" x2="{X1}" y2="{y0}" stroke="{C["hyp_d"]}" '
                     f'stroke-width="1" stroke-dasharray="6 5" data-at="0.12"/>')
        o.append(f'<g data-at="0.14">{M(X0+18, y1-30, name.upper(), 8.5)}'
                 f'{S(X0+18, y1-15, d, 9.5)}</g>')

    # дольки
    idx = 0
    layout = [(158, 244, 7, 1), (244, 344, 6, 2), (344, 402, 4, 1)]
    scale = [1.0, 1.35, 1.25]
    for row, (y0, y1, cols, rows) in enumerate(layout):
        for r in range(rows):
            for c in range(cols):
                sc = scale[row]
                cx = X0 + (X1 - X0) * (c + 0.5) / cols + (16 if r % 2 else -10)
                cy = y0 + (y1 - y0) * (r + 0.5) / rows
                rx = 42 * sc
                ry = 24 * sc
                # отступ под подпись слева
                if cx - rx < X0 + 150 and row == 0:
                    cx += 90
                if cx + rx > X1 - 8:
                    cx = X1 - 8 - rx
                o.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" '
                         f'fill="{C["fat"]}" stroke="{C["fat_d"]}" stroke-width="1" '
                         f'data-at="{0.18+idx*0.014}"/>')
                o.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{2.6*sc:.1f}" '
                         f'fill="{C["fat_d"]}" opacity=".5" data-at="{0.20+idx*0.014}"/>')
                idx += 1

    # септы
    for i in range(1, 9):
        x = X0 + 150 + (X1 - X0 - 150) * i / 9
        o.append(f'<path d="M{x:.0f},158 L{x:.0f},402" stroke="#D7BE8E" stroke-width="1.6" '
                 f'opacity=".7" data-at="{0.32+i*0.012}"/>')

    o.append(f'<line x1="{X0}" y1="402" x2="{X1}" y2="402" stroke="{C["der_d"]}" '
             f'stroke-width="2.2" data-at="0.34"/>')
    o.append(f'<g data-at="0.36">{M(X0+18, 424, "ПОВЕРХНОСТНАЯ ФАСЦИЯ МЫШЦЫ", 8.5)}</g>')

    o.append(f'<g data-at="0.40">{M(X0+18, 180, "СЕПТЫ", 8.5, fill=C["accent"])}'
             f'{S(X0+18, 194, "соединительнотканные перемычки", 9.5)}</g>')

    o.append(f'<g data-at="0.48">{S(X0, 452, "Объём гиподермы меняется годами, а не после процедуры: ", 10.5)}'
             f'{S(X0+360, 452, "«плотность» и «объём» — разные задачи.", 10.5)}</g>')

    return svg(W, H, "".join(o), defs)


# =====================================================================
# ВАЛИДАТОР
# =====================================================================
def validate(name, svg_text):
    """Проверяет, что подписи не выходят за пределы viewBox."""
    vb = re.search(r'viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"', svg_text)
    if not vb:
        return [f"{name}: нет viewBox"]
    W, H = float(vb.group(1)), float(vb.group(2))
    problems = []

    for m in re.finditer(r'<text ([^>]*)>(.*?)</text>', svg_text, re.S):
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

        # грубая оценка ширины: кириллица ~0.56em
        w = len(content) * size * 0.56
        left = x if anchor == "start" else (x - w if anchor == "end" else x - w / 2)

        if left < -2 or left + w > W + 2:
            problems.append(f"{name}: «{content[:34]}» x={left:.0f}..{left+w:.0f} (W={W:.0f})")
        if y < 6 or y > H - 2:
            problems.append(f"{name}: «{content[:34]}» y={y} (H={H:.0f})")

    return problems


FIGURES = {
    "fig-cross-section": fig_cross_section,
    "fig-epidermis": fig_epidermis,
    "fig-vessels": fig_vessels,
    "fig-fibroblast": fig_fibroblast,
    "fig-collagen-orders": fig_collagen_orders,
    "fig-timeline": fig_timeline,
    "fig-hypodermis": fig_hypodermis,
}

if __name__ == "__main__":
    all_problems = []
    for name, fn in FIGURES.items():
        s = fn()
        open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8").write(s)
        cairosvg.svg2png(bytestring=s.encode(), write_to=os.path.join(OUT, name + ".png"),
                         output_width=1300, background_color="#FAF7F2")
        probs = validate(name, s)
        all_problems += probs
        print(f"{name:22} {len(s)/1024:5.1f} КБ   {'OK' if not probs else str(len(probs))+' замечаний'}")

    if all_problems:
        print("\nЗАМЕЧАНИЯ:")
        for p in all_problems:
            print("  •", p)
        sys.exit(1)
    print("\nВсе подписи в пределах холста.")
