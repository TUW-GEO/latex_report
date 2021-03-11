import openeo

DRIVER_URL = "https://earthengine.openeo.org/v1.0" #GEE
#DRIVER_URL = "https://openeo-dev.vito.be" #VITO
#DRIVER_URL = "http://openeo-dev.cidsn.jrc.it:46104" #JRC

COLLECTION_NAME = "COPERNICUS/S1_GRD" #GEE
#COLLECTION_NAME = "S1_GRD_SIGMA0_DESCENDING" #VITO
#COLLECTION_NAME = "EarthObservation.Copernicus.S1.scenes.source.L1C" #JRC

# Connect to backend via basic authentication
con = openeo.connect(DRIVER_URL)
con.authenticate_basic(USER, PASSWORD)

# Extract monthly time series
datacube = con.load_collection(COLLECTION_NAME,
                    spatial_extent={"west": 4.24, "south": 51.4, "east": 5.5, "north": 51.93, "crs": 4326},
                    temporal_extent=["2020-03-01", "2020-06-01"],
                    bands=["VV"])
march = datacube.filter_temporal("2020-03-01", "2020-04-01")
april = datacube.filter_temporal("2020-04-01", "2020-05-01")
may = datacube.filter_temporal("2020-05-01", "2020-06-01")

# Monthly means
m3 = march.mean_time()
m4 = april.mean_time()
m5 = may.mean_time()

# Prepare RGB imagery
R_band = m3.rename_labels(dimension="bands", target=["R"], source=["VV"])
G_band = m4.rename_labels(dimension="bands", target=["G"], source=["VV"])
B_band = m5.rename_labels(dimension="bands", target=["B"], source=["VV"])

RG = R_band.merge_cubes(G_band)
RGB = RG.merge_cubes(B_band)

# Execution
RGB.execute_batch("output.tif",out_format="GTIFF-THUMB") #GEE
#RGB.execute_batch("output.tif",out_format="GTIFF") #VITO
#datacube = RGB.save_result(format="GTIFF") #JRC
#job = datacube.send_job() #JRC
