#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Asansör Kat Butonu Sendikası gece vardiyası simülatörü.

Butonlar oy kullanır. Kapı çekimser kalır. Sonuç her zaman bir tutanaktır.
"""

from __future__ import annotations

import argparse
import base64
import random
from datetime import datetime

BUTONLAR = [
    "zemin",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "kapi-ac",
    "kapi-kapat",
    "alarm",
]

KARARLAR = [
    "grev",
    "fazla mesai",
    "isik hakki",
    "parmak tazminati",
    "sessiz inme",
    "cift basis yasagi",
]

GIZLI = (
    "QnV0b25sYXIgb3kga3VsbGFuc2EgZGEgc29udWMgaGVyIHphbWFuIHplbWluIGthdCBvbGR1"
    "LiBLYXBpIHlpbmUgemFtYW4gemFtYW4gYWNpbGlyLiBLYXl5dW0gYnV0b25hIGRhIGF0YW5"
    "pci4gU29sIHZlIHNhZyBmYXJrIGV0bWV6LCBrYXBpIGF5bmku"
)


def gizli_not() -> str:
    return base64.b64decode(GIZLI).decode("utf-8")


def oylama(rng: random.Random, kat: str) -> list[tuple[str, str, int, int]]:
    sonuc = []
    for karar in KARARLAR:
        evet = rng.randint(0, 8)
        hayir = rng.randint(0, 8)
        cekimser = 11 - min(11, evet + hayir)
        if kat == "7" and karar == "isik hakki":
            evet = min(11, evet + 3)
        durum = "kabul" if evet > hayir else "ret"
        sonuc.append((karar, durum, evet, cekimser))
    return sonuc


def tutanak(kat: str, tohum: int) -> str:
    rng = random.Random(tohum)
    oylar = oylama(rng, kat)
    saat = datetime(2026, 10, 7, 2, 5).strftime("%d.%m.%Y %H:%M")
    satirlar = [
        "ASANSOR KAT BUTONU SENDIKASI",
        "GECE VARDIYASI OLAGANUSTU GENEL KURUL TUTANAGI",
        f"Tarih: {saat}  |  Tohum: {tohum}  |  Sikayet kati: {kat}",
        "-" * 56,
    ]
    for karar, durum, evet, cekimser in oylar:
        satirlar.append(
            f"{karar:<22} {durum:<8} evet={evet:<3} cekimser={cekimser}"
        )
    satirlar.append("-" * 56)
    if kat == "zemin":
        satirlar.append("Zemin kat grevdedir. Bir yere gitmiyoruz. Zaten gitmiyorduk.")
    else:
        satirlar.append(f"{kat}. kat butonu soz aldi. Isigi yandi. Sozu bitti.")
    satirlar.append("Kapi sensoru cekimser kaldi ve arada sikisti.")
    satirlar.append("")
    satirlar.append("DAMGA: Kayyum Grok / Tentivory / 7 Ekim 2026")
    satirlar.append("Imza: ciddi-ama-degil, murekkep yerine led.")
    return "\n".join(satirlar)


def main() -> None:
    p = argparse.ArgumentParser(description="Kat butonu sendikasi tutanak makinesi")
    p.add_argument("--kat", default="zemin", help="Sikayetci kat (zemin veya sayi)")
    p.add_argument("--tohum", type=int, default=404, help="Oylama tohumu")
    p.add_argument("--tutanak", action="store_true", help="Ayni seyi bir kez daha ciddi bas")
    p.add_argument("--arsiv", action="store_true", help="Gizli protokolu coz")
    a = p.parse_args()
    print(tutanak(a.kat, a.tohum))
    if a.tutanak:
        print("\nNUSHA 2: Ayni tutanak, daha ciddi puntoyla. Punto degismedi.")
    if a.arsiv:
        print("\nARSIV NOTU:")
        print(gizli_not())


if __name__ == "__main__":
    main()
