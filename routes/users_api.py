from typing import List

from beanie import PydanticObjectId
from databases.connections import Database
from fastapi import APIRouter, Depends, HTTPException, status
from models.users import User
from fastapi import Request
from typing import Optional
router = APIRouter(
    tags=["User"]
)

# http://127.0.0.1:8000/users_api
'''
테스트 데이터
    {"name": "홍길동", "email": "gildong@example.com", "pswd": "gildong1234", "manager": "김매니저", "sellist1": "옵션A", "text": "문의사항이 있습니다. 연락주세요."}
'''
user_database = Database(User)

# 새로운 레코드 추가
@router.post("/")
async def create_event(body: User) -> dict:
    document = await user_database.save(body)
    return {
        "message": "user_data created successfully"
        ,"datas": document
    }



# id를 기준으로 row 확인
@router.get("/{id}/{pswd}", response_model=User)
async def retrieve_event(id: PydanticObjectId, pswd: Optional[str] = None):
    user_data = await user_database.get(id)
    user_data_dict = dict(user_data)
    
    if pswd != user_data_dict['pswd']:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="비밀번호가 일치 하지 않습니다."
        )

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user_data with supplied ID does not exist"
        )
    return user_data

# id에 따른 레코드 삭제
@router.delete("/{id}")
async def delete_user(id: PydanticObjectId) -> dict:
    user_data = await user_database.get(id)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user_data not found"
        )
    user_data = await user_database.delete(id)

    return {
        "message": "user_data deleted successfully."
        ,"datas": user_data
    }

# id로 업데이트

@router.put("/{id}", response_model=User)
async def update_user_data_withjson(id: PydanticObjectId, request:Request) -> User:
    user_data = await user_database.get(id)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user_data not found"
        )
    body = await request.json()
    updated_user_data = await user_database.update_withjson(id, body)
    if not updated_user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user_data with supplied ID does not exist"
        )
    return updated_user_data