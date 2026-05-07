import fastapi
import uvicorn
import pydantic
from fastapi.params import Query
from starlette.responses import JSONResponse
from database.database_operation import (create_user,
                                         add_dish,
                                         add_bar,
                                         get_all_bars,
                                         bars_menu,
                                         create_order)
from datetime import time, datetime


app = fastapi.FastAPI(debug=True)


class ValidUser(pydantic.BaseModel):
    user_name: str
    user_phone: str


class ValidBarAndDish(pydantic.BaseModel):
    coffie_bar_id: int = None
    bar_name: str = None
    name: str = None
    open_time: time = None
    close_time: time = None
    descriprion: str = None
    price: int = None


class ValidOrder(pydantic.BaseModel):
    user_id: int
    bar_id: int
    coffee_id: int
    create_date: datetime = pydantic.Field(default_factory=datetime.now) # дописать формат
    get_order_date: datetime = pydantic.Field(description="Желаемая дата получения заказа (указывает пользователь)")


class Statistic(pydantic.BaseModel):
    bar_name: str
    start_time: datetime | None = None
    end_time: datetime | None = None
    date: datetime | None = None


# добавить в проверяющие функции is_
@app.post('/registration')
async def registration_user(data: ValidUser):
    new_name = data.user_name
    new_phone = data.user_phone
    if new_name and new_phone:
        is_result = await create_user(name=new_name, phone=new_phone)
        if is_result:
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
    is_result = await add_dish(coffie_bar_id, name_dish, description, price)
    if is_result:
        return JSONResponse(status_code=201,
                            content={'successfully': f'drink {name_dish} have been added'})
    return JSONResponse(status_code=500,
                        content={"message": "coffee_bar is not found or drink already added"})


@app.post('/add_bar')
async def add_coffie_bar(data: ValidBarAndDish):
    bar_name = data.bar_name
    open_time = data.open_time
    close_time = data.close_time
    result = await add_bar(bar_name, open_time, close_time)
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


@app.post('/create_order') # пишу это
async def order(data: ValidOrder):
    user_id = data.user_id
    bar_id = data.bar_id
    coffee_id = data.coffee_id
    create_date = data.create_date
    get_order_date = data.get_order_date
    is_result = await create_order(user_id, bar_id, coffee_id, create_date, get_order_date)
    if is_result:
        return JSONResponse(status_code=200,
                            content={'successfully': f'order for {user_id} have been created'})


@app.get('/period_statistic') #статистика за период
async def stat_month(data: Statistic):
    start = data.start_time
    end = data.end_time
    bar = data.bar_name
    result = {'bar': bar,
              'statistic period': f'{start} - {end}'}
    pass


@app.get('/date_stat') # статистика по дням
async def date_stat(data: Statistic):
    pass


if __name__ == '__main__':
    uvicorn.run(app, port=8000, log_level='info')