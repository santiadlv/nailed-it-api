from ..core import settings
import pytest
import nest_asyncio
nest_asyncio.apply()

@pytest.mark.asyncio
async def test_get_all_reviews_by_salons(test_app):
    test_review = {
        "title": "Excellent Service",
        "date": "1998-09-05",
        "reviewDescription": "Excellent service Beautify Salon. Loved my shellac and the color.",
        "salon_id": "6085df4104159a9c9c81b968",
        "user_id": "605cdde73755ee16f9aeb90d",
        "service_id": "608608d7041aa13d76554244"
    }

    # CREATE A NEW REVIEW
    first_response = test_app.post("/reviews/new", json=test_review)
    assert first_response.status_code == 201
    assert first_response.json().get('message') == "Review created successfully"

    # GET COUNT OF THE JSON ARRAY THAT THE .GET FUNCTION RETURNS 
    s_id = test_review["salon_id"]
    response = test_app.get(f"/reviews/salon/{s_id}")
    data = (response.json().get('data'))
    size = len(data) #GET THE LENGTH OF THE LIST 
    print(size)

    # GET THE COUNT OF THE NUMBER OF DOCUMENTS INSIDE THE COLLECTION 
    count = await test_app.mongodb[settings.MONGODB_COLLECTION_REVIEWS].count_documents({"salon_id": test_review["salon_id"]})

    # # ASSERT THAT THE ROUTER FUNCTION RETURNS THE EXACT NUMBER OF DOCUMENTS INSIDE THE COLLETION 
    assert count == size

    # DELETE CREATED DOCUMENT
    delete_review = await test_app.mongodb[settings.MONGODB_COLLECTION_REVIEWS].find_one_and_delete({"_id": first_response.json().get("data")["_id"]})
    assert delete_review is not None
