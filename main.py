import fastapi
import uvicorn
import pydantic
from starlette.responses import JSONResponse
from database.database_operation import create_user, add_dish

app = fastapi.FastAPI()


class ValidUser(pydantic.BaseModel):
    user_name: str
    user_phone: str



class ValidBarAndDish(pydantic.BaseModel):
    coffie_bar_id: int
    coffie_bar_name: str
    name: str
    descriprion: str
    price: int


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
    coffie_bar_name = data.coffie_bar_name
    name_dish = data.name
    description = data.descriprion
    price = data.price
    await add_dish(coffie_bar_id, coffie_bar_name, name_dish, description, price)




if __name__ == '__main__':
    uvicorn.run(app, log_level='info')