"""
csv_plot.py

Usage examples:
  python csv_plot.py data.csv --x time --y value --kind line --out plot.png
  python csv_plot.py data.csv --cols 0 2 --kind scatter --xlabel "Index" --ylabel "Value" --title "Scatter" --out scatter.png
  python csv_plot.py data.csv --y value --agg mean --groupby category --kind bar --out bar.png

Features:
- Select x and y columns by name or index
- Plot multiple y columns
- Optional grouping + aggregation for bar/line charts
- Apply simple row filters (column op value)
- Save figure file and optionally show it
- Configurable plot size, style
"""

import argparse
import sys
import ast
from typing import List, Optional, Tuple

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- Helpers ---------------------------------------------------------------


def parse_index_or_name(s: str):
    """Return either int (index) or string (name)."""
    try:
        return int(s)
    except ValueError:
        return s


def locate_columns(df: pd.DataFrame, items: List[str]):
    """Convert list of index-or-name items into actual column names."""
    cols = []
    for it in items:
        key = parse_index_or_name(it)
        if isinstance(key, int):
            cols.append(df.columns[key])
        else:
            if key not in df.columns:
                raise KeyError(f"Column '{key}' not found in CSV")
            cols.append(key)
    return cols


def apply_filters(df: pd.DataFrame, filters: List[str]):
    """Apply filters in the form 'col op value' where op in (=,==,>,<,>=,<=,!=,in).
    Example: ['age>30', 'country==AU', 'tag in [A,B]']
    """
    if not filters:
        return df
    q = []
    for f in filters:
        # support Python-like expressions; be cautious with eval by parsing values
        # transform `col in [a,b]` to `df["col"].isin([...])`
        if " in " in f:
            col, rest = f.split(" in ", 1)
            col = col.strip()
            val = ast.literal_eval(rest.strip())
            return df[df[col].isin(val)]
        # otherwise use pandas query-friendly form, assuming simple ops
        q.append(f)
    query = " and ".join(q)
    return df.query(query)


def try_parse_datetime(series: pd.Series):
    """Attempt to parse a series to datetime if it looks like dates."""
    if series.dtype == object:
        try:
            parsed = pd.to_datetime(series, infer_datetime_format=True, errors="coerce")
            if parsed.notna().sum() > 0:
                return parsed
        except Exception:
            pass
    return series


# --- Main plotting logic --------------------------------------------------


def plot_csv(
    filename: str,
    x: Optional[str],
    y: List[str],
    kind: str = "line",
    groupby: Optional[str] = None,
    agg: Optional[str] = None,
    filters: Optional[List[str]] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    title: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 6),
    style: str = "default",
    out: Optional[str] = None,
    show: bool = False,
    legend: bool = True,
):
    plt.style.use(style)
    df = pd.read_csv(filename)
    if filters:
        df = apply_filters(df, filters)

    # Determine y columns
    y_cols = locate_columns(df, y) if y else []
    if not y_cols:
        raise ValueError("No y columns specified or found.")

    # Determine x column
    if x is not None:
        x_key = parse_index_or_name(x)
        if isinstance(x_key, int):
            x_col = df.columns[x_key]
        else:
            if x_key not in df.columns:
                raise KeyError(f"X column '{x_key}' not found")
            x_col = x_key
        df[x_col] = try_parse_datetime(df[x_col])
    else:
        x_col = None

    # Grouping + aggregation logic
    if groupby and agg:
        gb_col = parse_index_or_name(groupby)
        if isinstance(gb_col, int):
            gb_name = df.columns[gb_col]
        else:
            gb_name = gb_col
        agg_func = agg
        grouped = df.groupby(gb_name)[y_cols].agg(agg_func)
        ax = grouped.plot(kind=kind, figsize=figsize)
    else:
        if x_col:
            ax = df.plot(x=x_col, y=y_cols, kind=kind, figsize=figsize)
        else:
            ax = df[y_cols].plot(kind=kind, figsize=figsize)

    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)

    if legend:
        ax.legend()
    # If x axis contains datetimes, improve formatting
    if x_col and pd.api.types.is_datetime64_any_dtype(df[x_col]):
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(mdates.AutoDateLocator()))
        plt.gcf().autofmt_xdate()

    plt.tight_layout()
    if out:
        plt.savefig(out)
        print(f"Saved plot to {out}")
    if show:
        plt.show()
    plt.close()


# --- CLI ------------------------------------------------------------------


def parse_args():
    p = argparse.ArgumentParser(description="Plot CSV columns with flexible options")
    p.add_argument("csv", help="Path to CSV file")
    p.add_argument("--x", help="X column name or zero-based index", default=None)
    p.add_argument(
        "--y",
        help="Y column names or indexes (space-separated)",
        nargs="+",
        required=True,
    )
    p.add_argument(
        "--cols", help="Alias for --y (keeps backward compatibility)", nargs="+"
    )
    p.add_argument(
        "--kind",
        help="Plot kind: line, scatter, bar",
        default="line",
        choices=["line", "scatter", "bar"],
    )
    p.add_argument(
        "--groupby", help="Column to group by before aggregating", default=None
    )
    p.add_argument(
        "--agg",
        help="Aggregation for grouped data: mean,sum,median,count",
        default=None,
    )
    p.add_argument(
        "--filter",
        help="Row filter expression(s). Example: age>30 country=='AU'",
        nargs="+",
        default=[],
    )
    p.add_argument("--xlabel", help="X axis label", default=None)
    p.add_argument("--ylabel", help="Y axis label", default=None)
    p.add_argument("--title", help="Plot title", default=None)
    p.add_argument(
        "--figsize",
        help="Figure size WxH in inches",
        nargs=2,
        type=float,
        default=[10, 6],
    )
    p.add_argument("--style", help="Matplotlib style", default="default")
    p.add_argument("--out", help="Save plot to file (png, pdf, svg)", default=None)
    p.add_argument("--show", help="Display plot interactively", action="store_true")
    p.add_argument("--no-legend", help="Do not show legend", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()
    ylist = args.y or args.cols
    if args.cols and not args.y:
        ylist = args.cols
    try:
        plot_csv(
            filename=args.csv,
            x=args.x,
            y=ylist,
            kind=args.kind,
            groupby=args.groupby,
            agg=args.agg,
            filters=args.filter,
            xlabel=args.xlabel,
            ylabel=args.ylabel,
            title=args.title,
            figsize=(args.figsize[0], args.figsize[1]),
            style=args.style,
            out=args.out,
            show=args.show,
            legend=not args.no_legend,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
