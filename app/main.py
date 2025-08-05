from fastapi import FastAPI
from app.models import Base, engine
from app.routers import user, customer, product, order, auth
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(title="E-commerce Challenge")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])  
app.include_router(customer.router, prefix="/customers", tags=["Customers"])
app.include_router(product.router, prefix="/products", tags=["Products"])
app.include_router(order.router, prefix="/orders", tags=["Orders"])


@app.get("/")
def read_root():
    return {"message": "API operativa"}
