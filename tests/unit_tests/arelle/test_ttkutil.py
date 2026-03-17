from arelle.TtkUtil import coerce_style_int, compute_dialog_width, compute_toolbar_icon_scale, compute_treeview_rowheight


def test_coerce_style_int_accepts_numeric_strings():
    assert coerce_style_int("18") == 18
    assert coerce_style_int("18.0") == 18


def test_coerce_style_int_rejects_non_numeric_values():
    assert coerce_style_int(None) is None
    assert coerce_style_int("") is None
    assert coerce_style_int("default") is None


def test_compute_treeview_rowheight_respects_existing_larger_height():
    assert compute_treeview_rowheight(18, 32) == 32


def test_compute_treeview_rowheight_grows_to_fit_font_linespace():
    assert compute_treeview_rowheight(18, 20) == 25


def test_compute_toolbar_icon_scale_keeps_default_size_for_normal_fonts():
    assert compute_toolbar_icon_scale(18) == 1


def test_compute_toolbar_icon_scale_doubles_icons_for_large_desktop_fonts():
    assert compute_toolbar_icon_scale(37) == 2


def test_compute_dialog_width_prefers_requested_width_when_screen_allows():
    assert compute_dialog_width(1920, 760, 560) == 760


def test_compute_dialog_width_caps_to_screen_fraction():
    assert compute_dialog_width(900, 760, 560) == 560
