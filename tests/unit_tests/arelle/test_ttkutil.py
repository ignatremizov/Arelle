from arelle.TtkUtil import coerce_style_int, compute_treeview_rowheight


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
