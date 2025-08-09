from fastapi import FastAPI

app = FastAPI()
# MUCH OF THIS CODE IS PURELY FOR THE TESTING OF THE MVP.
# SOME PARTICULAR SECTIONS OF TAGGED WITH A "TEMP" MESSAGE.
# HOWEVER, MUCH OF THE REST WILL CHANGE TOO.

# TEMP in-memory storage for testing MVP
# Tracker format: {tracker_name: {id, tracker_name, current, total}}
trackers = {
    "tracker1": ["1", "The Oxford History of Britain", 582, 751],
    "tracker2": ["2", "Churchill: Walking with Destiny", 0, 982]
}


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


# GET Functions
@app.get("/trackers")
async def get_trackers():
    return trackers


@app.get("/trackers/{tracker_name}")
async def get_tracker(tracker_name: str):
    return trackers[tracker_name]


# POST Functions
# TEMP function for testing MVP
@app.post("/new")
async def create_tracker(trackername: str, current: int, total: int):
    global trackers
    new_id = len(trackers)+1
    trackers[f"tracker{new_id}"] = [str(new_id), trackername, current, total]
    return {"message": "Tracker Created!"}
