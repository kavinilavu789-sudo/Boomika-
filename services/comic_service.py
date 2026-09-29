from app.ai.gemini_service import (
    generate_outline,
    generate_story
)

from app.ai.image_service import (
    generate_image
)

from app.models import (
    PromptRequest,
    ComicResponse
)

from app.services.layout_builder import (
    build_comic_layout
)

from app.services.exporters import (
    save_pdf
)


def create_comic(
    request: PromptRequest
) -> ComicResponse:

    outline = generate_outline(

        request.prompt,

        request.character_name,

        request.setting,

        request.tone,

        request.art_style
    )

    panels = generate_story(

        outline,

        request.prompt,

        request.character_name,

        request.tone
    )

    for panel in panels:

        panel.image_url = generate_image(

            panel.image_prompt,

            panel.panel_number
        )

    title = (
        f"{request.character_name}'s "
        f"Comic Adventure"
    )

    build_comic_layout(
        panels
    )

    pdf_url = save_pdf(
        title,
        panels
    )

    return ComicResponse(

        title=title,

        panels=panels,

        pdf_url=pdf_url
    )