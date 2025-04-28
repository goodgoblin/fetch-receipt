from app.models import Receipt
import math
# Assumes the receipt is a good receipt with all the right fields
# Goes through and counts up the points 
def count_points(receipt: Receipt):
    #start at zer0
    points = 0
    points += count_points_retailer_name(receipt)
    points += count_points_round_dollar(receipt)
    points += count_points_multiple_25(receipt)
    points += count_points_every_2_items(receipt)
    points += count_points_description_times_3(receipt)
    points += count_points_purchase_date_odd(receipt)
    points += count_points_purchase_time_2_to_4(receipt)
    return points

# 1 point for every alpha numeric character in a retailer name
def count_points_retailer_name(receipt: Receipt):
    #start at zer0
    points = 0
    for char in receipt.retailer:
        if char.isalnum():
            points+=1
    return points

# 50 points if it's a round dollar
def count_points_round_dollar(receipt: Receipt):
    #start at zer0
    points = 0
    if(receipt.total.endswith(".00")):
        points+=50
    return points

# 25 points if it's a multiple of .25
def count_points_multiple_25(receipt: Receipt):
    #start at zer0
    points = 0
    t = receipt.total
    if(t.endswith(".00") or t.endswith(".25") or t.endswith(".50") or t.endswith(".75")):
        points+=25
    return points

# 5 points for every 2 items
def count_points_every_2_items(receipt: Receipt):
    size = len(receipt.items)
    by_2 = size//2 # no remainder division
    return by_2 *5

# If the trimmed length of the item description is a multiple of 3,
# multiply the price by 0.2 and round up to the nearest integer.
def count_points_description_times_3(receipt: Receipt):
    #start at zer0
    points =0
    for item in receipt.items:
        trimmed = item.shortDescription.strip()
        size = len(trimmed)
        if size % 3 == 0:
            price = float(item.price)
            points+= math.ceil(price * .2)
    return points

# 6 points if the day in the purchase date is odd.
def count_points_purchase_date_odd(receipt: Receipt):
    if receipt.purchaseDate.day % 2 == 1:
        return 6
    else:
        return 0

# 10 points if the time of purchase is after 2:00pm and before 4:00pm.
def count_points_purchase_time_2_to_4(receipt: Receipt):
    if( receipt.purchaseTime.hour >=14 and receipt.purchaseTime.hour < 16):
        return 10
    else:
        return 0
