# Aplication for Codhab --#
# Daniel Moraes ----------#
# API - CRUD -------------#

from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI,Depends, HTTPException, status, Response
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.orm import Session
from models import Usuario 
from repositories import UsuarioRepository
from database import engine, Base, get_db
from schemas import UsuarioRequest, UsuarioResponse
import redis
import time
from flask import Flask


Base.metadata.create_all(bind=engine)

app = FastAPI()

##docker and flask #######################
#
#app = Flask(__name__)
#
#cache = redis.Redis(host='redis', port=6379)
#
#def get_hit_count():
#    retries = 5
#    while True:
#        try:
#            return cache.incr('hits')
#        except redis.exceptions.ConnectionError as exc:
#            if retries == 0:
#                raise exc
#            retries -= 1
#            time.sleep(0.5)
#######################################

@app.get("/")
def aplicacao_codhab():
    return {"Mensagem":"CRUD Codhab"}

#CADASTRO
@app.post("/api/usuarios/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED) #Requisicoes do tipo POST // Rotas de requisicoes //<< Injecao de dependencias >>
def create(request: UsuarioRequest, db: Session = Depends(get_db)):
    usuario = UsuarioRepository.save(db, Usuario(**request.dict()))
    return UsuarioResponse.from_orm(usuario)

#LISTAGEM
@app.get("/api/usuarios/",response_model=list[UsuarioResponse]) # E retornado apenas o status code 200 (requisicao processada com sucesso) o que ja eh padrao na rotina.
def find_all(db: Session = Depends(get_db)):
    usuarios = UsuarioRepository.find_all(db)
    return [UsuarioResponse.from_orm(usuario)for usuario in usuarios]

#BUSCA POR ID
@app.get("/api/usuarios/{id}", response_model = UsuarioResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    usuario = UsuarioRepository.find_by_id(db,id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario nao encontrado"
        )
    return UsuarioResponse.from_orm(usuario)

#EXCLUIR
@app.delete("/api/usuarios/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    if not UsuarioRepository.exists_by_id(db,id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario nao encontrado"
        )
    UsuarioRepository.delete_by_id(db,id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#ATUALIZACAO
@app.put("/api/usuarios/{id}",response_model=UsuarioResponse)
def update(id: int, request: UsuarioRequest,db: Session = Depends(get_db)):
    if not UsuarioRepository.exists_by_id(db, id):
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Usuario nao encontrado"
        )
    usuario = UsuarioRepository.save(db, Usuario(id=id, **request.dict()))
    return UsuarioResponse.from_orm(usuario)


