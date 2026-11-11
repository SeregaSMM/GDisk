#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Схемы для трёх новых статей. Без дозировок и протоколов."""

import os, re, sys
import cairosvg

OUT = os.path.dirname(os.path.abspath(__file__))
SANS = "'Plus Jakarta Sans','DejaVu Sans',sans-serif"
MONO = "'JetBrains Mono','DejaVu Sans Mono',monospace"

C = dict(
    brand="#234233", brand_s="#2F5643", accent="#D96B43",
    text="#1C2420", muted="#5A655E", border="#E6E1D6", stone="#F2EFE9",
    skin="#F2E1D5", skin_d="#D3B29C", fat="#F4E6C6", fat_d="#DCC49A",
    musc="#D9B9A4", musc_d="#B8907A", bone="#E4DED2", bone_d="#BFB6A4",
    gel="#C9D8CE", gel_d="#5C7A66", warn="#B4553A", plasma="#F0D77C",
    blood="#C4675C", pale="#FAF7F2",
)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(x, y, t, size=13, weight=600, fill=None, anchor="start", mono=False, ls="0"):
    return (f'<text x="{x}" y="{y}" font-family="{MONO if mono else SANS}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill or C["text"]}" text-anchor="{anchor}" '
            f'letter-spacing="{ls}">{esc(t)}</text>')


def B(x, y, t, size=13, anchor="start", fill=None):
    return T(x, y, t, size, 600, fill, anchor)


def S(x, y, t, size=11, anchor="start", fill=None):
    return T(x, y, t, size, 400, fill or C["muted"], anchor)


def M(x, y, t, size=9, anchor="start", fill=None, ls=".08em"):
    return T(x, y, t, size, 500, fill or C["muted"], anchor, mono=True, ls=ls)


def marker(pid, color):
    return (f'<marker id="{pid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" '
            f'markerHeight="5" orient="auto"><path d="M0,1 L9,5 L0,9 z" fill="{color}"/></marker>')


def svg(w, h, body, defs=""):
    body = body.replace('data-draw="1"', 'data-draw="1" pathLength="100"')
    return (f'<svg viewBox="0 0 {w} {h}" role="img" xmlns="http://www.w3.org/2000/svg">'
            f'<defs>{defs}</defs>{body}</svg>')


def panel(x, y, w, h, at, fill=None, r=12):
    return (f'<g data-at="{at}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
            f'fill="{fill or C["stone"]}" stroke="{C["border"]}"/></g>')


# =====================================================================
# A1 · ЧЕТЫРЕ СЛОЯ, ЧЕТЫРЕ РАЗНЫХ ВОЗРАСТА
# =====================================================================
def ag_layers():
    W, H = 940, 560
    rows = [
        ("КОЖА", "плотная, упругая", "тоньше, суше, медленнее восстанавливается", C["skin"], C["skin_d"], 0.10),
        ("ЖИР", "пакеты держат объём на месте", "смещаются вниз, овал «плывёт»", C["fat"], C["fat_d"], 0.22),
        ("МЫШЦА", "ровный тонус", "гипертонус и спазм дают заломы", C["musc"], C["musc_d"], 0.34),
        ("КОСТЬ", "опора стабильна", "резорбция: опора проседает", C["bone"], C["bone_d"], 0.46),
    ]
    o = []
    o.append(f'<g data-at="0.02">{M(40, 44, "ЧЕТЫРЕ СЛОЯ · ЧЕТЫРЕ РАЗНЫХ СКОРОСТИ СТАРЕНИЯ", 9, fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.04">{S(40, 66, "Слои стареют не одновременно — поэтому одно средство не решает всё.", 10.5)}</g>')

    # ось времени
    o.append(f'<line x1="70" y1="100" x2="70" y2="520" stroke="{C["border"]}" stroke-width="2"/>')
    o.append(f'<g data-at="0.06">{M(70, 96, "25 ЛЕТ", 8.5, anchor="start")}'
             f'{M(70, 500, "65+", 8.5, anchor="start")}</g>')

    for i, (name, was, now, col, cold, at) in enumerate(rows):
        y = 108 + i * 100
        o.append(f'<g data-at="{at}">'
                 f'<rect x="96" y="{y}" width="800" height="86" rx="12" fill="{C["pale"]}" '
                 f'stroke="{C["border"]}"/>'
                 f'<rect x="96" y="{y}" width="8" height="86" rx="4" fill="{col}"/></g>')
        o.append(f'<g data-at="{at+0.03}">{B(122, y + 38, name, 13)}</g>')
        o.append(f'<g data-at="{at+0.05}">{S(122, y + 58, "что было", 9.5, fill=C["muted"])}</g>')
        o.append(f'<g data-at="{at+0.06}">{S(122, y + 74, was if len(was) < 30 else was[:29] + "…", 10)}</g>')
        o.append(f'<g data-at="{at+0.08}"><path d="M400,{y+43} L432,{y+43}" stroke="{C["accent"]}" '
                 f'stroke-width="1.4" marker-end="url(#agArr)"/></g>')
        o.append(f'<g data-at="{at+0.10}">{S(452, y + 38, "что стало к 60", 9.5, fill=C["accent"])}</g>')
        o.append(f'<g data-at="{at+0.11}">{B(452, y + 58, now, 11.5)}</g>')

    o.append(f'<g data-at="0.66">{S(40, 544, "Порядок неслучаен: кожа стареет первой и заметнее всего, кость — медленнее, "
                                            "но именно она задаёт форму лица.", 10.5)}</g>')
    return svg(W, H, "".join(o), marker("agArr", C["accent"]))


# =====================================================================
# A2 · ТРИ ТИПА СТАРЕНИЯ
# =====================================================================
def ag_types():
    W, H = 940, 400
    PW, GAP, TOP = 268, 22, 90

    o = []
    o.append(f'<g data-at="0.02">{M(40, 44, "ТРИ СЦЕНАРИЯ СТАРЕНИЯ · ТИП ОПРЕДЕЛЯЕТ ТАКТИКУ", 9, fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.04">{S(40, 66, "Одинаковый возраст выглядит по-разному: у кого-то сетка морщин, у кого-то «поплывший» овал.", 10.5)}</g>')

    types = [
        ("Мелкоморщинистый", "тонкая сухая кожа, густая сетка\nлиний, форма лица держится", 0.10),
        ("Деформационный", "кожа плотная, но овал тяжёлый,\nбрыли и отёчность, складки глубокие", 0.28),
        ("Усталый", "плоские щёки, западение\nпод глазами, «серое» выражение", 0.46),
    ]

    for i, (name, desc, at) in enumerate(types):
        x = 40 + i * (PW + GAP)
        cx = x + PW // 2
        o.append(panel(x, TOP - 16, PW, 218, at))
        o.append(f'<g data-at="{at+0.04}">')
        # овал лица
        o.append(f'<ellipse cx="{cx}" cy="{TOP+86}" rx="62" ry="84" fill="{C["skin"]}" '
                 f'stroke="{C["skin_d"]}" stroke-width="1.2"/>')
        o.append(f'<path d="M{cx-46},{TOP+120} Q{cx},{TOP+176} {cx+46},{TOP+120}" fill="none" '
                 f'stroke="{C["skin_d"]}" stroke-width="1"/>')
        o.append('</g>')

        if i == 0:  # мелкие морщины
            for k in range(7):
                yy = TOP + 30 + k * 14
                o.append(f'<g data-at="{at+0.06+k*0.01}">'
                         f'<path d="M{cx-54},{yy} q14,-5 28,0" fill="none" stroke="{C["musc_d"]}" stroke-width=".9"/>'
                         f'<path d="M{cx+26},{yy} q14,-5 28,0" fill="none" stroke="{C["musc_d"]}" stroke-width=".9"/></g>')
            o.append(f'<g data-at="{at+0.18}">'
                     f'<path d="M{cx-40},{TOP+58} q10,-8 20,0" fill="none" stroke="{C["accent"]}" stroke-width="1.3"/>'
                     f'<path d="M{cx+20},{TOP+58} q10,-8 20,0" fill="none" stroke="{C["accent"]}" stroke-width="1.3"/></g>')
        elif i == 1:  # брыли и тяжёлый овал
            o.append(f'<g data-at="{at+0.10}">'
                     f'<path d="M{cx-58},{TOP+118} q10,34 26,44" fill="none" stroke="{C["warn"]}" stroke-width="2"/>'
                     f'<path d="M{cx+58},{TOP+118} q-10,34 -26,44" fill="none" stroke="{C["warn"]}" stroke-width="2"/></g>')
            o.append(f'<g data-at="{at+0.14}">'
                     f'<path d="M{cx-30},{TOP+150} q14,10 28,0" fill="none" stroke="{C["warn"]}" stroke-width="1.2" '
                     f'stroke-dasharray="4 3"/></g>')
            o.append(f'<g data-at="{at+0.16}">'
                     f'<path d="M{cx-44},{TOP+96} q4,30 16,40" fill="none" stroke="{C["musc_d"]}" stroke-width="1.2"/>'
                     f'<path d="M{cx+44},{TOP+96} q-4,30 -16,40" fill="none" stroke="{C["musc_d"]}" stroke-width="1.2"/></g>')
        else:  # плоское лицо
            o.append(f'<g data-at="{at+0.10}">'
                     f'<ellipse cx="{cx-30}" cy="{TOP+62}" rx="16" ry="10" fill="#E6D2C4"/>'
                     f'<ellipse cx="{cx+30}" cy="{TOP+62}" rx="16" ry="10" fill="#E6D2C4"/></g>')
            o.append(f'<g data-at="{at+0.14}">'
                     f'<path d="M{cx-50},{TOP+80} q22,14 44,0" fill="none" stroke="{C["musc_d"]}" stroke-width="1.1" '
                     f'stroke-dasharray="3 3"/>'
                     f'<path d="M{cx-50},{TOP+130} q22,10 44,0" fill="none" stroke="{C["musc_d"]}" stroke-width="1.1" '
                     f'stroke-dasharray="3 3"/></g>')

        o.append(f'<g data-at="{at+0.20}">{B(cx, TOP + 232, name, 12, anchor="middle")}</g>')
        for k, line in enumerate(desc.split("\n")):
            o.append(f'<g data-at="{at+0.22}">{S(cx, TOP + 252 + k * 15, line, 9.5, anchor="middle")}</g>')

    o.append(f'<g data-at="0.72">{S(40, 372, "Чистых типов почти не бывает — обычно два-три признака сразу. "
                                            "Но ведущий признак существует, и он определяет, с чего начинать.", 10.5)}</g>')
    return svg(W, H, "".join(o))


# =====================================================================
# A3 · КУДА СМЕЩАЮТСЯ ЖИРОВЫЕ ПАКЕТЫ
# =====================================================================
def ag_gravity():
    W, H = 940, 520
    CX, CY = 330, 250

    o = []
    o.append(f'<g data-at="0.02">{M(40, 44, "ЖИР НЕ РАССАСЫВАЕТСЯ — ОН СПОЛЗАЕТ", 9, fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.04">{S(40, 66, "Пакеты жира на щеке смещаются вниз и внутрь. Отсюда складки, брыли и «второй подбородок».", 10.5)}</g>')

    # контур лица
    face = (f'M{CX},{CY-200} C{CX+115},{CY-200} {CX+165},{CY-90} {CX+165},{CY+10} '
            f'C{CX+165},{CY+120} {CX+110},{CY+215} {CX},{CY+235} '
            f'C{CX-110},{CY+215} {CX-165},{CY+120} {CX-165},{CY+10} '
            f'C{CX-165},{CY-90} {CX-115},{CY-200} {CX},{CY-200} Z')
    o.append(f'<g data-at="0.06"><path d="{face}" fill="{C["skin"]}" stroke="{C["skin_d"]}" stroke-width="1.4"/></g>')

    # нос и линия складки
    o.append(f'<g data-at="0.08"><path d="M{CX},{CY-40} L{CX-14},{CY+40} Q{CX},{CY+52} {CX+16},{CY+40}" '
             f'fill="none" stroke="{C["skin_d"]}" stroke-width="1.2"/></g>')
    for sgn in (-1, 1):
        o.append(f'<path d="M{CX+sgn*30},{CY+46} Q{CX+sgn*54},{CY+120} {CX+sgn*58},{CY+176}" fill="none" '
                 f'stroke="{C["warn"]}" stroke-width="1.4" opacity=".5" data-at="0.12" data-draw="1"/>')

    packs = [
        ("НОСОГУБНЫЙ", CX - 54, CY + 70, 0.24),
        ("МЕДИАЛЬНЫЙ ЩЁЧНЫЙ", CX - 92, CY - 20, 0.32),
        ("СРЕДНИЙ ЩЁЧНЫЙ", CX + 78, CY - 26, 0.40),
    ]
    for name, px, py, at in packs:
        o.append(f'<g data-at="{at}"><ellipse cx="{px}" cy="{py-26}" rx="42" ry="26" fill="none" '
                 f'stroke="{C["muted"]}" stroke-width="1" stroke-dasharray="4 4" opacity=".65"/>'
                 f'<ellipse cx="{px}" cy="{py}" rx="42" ry="26" fill="{C["fat"]}" '
                 f'stroke="{C["fat_d"]}" stroke-width="1.2"/></g>')
        o.append(f'<g data-at="{at+0.03}"><path d="M{px},{py+30} L{px},{py+72}" stroke="{C["warn"]}" '
                 f'stroke-width="1.8" marker-end="url(#agArr2)"/></g>')

    # подписи справа
    labels = [
        ("овал «поплыл»", "тяжёлая нижняя треть, брыли", CY + 96, 0.52),
        ("складка углубилась", "валик нависает над линией", CY + 26, 0.58),
        ("скула опустела", "объём ушёл вниз, щека плоская", CY - 44, 0.64),
    ]
    for title, sub, ly, at in labels:
        o.append(f'<g data-at="{at}"><line x1="{CX+170}" y1="{ly-6}" x2="620" y2="{ly-6}" '
                 f'stroke="{C["border"]}" stroke-dasharray="3 4"/>'
                 f'{B(632, ly, title, 11.5)}</g>')
        o.append(f'<g data-at="{at+0.02}">{S(632, ly + 16, sub, 10)}</g>')

    o.append(f'<g data-at="0.72">{S(40, 496, "Пунктиром показано, где пакет лежал в молодости. "
                                            "Вернуть его на место «массажем» нельзя — можно только поддержать или восполнить объём.", 10.5)}</g>')
    return svg(W, H, "".join(o), marker("agArr2", C["warn"]))


# =====================================================================
# B1 · ЧТО В ПРОБИРКЕ
# =====================================================================
def prp_layers():
    W, H = 940, 470
    TX, TW = 300, 130

    o = []
    o.append(f'<g data-at="0.02">{M(40, 44, "ЧТО ПРОИСХОДИТ С КРОВЬЮ В ПРОБИРКЕ", 9, fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.04">{S(40, 66, "Кровь — это не жидкость одного цвета. Центрифуга разделяет её на слои по плотности.", 10.5)}</g>')

    # пробирка
    o.append(f'<g data-at="0.08"><rect x="{TX}" y="96" width="{TW}" height="330" rx="14" '
             f'fill="{C["pale"]}" stroke="{C["border"]}" stroke-width="1.5"/>'
             f'<path d="M{TX},{96+330} q{TW/2},26 {TW},0" fill="none" stroke="{C["border"]}" stroke-width="1.5"/></g>')

    # слои (появляются по мере разделения)
    o.append(f'<g data-at="0.14"><rect x="{TX+3}" y="99" width="{TW-6}" height="120" rx="10" '
             f'fill="{C["plasma"]}" stroke="#D9BE5E"/></g>')
    o.append(f'<g data-at="0.26"><rect x="{TX+3}" y="221" width="{TW-6}" height="26" fill="#E7D9C0"/></g>')
    o.append(f'<g data-at="0.20"><rect x="{TX+3}" y="249" width="{TW-6}" height="174" rx="10" '
             f'fill="{C["blood"]}" stroke="#A95348"/></g>')

    # подписи внутри
    o.append(f'<g data-at="0.30">{M(TX+TW/2, 150, "ПЛАЗМА", 9, anchor="middle")}</g>')
    o.append(f'<g data-at="0.32">{S(TX+TW/2, 168, "светлая, жидкая", 9.5, anchor="middle")}</g>')
    o.append(f'<g data-at="0.34">{M(TX+TW/2, 214, "ТРОМБОЦИТЫ И ЛЕЙКОЦИТЫ", 7.5, anchor="middle")}</g>')
    o.append(f'<g data-at="0.26">{M(TX+TW/2, 300, "ЭРИТРОЦИТЫ", 9, anchor="middle", fill="#F7E9E5")}</g>')
    o.append(f'<g data-at="0.28">{S(TX+TW/2, 318, "клетки-переносчики", 9.5, anchor="middle", fill="#F7E9E5")}</g>')

    # пояснения справа
    notes = [
        ("Плазма — рабочий материал", "именно её вводят в кожу", 150, 0.40),
        ("Тонкое кольцо — самое ценное", "в нём тромбоциты, а в них факторы роста", 240, 0.48),
        ("Эритроциты тяжелее всех", "оседают вниз, в плазме их быть почти не должно", 330, 0.56),
    ]
    for title, sub, ny, at in notes:
        o.append(f'<g data-at="{at}"><line x1="{TX+TW+18}" y1="{ny-6}" x2="{TX+TW+56}" y2="{ny-6}" '
                 f'stroke="{C["border"]}" stroke-dasharray="3 4"/>'
                 f'{B(TX+TW+68, ny, title, 11)}</g>')
        o.append(f'<g data-at="{at+0.02}">{S(TX+TW+68, ny+16, sub, 9.5)}</g>')

    # стрелка центрифуги
    o.append(f'<g data-at="0.10"><circle cx="160" cy="260" r="52" fill="none" stroke="{C["border"]}" '
             f'stroke-width="1.4" stroke-dasharray="5 4"/>'
             f'<path d="M160,206 a54,54 0 0 1 40,16" fill="none" stroke="{C["brand"]}" stroke-width="2" '
             f'marker-end="url(#prArr)"/>'
             f'{M(160, 268, "ЦЕНТРИФУГА", 8.5, anchor="middle")}'
             f'{S(160, 284, "разделяет по весу", 9, anchor="middle")}</g>')

    o.append(f'<g data-at="0.66">{S(40, 434, "Чем аккуратнее разделение, тем меньше в плазме «лишних» клеток "
                                            "и тем предсказуемее результат.", 10.5)}</g>')
    o.append(f'<g data-at="0.68">{S(40, 452, "Это одна из причин, почему у двух клиник с одинаковым названием процедуры "
                                            "получается разный эффект.", 10.5)}</g>')
    return svg(W, H, "".join(o), marker("prArr", C["brand"]))


# =====================================================================
# B2 · КАК ПЛАЗМА РАБОТАЕТ
# =====================================================================
def prp_cascade():
    W, H = 940, 400
    BW, BH, GAP, TOP, X0 = 190, 116, 26, 150, 44

    steps = [
        ("ТРОМБОЦИТ", "клетка крови,\n«аптечка» внутри", 0.08),
        ("ФАКТОРЫ РОСТА", "выделяются при\nактивации", 0.20),
        ("ФИБРОБЛАСТ", "клетка, которая\nстроит коллаген", 0.34),
        ("НОВЫЙ КОЛЛАГЕН", "плотнее и\nэластичнее кожа", 0.48),
    ]

    o = []
    o.append(f'<g data-at="0.02">{M(40, 44, "ЦЕПОЧКА, КОТОРУЮ ЗАПУСКАЕТ ПЛАЗМА", 9, fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.04">{S(40, 66, "Плазма не «питает» кожу напрямую — она даёт сигнал клеткам, "
                                            "которые сами начинают работать.", 10.5)}</g>')

    for i, (title, desc, at) in enumerate(steps):
        x = X0 + i * (BW + GAP)
        o.append(f'<g data-at="{at}"><rect x="{x}" y="{TOP}" width="{BW}" height="{BH}" rx="12" '
                 f'fill="{C["stone"]}" stroke="{C["border"]}"/></g>')
        o.append(f'<g data-at="{at+0.02}">{M(x+16, TOP+26, f"{i+1}", 9, fill=C["accent"])}</g>')
        o.append(f'<g data-at="{at+0.04}">{B(x+16, TOP+52, title, 10.5)}</g>')
        for k, line in enumerate(desc.split("\n")):
            o.append(f'<g data-at="{at+0.06}">{S(x+16, TOP+74+k*15, line, 9.5)}</g>')
        if i < len(steps) - 1:
            o.append(f'<g data-at="{at+0.08}"><path d="M{x+BW+4},{TOP+BH/2} L{x+BW+GAP-6},{TOP+BH/2}" '
                     f'stroke="{C["accent"]}" stroke-width="1.6" marker-end="url(#pcArr)"/></g>')

    # побочная ветка — сосуды
    o.append(f'<g data-at="0.56"><path d="M{X0+BW+GAP+BW/2},{TOP+BH+2} L{X0+BW+GAP+BW/2},{TOP+BH+46}" '
             f'stroke="{C["gel_d"]}" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#pcArr2)"/>'
             f'{M(X0+BW+GAP+BW/2+12, TOP+BH+34, "и к сосудам: плотность капилляров", 9, fill=C["gel_d"])}</g>')

    o.append(f'<g data-at="0.62">{M(40, 306, "ЧТО ЭТО ЗНАЧИТ ДЛЯ ПАЦИЕНТА", 9)}</g>')
    o.append(f'<g data-at="0.64">{S(40, 328, "Эффект не мгновенный: клеткам нужно время, чтобы построить новый коллаген. "
                                            "Поэтому плазму не назначают «за неделю до события».", 10.5)}</g>')
    o.append(f'<g data-at="0.68">{S(40, 348, "И это же объясняет, почему результат накапливается курсом, а не с одного раза.", 10.5)}</g>')
    return svg(W, H, "".join(o), marker("pcArr", C["accent"]) + marker("pcArr2", C["gel_d"]))


# =====================================================================
# B3 · ОЖИДАНИЕ И РЕАЛЬНОСТЬ
# =====================================================================
def prp_curve():
    W, H = 940, 420
    AX0, AY0, AX1, AY1 = 90, 320, 860, 90

    o = []
    o.append(f'<g data-at="0.02">{M(40, 44, "КАК РАБОТАЕТ ЭФФЕКТ ВО ВРЕМЕНИ", 9, fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.04">{S(40, 66, "Красная линия — типичное ожидание. Зелёная — то, что обычно происходит.", 10.5)}</g>')

    # оси
    o.append(f'<line x1="{AX0}" y1="{AY1}" x2="{AX0}" y2="{AY0}" stroke="{C["border"]}" stroke-width="1.5"/>')
    o.append(f'<line x1="{AX0}" y1="{AY0}" x2="{AX1}" y2="{AY0}" stroke="{C["border"]}" stroke-width="1.5"/>')
    for k, m in enumerate(["0", "1", "3", "6", "12"]):
        x = AX0 + (AX1 - AX0) * (k / 4)
        o.append(f'<g data-at="0.05"><line x1="{x}" y1="{AY0}" x2="{x}" y2="{AY0+6}" stroke="{C["border"]}"/>'
                 f'{M(x, AY0+22, m, 9, anchor="middle")}</g>')
    o.append(f'<g data-at="0.06">{M(AX1-6, AY0+40, "МЕСЯЦЫ", 8.5, anchor="end")}</g>')
    o.append(f'<g data-at="0.06">{M(AX0-14, AY1, "ЭФФЕКТ", 8.5, anchor="end")}</g>')

    # ожидание
    exp = f"M{AX0},{AY0-6} C{AX0+150},{AY0-60} {AX0+320},{AY1+18} {AX1},{AY1+6}"
    o.append(f'<path d="{exp}" fill="none" stroke="{C["warn"]}" stroke-width="2.2" '
             f'stroke-dasharray="6 5" data-at="0.12" data-draw="1"/>')
    o.append(f'<g data-at="0.26">{B(AX1-10, AY1-4, "ожидание", 11, anchor="end", fill=C["warn"])}</g>')
    o.append(f'<g data-at="0.28">{S(AX1-10, AY1+14, "«с каждым разом всё лучше»", 9.5, anchor="end", fill=C["warn"])}</g>')

    # реальность
    real = (f"M{AX0},{AY0-4} C{AX0+60},{AY0-58} {AX0+130},{AY1+46} {AX0+215},{AY1+40} "
            f"C{AX0+330},{AY1+32} {AX0+420},{AY0-40} {AX1},{AY0-24}")
    o.append(f'<path d="{real}" fill="none" stroke="{C["gel_d"]}" stroke-width="2.6" '
             f'data-at="0.16" data-draw="1"/>')
    o.append(f'<g data-at="0.40">{B(AX0+150, AY1+22, "реальность", 11, fill=C["gel_d"])}</g>')

    # пик
    px = AX0 + (AX1 - AX0) * 0.42
    o.append(f'<g data-at="0.46"><line x1="{px}" y1="{AY0}" x2="{px}" y2="{AY1+44}" '
             f'stroke="{C["border"]}" stroke-dasharray="3 5"/>'
             f'{M(px+10, AY1+10, "ЗДЕСЬ ВИДЕН МАКСИМУМ", 8.5)}</g>')
    o.append(f'<g data-at="0.50">{S(px+10, AY1+26, "оценивать эффект раньше — бессмысленно", 10)}</g>')

    o.append(f'<g data-at="0.62">{S(40, 378, "Плазма не «подтягивает» лицо и не убирает гравитацию. "
                                            "Она улучшает качество кожи: плотность, ровность, мелкие линии.", 10.5)}</g>')
    o.append(f'<g data-at="0.66">{S(40, 398, "Если ждать от неё эффекта подтяжки — разочарование гарантировано. Это разные задачи.", 10.5)}</g>')
    return svg(W, H, "".join(o))


# =====================================================================
# C1 · ТРИ СЕМЕЙСТВА НИТЕЙ
# =====================================================================
def thr_types():
    W, H = 940, 420
    PW, GAP, TOP = 268, 22, 96

    o = []
    o.append(f'<g data-at="0.02">{M(40, 44, "ТРИ СЕМЕЙСТВА НИТЕЙ · РАЗНАЯ ЗАДАЧА", 9, fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.04">{S(40, 66, "Нить — это не «подтяжка без операции». Разные нити решают разные задачи.", 10.5)}</g>')

    items = [
        ("Гладкая", "армирование: сетка\nпод кожей, без объёма", 0.10, "mono"),
        ("Плетёная", "плотный каркас,\nбольше точек сцепления", 0.30, "braid"),
        ("Объёмная", "заполняет дефицит:\nспираль расправляется", 0.50, "coil"),
    ]

    for i, (name, desc, at, kind) in enumerate(items):
        x = 40 + i * (PW + GAP)
        cx = x + PW // 2
        o.append(panel(x, TOP - 16, PW, 176, at))
        o.append(f'<g data-at="{at+0.04}">')

        y0, y1 = TOP + 26, TOP + 120
        if kind == "mono":
            o.append(f'<line x1="{x+46}" y1="{y0}" x2="{x+PW-46}" y2="{y1}" stroke="{C["brand"]}" stroke-width="2"/>')
            for k in range(9):
                t = k / 8
                px = x + 46 + (PW - 92) * t
                py = y0 + (y1 - y0) * t
                o.append(f'<line x1="{px}" y1="{py-5}" x2="{px}" y2="{py+5}" stroke="{C["brand_s"]}" stroke-width="1.2"/>')
        elif kind == "braid":
            for off in (0, 6):
                d = "M" + f"{x+46},{y0+off} "
                for k in range(1, 9):
                    t = k / 8
                    px = x + 46 + (PW - 92) * t
                    py = y0 + 5 + (y1 - y0 - 10) * t + (8 if k % 2 else -8) + off
                    d += f"L{px:.0f},{py:.0f} "
                o.append(f'<path d="{d}" fill="none" stroke="{C["brand_s"]}" stroke-width="2"/>')
        else:
            o.append(f'<line x1="{x+46}" y1="{y0+47}" x2="{x+PW-46}" y2="{y0+47}" stroke="{C["brand"]}" stroke-width="1.6"/>')
            for k in range(9):
                px = x + 56 + k * 19
                o.append(f'<ellipse cx="{px}" cy="{y0+47}" rx="10" ry="17" fill="none" '
                         f'stroke="{C["accent"]}" stroke-width="1.6"/>')
        o.append('</g>')

        o.append(f'<g data-at="{at+0.12}">{B(cx, TOP + 190, name, 12.5, anchor="middle")}</g>')
        for k, line in enumerate(desc.split("\n")):
            o.append(f'<g data-at="{at+0.14}">{S(cx, TOP + 210 + k * 15, line, 9.5, anchor="middle")}</g>')

    o.append(f'<g data-at="0.70">{S(40, 386, "Толщина и длина подбираются под зону и задачу. "
                                            "Одинаковых «ниток для лица» не существует — как нет одинаковых шурупов для мебели и для стены.", 10.5)}</g>')
    return svg(W, H, "".join(o))


# =====================================================================
# C2 · КАРКАС ПРОТИВ ОБЪЁМА
# =====================================================================
def thr_mechanics():
    W, H = 940, 440
    PW = 420

    o = []
    o.append(f'<g data-at="0.02">{M(46, 44, "АРМИРОВАНИЕ", 9, fill=C["brand"])}</g>')
    o.append(f'<g data-at="0.02">{M(506, 44, "ВОЛЮМИЗАЦИЯ", 9, fill=C["accent"])}</g>')

    # левая панель — сетка
    o.append(panel(46, 62, PW, 268, 0.06))
    skin_l = "M62,240 L152,240 L188,170 L224,240 L452,240"
    o.append(f'<g data-at="0.10"><path d="{skin_l} L452,300 L62,300 Z" fill="url(#thSkin)" '
             f'stroke="{C["skin_d"]}" stroke-width="1"/></g>')
    o.append(f'<path d="{skin_l}" fill="none" stroke="{C["brand"]}" stroke-width="2" data-at="0.12" data-draw="1"/>')
    for k in range(4):
        o.append(f'<g data-at="{0.22+k*0.04}"><path d="M{120+k*80},258 L{188+k*40},196" '
                 f'stroke="{C["gel_d"]}" stroke-width="3" stroke-linecap="round"/>'
                 f'<path d="M{110+k*82},206 L{210+k*22},252" stroke="{C["gel_d"]}" stroke-width="3" '
                 f'stroke-linecap="round" opacity=".75"/></g>')
    o.append(f'<g data-at="0.44">{S(62, 316, "сетка держит кожу от повторного складывания", 10)}</g>')

    # правая панель — объём
    o.append(panel(506, 62, PW, 268, 0.08))
    skin_r = "M522,240 L612,240 L648,170 L684,240 L912,240"
    o.append(f'<g data-at="0.14"><path d="{skin_r} L912,300 L522,300 Z" fill="url(#thSkin2)" '
             f'stroke="{C["skin_d"]}" stroke-width="1"/></g>')
    o.append(f'<path d="{skin_r}" fill="none" stroke="{C["brand"]}" stroke-width="2" data-at="0.16" data-draw="1"/>')
    o.append(f'<g data-at="0.30"><ellipse cx="660" cy="252" rx="58" ry="26" fill="{C["gel"]}" '
             f'stroke="{C["gel_d"]}" stroke-width="1.4"/></g>')
    o.append(f'<g data-at="0.34"><path d="M660,226 L660,190" stroke="{C["accent"]}" stroke-width="1.8" '
             f'marker-end="url(#thArr)"/></g>')
    o.append(f'<g data-at="0.40">{S(522, 316, "объём приподнимает кожу изнутри", 10)}</g>')

    o.append(f'<g data-at="0.60">{S(46, 364, "Армирование отвечает на вопрос «чтобы не складывалось». "
                                            "Волюмизация — «чтобы было чем держать».", 10.5)}</g>')
    o.append(f'<g data-at="0.64">{S(46, 384, "Поэтому при выраженном дефиците объёма нити-сетка работают хуже: "
                                            "держать нечего, и каркас просто фиксирует пустоту.", 10.5)}</g>')
    o.append(f'<g data-at="0.68">{S(46, 412, "Обратное тоже верно: объём без поддержки сползает быстрее.", 10.5)}</g>')
    return svg(W, H, "".join(o),
               '<linearGradient id="thSkin" x1="0" y1="0" x2="0" y2="1">'
               f'<stop offset="0" stop-color="{C["skin"]}"/><stop offset="1" stop-color="#E6CCBC"/></linearGradient>'
               '<linearGradient id="thSkin2" x1="0" y1="0" x2="0" y2="1">'
               f'<stop offset="0" stop-color="{C["skin"]}"/><stop offset="1" stop-color="#E6CCBC"/></linearGradient>'
               + marker("thArr", C["accent"]))


# =====================================================================
# C3 · ЧТО ПРОИСХОДИТ ВО ВРЕМЕНИ
# =====================================================================
def thr_timeline():
    W, H = 940, 430
    AX0, AX1 = 170, 880
    TOP, ROWH = 120, 74

    o = []
    o.append(f'<g data-at="0.02">{M(46, 44, "ТРИ ПРОЦЕССА ИДУТ ОДНОВРЕМЕННО", 9, fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.04">{S(46, 66, "Нить работает не «сама по себе»: пока она рассасывается, ткань вокруг меняется.", 10.5)}</g>')

    ticks = ["0", "3 мес", "6 мес", "12 мес", "18 мес"]
    for k, t in enumerate(ticks):
        x = AX0 + (AX1 - AX0) * (k / 4)
        o.append(f'<g data-at="0.06"><line x1="{x}" y1="86" x2="{x}" y2="{TOP+ROWH*3+8}" '
                 f'stroke="{C["border"]}" stroke-dasharray="3 5"/>'
                 f'{M(x, 78, t, 9, anchor="middle")}</g>')

    rows = [
        ("МЕХАНИЧЕСКАЯ ПОДДЕРЖКА", "максимум сразу, дальше слабеет", C["brand"], 0.10,
         lambda x1, x2, y: f"M{x1},{y-26} C{x1+120},{y-26} {x1+180},{y+2} {x2},{y+4}"),
        ("НОВЫЙ КОЛЛАГЕН", "растёт медленно, держится дольше", C["accent"], 0.28,
         lambda x1, x2, y: f"M{x1},{y+4} C{x1+120},{y-34} {x1+260},{y-30} {x2},{y-16}"),
        ("САМА НИТЬ", "постепенно растворяется", C["muted"], 0.42,
         lambda x1, x2, y: f"M{x1},{y-26} C{x1+200},{y-20} {x1+300},{y+6} {x2},{y+16}"),
    ]

    for i, (name, sub, col, at, pathf) in enumerate(rows):
        y = TOP + i * ROWH + 20
        o.append(f'<g data-at="{at}">{M(46, y-14, name, 8.5, fill=col)}</g>')
        o.append(f'<g data-at="{at}">{S(46, y+2, sub, 9.5)}</g>')
        o.append(f'<path d="{pathf(AX0, AX1, y)}" fill="none" stroke="{col}" stroke-width="2.4" '
                 f'data-at="{at+0.06}" data-draw="1"/>')

    o.append(f'<g data-at="0.60">{S(46, 366, "Практический смысл: первые недели лицо держит нить, "
                                            "а через полгода — уже собственная ткань, которая уплотнилась вокруг неё.", 10.5)}</g>')
    o.append(f'<g data-at="0.64">{S(46, 386, "Именно поэтому результат оценивают не через три дня, а через несколько месяцев.", 10.5)}</g>')
    o.append(f'<g data-at="0.68">{S(46, 412, "Сроки на схеме — ориентир, а не гарантия: они зависят от материала, зоны и самой ткани.", 10)}</g>')
    return svg(W, H, "".join(o))


# =====================================================================
# NB · ТРИ МЕСТА ПРИЛОЖЕНИЯ (без доз)
# =====================================================================
def nl_botox():
    W, H = 900, 560
    CX = 430

    defs = ('<radialGradient id="nbSkin" cx="50%" cy="40%" r="65%">'
            f'<stop offset="0" stop-color="#FAF1E8"/><stop offset="1" stop-color="#EFDCCD"/></radialGradient>'
            + marker("nbArr", C["warn"]))

    o = []
    nose = (f'M{CX},150 C{CX-26},176 {CX-34},220 {CX-46},262 '
            f'C{CX-56},300 {CX-58},330 {CX-44},348 '
            f'C{CX-30},364 {CX-14},368 {CX},366 '
            f'C{CX+14},368 {CX+30},364 {CX+44},348 '
            f'C{CX+58},330 {CX+56},300 {CX+46},262 '
            f'C{CX+34},220 {CX+26},176 {CX},150 Z')
    o.append(f'<g data-at="0.02"><path d="{nose}" fill="url(#nbSkin)" stroke="{C["skin_d"]}" stroke-width="1.4"/></g>')
    o.append(f'<g data-at="0.06"><ellipse cx="{CX-22}" cy="350" rx="16" ry="9" fill="#E5CFC0" '
             f'stroke="{C["musc_d"]}"/><ellipse cx="{CX+22}" cy="350" rx="16" ry="9" '
             f'fill="#E5CFC0" stroke="{C["musc_d"]}"/></g>')
    for sgn in (-1, 1):
        o.append(f'<path d="M{CX+sgn*40},368 C{CX+sgn*58},404 {CX+sgn*66},446 {CX+sgn*70},492" '
                 f'fill="none" stroke="{C["accent"]}" stroke-width="1.6" opacity=".5" '
                 f'data-at="0.12" data-draw="1"/>')
    o.append(f'<g data-at="0.14">{M(CX, 512, "НОСОГУБНАЯ СКЛАДКА", 8, anchor="middle")}</g>')

    o.append(f'<g data-at="0.24"><circle cx="{CX+96}" cy="356" r="14" fill="none" stroke="{C["brand"]}" stroke-width="1.6"/>'
             f'<circle cx="{CX+96}" cy="356" r="4.5" fill="{C["brand"]}"/>'
             f'<path d="M{CX+112},356 L{CX+150},356" stroke="{C["border"]}"/>'
             f'{M(CX+156, 344, "НИЖЕ У КРЫЛА НОСА", 8, fill=C["brand"])}</g>')
    o.append(f'<g data-at="0.26">{S(CX+156, 358, "расслабляет мышцу сильно:", 10)}'
             f'{S(CX+156, 372, "губа поднимается меньше", 10)}</g>')

    o.append(f'<g data-at="0.38"><circle cx="{CX+44}" cy="238" r="14" fill="none" stroke="{C["brand_s"]}" '
             f'stroke-width="1.6" stroke-dasharray="4 3"/>'
             f'<circle cx="{CX+44}" cy="238" r="4.5" fill="{C["brand_s"]}"/>'
             f'<path d="M{CX+58},238 L{CX+150},232" stroke="{C["border"]}"/>'
             f'{M(CX+156, 222, "ВЫШЕ, НА СКАТЕ НОСА", 8, fill=C["brand_s"])}</g>')
    o.append(f'<g data-at="0.40">{S(CX+156, 236, "мягче: убирает тягу,", 10)}'
             f'{S(CX+156, 250, "почти не трогая губу", 10)}</g>')

    o.append(f'<g data-at="0.52"><circle cx="{CX-70}" cy="432" r="11" fill="none" stroke="{C["warn"]}" stroke-width="1.5"/>'
             f'<circle cx="{CX-70}" cy="432" r="4" fill="{C["warn"]}"/>'
             f'<circle cx="{CX-64}" cy="472" r="11" fill="none" stroke="{C["warn"]}" stroke-width="1.5"/>'
             f'<circle cx="{CX-64}" cy="472" r="4" fill="{C["warn"]}"/>'
             f'<path d="M{CX-84},452 L{CX-150},452" stroke="{C["border"]}"/>'
             f'{M(CX-156, 440, "ПО ХОДУ СКЛАДКИ", 8, anchor="end", fill=C["warn"])}</g>')
    o.append(f'<g data-at="0.54">{S(CX-156, 454, "самый осторожный вариант:", 10, anchor="end")}'
             f'{S(CX-156, 468, "эффект скромный, риск ниже", 10, anchor="end")}</g>')

    o.append(f'<g data-at="0.64"><path d="M{CX-64},392 Q{CX},404 {CX+64},392" fill="none" '
             f'stroke="{C["warn"]}" stroke-width="1" stroke-dasharray="4 4"/>'
             f'{M(CX, 388, "КРАСНАЯ КАЙМА — НЕ МЕСТО ДЛЯ УКОЛА", 8, anchor="middle", fill=C["warn"])}</g>')

    o.append(f'<g data-at="0.72">{S(34, 546, "Речь об одной и той же мышце. Разница только в том, какую её часть "
                                            "расслабляют — и насколько.", 10.5)}</g>')
    return svg(W, H, "".join(o), defs)


# =====================================================================
# NB2 · ТРИ СПОСОБА ПОМОЧЬ СКЛАДКЕ (вместо протокола)
# =====================================================================
def nl_ways():
    W, H = 940, 430
    PW, GAP, TOP = 268, 22, 108

    o = []
    o.append(f'<g data-at="0.02">{M(40, 44, "ТРИ РАЗНЫХ СПОСОБА · ТРИ РАЗНЫХ РЕЗУЛЬТАТА", 9, fill=C["accent"])}</g>')
    o.append(f'<g data-at="0.04">{S(40, 66, "Выбор начинается не с препарата, а с вопроса: чего именно не хватает?", 10.5)}</g>')

    items = [
        ("Расслабить мышцу", "ботулотоксин", "снимает тягу, которая\nформирует перепад", "не добавит объёма\nи не разгладит кожу",
         C["brand"], 0.10, "musc"),
        ("Восстановить опору", "филлер", "возвращает объём там,\nгде просела кость", "не работает против\nмышцы и гравитации",
         C["accent"], 0.30, "gel"),
        ("Укрепить каркас", "нити, аппаратные методики", "уплотняет ткань,\nдержит от провисания", "не заменяет объём\nи не убирает тягу",
         C["gel_d"], 0.50, "thread"),
    ]

    for i, (name, tool, gives, notgives, col, at, kind) in enumerate(items):
        x = 40 + i * (PW + GAP)
        cx = x + PW // 2
        o.append(panel(x, TOP - 18, PW, 236, at))
        o.append(f'<g data-at="{at+0.03}"><rect x="{x}" y="{TOP-18}" width="{PW}" height="4" rx="2" fill="{col}"/></g>')
        o.append(f'<g data-at="{at+0.05}">{B(x + 18, TOP + 14, name, 12)}</g>')

        # пиктограмма
        if kind == "musc":
            o.append(f'<g data-at="{at+0.08}"><ellipse cx="{cx}" cy="{TOP+62}" rx="46" ry="16" fill="{C["musc"]}" '
                     f'stroke="{C["musc_d"]}" stroke-width="1.2"/>'
                     f'<path d="M{cx-70},{TOP+62} L{cx-52},{TOP+62}" stroke="{C["brand"]}" stroke-width="2"/>'
                     f'<path d="M{cx+52},{TOP+62} L{cx+70},{TOP+62}" stroke="{C["brand"]}" stroke-width="2" opacity=".4"/></g>')
        elif kind == "gel":
            o.append(f'<g data-at="{at+0.08}"><ellipse cx="{cx}" cy="{TOP+62}" rx="40" ry="26" fill="{C["gel"]}" '
                     f'stroke="{C["gel_d"]}" stroke-width="1.3"/>'
                     f'<ellipse cx="{cx}" cy="{TOP+62}" rx="16" ry="9" fill="#fff" opacity=".5"/></g>')
        else:
            o.append(f'<g data-at="{at+0.08}">')
            for k in range(3):
                o.append(f'<path d="M{cx-34+k*34},{TOP+40} L{cx-14+k*34},{TOP+84}" stroke="{col}" '
                         f'stroke-width="2" stroke-linecap="round"/>')
            o.append(f'<path d="M{cx-46},{TOP+62} L{cx+46},{TOP+62}" stroke="{col}" stroke-width="2" '
                     f'stroke-linecap="round" opacity=".5"/></g>')

        o.append(f'<g data-at="{at+0.12}">{S(x+18, TOP+120, tool, 9.5, fill=col)}</g>')
        o.append(f'<g data-at="{at+0.14}">{M(x+18, TOP+144, "ЧТО ДАЁТ", 8)}</g>')
        for k, line in enumerate(gives.split("\n")):
            o.append(f'<g data-at="{at+0.16}">{S(x+18, TOP+162+k*15, line, 9.5)}</g>')
        o.append(f'<g data-at="{at+0.18}">{M(x+18, TOP+200, "ЧЕГО НЕ ДЕЛАЕТ", 8, fill=C["warn"])}</g>')
        for k, line in enumerate(notgives.split("\n")):
            o.append(f'<g data-at="{at+0.20}">{S(x+18, TOP+218+k*15, line, 9.5)}</g>')

    o.append(f'<g data-at="0.72">{S(40, 400, "Работающая тактика почти всегда составная и почти всегда разнесена во времени. "
                                            "Обещание «всё одним уколом» — маркер некомпетентности, а не смелости.", 10.5)}</g>')
    return svg(W, H, "".join(o))


FIGURES = {
    "ag-layers": ag_layers,
    "ag-types": ag_types,
    "ag-gravity": ag_gravity,
    "prp-layers": prp_layers,
    "prp-cascade": prp_cascade,
    "prp-curve": prp_curve,
    "thr-types": thr_types,
    "thr-mechanics": thr_mechanics,
    "thr-timeline": thr_timeline,
    "nl-botox": nl_botox,
    "nl-ways": nl_ways,
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
        if left < -3 or left + w > W + 3:
            probs.append(f"{name}: «{content[:30]}» x={left:.0f}..{left+w:.0f} (W={W:.0f})")
        if y < 8 or y > H - 3:
            probs.append(f"{name}: «{content[:30]}» y={y} (H={H:.0f})")
        boxes.append((content[:24], left, y - size * 0.8, left + w, y + size * 0.25))
    for i, a in enumerate(boxes):
        for b in boxes[i + 1:]:
            if min(a[3], b[3]) - max(a[1], b[1]) > 3 and min(a[4], b[4]) - max(a[2], b[2]) > 2:
                probs.append(f"{name}: наложение «{a[0]}» и «{b[0]}»")
    return probs


if __name__ == "__main__":
    allp = []
    for name, fn in FIGURES.items():
        s = fn()
        open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8").write(s)
        cairosvg.svg2png(bytestring=s.encode(), write_to=os.path.join(OUT, name + ".png"),
                         output_width=1300, background_color="#FAF7F2")
        p = validate(name, s)
        allp += p
        print(f"{name:16} {len(s)/1024:5.1f} КБ  {'OK' if not p else str(len(p)) + ' замечаний'}")
    if allp:
        print("\nЗАМЕЧАНИЯ:")
        for x in allp:
            print("  •", x)
        sys.exit(1)
    print("\nВсе подписи в пределах холста, наложений нет.")
