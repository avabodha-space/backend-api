from api.app import app

from api.routers import auth, register, user, classroom, posts


app.include_router(auth.router)
app.include_router(register.router)
app.include_router(user.router)
app.include_router(classroom.router)
app.include_router(posts.router)
