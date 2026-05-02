import fastapi
import uvicorn
import pydantic
from fastapi.params import Query
from starlette.responses import JSONResponse
from database.database_operation import create_user, add_dish, add_bar, get_all_bars, bars_menu


app = fastapi.FastAPI(debug=True)


class ValidUser(pydantic.BaseModel):
    user_name: str
    user_phone: str


class ValidBarAndDish(pydantic.BaseModel):
    coffie_bar_id: int = None
    bar_name: str = None
    name: str = None
    descriprion: str = None
    price: int = None


# добавить в проверяющие функции is_
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
async def add_coffie_bar(data: ValidBarAndDish):
    bar_name = data.bar_name
    result = await add_bar(bar_name)
    if result:
        return JSONResponse(status_code=201,
                            content={'successfully': f'bar {bar_name} have been added'})
    return JSONResponse(status_code=500,
                        content={"message": "coffee bar already added"})


@app.get('/bars') # все кофейни
async def all_coffee_bars():
    result = await get_all_bars()
    return JSONResponse(status_code=200, content=result)


@app.get('/bars_menu') # меню одной кофейни
async def menu_bar(bar_name: str = Query()):
    result = await bars_menu(bar_name)
    return JSONResponse(status_code=200, content=result)


@app.post('/create_order')
async def order():
    pass





if __name__ == '__main__':
    uvicorn.run(app, log_level='info')