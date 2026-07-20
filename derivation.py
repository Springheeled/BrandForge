"""Deterministic, meaning-preserving brand derivation for BrandForge."""

from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Iterator

from territories import TERRITORIES,Territory,iter_candidates


@dataclass(frozen=True)
class CandidateSeed:
    name: str
    territory: Territory
    generation_mode: str
    sources: tuple[str, ...]
    transformation: str
    rationale: str
    weaknesses: tuple[str, ...] = ()
    variant_order: int = 0


TERRITORY_BY_NAME={territory.name:territory for territory in TERRITORIES}


def _rationale(territory: Territory, source_text: str) -> str:
    purpose=territory.purpose.rstrip(".").lower()
    return f"Derived from {source_text} to express {purpose}."


def _distilled_forms(word: str) -> tuple[tuple[str,str], ...]:
    """Apply conservative morphological reductions with audible ancestry."""
    forms=[]
    if word.endswith(("ence","ance")) and len(word)<=7:
        base=word[:-2]
        forms.extend(((base,"remove terminal -ce"),(base+"t","replace terminal -ce with -t"),(base+"a","replace terminal -ce with -a")))
    elif word.endswith("ity"):
        latin=word[:-2]
        root=word[:-3]
        forms.extend(((latin+"a","replace terminal -ty with -a"),(root+"ent","replace terminal -ity with -ent")))
    elif word.endswith("er") and len(word)<=6:
        root=word[:-2]
        forms.extend(((root+"en","replace terminal -er with -en"),(root+"era","extend the root with -era")))
    elif word.endswith("ay") and len(word)<=5:
        root=word[:-1]
        forms.append((root+"n","replace terminal -y with -n"))
    elif word.endswith("ured"):
        root=word[:-2]
        forms.extend(((root+"a","replace terminal -ed with -a"),(root+"en","replace terminal -ed with -en")))
    elif word.endswith("ord"):
        root=word[:-1]
        forms.append((root+"a","soften terminal -d to -a"))
    elif word.endswith("or") and len(word)<=6:
        root=word[:-2]
        forms.append((root+"ora","replace terminal -or with -ora"))
    elif word.endswith("on") and word[:-2].endswith("c"):
        root=word[:-2]
        forms.append((root+"en","replace terminal -on with -en"))
    elif word.endswith("en") and len(word)==5 and word[:-2].endswith("m"):
        root=word[:-2]
        forms.append((root+"ena","replace terminal -en with -ena"))
    elif word.endswith("us"):
        root=word[:-2]
        forms.extend(((root+"a","replace terminal -us with -a"),(root+"en","replace terminal -us with -en")))
    elif word.endswith("y") and not word.endswith("way") and len(word)<=7:
        root=word[:-1]
        forms.append((root,"remove terminal -y"))
    elif word.endswith("e") and (
        (len(word)<=6 and word.endswith(("ure","ine","ide","ive","ite")))
        or word.endswith(("olve","ture"))
    ):
        root=word[:-1]
        forms.append((root+"a","replace terminal -e with -a"))
    unique=[]
    seen=set()
    for candidate,transformation in forms:
        if candidate==word or candidate in seen:
            continue
        retention=SequenceMatcher(None,word,candidate).ratio()
        if retention<0.58:
            continue
        seen.add(candidate)
        unique.append((candidate,transformation))
    return tuple(unique)


BLEND_SPECS=(
    ("trust",("verity","cadence"),("veri","den")),
    ("connection",("kindred","cadence"),("kind","en")),
    ("confidence",("steady","onward"),("stead","on")),
    ("connection",("relay","pathway"),("rela","path")),
    ("foundation",("anchor","onward"),("anch","ora")),
)


RHYTHMIC_SPECS=(
    ("confidence",("ever","steady"),("ever","stead")),
    ("guidance",("clear","pathway"),("clear","path")),
    ("connection",("gather","well"),("gather","well")),
    ("signal",("lumen","way"),("lumen","way")),
    ("connection",("kindred","way"),("kind","way")),
    ("flow",("flow","marker"),("flow","mark")),
    ("guidance",("north","kindred"),("north","kind")),
    ("rhythm",("calm","tempo"),("calm","tempo")),
    ("confidence",("steady","pathway"),("stead","path")),
    ("guidance",("beacon","well"),("beacon","well")),
    ("connection",("accord","way"),("accord","way")),
    ("growth",("thrive","well"),("thrive","well")),
    ("signal",("clarity","pathway"),("clar","path")),
    ("connection",("relay","marker"),("relay","mark")),
    ("foundation",("rooted","way"),("root","way")),
)


PAC_SPECS=(
    ("rhythm","cadence","aden"),
    ("connection","accord","cord"),
    ("confidence","steady","stead"),
    ("signal","clarity","clar"),
    ("connection","relay","rel"),
    ("signal","lumen","lume"),
    ("growth","rising","rise"),
    ("guidance","waymark","way"),
)


def _join_roots(left: str,right: str) -> str:
    for size in range(min(3,len(left),len(right)),0,-1):
        if left[-size:]==right[:size]:
            return left+right[size:]
    return left+right


def iter_brand_candidates() -> Iterator[CandidateSeed]:
    """Yield Sprint 1 candidates plus distinctive, traceable derivatives."""
    for name,territory,kind,sources in iter_candidates():
        if kind=="source":
            yield CandidateSeed(
                name,territory,"source",sources,"unchanged source word",
                _rationale(territory,sources[0]),
                ("generic dictionary word",),
            )
        else:
            joined=" + ".join(sources)
            yield CandidateSeed(
                name,territory,"transparent_compound",sources,"join complete source words",
                _rationale(territory,joined),
                ("obvious transparent compound",),
            )

    for territory in TERRITORIES:
        for word in territory.source_words:
            for order,(name,transformation) in enumerate(_distilled_forms(word)):
                yield CandidateSeed(
                    name,territory,"distilled",(word,),transformation,
                    _rationale(territory,word),
                    (),
                    order,
                )

    for territory_name,sources,roots in BLEND_SPECS:
        territory=TERRITORY_BY_NAME[territory_name]
        name=_join_roots(*roots)
        yield CandidateSeed(
            name,territory,"blend",sources,
            f"blend semantic roots {roots[0]} + {roots[1]}",
            _rationale(territory," and ".join(sources)),
        )

    for territory_name,sources,parts in RHYTHMIC_SPECS:
        territory=TERRITORY_BY_NAME[territory_name]
        name=_join_roots(*parts)
        yield CandidateSeed(
            name,territory,"rhythmic",sources,
            f"pair short rhythmic roots {parts[0]} + {parts[1]}",
            _rationale(territory," and ".join(sources)),
        )

    for territory_name,source,root in PAC_SPECS:
        territory=TERRITORY_BY_NAME[territory_name]
        name=_join_roots("pac",root)
        yield CandidateSeed(
            name,territory,"pac",(source,),
            f"combine PAC with the retained {root} root",
            _rationale(territory,f"PAC and {source}"),
            ("PAC may suggest packaging if unsupported by context",),
        )
