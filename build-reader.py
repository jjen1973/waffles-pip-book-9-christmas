from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANUSCRIPT = ROOT / "manuscripts" / "book-09-the-very-suspicious-christmas-trail-manuscript.md"

SCENES = [
    (range(0, 3), "artwork/bell-trail.png", "Waffles and Pip discover a silver bell, red ribbon, and cookie crumbs along a snowy trail."),
    (range(3, 11), "artwork/friends-trail.png", "The woodland friends gather around Waffles, Pip, a green mitten, and a tiny golden ornament in the snow."),
    (range(11, 14), "artwork/charlie-reunion.png", "Waffles and Charlie tumble happily into the snow while Pip watches from the farm fence."),
    (range(14, 20), "artwork/farm-meeting.png", "Waffles and Pip meet Lily, Grandma, Charlie, and Cracker beside the decorated farm."),
    (range(20, 24), "artwork/tree-decorating.png", "Waffles, Pip, Charlie, Lily, Grandma, and Cracker decorate the farm Christmas tree."),
    (range(24, 29), "artwork/christmas-together.png", "Lily sits with Waffles and Pip beside the glowing tree while their friends share treats at the snowy farm."),
    (range(29, 30), "artwork/bell-trail.png", "Waffles and Pip follow one more clue along the snowy woodland trail."),
]


def clean_markdown(text: str) -> str:
    text = re.sub(r"(?m)^#+\s*", "", text)
    return text.replace("**", "").strip()


def scene_for(index: int) -> tuple[str, str]:
    for page_range, image, alt in SCENES:
        if index in page_range:
            return image, alt
    raise ValueError(f"No artwork mapping for page {index + 1}")


source = MANUSCRIPT.read_text(encoding="utf-8")
sections = [section.strip() for section in source.split("\n---\n") if section.strip()]
sections[0] = re.sub(r"^#\s+\*\*.*?\*\*\s*", "", sections[0], count=1).strip()

pages = []
for index, section in enumerate(sections):
    image, alt = scene_for(index)
    pages.append({"text": clean_markdown(section), "image": image, "alt": alt})

reader = {
    "title": "Waffles & Pip and the Very Suspicious Christmas Trail",
    "book_number": 9,
    "layout": "full-manuscript",
    "cover": "artwork/cover.png",
    "pages": pages,
}

json_text = json.dumps(reader, ensure_ascii=False, indent=2) + "\n"
(ROOT / "reader.json").write_text(json_text, encoding="utf-8")
(ROOT / "reader.js").write_text("window.BOOK_READER = " + json_text.rstrip() + ";\n", encoding="utf-8")
print(f"Built Book 9 reader data: {len(pages)} story pages")
