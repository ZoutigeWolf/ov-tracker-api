from google.transit import gtfs_realtime_pb2

def get_realtime_data(file: str):
    try:
        with open(file, "rb") as f:
            data = f.read()

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(data)

        return feed.entity

    except Exception:
        print("Error fetching vehicle positions")
        return []
