import numpy as np
import pandas as pd

import folium
from shapely.geometry import LineString, Point

import pandas_profiling

import matplotlib.pyplot as plt
import html

# %matplotlib inline

print ('Done with imports')

# plt.plot(np.random.randn(3, 8))
# np.random.randn()

# reading an excel file into a DataFrame
infopro_route = pd.read_excel('../data/infopro_route.xls')

infopro_route = infopro_route.sort_values('Print Seq')
infopro_route.head(10)

# need to reroute this to local .data file
routes = pd.read_parquet('../data/littleyork.fl1066-v4_scrubbed_dtypes_DOW_4.parquet.gzip')

# sorting the dataframe by source and by date
routes = routes.sort_values(['file_source', 'Time'])

print ('{:,} records'.format(len(routes)))
routes.head() # first 5 records by default

# transposing is helpful when you have a wide DataFrame
routes.head().T

# Pandas Series
routes['file_source'].head()

# accessing the Series with the dot operator
routes.Status.head()

# selecting multiple columns
routes[['Latitude', 'Longitude']].head()

# using .loc to select rows and columns
# label based indexing
routes.loc[:2,['Latitude', 'Longitude']]

# selecting a range of columns
routes.loc[:2,'Latitude':'Speed Limit']

# using .iloc to demonstrate integer based indexing
routes.iloc[3000:3005,5:10]

# basic information about a DataFrame
routes.info()

# describe() displays basic stats about a DataFrame's numeric columns
routes.describe()

# generating a profile report about a DataFrame
print('break here')
pandas_profiling.ProfileReport(routes.head(10000))
print('not here')

# infopro_route.columns#.str.lower()#.str.replace('.#/', '')#.str.replace(' ', '_')
print(routes.columns)

# formatting column names. lower case -> remove periods -> replacing spaces with underscores
for frame in [routes, infopro_route]:
    frame.columns = frame.columns.str.lower().str.replace('.#/', '').str.replace(' ', '_')

# get rid of columns that don't have values
# note the copy()
print (routes.shape)
routes = routes.dropna(axis='columns', how='all').copy()
print (routes.shape)

# time actually contains datetimes
routes['time'].head()

routes['time'].head().dt.time

# creating a new column/series called date_time
routes['date_time'] = routes['time']
routes[['date_time', 'time']].head()

# time will now contain just time
routes['time'] = routes['time'].dt.time
routes[['date_time', 'time']].head()

# checking on duplicate timestamps
# using groupby which is not unlike SQL's groupby
# sorting descending
routes.groupby(['file_source', 'date_time'])['date_time'].count().sort_values(ascending=False).head()

# removing duplicates timestamps
# drop_duplicates() 
print ('{:,} records'.format(len(routes)))
routes = routes.drop_duplicates(subset=['file_source', 'date_time']).copy()
print ('{:,} records'.format(len(routes)))

# boolean indexing examples
filter = routes['speed'] > 60
filter.head()

filter.value_counts()

# demo tilde
# routes[~filter].head()
routes[filter].head()
routes[~filter].head()

# using multiple conditions
filter = (routes['speed'] > 60) & (routes['speed'] > routes['speed_limit'])
routes[filter].head()

# using the query method which might be preferred by some
routes.query('speed > 60 and speed > speed_limit').head()

# updating a column with boolean indexing
# filter = routes['speed'] > routes['speed_limit']
# routes[filter]['speeding_violation'] = 'Y'
# routes[~filter]['speeding_violation'] = 'N'

# updating a column with boolean indexing the right way
filter = routes['speed'] > routes['speed_limit']
routes.loc[filter,'speeding_violation'] = 'Y'
routes.loc[~filter,'speeding_violation'] = 'N'
routes['speeding_violation'].head()

routes.loc[416377:416379, ['latitude', 'longitude']]

# a naive technique using forward fill ie use prior record
# no updates yet
routes.loc[416377:416379, ['latitude', 'longitude']].fillna(method='ffill')

# using an advance technique called interpolate to split the difference between the before and after records
routes.loc[416377:416379, ['latitude', 'longitude']].interpolate()

# using shift() to compare current row to prior row
filter = (routes['latitude'].isnull()) & (routes['latitude'].shift().isnull())
routes[filter][['file_source', 'time', 'latitude', 'longitude']].head()

# fill in the blanks for the singles by using interpolate with limit=1
routes['latitude'] = routes['latitude'].interpolate(limit=1)
routes['longitude'] = routes['longitude'].interpolate(limit=1)

# drop the rest using dropna
routes = routes.dropna(how='any', subset=['latitude', 'longitude']).copy()

filter = (routes['latitude'].isnull()) | (routes['longitude'].isnull())
routes[filter][['file_source', 'time', 'latitude', 'longitude']].head()

# EDA
routes['speed'].min()
routes['file_source'].value_counts()

# max status
routes.groupby('status')['speed'].agg(['count', 'mean', 'min', 'max']).head()

# multi-dimensional analysis with pivot tables
# inline transformation with dt.hour
routes.pivot_table(values='speed', index=routes['date_time'].dt.hour, 
                   columns='speeding_violation', aggfunc='count')#.plot()

# speed plot
filter = (routes['file_source'] == 'Telemetry-1527608759449.xls') & (routes['speed'].isnull() == False)
routes[filter].plot(x='time', y='speed', figsize=[20,8])

# groupby and nlargest to display the top n statuses by count
routes.groupby(['status'])['time'].count().nlargest(n=3).plot(kind='bar')

# applying a user defined function to a column
def square_it(x):
    return x * x

routes['latitude'].apply(square_it).head()

# applying a user defined function to rows
def divide_them(x):
    return x['latitude'] / x['longitude']

# just the first 5 rows
routes.head().apply(divide_them, axis=1)

# same results as above but easier and faster
(routes['latitude'] / routes['longitude']).head()

# creating a map that's centered on our dataset
some_map = folium.Map(location=[infopro_route['latitude'].mean(), 
                                infopro_route['longitude'].mean()], 
                                zoom_start=10)

for _, row in infopro_route.iterrows():
    folium.Marker(row[['latitude', 'longitude']].values, 
                  popup=html.escape(row['site_name'])).add_to(some_map)
    
for _, row in routes.iterrows():
    folium.Marker(row[['latitude', 'longitude']].values,
                  popup=html.escape(row['time']).add_to(some_map))

some_map

# creating a Shapely LineString from a part of a route
line = LineString(routes[['longitude', 'latitude']].iloc[11000: 12000].values)
line

# creating a buffer or the fence
line_buffer = line.buffer(.00025)
line_buffer

# example of a point in the fence(green_point) and outside the fence(red_point) 
fig, ax = plt.subplots(figsize=(15,8))

# defining the axis values
plt.axis([min(line_buffer.exterior.xy[0]), max(line_buffer.exterior.xy[0]), 
          min(line_buffer.exterior.xy[1]), max(line_buffer.exterior.xy[1])])

# plotting the LineString or Polyline
ax.plot(line.xy[0], line.xy[1], color='black', linewidth=2)

# plotting the geofence or buffer
ax.plot(line_buffer.exterior.xy[0], line_buffer.exterior.xy[1], 
                                color='blue', linewidth=5)

# creating two examples points
green_point = Point(-95.416, 30.0735)
red_point = Point(-95.416, 30.075)

# plotting the two example points
ax.scatter(green_point.x, green_point.y, color='green', s=100)
ax.scatter(red_point.x, red_point.y, color='red', s=100)

green_point.within(line_buffer)
red_point.within(line_buffer)
