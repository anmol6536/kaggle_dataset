import pandas as pd
import seaborn as sns
from geopy.geocoders import Nominatim
import plotly.express as px
from tqdm import tqdm
import numpy as np
from functools import cache

tqdm.pandas()
plotly_mapstyle_options = [
    "open-street-map",
    "carto-positron",
    "carto-darkmatter",
    "stamen-terrain",
    "stamen-toner",
    "stamen-watercolor",
]


class GetLocation:
    def __init__(self, city, state, country) -> None:
        self._city: str = None
        self.city = city

        self._state: str = None
        self.state = state

        self._country: str = None
        self.country = country

        self.longitude = None
        self.latitude = None

        self.geolocator = Nominatim(user_agent="my_user_agent")

        self.__get_location()
        return

    def __get_location(self) -> None:
        self.__address_generator()
        loc = self.geolocator.geocode(self.valid_address)
        self.longitude, self.latitude = loc.longitude, loc.latitude
        return

    def __address_generator(self) -> None:
        not_valid_address_components = []
        address_components = [self.city, self.state, self.country]
        for val in address_components:
            if val is None:
                not_valid_address_components.append(val)

        self.valid_address = ','.join(i for i in address_components if i not in not_valid_address_components)
        return

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        pass

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        self._city = value
        pass

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, value):
        self._country = value
        pass


@cache
def lat_lon_generator(city, state, country=None):
    try:
        loc = GetLocation(city=city, state=state, country=country)
        return loc.latitude, loc.longitude
    except Exception as e:
        print(e)
        return None, None


df = pd.read_csv('/Users/anmolgorakshakar/python/github/kaggle_projects/data/shootings.csv')
# df = df[df.state.isin(['WI', 'NY'])]
df_loc = df[['city', 'state']].drop_duplicates(subset=['city'])
locations = np.array([np.array(i) for i in df_loc.apply(lambda x: lat_lon_generator(x['city'], x['state']), axis=1)])
df_loc['lat'] = locations[:, 0]
df_loc['lon'] = locations[:, 1]

df = df.merge(df_loc, left_on=['city', 'state'], right_on=['city', 'state'], how='left')
df = df.dropna(subset='city')
print(df)

fig = px.density_mapbox(df,
                        lat="lat",
                        lon="lon",
                        hover_data=['state'],
                        color_continuous_scale=px.colors.sequential.Viridis,
                        opacity=0.5,
                        zoom=9,
                        height=800)

fig.update_layout(mapbox_style=plotly_mapstyle_options[-2],
                  mapbox_zoom=4,
                  mapbox_center_lat=41,
                  margin={"r": 0, "t": 0, "l": 0, "b": 0})

fig.show()
