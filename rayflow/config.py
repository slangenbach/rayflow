"""Package-wide configuration."""

COLS_TO_LOAD = ["passenger_count", "trip_distance", "RatecodeID", "payment_type", "fare_amount"]
COLS_TO_DROP = [
    "VendorID",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "store_and_fwd_flag",
    "PULocationID",
    "DOLocationID",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "total_amount",
    "congestion_surcharge",
    "airport_fee",
]
