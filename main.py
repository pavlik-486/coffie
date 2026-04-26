import fastapi
import uvicorn
import pydantic
from starlette.responses import JSONResponse
from database.database_operation import create_user


app = fastapi.FastAPI()


class ValidUser(pydantic.BaseModel):
    user_name: str
    user_phone: str


@app.post('/registration')
async def registration_user(data: ValidUser):
    result = await create_user(data)
    if result:
        return JSONResponse(status_code=201,
                        content={'successfully': f'user {data.user_name} have been created'})
    return JSONResponse(status_code=404,
                        content={"message": "Something went wrong"})




if __name__ == '__main__':
    uvicorn.run(app, log_level='info')