from __future__ import annotations

from typing import Any, Iterable, List, Optional

from chartcraft.core.models import (
    Area,
    Bar,
    Dashboard,
    Donut,
    KPI,
    Line,
    Scatter,
    SectionHeader,
    Table,
    TextBlock,
)


def _flatten(items: Iterable[Any]) -> List[Any]:
    flat: List[Any] = []
    for item in items:
        if item is None:
            continue
        if isinstance(item, (list, tuple)):
            flat.extend(_flatten(item))
        else:
            flat.append(item)
    return flat


def Page(
    title: str = "",
    subtitle: str = "",
    *,
    kpis: Optional[list] = None,
    filters: Optional[list] = None,
    content: Optional[Iterable[Any]] = None,
    charts: Optional[Iterable[Any]] = None,
    cols: int = 12,
    refresh: int | None = None,
    background: str = "",
    icon: str = "",
) -> Dashboard:
    pieces = content if content is not None else charts or []
    return Dashboard(
        title=title,
        subtitle=subtitle,
        kpis=kpis or [],
        filters=filters or [],
        charts=_flatten(pieces),
        cols=cols,
        refresh=refresh,
        background=background,
        icon=icon,
    )


def executive_page(
    title: str,
    subtitle: str = "",
    *,
    kpis: Optional[list] = None,
    hero: Optional[Iterable[Any]] = None,
    hero_subtitle: str = "",
    performance: Optional[Iterable[Any]] = None,
    note_text: str = "",
    content: Optional[Iterable[Any]] = None,
    filters: Optional[list] = None,
    icon: str = "",
) -> Dashboard:
    return Page(
        title=title,
        subtitle=subtitle,
        kpis=kpis,
        filters=filters,
        icon=icon,
        content=[
            section("Momentum & Mix", *(hero or []), subtitle=hero_subtitle)
            if hero
            else None,
            note(note_text) if note_text else None,
            section("Regional Performance & Top States", *(performance or []))
            if performance
            else None,
            *(content or []),
        ],
    )


def sales_page(
    title: str,
    subtitle: str = "",
    *,
    filters: Optional[list] = None,
    kpis: Optional[list] = None,
    trend: Optional[Iterable[Any]] = None,
    trend_subtitle: str = "",
    analysis: Optional[Iterable[Any]] = None,
    ranking: Optional[Iterable[Any]] = None,
    note_text: str = "",
    icon: str = "",
) -> Dashboard:
    return Page(
        title=title,
        subtitle=subtitle,
        filters=filters,
        kpis=kpis,
        icon=icon,
        content=[
            section("Sales Arc", *(trend or []), subtitle=trend_subtitle)
            if trend
            else None,
            note(note_text) if note_text else None,
            section("Category & Sub-Category Analysis", *(analysis or []))
            if analysis
            else None,
            section("Top Products by Revenue", *(ranking or [])) if ranking else None,
        ],
    )


def customer_page(
    title: str,
    subtitle: str = "",
    *,
    filters: Optional[list] = None,
    kpis: Optional[list] = None,
    mix: Optional[Iterable[Any]] = None,
    mix_subtitle: str = "",
    geography: Optional[Iterable[Any]] = None,
    accounts: Optional[Iterable[Any]] = None,
    icon: str = "",
) -> Dashboard:
    return Page(
        title=title,
        subtitle=subtitle,
        filters=filters,
        kpis=kpis,
        icon=icon,
        content=[
            section("Segment Breakdown", *(mix or []), subtitle=mix_subtitle)
            if mix
            else None,
            section("Geographic Performance", *(geography or []))
            if geography
            else None,
            section("Top Accounts", *(accounts or [])) if accounts else None,
        ],
    )


def product_page(
    title: str,
    subtitle: str = "",
    *,
    filters: Optional[list] = None,
    kpis: Optional[list] = None,
    overview: Optional[Iterable[Any]] = None,
    overview_subtitle: str = "",
    note_text: str = "",
    profitability: Optional[Iterable[Any]] = None,
    leaders: Optional[Iterable[Any]] = None,
    icon: str = "",
) -> Dashboard:
    return Page(
        title=title,
        subtitle=subtitle,
        filters=filters,
        kpis=kpis,
        icon=icon,
        content=[
            section("Category Overview", *(overview or []), subtitle=overview_subtitle)
            if overview
            else None,
            note(note_text) if note_text else None,
            section("Profitability & Discount Impact", *(profitability or []))
            if profitability
            else None,
            section("Sub-Category & Top Products", *(leaders or []))
            if leaders
            else None,
        ],
    )


def section(
    title: str,
    *content: Any,
    subtitle: str = "",
    col: int = 0,
    colspan: int = 12,
) -> list[Any]:
    return [
        SectionHeader(title=title, subtitle=subtitle, col=col, colspan=colspan),
        *_flatten(content),
    ]


def note(
    content: str,
    *,
    col: int = 0,
    colspan: int = 12,
    font_size: str = "0.95rem",
    align: str = "left",
) -> TextBlock:
    return TextBlock(
        content=content, col=col, colspan=colspan, font_size=font_size, align=align
    )


def stat(title: str, value: Any = None, **kwargs: Any) -> KPI:
    return KPI(title=title, value=value, **kwargs)


def trend_line(
    *args: Any,
    colors: Optional[list[str]] = None,
    show_dots: bool = False,
    smooth: bool = True,
    **kwargs: Any,
) -> Line:
    return Line(
        *args,
        colors=colors or ["#7C3AED", "#14B8A6"],
        show_dots=show_dots,
        smooth=smooth,
        **kwargs,
    )


def trend_area(
    *args: Any,
    colors: Optional[list[str]] = None,
    smooth: bool = True,
    gradient: bool = True,
    **kwargs: Any,
) -> Area:
    return Area(
        *args,
        colors=colors or ["#F97316", "#FB7185"],
        smooth=smooth,
        gradient=gradient,
        **kwargs,
    )


def comparison_bars(
    *args: Any,
    colors: Optional[list[str]] = None,
    grouped: bool = True,
    show_values: bool = False,
    **kwargs: Any,
) -> Bar:
    return Bar(
        *args,
        colors=colors or ["#8B5CF6", "#14B8A6", "#F59E0B"],
        grouped=grouped,
        show_values=show_values,
        **kwargs,
    )


def ranked_bars(
    *args: Any,
    colors: Optional[list[str]] = None,
    horizontal: bool = True,
    show_values: bool = True,
    **kwargs: Any,
) -> Bar:
    return Bar(
        *args,
        colors=colors or ["#0EA5E9"],
        horizontal=horizontal,
        show_values=show_values,
        **kwargs,
    )


def spotlight_donut(
    *args: Any,
    colors: Optional[list[str]] = None,
    inner_radius: str = "64%",
    center_text: str = "",
    **kwargs: Any,
) -> Donut:
    return Donut(
        *args,
        colors=colors or ["#7C3AED", "#06B6D4", "#F59E0B", "#22C55E"],
        inner_radius=inner_radius,
        center_text=center_text,
        **kwargs,
    )


def insight_scatter(
    *args: Any, min_radius: int = 8, max_radius: int = 24, **kwargs: Any
) -> Scatter:
    return Scatter(*args, min_radius=min_radius, max_radius=max_radius, **kwargs)


def data_table(
    *args: Any,
    page_size: int = 8,
    sortable: bool = True,
    searchable: bool = True,
    **kwargs: Any,
) -> Table:
    return Table(
        *args, page_size=page_size, sortable=sortable, searchable=searchable, **kwargs
    )


def _resolve_query(spec: Any, filters: dict) -> tuple[str, Any]:
    if callable(spec):
        resolved = spec(filters or {})
        if isinstance(resolved, tuple):
            return str(resolved[0]), resolved[1]
        return str(resolved), None
    return str(spec), None


def _sql_rows(connector: Any, sql: Any, params: Any = None):
    def _data(filters: dict | None = None):
        active = filters or {}
        query, inline_params = _resolve_query(sql, active)
        final_params = params(active) if callable(params) else params
        if inline_params is not None and final_params is None:
            final_params = inline_params
        return connector.query_dict(query, final_params)

    return _data


def _sql_value(
    connector: Any,
    sql: Any,
    params: Any = None,
    field: str | None = None,
    formatter: Any = None,
):
    def _data(filters: dict | None = None):
        rows = _sql_rows(connector, sql, params)(filters)
        if not rows:
            return ""
        row = rows[0]
        value = row.get(field) if field else next(iter(row.values()), "")
        return formatter(value, filters or {}) if callable(formatter) else value

    return _data


def _chart_from_sql(
    cls: Any, connector: Any, sql: Any, *, params: Any = None, **kwargs: Any
):
    return cls(data_fn=_sql_rows(connector, sql, params), **kwargs)


def _kpi_from_sql(
    cls: Any,
    title: str,
    connector: Any,
    sql: Any,
    *,
    params: Any = None,
    field: str | None = None,
    formatter: Any = None,
    **kwargs: Any,
):
    return cls(
        title=title,
        data_fn=_sql_value(connector, sql, params, field, formatter),
        **kwargs,
    )


def _attach_from_sql() -> None:
    for chart_cls in (Bar, Line, Area, Donut, Scatter, Table):
        setattr(
            chart_cls,
            "from_sql",
            classmethod(
                lambda cls, connector, sql, params=None, **kwargs: _chart_from_sql(
                    cls, connector, sql, params=params, **kwargs
                )
            ),
        )
    setattr(
        KPI,
        "from_sql",
        classmethod(
            lambda cls, title, connector, sql, params=None, field=None, formatter=None, **kwargs: (
                _kpi_from_sql(
                    cls,
                    title,
                    connector,
                    sql,
                    params=params,
                    field=field,
                    formatter=formatter,
                    **kwargs,
                )
            )
        ),
    )


_attach_from_sql()


def sql_kpi(
    title: str,
    connector: Any,
    sql: Any,
    *,
    params: Any = None,
    field: str | None = None,
    formatter: Any = None,
    **kwargs: Any,
) -> KPI:
    return _kpi_from_sql(
        KPI,
        title,
        connector,
        sql,
        params=params,
        field=field,
        formatter=formatter,
        **kwargs,
    )


def sql_line(connector: Any, sql: Any, *, params: Any = None, **kwargs: Any) -> Line:
    return _chart_from_sql(Line, connector, sql, params=params, **kwargs)


def sql_area(connector: Any, sql: Any, *, params: Any = None, **kwargs: Any) -> Area:
    return _chart_from_sql(Area, connector, sql, params=params, **kwargs)


def sql_bar(connector: Any, sql: Any, *, params: Any = None, **kwargs: Any) -> Bar:
    return _chart_from_sql(Bar, connector, sql, params=params, **kwargs)


def sql_donut(connector: Any, sql: Any, *, params: Any = None, **kwargs: Any) -> Donut:
    return _chart_from_sql(Donut, connector, sql, params=params, **kwargs)


def sql_scatter(
    connector: Any, sql: Any, *, params: Any = None, **kwargs: Any
) -> Scatter:
    return _chart_from_sql(Scatter, connector, sql, params=params, **kwargs)


def sql_table(connector: Any, sql: Any, *, params: Any = None, **kwargs: Any) -> Table:
    return _chart_from_sql(Table, connector, sql, params=params, **kwargs)
