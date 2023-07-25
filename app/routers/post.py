from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    print(limit)


    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

#@app.post("/createposts")
#def create_posts(payLoad: dict = Body(...)):
#    print(payLoad)
#    return {"new_post": f"title: {payLoad['title']} content: {payLoad['content']}"}
 
#Создание поста. user_id: int = Depends(oauth2.get_current_user) – проверка пользователя
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING * """, (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    #print(post.dict())
    print(current_user.id)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#@router.get("/latest")
#def get_latest_post():
    #post = cursor.execute("""SELECT * FROM posts ORDER BY ID DESC LIMIT 1""")
    #post = my_posts[len(my_posts)-1]
 #   return post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()


    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone() 
    #post = find_post(int(id))
    if not post: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    #ищем id

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    
    post_query.delete(synchronize_session=False)
    db.commit()
    

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    #return {'message': 'post was successfully deleted'}




@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title,post.content,post.published,id,))
    # updated_post = cursor.fetchone()
    # conn.commit()
    #ищем id
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    

    return post_query.first()


