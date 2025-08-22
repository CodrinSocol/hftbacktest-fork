import warnings
from typing import List

import polars as pl

SECONDS_PER_DAY = 24 * 60 * 60


def get_num_samples_per_day(timestamp: pl.Series) -> float:
    interval = timestamp.diff()
    if (interval[1:-1] != interval[2:]).sum() > 0:
        warnings.warn('The sampling interval is not consistent. Use resample().', UserWarning)
    sampling_interval = (timestamp[1] - timestamp[0]).total_seconds()
    return SECONDS_PER_DAY / sampling_interval


def get_total_days(timestamp: pl.Series) -> float:
    return (timestamp[-1] - timestamp[0]).total_seconds() / SECONDS_PER_DAY


def monthly(df: pl.DataFrame) -> List[pl.DataFrame]:
    return df.with_columns(
        pl.col('timestamp').dt.strftime('%Y%m').alias('dt')
    ).partition_by('dt')


def daily(df: pl.DataFrame) -> List[pl.DataFrame]:
    return df.with_columns(
        pl.col('timestamp').dt.strftime('%Y%m%d').alias('dt')
    ).partition_by('dt')


def hourly(df: pl.DataFrame) -> List[pl.DataFrame]:
    return df.with_columns(
        pl.col('timestamp').dt.strftime('%Y%m%d:%H').alias('dt')
    ).partition_by('dt')


def resample(df: pl.DataFrame, frequency: str) -> pl.DataFrame:
    agg_cols = []
    for col in df.columns:
        if col == 'timestamp':
            continue
        elif col == 'trading_value_':
            agg_cols.append(pl.col(col).sum())
        elif col == 'trading_volume_':
            agg_cols.append(pl.col(col).sum())
        elif col == 'num_trades_':
            agg_cols.append(pl.col(col).sum())
        else:
            agg_cols.append(pl.col(col).last())
    return df.group_by_dynamic('timestamp', every=frequency).agg(*agg_cols)


def pan_zoom_factory(fig, base_scale=1.5, pan_factor=0.1):
    """
    Attaches a pan and zoom function to the figure `fig` passed as parameter.
    - Scroll to pan the x-axis.
    - Shift + Scroll to zoom in/out on the cursor's position.
    """

    def pan_zoom_fun(event):
        ax = event.inaxes
        if ax is None:
            return

        if event.key is None:  # PAN
            cur_xlim = ax.get_xlim()
            x_range = cur_xlim[1] - cur_xlim[0]
            pan_amount = x_range * pan_factor
            if event.button == 'up':
                ax.set_xlim(cur_xlim[0] + pan_amount, cur_xlim[1] + pan_amount)
            elif event.button == 'down':
                ax.set_xlim(cur_xlim[0] - pan_amount, cur_xlim[1] - pan_amount)
            fig.canvas.draw_idle()

        elif event.key == 'shift':  # ZOOM
            if event.xdata is None or event.ydata is None:
                return
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            x_range = (cur_xlim[1] - cur_xlim[0]) * 0.5
            y_range = (cur_ylim[1] - cur_ylim[0]) * 0.5
            xdata, ydata = event.xdata, event.ydata
            if event.button == 'up':
                scale = 1 / base_scale
            elif event.button == 'down':
                scale = base_scale
            else:
                scale = 1
            ax.set_xlim([xdata - x_range * scale, xdata + x_range * scale])
            ax.set_ylim([ydata - y_range * scale, ydata + y_range * scale])
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect('scroll_event', pan_zoom_fun)

    return pan_zoom_fun