import asyncio
from datetime import datetime
from typing import Dict, List, Union, Optional

from VoteBot import app, LOGGER
from VoteBot.core.mongo import mongodb

# =====================================================
# USERS DATABASE
# =====================================================

usersdb = mongodb.users

async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    return bool(user)

async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list

async def add_served_user(user_id: int):
    if await is_served_user(user_id):
        return
    await usersdb.insert_one({"user_id": user_id, "joined_on": str(datetime.now())})

# ========================================
