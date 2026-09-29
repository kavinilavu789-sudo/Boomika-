from pathlib import Path
from datetime import datetime

from fpdf import FPDF

from PIL import Image

from app.config import OUTPUT_DIR

from app.models import Panel


def save_pdf(
    title: str,
    panels: list[Panel]
) -> str:

    filename = (
        f"comic_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        f".pdf"
    )

    path = (
        OUTPUT_DIR /
        filename
    )

    pdf = FPDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    for panel in panels:

        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            18
        )

        pdf.multi_cell(
            0,
            10,
            (
                f"{title} - "
                f"Panel {panel.panel_number}: "
                f"{panel.title}"
            )
        )

        if panel.image_url:

            image_path = (
                OUTPUT_DIR /
                Path(
                    panel.image_url
                ).name
            )

            if image_path.exists():

                try:

                    with Image.open(
                        image_path
                    ) as image:

                        width, height = (
                            image.size
                        )

                    max_width = 175
                    max_height = 105

                    ratio = min(
                        max_width / width,
                        max_height / height
                    )

                    display_width = (
                        width * ratio
                    )

                    display_height = (
                        height * ratio
                    )

                    pdf.image(
                        str(image_path),
                        x=17,
                        y=35,
                        w=display_width,
                        h=display_height
                    )

                    pdf.set_y(
                        35 +
                        display_height +
                        8
                    )

                except Exception:

                    pass

        pdf.set_font(
            "Helvetica",
            "B",
            12
        )

        pdf.multi_cell(
            0,
            8,
            "Narration"
        )

        pdf.set_font(
            "Helvetica",
            "",
            11
        )

        pdf.multi_cell(
            0,
            7,
            panel.narration or ""
        )

        if panel.dialogue:

            pdf.ln(3)

            pdf.set_font(
                "Helvetica",
                "B",
                12
            )

            pdf.multi_cell(
                0,
                8,
                "Dialogue"
            )

            pdf.set_font(
                "Helvetica",
                "",
                11
            )

            for line in panel.dialogue:

                pdf.multi_cell(
                    0,
                    7,
                    f"- {line}"
                )

    pdf.output(
        str(path)
    )

    return (
        f"/outputs/{path.name}"
    )