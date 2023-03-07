from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user=Depends(oauth2.get_current_user),
              limit: int = 0, skip: int = 0, search: Optional[str] = ""):
    if limit != 0:
        posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Post.id == models.Vote.post_id, isouter=True).order_by(
            models.Post.id).group_by(models.Post.id).limit(limit).offset(skip).filter(
            models.Post.title.contains(search)).all()
    else:
        posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).order_by(
            models.Post.id).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).all()
    return posts


@router.get("/my-posts", response_model=List[schemas.PostOut])
def get_my_posts(db: Session = Depends(get_db),
                 current_user=Depends(oauth2.get_current_user)):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).order_by(
        models.Post.id).group_by(models.Post.id).filter(
        models.Post.owner_id == current_user.id).all()
    return posts


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
             current_user=Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user=Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    else:
        if deleted_post.first().owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You are unauthorized to delete this post")
        deleted_post.delete(synchronize_session=False)
        db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    else:
        if updated_post.first().owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You are unauthorized to update this post")
        updated_post.update(post.dict(), synchronize_session=False)
        db.commit()
    return updated_post.first()
