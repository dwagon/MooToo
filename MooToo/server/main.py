""" Run the game server"""

import time
import uvicorn
from fastapi import FastAPI, Request
from .server_utils import GALAXY
from MooToo.galaxy import save
from .routers import system, ship, planet, empire, galaxy

app = FastAPI()
app.include_router(system.router)
app.include_router(ship.router)
app.include_router(planet.router)
app.include_router(empire.router)
app.include_router(galaxy.router)


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
def save_game(filename):
    save(GALAXY, filename)


#####################################################################################################
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
# EOF
