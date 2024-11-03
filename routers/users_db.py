### Users_DB API ###

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema
from db.client import db_client


router = APIRouter(prefix="/usersdb",
                tags=["usersdb"],
                responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
                )

#funcion para buscar un usuario creado
def search_user(field,key):
    try:
        user= db_client.local.users.find_one({field:key})
        return User(**(user_schema(user)))
    except:
        return {"error":"No se ha encontrado el usuario"}

    
### Peticiones

@router.get("/")
async def users_db():
    return " "


@router.post("/", response_model=User,status_code=status.HTTP_201_CREATED)
async def user(user: User):
    
    if type(search_user("email",user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail= "El usuario ya existe"
        ) # Verifica si el usuario ya existe
    
    user_dict= dict(user) #crear formato dict para user
    del user_dict["id"] #eliminar campo id para que lo genere automaticamente mongoDB
    
    id= db_client.local.users.insert_one(user_dict).inserted_id #crea usuario, inserta usuario y nos quedamos con el id
    
    new_user = user_schema(db_client.local.users.find_one({"_id":id})) # hacemos la transformacion en el formato para devolverlo despues de encontrarlo por id
    
    return User(**new_user)