"""Meaning-led source material for BrandForge.

Every candidate is either a complete source word or a curated compound of
complete source words. There are no arbitrary syllables in this module.
"""

from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class Territory:
    name: str
    purpose: str
    source_words: tuple[str, ...]
    compounds: tuple[tuple[str, str], ...]
    warmth: int
    professionalism: int


TERRITORIES = (
    Territory(
        "confidence",
        "Quiet certainty, composure and control.",
        ("assured", "steady", "poise", "certain", "secure", "resolve", "composed", "grounded"),
        (("true", "hold"), ("sure", "foot"), ("calm", "stead"), ("steady", "way"),
         ("calm", "guide"), ("sure", "path"), ("true", "base"), ("poise", "well")),
        82,
        93,
    ),
    Territory(
        "rhythm",
        "Repeatable work moving at a natural pace.",
        ("cadence", "tempo", "pulse", "measure", "pattern", "harmony", "motion", "balance", "sequence"),
        (("flow", "beat"), ("calm", "tempo"), ("true", "pulse"), ("even", "flow"),
         ("even", "pace"), ("work", "pace"), ("flow", "pace"), ("calm", "beat")),
        84,
        88,
    ),
    Territory(
        "flow",
        "Frictionless movement and operational ease.",
        ("current", "stream", "glide", "fluent", "onward", "smooth", "channel", "course"),
        (("clear", "flow"), ("flow", "line"), ("flow", "path"), ("stream", "way"),
         ("glide", "path"), ("ease", "flow"), ("calm", "flow"), ("open", "flow"),
         ("flow", "well"), ("smooth", "way")),
        91,
        86,
    ),
    Territory(
        "guidance",
        "Clear direction and confident next steps.",
        ("beacon", "compass", "lantern", "north", "guide", "pathway", "waymark", "bearing", "orient", "pilot"),
        (("true", "north"), ("clear", "path"), ("north", "way"), ("guide", "post"),
         ("way", "finder"), ("path", "light"), ("beacon", "way"), ("sure", "guide"),
         ("clear", "way"), ("north", "mark")),
        86,
        92,
    ),
    Territory(
        "growth",
        "Healthy progress that scales with the customer.",
        ("thrive", "flourish", "bloom", "rising", "ascend", "scale", "progress", "prosper", "expand", "unfold"),
        (("ever", "rise"), ("grow", "well"), ("rise", "well"), ("thrive", "on"),
         ("bloom", "way"), ("grow", "path"), ("ever", "grow"), ("rise", "ward"),
         ("thrive", "way")),
        92,
        85,
    ),
    Territory(
        "journey",
        "Forward movement with a dependable companion.",
        ("onward", "venture", "passage", "voyage", "route", "horizon", "stride", "explore"),
        (("true", "path"), ("path", "wise"), ("way", "bound"), ("stride", "on"),
         ("venture", "on"), ("path", "ward"), ("course", "way"), ("sure", "way")),
        87,
        83,
    ),
    Territory(
        "foundation",
        "A stable base for operations and growth.",
        ("anchor", "bedrock", "rooted", "ground", "solid", "basis", "footing", "steadfast"),
        (("true", "base"), ("firm", "base"), ("root", "well"), ("firm", "root"),
         ("rooted", "way"), ("solid", "base"), ("anchor", "way"), ("base", "point")),
        74,
        95,
    ),
    Territory(
        "connection",
        "People, channels and work joined together.",
        ("accord", "kinship", "weave", "thread", "unite", "relay", "nexus", "gather", "joined", "kindred"),
        (("true", "bond"), ("link", "well"), ("weave", "way"), ("join", "path"),
         ("bond", "line"), ("accord", "way"), ("kin", "link"), ("join", "way")),
        93,
        84,
    ),
    Territory(
        "signal",
        "Visibility that makes the next action obvious.",
        ("signal", "beacon", "lumen", "clarity", "bright", "lucid", "notice", "marker", "pulse"),
        (("clear", "line"), ("bright", "way"), ("true", "mark"), ("clear", "view"),
         ("sign", "post"), ("light", "way"), ("lucid", "path"), ("signal", "way")),
        77,
        91,
    ),
    Territory(
        "trust",
        "Reliability earned through honest operation.",
        ("verity", "honest", "pledge", "assured", "reliable", "faithful", "candid", "certain", "proven", "secure"),
        (("true", "word"), ("sure", "hold"), ("fair", "deal"), ("good", "faith"),
         ("trust", "well"), ("candid", "way"), ("proven", "way"), ("trust", "mark")),
        84,
        96,
    ),
    Territory(
        "bridge",
        "A practical path between systems and people.",
        ("bridge", "archway", "crossing", "gateway", "linkway", "traverse", "passage", "connect", "joining"),
        (("link", "span"), ("clear", "span"), ("arch", "link"), ("bridge", "way"),
         ("cross", "link"), ("join", "way"), ("span", "point"), ("link", "arch")),
        79,
        89,
    ),
    Territory(
        "craft",
        "Thoughtful work, made well and built to last.",
        ("craft", "forge", "shaped", "maker", "build", "refine", "detail", "finish", "quality"),
        (("well", "made"), ("true", "craft"), ("fine", "form"), ("craft", "way"),
         ("form", "well"), ("forge", "well"), ("make", "well"), ("hand", "craft")),
        89,
        88,
    ),
)


def iter_candidates() -> Iterator[tuple[str, Territory, str, tuple[str, ...]]]:
    """Yield deterministic candidates with their semantic provenance."""
    for territory in TERRITORIES:
        for word in territory.source_words:
            yield word, territory, "source", (word,)
        for left, right in territory.compounds:
            yield left + right, territory, "compound", (left, right)
