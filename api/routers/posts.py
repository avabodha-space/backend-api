# list of all posts in classroom
# new post (instructor, owner)
# edit post by id (owner, or creator of post)
from fastapi import APIRouter
from api.utils.current_classroom import RC_sp_Dep, RC_ip_Dep, RC_o_Dep
from api.models.post import Post, PostIn, PostOut
from typing import List
from beanie import PydanticObjectId
from datetime import datetime
from api.utils.exceptions import post_not_found_exc

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/all")
async def all_posts(rc: RC_sp_Dep) -> List[PostOut]:
    return (
        await Post.find(Post.classroom.id == rc.classroom.id).project(PostOut).to_list()
    )


# @router.get("/edit")
# async def edit_post(rc:)


# /new
@router.post("/new")
async def create_new_post(rc: RC_ip_Dep, post_in: PostIn) -> PydanticObjectId:
    now = datetime.now()
    post = Post(**post_in.dict(), created=now, last_updated=now, classroom=rc.classroom)
    await post.insert()
    return post.id


@router.post("/edit/{post_id}")
async def edit_post(
    rc: RC_o_Dep, post_id: PydanticObjectId, post_in: PostIn
) -> PydanticObjectId:
    post = await Post.find_one(Post.id == post_id, Post.classroom.id == rc.classroom.id)
    if not post:
        raise post_not_found_exc
    # if not post.classroom.id == rc.classroom.id:
    #     raise
    post = post.copy(update=post_in.dict(exclude_unset=True))
    await post.save()
    return post.id
