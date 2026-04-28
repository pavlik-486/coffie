import fastapi
import uvicorn
import pydantic
from starlette.responses import JSONResponse
from database.database_operation import create_user, add_dish, add_bar


app = fastapi.FastAPI(debug=True)


class ValidUser(pydantic.BaseModel):
    user_name: str
    user_phone: str


class ValidBarAndDish(pydantic.BaseModel):
    coffie_bar_id: int
    name: str
    descriprion: str
    price: int

class ValidBar(pydantic.BaseModel):
    name: str


@app.post('/registration')
async def registration_user(data: ValidUser):
    new_name = data.user_name
    new_phone = data.user_phone
    if new_name and new_phone:
        result = await create_user(name=new_name, phone=new_phone)
        if result:
            return JSONResponse(status_code=201,
                            content={'successfully': f'user {data.user_name} have been created'})
        else:
            return JSONResponse(status_code=500,
                        content={"message": "this user is already exists"})
    return JSONResponse(status_code=422,
                        content={"message": "something went wrong"})


@app.post('/add_dish')
async def add_coffie_bar(data: ValidBarAndDish):
    coffie_bar_id = data.coffie_bar_id
    name_dish = data.name
    description = data.descriprion
    price = data.price
    result = await add_dish(coffie_bar_id, name_dish, description, price)
    if result:
        return JSONResponse(status_code=201,
                            content={'successfully': f'drink {name_dish} have been added'})
    return JSONResponse(status_code=500,
                        content={"message": "coffee_bar is not found or drink already added"})


@app.post('/add_bar')
async def add_coffie_bar(data: ValidBar):
    bar_name = data.name
    result = await add_bar(bar_name)
    if result:
        return JSONResponse(status_code=201,
                            content={'successfully': f'bar {bar_name} have been added'})
    return JSONResponse(status_code=500,
                        content={"message": "coffee bar already added"})




if __name__ == '__main__':
    uvicorn.run(app, log_level='info')