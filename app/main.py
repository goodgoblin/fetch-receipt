from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.models import Item, Receipt
from app.rules import count_points
import uuid, logging, threading



app = FastAPI()

# all kids love log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  - %(levelname)s - %(message)s",
)
# The map where we put the points - locked in case of multi-threading hijinx
points_map = {}
points_lock = threading.Lock()

@app.get("/")
async def root():
    return {"message" : "Hello Fetch!"}

# Check the points map and return if the id exists 
@app.get("/receipts/{id}/points")
async def fetch_points(id: str):
    if id in points_map:
        p = points_map[id]
        logging.info(f"Points fetched successfully for ID {id}: {p}")
        return {"points" : p}
    else:
        logging.warning(f"Points requested for non-existent ID {id}")
        response = { "description": "No receipt found for that ID."}
        return JSONResponse(status_code=404, content=response)

# Process the receipt and save the points in the points map
@app.post("/receipts/process")
async def process_reciept(receipt: Receipt):
    #the counting logic
    points = count_points(receipt)
    r_id = str(uuid.uuid4())
    # lock the map just in case - probably overkill but simple
    with points_lock:
        points_map[r_id] = points
    logging.info(f"Receipt processed successfully {r_id} : {points}")
    return {"id": r_id}

# Validation is done in the models
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(f"Validation failed: {exc.errors()}")
    response = { "description": "The receipt is invalid."}
    return JSONResponse(status_code=422, content=response)

# For debugging
def print_receipt(receipt: Receipt):
    print("Receipt retailer is ..."+receipt.retailer)
    print("Items are ")
    for item in receipt.items:
        print(item.shortDescription)
        print(item.price)
