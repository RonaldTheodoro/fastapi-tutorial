import enum
import typing

import fastapi
import uvicorn


class ModelName(str, enum.Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    letnet = 'letnet'


app = fastapi.FastAPI()


fake_items_db = [
    {'item_name': 'Foo'},
    {'item_name': 'Bar'},
    {'item_name': 'Baz'},
]

@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/items/{item_id}')
async def item(item_id: int):
    return {'item_id': item_id}


@app.get('/users/me')
async def read_user_me():
    return {'user_id': 'the current user'}


@app.get('/users/{user_id}')
async def read_user(user_id: str):
    return {'user_id': user_id}


@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {'model_name': model_name, 'message': 'Deep Learning FTW!'}

    if model_name.value == 'letnet':
        return {'model_name': model_name, 'message': 'LeCNN all the images'}

    return {'model_name': model_name, 'message': 'Have some residuals'}


@app.get('/files/{file_path:path}')
async def read_file(file_path: str):
    return {'file_path': file_path}


@app.get('/items/')
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get('/users/{user_id}/items/{item_id}')
async def read_item_query(
    user_id: int,
    item_id: str,
    q: typing.Optional[str] = None,
    short: bool = False
):
    item = {'item_id': item_id, 'owner_id': user_id}
    if q:
        item.update({'q': q})
    if not short:
        item.update(
            {
                'description': (
                    'This is an amazing item that has a long description'
                )
            }
        )
    return item

@app.get('/items_user/{item_id}')
async def read_user_item(
    item_id: str,
    needy: str,
    skip: int = 0,
    limit: typing.Optional[int] = None
):
    return {'item_id': item_id, 'needy': needy, 'skip': skip, 'limit': limit}


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True, debug=True)
