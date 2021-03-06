import enum
import typing

import fastapi
import uvicorn
import pydantic


class ModelName(str, enum.Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    letnet = 'letnet'


class Item(pydantic.BaseModel):
    name: str
    description: typing.Optional[str] = None
    price: float
    tax: typing.Optional[float] = None


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
    return fake_items_db[skip: skip + limit]


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


@app.post('/items/')
async def create_item(item: Item):
    item_dict = item.dict()

    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})
    return item_dict


@app.put('/items/{item_id}')
async def update_item(item_id: int, item: Item, q: typing.Optional[str] = None):
    result = {'item_id': item_id, **item.dict()}
    if q:
        result.update({'q': q})
    return result


@app.get('/read_items/')
async def read_items(
    q: typing.Optional[str] = fastapi.Query(None, min_length=3, max_length=10)
):
    results = {'items': [{'item_id': 'Foo'}, {'item_id': 'Bar'}]}
    if q:
        results.update({'q': q})
    return results


@app.get('/cnpj/')
async def read_items(
    cnpj: str = fastapi.Query(..., regex='^\d{2}\.\d{3}\.\d{3}/\d{4}\-\d{2}$')
):
    return {'cnpj': cnpj}


@app.get('/cnpjs/')
async def cnpjs(c: typing.Optional[typing.List[str]] = fastapi.Query(None)):
    return {'c': c}


@app.get('/cpfs/')
async def cpfs(c: typing.List[str] = fastapi.Query(['456', '123'])):
    return {'c': c}


@app.get('/xelo/')
async def cpfs(
    c: typing.Optional[str] = fastapi.Query(
        None,
        title='cnjs',
        description='cnjs numbers',
        alias='item-query',
        deprecated=True
    ),
):
    return {'c': c}


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True, debug=True)
