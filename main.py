from typing import Optional,List,Set,Dict
from fastapi import FastAPI, Query , Path ,Body
from pydantic import BaseModel,Field,HttpUrl

app = FastAPI()


#Path parameter
@app.get("/items/{item_id}")
async def read_item(item_id:int):
    return {"item_id": item_id}

# -------------
#Query Parameter
# -------------
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# http://localhost:8000/getitems
# http://localhost:8000/getitems/?skip=2&limit=9

@app.get("/query/{item_id}")
def read_item(item_id: int, q: Optional[str]):
    return {"item_id": item_id, "q": q}

@app.get("/getitems/")
async def read_item(skip: int = 0, limit: int = 10):
    return {"skip" : skip , "limit":limit}

@app.get("/getqueryparam/{item_id}")

# http://localhost:8000/getqueryparam/1
# http://localhost:8000/getqueryparam/1?q=query&short=1

async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

#--------------
#Request Body
#-------------

class Image(BaseModel):
    url:HttpUrl
    name:str

class Item(BaseModel):
    name: str
    description: str =  Field(None, title="The description of the item", max_length=10)
    price: float
    tax: Optional[float] = None
    tags:List[str] = []
    image:Image # nested Model
    # tags:Set[str] = []


@app.post("/reqbody/")
#use postman
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


#--------------
#Query Parameter string validations
#--------------

@app.get("/queryvalidation/")
#we can use None or ... as required query parameter
# we can use regex and also we can pass default query parameter by replacing None to some values
async def read_items(q: str = Query(None, min_length=2,max_length=10,title = "String Validation",description="This for testing String Validation",alias="q-test")):  
    results = {"items": [{"a": "Foo"}, {"b": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#--------------
#Path Parameter string validations
#--------------
@app.get("/pathvalidation/{item_id}")
#we can use None or ... as required query parameter
#gt = greater than
#ge = greater than or equal to 
#lt = lesser than
#le = lesser than or equal to 
# we can use regex and also we can pass default query parameter by replacing None to some values
async def read_items(q: str = Query(None, min_length=2,max_length=10,title = "Query Validation",description="This for testing Query Validation",alias="q-test"),
                     item_id :float = Path(...,gt=2,lt=10,title = "Path Validation",description="This for testing Path Validation")):  
    results = {"items": [{"a": "Foo"}, {"b": "Bar"}]}
    if q:
        results.update({"q": q,"item_id":item_id})
    return results


#--------------
#Body Multiple Parameters => Making query Parameters as request Body
# --------------


class User(BaseModel):
    username: str
    full_name: Optional[str] = None



@app.put("/body_multiple/{item_id}")
async def update_item(
    item_id: int, item: Item, user: User, q: int = Body(...)
):
    results = {"item_id": item_id, "item": item, "user": user, "q": q}
    return results



#--------------
#Validations in Key/Value pair using Dict
# --------------

@app.put("/weights")
async def weights(weights:Dict[int,str]):
    return weights

# Special DataTypes like Date,Color,PaymentCard etc