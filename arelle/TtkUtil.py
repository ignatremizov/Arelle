"""
Helpers for sizing ttk widgets consistently across platforms/themes.

See COPYRIGHT.md for copyright information.
"""
from __future__ import annotations

import math
from typing import Any


def coerce_style_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(float(value))
        except ValueError:
            return None
    return None


def compute_treeview_rowheight(font_linespace: int, configured_rowheight: Any = None) -> int:
    """
    Ensure the row height can fully contain the rendered font.

    Some Linux themes render larger Treeview fonts than their default row heights,
    which clips text across package/plugin managers and inspector panes.
    """
    configured_height = coerce_style_int(configured_rowheight) or 0
    content_padding = max(6, math.ceil(font_linespace * 0.35))
    minimum_height = font_linespace + content_padding
    return max(configured_height, minimum_height)


def compute_toolbar_icon_scale(font_linespace: int, base_icon_size: int = 16) -> int:
    """
    Scale fixed-size toolbar icons to match larger desktop font metrics.

    The bundled toolbar GIFs are 16x16. On higher-DPI Linux desktops the default
    Tk font can be much taller, which leaves the toolbar looking disproportionately
    small even after text-based widgets are corrected.
    """
    target_icon_size = max(base_icon_size, math.ceil(font_linespace * 0.8))
    return max(1, round(target_icon_size / base_icon_size))


def compute_dialog_width(
    screen_width: int,
    preferred_width: int,
    minimum_width: int,
    maximum_fraction: float = 0.6,
) -> int:
    """
    Size dialogs to a readable width while keeping them within a fraction of the screen.
    """
    maximum_width = max(minimum_width, math.floor(screen_width * maximum_fraction))
    return max(minimum_width, min(preferred_width, maximum_width))
