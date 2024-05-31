# import pandas as pd
# import geopandas as gpd
# import googlemaps
# from shapely.geometry import Point
# import json
# from dotenv import load_dotenv
# import os

# load_dotenv()

# GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# def load_data(filepath):
#     """
#     Load latitude and longitude data from a CSV file into a GeoDataFrame.

#     Parameters:
#         filepath (str): Path to the CSV file.

#     Returns:
#         gpd.GeoDataFrame: GeoDataFrame containing the points.
#     """
#     # Load data
#     df = pd.read_csv(filepath)

#     # Remove columns that have a name starting with 'Unnamed'
#     df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    

#     # Assuming columns are named 'latitude' and 'longitude'
#     gdf = gpd.GeoDataFrame(
#         df, geometry=[Point(xy) for xy in zip(df.longitude, df.latitude)],
#         crs="EPSG:4326"
#     )
#     return gdf

# # load all datasets
# cap_industrial_gdf     = load_data('./updated_rentals_industrial/updated_caprates_industrial.csv')
# cap_office_gdf         = load_data('./updated_rentals_industrial/updated_caprates_office.csv')
# rentals_industrial_gdf = load_data('./updated_rentals_industrial/updated_rentals_industrial.csv')
# rentals_office_gdf     = load_data('./updated_rentals_industrial/updated_rentals_office.csv')

# rentals_office_gdf.rename(columns={'rental_office_2022:2': 'rental'}, inplace=True)
# rentals_office_gdf['office_grade'] = rentals_office_gdf['office_grade'].str.strip().str[-1]
# rentals_office_gdf['size'] = 1

# rentals_industrial_gdf.rename(columns={'rental_industrial_2022:2': 'rental'}, inplace=True)
# rentals_industrial_gdf.rename(columns={'industrial_size': 'size'}, inplace=True)

# cap_office_gdf.rename(columns={'caprate_office_2022:2': 'caprate'}, inplace=True)
# cap_office_gdf['office_grade'] = cap_office_gdf['office_grade'].str.strip().str[-1]

# cap_industrial_gdf.rename(columns={'caprate_industrial_2022:2': 'caprate'}, inplace=True)
# cap_industrial_gdf['industrial_subtype'] = cap_industrial_gdf['industrial_subtype'].str.strip()
# cap_industrial_gdf['type'] = cap_industrial_gdf['type'].str.strip()

# rentals_industrial_gdf['size'] = rentals_industrial_gdf['size'].str.extract('(\d+)').astype(int)

# # define functions

# def geolocate(address, api_key):
#     """
#     Geolocate an address using Google Maps API.

#     Parameters:
#         address (str): The address to geocode.
#         api_key (str): Your Google Maps API key.

#     Returns:
#         tuple or None: Returns a tuple (latitude, longitude) if the address is found,
#                        None otherwise.
#     """
#     # Initialize the Google Maps client with your API key
#     gmaps = googlemaps.Client(key=api_key)

#     try:
#         # Geocode the given address
#         geocode_result = gmaps.geocode(address)

#         # Check if the geocode results exist
#         if geocode_result:
#             latitude = geocode_result[0]['geometry']['location']['lat']
#             longitude = geocode_result[0]['geometry']['location']['lng']
#             return (latitude, longitude)
#         else:
#             return None
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None

# def is_near(query_location, gdf, distance=1000):
#     """
#     Return rows in the GeoDataFrame that are within a specified distance (in meters) of the query location.

#     Parameters:
#         query_location (tuple): Tuple (latitude, longitude) of the query location.
#         gdf (gpd.GeoDataFrame): GeoDataFrame containing location points.
#         distance (int): Distance threshold in meters.

#     Returns:
#         gpd.GeoDataFrame: GeoDataFrame containing the points that are near the query location.
#     """
#     # Convert latitude and longitude to Point
#     query_point = Point(query_location[1], query_location[0])

#     # Calculate UTM zone from the longitude to use a CRS for distance calculation in meters
#     utm_zone = int((query_location[1] + 180) / 6) + 1
#     utm_crs = f'EPSG:326{utm_zone}' if query_location[0] >= 0 else f'EPSG:327{utm_zone}'

#     # Transform the GeoDataFrame to the calculated UTM CRS
#     gdf_utm = gdf.to_crs(utm_crs)

#     # Create a temporary GeoDataFrame to transform the query point
#     temp_gdf = gpd.GeoDataFrame([{'geometry': query_point}], crs='EPSG:4326')
#     temp_gdf = temp_gdf.to_crs(utm_crs)

#     # Get the transformed query point
#     query_point_utm = temp_gdf.geometry.iloc[0]

#     # Buffer the point by the specified distance in meters
#     query_buffer = query_point_utm.buffer(distance)

#     # Filter GeoDataFrame for rows where geometry intersects with buffer
#     near_gdf = gdf_utm[gdf_utm.geometry.intersects(query_buffer)]

#     # Optionally, transform back to original CRS if needed
#     return near_gdf.to_crs(gdf.crs)



# def filter_results(address, property_type, industrial_size, industrial_subtype, office_grade, distance=3000, expense=0.3):
#     location = geolocate(address, GOOGLE_MAPS_API_KEY)
#     if property_type == "office":
#         rentals = is_near(location, rentals_office_gdf.dropna(), distance)
#         caprates = is_near(location, cap_office_gdf.dropna(), distance)

#         rentals = rentals[rentals["office_grade"] == office_grade]
#         caprates = caprates[caprates["office_grade"] == office_grade]
#     else:
#         rentals = is_near(location, rentals_industrial_gdf.dropna(), distance)
#         caprates = is_near(location, cap_industrial_gdf.dropna(), distance)

#         rentals = rentals[rentals["size"] >= float(industrial_size)]
#         caprates = caprates[caprates["industrial_subtype"] == industrial_subtype]

#     if caprates.size > 0:
#         caprate = caprates.iloc[0]['caprate']
#     else:
#         caprate = 0
#     rentals['caprate'] = caprate
#     result = rentals

#     return result

# def calc_valuation(df, expense=0.3):
#     df['monthly_rental'] = df['rental'] * df['size']
#     df['annual_rental'] = df['monthly_rental'] * 12
#     df['net_income_after_expenses'] = df['annual_rental'] * (1 - expense)
#     df['valuation'] = df['net_income_after_expenses'] / df['caprate']
#     df = df[['area', 'region', 'valuation', 'latitude', 'longitude']]
#     return df[df['valuation'].notna()]

# def compute_valuation(address, property_type, industrial_size, industrial_subtype, office_grade, distance=3000, expense=0.3):
#     df = filter_results(address, property_type, industrial_size, industrial_subtype, office_grade)
#     df_valuation = calc_valuation(df)
#     json_result = json.loads(df_valuation.to_json(orient="records"))
#     return json_result

# if __name__ == '__main__':
#     address = 'mcdonalds Westdene Bloemfontein, 9301, South Africa'
#     property_type = 'office' # industrial
#     industrial_size = 0
    
#     # ['prime industrial park', 'prime leaseback',
#     # 'prime quality non-leaseback', 'secondary quality building']
#     industrial_subtype = 'prime industrial park'
#     office_grade = 'A'

#     json_result = compute_valuation(address, property_type, industrial_size, industrial_subtype, office_grade)
import pandas as pd
import geopandas as gpd
import googlemaps
from shapely.geometry import Point
import json
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

def load_data(filepath):
    """
    Load latitude and longitude data from a CSV file into a GeoDataFrame.

    Parameters:
        filepath (str): Path to the CSV file.

    Returns:
        gpd.GeoDataFrame: GeoDataFrame containing the points.
    """
    # Load data
    df = pd.read_csv(filepath)

    # Remove columns that have a name starting with 'Unnamed'
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    

    # Assuming columns are named 'latitude' and 'longitude'
    gdf = gpd.GeoDataFrame(
        df, geometry=[Point(xy) for xy in zip(df.longitude, df.latitude)],
        crs="EPSG:4326"
    )
    return gdf

# load all datasets
cap_industrial_gdf     = load_data('./updated_rentals_industrial/updated_caprates_industrial.csv')
cap_office_gdf         = load_data('./updated_rentals_industrial/updated_caprates_office.csv')
rentals_industrial_gdf = load_data('./updated_rentals_industrial/updated_rentals_industrial.csv')
rentals_office_gdf     = load_data('./updated_rentals_industrial/updated_rentals_office.csv')

rentals_office_gdf.rename(columns={'rental_office_2022:2': 'rental'}, inplace=True)
rentals_office_gdf['office_grade'] = rentals_office_gdf['office_grade'].str.strip().str[-1]
rentals_office_gdf['size'] = 1

rentals_industrial_gdf.rename(columns={'rental_industrial_2022:2': 'rental'}, inplace=True)
rentals_industrial_gdf.rename(columns={'industrial_size': 'size'}, inplace=True)

cap_office_gdf.rename(columns={'caprate_office_2022:2': 'caprate'}, inplace=True)
cap_office_gdf['office_grade'] = cap_office_gdf['office_grade'].str.strip().str[-1]

cap_industrial_gdf.rename(columns={'caprate_industrial_2022:2': 'caprate'}, inplace=True)
cap_industrial_gdf['industrial_subtype'] = cap_industrial_gdf['industrial_subtype'].str.strip()
cap_industrial_gdf['type'] = cap_industrial_gdf['type'].str.strip()

rentals_industrial_gdf['size'] = rentals_industrial_gdf['size'].str.extract('(\d+)').astype(int)

# define functions

def geolocate(address, api_key):
    """
    Geolocate an address using Google Maps API.

    Parameters:
        address (str): The address to geocode.
        api_key (str): Your Google Maps API key.

    Returns:
        tuple or None: Returns a tuple (latitude, longitude) if the address is found,None otherwise.
    """
    # Initialize the Google Maps client with your API key
    gmaps = googlemaps.Client(key=api_key)

    try:
        # Geocode the given address
        geocode_result = gmaps.geocode(address)

        # Check if the geocode results exist
        if geocode_result:
            latitude = geocode_result[0]['geometry']['location']['lat']
            longitude = geocode_result[0]['geometry']['location']['lng']
            return (latitude, longitude)
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def is_near(query_location, gdf, distance=1000):
    """
    Return rows in the GeoDataFrame that are within a specified distance (in meters) of the query location.

    Parameters:
        query_location (tuple): Tuple (latitude, longitude) of the query location.
        gdf (gpd.GeoDataFrame): GeoDataFrame containing location points.
        distance (int): Distance threshold in meters.

    Returns:
        gpd.GeoDataFrame: GeoDataFrame containing the points that are near the query location.
    """
    # Convert latitude and longitude to Point
    query_point = Point(query_location[1], query_location[0])

    # Calculate UTM zone from the longitude to use a CRS for distance calculation in meters
    utm_zone = int((query_location[1] + 180) / 6) + 1
    utm_crs = f'EPSG:326{utm_zone}' if query_location[0] >= 0 else f'EPSG:327{utm_zone}'

    # Transform the GeoDataFrame to the calculated UTM CRS
    gdf_utm = gdf.to_crs(utm_crs)

    # Create a temporary GeoDataFrame to transform the query point
    temp_gdf = gpd.GeoDataFrame([{'geometry': query_point}], crs='EPSG:4326')
    temp_gdf = temp_gdf.to_crs(utm_crs)

    # Get the transformed query point
    query_point_utm = temp_gdf.geometry.iloc[0]

    # Buffer the point by the specified distance in meters
    query_buffer = query_point_utm.buffer(distance)

    # Filter GeoDataFrame for rows where geometry intersects with buffer
    near_gdf = gdf_utm[gdf_utm.geometry.intersects(query_buffer)]

    # Optionally, transform back to original CRS if needed
    return near_gdf.to_crs(gdf.crs)



def filter_results(address, property_type, industrial_size, industrial_subtype, office_grade, distance=3000, expense=0.3):
    location = geolocate(address, GOOGLE_MAPS_API_KEY)
    if property_type == "office":
        rentals = is_near(location, rentals_office_gdf.dropna(), distance)
        caprates = is_near(location, cap_office_gdf.dropna(), distance)

        rentals = rentals[rentals["office_grade"] == office_grade]
        caprates = caprates[caprates["office_grade"] == office_grade]
    else:
        rentals = is_near(location, rentals_industrial_gdf.dropna(), distance)
        caprates = is_near(location, cap_industrial_gdf.dropna(), distance)

        rentals = rentals[rentals["size"] >= industrial_size]
        caprates = caprates[caprates["industrial_subtype"] == industrial_subtype]

    result = pd.merge(rentals, caprates, on=['area', 'region'], how='outer')
    result['latitude'] = result['latitude_x']
    result['longitude'] = result['longitude_x']
    # result = result.fillna(0)
    return result

def calc_valuation(df, expense=0.3):
    df['monthly_rental'] = df['rental'] * df['size']
    df['annual_rental'] = df['monthly_rental'] * 12
    df['net_income_after_expenses'] = df['annual_rental'] * (1 - expense)
    df['valuation'] = df['net_income_after_expenses'] / df['caprate']
    df = df[['area', 'region', 'valuation', 'latitude', 'longitude']]
    return df[df['valuation'].notna()]

def compute_valuation(address, property_type, industrial_size, industrial_subtype, office_grade, distance=3000, expense=0.3):
    df = filter_results(address, property_type, industrial_size, industrial_subtype, office_grade)
    df_valuation = calc_valuation(df)
    json_result = json.loads(df_valuation.to_json(orient="records"))
    return json_result

if __name__ == '__main__':
    address = 'mcdonalds Westdene Bloemfontein, 9301, South Africa'
    property_type = 'office' # industrial
    industrial_size = 0
    
    # ['prime industrial park', 'prime leaseback',
    # 'prime quality non-leaseback', 'secondary quality building']
    industrial_subtype = 'prime industrial park'
    office_grade = 'A'

    json_result = compute_valuation(address, property_type, industrial_size, industrial_subtype, office_grade)
    print(json_result)
