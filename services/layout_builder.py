from typing import List

from app.models import Panel


def build_comic_layout(
    panels: List[Panel]
) -> dict:

    return {

        "panel_count": len(panels),

        "panels": [

            {
                "number": panel.panel_number,

                "title": panel.title,

                "image_url": panel.image_url,

                "narration": panel.narration,

                "dialogue": panel.dialogue
            }

            for panel in panels
        ]
    }