from ..core import settings
import pytest
import nest_asyncio
nest_asyncio.apply()

@pytest.mark.asyncio
async def test_get_all_salons(test_app):
    # GET COUNT OF THE JSON ARRAY THAT THE .GET FUNCTION RETURNS 
    response = test_app.get("/salons/list")
    data = (response.json().get('data'))
    size = len(data) #GET THE LENGTH OF THE LIST 

    # GET THE COUNT OF THE NUMBER OF DOCUMENTS INSIDE THE COLLECTION 
    count = await test_app.mongodb[settings.MONGODB_COLLECTION_SALONS].count_documents({})

    # ASSERT THAT THE ROUTER FUNCTION RETURNS THE EXACT NUMBER OF DOCUMENTS INSIDE THE COLLETION 
    assert count == size
