"""
See COPYRIGHT.md for copyright information.
"""
from __future__ import annotations

from typing import Any, cast

from arelle.ModelInstanceObject import ModelContext
from arelle.ModelXbrl import ModelXbrl
from arelle.XmlValidate import lexicalPatterns


def getContextsWithPeriodTime(modelXbrl: ModelXbrl) -> list[ModelContext | None]:
    """Return contexts whose period elements (startDate/endDate/instant) include time content."""
    result: list[ModelContext | None] = []
    datetimePattern = lexicalPatterns["XBRLI_DATEUNION"]
    for context in modelXbrl.contexts.values():
        for uncastElt in context.iterdescendants(
            "{http://www.xbrl.org/2003/instance}startDate",
            "{http://www.xbrl.org/2003/instance}endDate",
            "{http://www.xbrl.org/2003/instance}instant",
        ):
            elt = cast(Any, uncastElt)
            m = datetimePattern.match(elt.stringValue)
            if m and m.group(1):
                result.append(context)
    return result


def getContextsWithPeriodTimeZone(modelXbrl: ModelXbrl) -> list[ModelContext | None]:
    """Return contexts whose period elements include timezone."""
    result: list[ModelContext | None] = []
    datetimePattern = lexicalPatterns["XBRLI_DATEUNION"]
    for context in modelXbrl.contexts.values():
        for uncastElt in context.iterdescendants(
            "{http://www.xbrl.org/2003/instance}startDate",
            "{http://www.xbrl.org/2003/instance}endDate",
            "{http://www.xbrl.org/2003/instance}instant",
        ):
            elt = cast(Any, uncastElt)
            m = datetimePattern.match(elt.stringValue)
            if m and m.group(3):
                result.append(context)
    return result


def getContextsWithSegments(modelXbrl: ModelXbrl) -> list[ModelContext | None]:
    """Return contexts that contain xbrli:segment."""
    result: list[ModelContext | None] = []
    for context in modelXbrl.contexts.values():
        if context.hasSegment:
            result.append(context)
    return result


def getContextsWithScenarioContent(modelXbrl: ModelXbrl) -> list[ModelContext | None]:
    """Return contexts that contain scenario content."""
    result: list[ModelContext | None] = []
    for context in modelXbrl.contexts.values():
        if context.nonDimValues("scenario"):
            result.append(context)
    return result
