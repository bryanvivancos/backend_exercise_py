### Users_DB API ###

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema,users_schema
from db.client import db_client
from bson import ObjectId


router = APIRouter(prefix="/usersdb",
                tags=["usersdb"],
                responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
                )

#funcion para buscar un usuario creado
def search_user(field: str ,key):
    try:
        user= db_client.local.users.find_one({field:key})
        return User(**(user_schema(user)))
    except:
        return {"error":"No se ha encontrado el usuario"}

### PETICIONES

# PETICION PARA BUSCAR USUARIOS

@router.get("/",response_model=list[User]) #Buscar todos 
async def users_db():
    return users_schema(db_client.local.users.find())

@router.get("/{id}") #Path
async def user(id: str):
    return search_user("_id", ObjectId(id))

@router.get("/") #Query
async def user(id:str):
    return search_user("_id",ObjectId(id))


# PETICION PARA AGREGAR USUARIO A DB

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

# PETICION PARA ELIMINAR USUARIOS

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    
    found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        return {"error": "No se ha eliminado el usuario"}
    
# PETICION PARA ACTUALIZAR USUARIO

@router.put("/", response_model=User)
async def user(user: User):
    
    user_dict= dict(user) #crear formato dict para user
    del user_dict["id"] #eliminar campo id para que lo genere automaticamente mongoDB
    
    try:
        db_client.local.users.find_one_and_replace({"_id":ObjectId(user.id)},user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}
    
    return search_user("_id",ObjectId(user.id))