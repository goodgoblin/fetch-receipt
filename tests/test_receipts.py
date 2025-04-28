from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Sample valid receipt data
valid_receipt = {
    "retailer": "M&M Corner Market",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"}
    ],
    "total": "6.49"
}

twenty_eight_points = {
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },{
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },{
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },{
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },{
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}

one_hundred_nine_points = {
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}
ghost_receipt = {
  "retailer": " ",
  "purchaseDate": "2022-03-21",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": " ",
      "price": "0.00"
    },{
      "shortDescription": " ",
      "price": "0.00"
    },],
 "total": "00.00"
}

forty_two_points = {
  "retailer": "M&M Corner Markets",
  "purchaseDate": "2022-03-21",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.01"
    },{
      "shortDescription": "Gatorade",
      "price": "2.01"
    },{
      "shortDescription": "Gatorade",
      "price": "2.01"
    },{
      "shortDescription": "Gatorades",
      "price": "2.01"
    }
  ],
  "total": "12.06"
}


def test_process_receipt_valid():
    response = client.post("/receipts/process", json=valid_receipt)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], str)
    assert len(data["id"]) > 0

def test_process_receipt_invalid():
    # Invalid data: missing required field "retailer"
    invalid_receipt = valid_receipt.copy()
    del invalid_receipt["retailer"]

    response = client.post("/receipts/process", json=invalid_receipt)
    assert response.status_code == 422

def test_get_points_receipt_found():
    # First, submit a valid receipt
    process_response = client.post("/receipts/process", json=valid_receipt)
    receipt_id = process_response.json()["id"]

    # Then retrieve points using the returned ID
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    data = points_response.json()
    assert "points" in data
    assert isinstance(data["points"], int)

def test_get_points_receipt_not_found():
    fake_id = "nonexistent-id"
    response = client.get(f"/receipts/{fake_id}/points")
    assert response.status_code == 404
    assert response.json() == {"description": "No receipt found for that ID."}

def test_28_points():
    response = client.post("/receipts/process", json=twenty_eight_points)
    receipt_id = response.json()["id"]
    # Then retrieve points using the returned ID
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    data = points_response.json()
    points = data['points']
    assert data['points'] == 28

def test_109_points():
    response = client.post("/receipts/process", json=one_hundred_nine_points)
    receipt_id = response.json()["id"]
    # Then retrieve points using the returned ID
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    data = points_response.json()
    points = data['points']
    assert data['points'] == 109

# Why 42?
# 15 for retailer name
# 6 for odd purchase date
# 10 for special purchase time window
# 10 for having 4 items (5 * 2)
# 1 for Gatorades 2.01 * .2 rounded up to 1 
def test_42_points():
    response = client.post("/receipts/process", json=forty_two_points)
    receipt_id = response.json()["id"]
    # Then retrieve points using the returned ID
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    data = points_response.json()
    points = data['points']
    print(points)
    assert data['points'] == 42

# Ghost receipts are valid - but probably shouldn't be
# We could change some of the pattern regex for this in rules.py
def test_ghost_points():
    response = client.post("/receipts/process", json=ghost_receipt)
    receipt_id = response.json()["id"]
    # Then retrieve points using the returned ID
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    data = points_response.json()
    points = data['points']
    assert data['points'] == 96
