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
