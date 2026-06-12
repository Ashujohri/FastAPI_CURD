from fastapi import FastAPI
from app.routes import todo
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.config.app_config import getAppConfig

app = FastAPI()

# Includes all routes
app.include_router(todo.router)

@app.exception_handler(RequestValidationError)
async def validation_execption_handler(request, exc):
    errors = {}
    for error in exc.errors():
        print(f"The error is: {error}")
        errors[error["loc"][-1]] = error["msg"]
    
    return JSONResponse(
        {"message": "Validation error", "errors":errors},
        status_code= 422,
    )

@app.get("/")
def root():
    config = getAppConfig()
    return {
        "message": "Welcome to Fast API dummy Project",
        "app_name": config.app_name,
        "app_env": config.app_env,
        "database_url": config.database_url,
        }
