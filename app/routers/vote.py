from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from ..oauth2 import get_current_user
from sqlalchemy.orm import Session
from ..schemas import NewVote
from ..models import Vote, Post
router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(new_vote: NewVote, db: Session = Depends(get_db),
         current_user=Depends(get_current_user)):
    check_post = db.query(Post).filter(Post.id == new_vote.post_id)
    if not check_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with the id of {new_vote.post_id} was not found")
    vote_query = db.query(Vote).filter(
        Vote.post_id == new_vote.post_id, Vote.user_id == current_user.id)
    if not vote_query.first():
        vote = Vote(user_id=current_user.id, post_id=new_vote.post_id)
        db.add(vote)
        db.commit()
        db.refresh(vote)
        return {"Message": f"{current_user.email} Upvoted Post with id of {new_vote.post_id}"}
    else:
        vote_query.delete(synchronize_session=False)
        db.commit()
    # return {"Message": "working"}
