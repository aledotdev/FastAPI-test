from fastapi import FastAPI


app = FastAPI(
    title="Ale.dev Test Challenge",
    version="0.0.1"
)


@app.get("/")
def main_function():
    """
    Home Page response
    """
    return {"Message": "Hello World"}

