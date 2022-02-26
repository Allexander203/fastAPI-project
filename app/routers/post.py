from fastapi import FastAPI, Response,status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN
from .. import models,schemas, oauth
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func
router = APIRouter(prefix = "/posts", tags=['Posts'])

#важно: ако path-a и към двете функии е един и същ, fastapi ще върне като резултат първият, който съвпада !

@router.get("/",response_model=List[schemas.PostOut])  
def get_posts(db: Session = Depends(get_db),
 current_user: int = Depends(oauth.get_current_user),
 Limit:int = 10, Skip:int = 0, search:Optional[str] = ""):

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(
    #     Limit).offset(Skip).all()#filter(models.Post.owner_id == current_user.id).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id,
        isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(
            search)).limit(Limit).offset(Skip).all()
    return posts

def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db), 
current_user: int = Depends(oauth.get_current_user)):#payLoad е име на променлива!
    #каквото и да се случва тук, то прави "unpacking" по-лесно 
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit() 
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)#id е path parameter
def get_post(id:int, db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))#ако получиш грешка тук, просто сложи запетая - (str(id),)
    #post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id,
        isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id {id} was not found")
    # if post.owner_id != current_user.id: ако искаш да извличаш само постовете на потребителят, от чийто профил си влязъл 
    #     raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=f"Not authorised to perform requested action")
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)): 

    post_query=db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=f"Not authorised to perform requested action")
    post_query.delete(synchronize_session=False)
    
    db.commit()

@router.put("/{id}",response_model=schemas.PostOut)
def update_post(id:int, updated_post:schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    # ако има проблем тук,върни се към оригиналната 'версия'. Виж репото за код .
    post_out_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id,
        isouter=True).group_by(models.Post.id).first()

    post = post_query.first()
   
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.update(updated_post.dict(),synchronize_session=False)
   
    db.commit()
    
    return post_out_query   