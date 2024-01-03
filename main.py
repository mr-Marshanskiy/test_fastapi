import uvicorn
from fastapi import FastAPI

# @app.post("/things")
# async def post_thing(thing: ThingModel, session: AsyncSession = Depends(get_async_session)):
#     session.add(Thing(text=thing.text))
#     await session.commit()
# @app.delete("/things/{id}")
# async def delete_thing(id: str, session: AsyncSession = Depends(get_async_session)):
#     thing = await session.get(Thing, id)
#     await session.delete(thing)
#     await session.commit()
# @app.put("/things/{id}")
# async def put_thing(id: str, new_thing: ThingModel, session: AsyncSession = Depends(get_async_session)):
#     thing = await session.get(Thing, id)
#     thing.text = new_thing.text
#     await session.commit()

from users.views import *
from articles.views import *
from config.signals import *

if __name__ == '__main__':
    uvicorn.run('config.apps:app', host='127.0.0.1', port=8080, reload=True)
