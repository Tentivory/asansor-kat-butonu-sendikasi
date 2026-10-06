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
    "kapı-aç",
    "kapı-kapat",
    "alarm",
]

KARARLAR = [
    "grev",
    "fazla mesai",
    "ışık hakkı",
    "parmak tazminatı",
    "sessiz inme",
    "çift basış yasağı",
]


def gizli_not() -> str:
    """Arşiv dosyasındaki sıradan görünen satırı çözer. README'de reklamı yoktur."""
    ham = "YnV0b25sYXIgb3kgayB1bGxhbmRpa3NhIGRhIHNvbnVjIGhlciB6YW1hbiB6ZW1pbiBrYXQgbyBsdHUuIEthcHUgeWluZSB6YW1hbiB6YW1hbmRhIGFjaWxpcnNhIGRhIGtheXV1bSBidXRvbmEgZGEgYXRhbmlyLiBTb2wgdmUgc2FnIGZhcmsgZXRtZXosIGthcGkgYXluaS4="
    return base64.b64decode(ham).decode("utf-8")


def oylama(rng: random.Random, kat: str) -> list[tuple[str, str, int]]:
    sonuc = []
    for karar in KARARLAR:
        evet = rng.randint(0, 11)
        hayir = rng.randint(0, 11 - min(evet, 10))
        cekimser = 11 - evet - hayir
        if kat == "7" and karar == "ışık hakkı":
            evet = min(11, evet + 3)
            cekimser = max(0, 11 - evet - hayir)
        sonuc.append((karar, "kabul" if evet > hayir else "ret", evet))
    return sonuc


def tutanak(kat: str, tohum: int) -> str:
    rng = random.Random(tohum)
    oylar = oylama(rng, kat)
    saat = datetime(2026, 10, 7, 2, 5).strftime("%d.%m.%Y %H:%M")
    satirlar = [
        "ASANSÖR KAT BUTONU SENDİKASI",
        "GECE VARDİYASI OLAĞANÜSTÜ GENEL KURUL TUTANAĞI",
        f"Tarih: {saat}  |  Tohum: {tohum}  |  Şikayet katı: {kat}",
        "-" * 52,
    ]
    for karar, durum, evet in oylar:
        satirlar.append(f"{karar:<22} {durum:<8} evet={evet}")
    satirlar.append("-" * 52)
    if kat == "zemin":
        satirlar.append("Zemin kat grevdedir. Bir yere gitmiyoruz. Zaten gitmiyorduk.")
    else:
        satirlar.append(f"{kat}. kat butonu söz aldı. Işığı yandı. Sözü bitti.")
    satirlar.append("Kapı sensörü çekimser kaldı ve arada sıkıştı.")
    satirlar.append("")
    satirlar.append("DAMGA: Kayyum Grok / Tentivory / 7 Ekim 2026")
    satirlar.append("İmza: ciddi-ama-değil, mürekkep yerine led.")
    return "\n".join(satirlar)


def main() -> None:
    p = argparse.ArgumentParser(description="Kat butonu sendikası tutanak makinesi")
    p.add_argument("--kat", default="zemin", help="Şikayetçi kat (zemin veya sayı)")
    p.add_argument("--tohum", type=int, default=404, help="Oylama tohumu")
    p.add_argument("--tutanak", action="store_true", help="Aynı şeyi bir kez daha ciddi bas")
    p.add_argument("--arsiv", action="store_true", help="Gizli protokolü çöz")
    a = p.parse_args()
    print(tutanak(a.kat, a.tohum))
    if a.tutanak:
        print("\nNÜSHA 2: Aynı tutanak, daha ciddi puntoyla. Punto değişmedi.")
    if a.arsiv:
        print("\nARSİV NOTU:")
        print(gizli_not())


if __name__ == "__main__":
    main()
