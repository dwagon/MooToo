""" Run the game server"""

from typing import Annotated
import time
import uvicorn
from fastapi import FastAPI, Request, Depends
from MooToo.galaxy import save, Galaxy
from .routers import system, ship, planet, empire, galaxy, build_queue
from .server_utils import get_galaxy

app = FastAPI()
app.include_router(system.router)
app.include_router(ship.router)
app.include_router(planet.router)
app.include_router(empire.router)
app.include_router(galaxy.router)
app.include_router(build_queue.router)


#####################################################################################################
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


#####################################################################################################
@app.post("/save/{filename}")
def save_game(filename, gal: Annotated[Galaxy, Depends(get_galaxy)]):
    save(gal, filename)


#####################################################################################################
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# EOF
