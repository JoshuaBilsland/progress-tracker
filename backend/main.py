from fastapi import FastAPI

app = FastAPI()

# Temporary in-memory storage for testing MVP
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
