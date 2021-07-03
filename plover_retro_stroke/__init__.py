#!/usr/bin/env python

from typing import *
import itertools
from plover.translation import Translator, Stroke, Translation

def flatten(x: List[List]) -> List:
    return list(itertools.chain.from_iterable(x))

def retro_stroke(translator: Translator, stroke: Stroke, cmdline: str):
    args = cmdline.split(",")
    separator = args[0] or " "
    before = args[1] or ""
    after = args[2] or ""

    all_translations = translator.get_state().translations
    affected_translation_cnt = len(list(
        itertools.takewhile(
            lambda x: x.strokes[-1] == stroke,
            reversed(all_translations)
        )
    ))
    affected_translations = all_translations[-(affected_translation_cnt + 1):]
    affected_strokes = flatten([x.strokes for x in affected_translations])
    result = separator.join([x.rtfcre for x in reversed(list(itertools.dropwhile(
        lambda x: x == stroke,
        reversed(affected_strokes)
    )))])
    my_trans = Translation(affected_strokes + [stroke], before + result + after)
    my_trans.replaced = affected_translations
    translator.translate_translation(my_trans)


