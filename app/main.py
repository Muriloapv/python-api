from fastapi import FastAPI

app = FastAPI()

#oque deve ter apos o localHost:8000, seu eu deixar @app.get('/'), ele vai cair na raiz apenas com o localhost8000
#ex: https://localhost:8000/product
@app.get("/")
def root():
    return{"mensagem" : "hello world."}
#         {chave      : valor         }
