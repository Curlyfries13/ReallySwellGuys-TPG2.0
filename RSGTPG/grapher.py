import pandas as pd
import mapper
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import re


ROUTE_COLS = ['Print Seq', 'Site Address #/Name', 'Site Address Line 2', 'Site Suite #', 'City', 'State', 'Zip', 'Longitude', 'Latitude']
TELE_COLS = ['Time', 'Latitude', 'Longitude', 'State']
timestamp_pattern = r'(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<year>[0-9]{4}) (?P<time>[0-9]{2}:[0-9]{2}:[0-9]{2})'
timestamp_parser = re.compile(timestamp_pattern)

def plot_expected_route():
    data = mapper.Mapper()
    day1 = data.route1
    day1 = day1[ROUTE_COLS]
    day1 = day1.sort_values(by='Print Seq')

    color_max = day1['Print Seq'].max()
    keywords = {'maximum':color_max}

    day1['color'] = day1.apply(func=normalize_sequence_color, axis=1,
                               **keywords)
    color_map = day1[['color']].values

    plt.plot(day1[['Longitude']].values, day1[['Latitude']].values, 'b', zorder=1)
    plt.scatter(day1[['Longitude']].values, day1[['Latitude']].values,
                c=color_map, cmap=cm.plasma, zorder=3)

    plt.show()

def plot_actual_route():
    data = mapper.Mapper()
    day1 = data.tele2
    day1 = day1[TELE_COLS]
    day1 = day1.sort_values(by='Time')
    start = np.datetime64(convert_timestamp(day1['Time'].head(1).values[0]))
    end = np.datetime64(convert_timestamp(day1['Time'].tail(1).values[0]))
    max_delta = end-start

    keywords = {'start':start}
    day1['delta'] = day1.apply(func=time_delta, axis=1, **keywords)

    keywords = {'maximum_delta':max_delta}
    day1['delta_color'] = day1.apply(func=normalize_tele_color, axis=1,
                                     **keywords)
    day1['lat_conv'] = day1[['Latitude']].apply(func=float, axis=1)
    day1['lon_conv'] = day1[['Longitude']].apply(func=float, axis=1)
    color_map = day1[['delta_color']].values
    plt.scatter(day1[['lon_conv']], day1[['lat_conv']],
                c=color_map, cmap=cm.plasma, zorder=2, alpha=.3)
    # print(day1.head())
    # print(day1.tail())
    plt.show()

def plot_both():
    data = mapper.Mapper()
    tele1 = data.tele2
    day1 = data.route1
    day1 = day1[ROUTE_COLS]
    day1 = day1.sort_values(by='Print Seq')

    color_max = day1['Print Seq'].max()
    keywords = {'maximum':color_max}

    day1['color'] = day1.apply(func=normalize_sequence_color, axis=1,
                               **keywords)
    color_map = day1[['color']].values

    # plt.plot(day1[['Longitude']].values, day1[['Latitude']].values, 'g',
             # zorder=1, alpha=.5)
    plt.scatter(day1[['Longitude']].values, day1[['Latitude']].values,
                c=color_map, cmap=cm.bwr, zorder=3)

    #plt.show()

    data = mapper.Mapper()
    tele1 = tele1[TELE_COLS]
    tele1 = tele1.sort_values(by='Time')
    start = np.datetime64(convert_timestamp(tele1['Time'].head(1).values[0]))
    end = np.datetime64(convert_timestamp(tele1['Time'].tail(1).values[0]))
    max_delta = end-start

    keywords = {'start':start}
    tele1['delta'] = tele1.apply(func=time_delta, axis=1, **keywords)

    keywords = {'maximum_delta':max_delta}
    tele1['delta_color'] = tele1.apply(func=normalize_tele_color, axis=1,
                                     **keywords)
    tele1['lat_conv'] = tele1[['Latitude']].apply(func=float, axis=1)
    tele1['lon_conv'] = tele1[['Longitude']].apply(func=float, axis=1)
    color_map = tele1[['delta_color']].values
    plt.scatter(tele1[['lon_conv']], tele1[['lat_conv']],
                c=color_map, cmap=cm.plasma, zorder=2, alpha=.03, s=5)
    # print(tele1.head())
    # print(tele1.tail())
    plt.show()


def normalize_sequence_color(row, maximum=1):
    x = row['Print Seq']
    return float(x/maximum)

def normalize_tele_color(row, maximum_delta=1):
    x = row['delta']
    return float(x/maximum_delta)

def time_delta(row, start):
    stamp = convert_timestamp(row['Time'])
    x = np.datetime64(stamp)
    delta = x - start
    return delta

def convert_timestamp(timestamp):
    match = timestamp_parser.search(timestamp)
    outstring=''
    outstring+='{}-{}-{}T{}'.format(match.group('year'), match.group('month'),
                                    match.group('day'), match.group('time'))
    return outstring



if __name__ == '__main__':
    # plot_expected_route()
    # plot_actual_route()
    plot_both()
