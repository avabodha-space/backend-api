
from api.app import app

from api.routers import auth, register, user,classroom

app.include_router(auth.router)
app.include_router(register.router)
app.include_router(user.router)
app.include_router(classroom.router)
