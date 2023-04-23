from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
# This is the code to fetch all the trades from the api , i have also implemented sorting so if you want all 
# trades sorted you can give in first parameter like (trade_date_time or price or quantity) and in second paramter
# you can add (asc or desc )based on what you want 
def test_when_request_get_all_trades__response_status_code_should_be_200_ok():
    response = client.get("/Trade?sort_by=trade_date_time&sort_order=asc")
    assert response.status_code == 200
    # we can use desc also in place of asc
def test_when_request_get_all_trades_in_desc_order_response_status_code_should_be_200_ok():
    response = client.get("/Trade?sort_by=price&sort_order=desc")
    assert response.status_code == 200

# This is the code to get all trades by id available 
def test_when_request_get_trades_by_id__response_status_code_should_be_200_ok():
    response = client.get("/Trade/1")
    assert response.status_code ==200

# This is the code to get all the trades by any parameter available in instrument_id,instrument_name,traders, counterparty
# you can provide any value in the search if the value is included any of the above field it will include that trade

def test_when_request_to_search_by_any_name_present__response_status_code_should_be_200_ok():
    response = client.get("/Trade/Search?search=John Smith")
    assert response.status_code ==200

# This is the request to get all the trades according to the filteration we want minPrice ,maxPrice , buy_sell_indicator
# asset_class , trade_date_time start and trade_date_time end 
def test_when_we_try_to_filter_trades_according_to_the_maxPrice_minPrice_buy_sell_indicator__response_status_code_should_be_200_ok():
    response  = client.get("/Trade/filter?minPrice=100&maxPrice=3000&buy_sell_indicator=BUY")
    assert response.status_code ==200


# I have also add a post method from  where we can push new trade  in the database but i am not mentioning it in the 
# test cases because it is not the part of the test cases or work that was given 
