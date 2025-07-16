from fastapi import APIRouter
from models.user_model import User
from database.config import client
from database.rules import Rules
from bson import ObjectId
import os

router = APIRouter()

@router.post("/")
async def leaderboard(user: User):
    user = dict(user)
    exsisting_user = Rules.get(client, os.getenv("DB_NAME"), "leaderboard", {"Name": user["profile_name"]})
    if exsisting_user is not None:
        exsisting_user["Matches"] += 1
        if sum(eval(user["score_list"])) >= int(user["target"]):
            exsisting_user["Won"] += 1
        exsisting_user["Runs"] += sum(eval(user["score_list"]))
        exsisting_user["6s"] += eval(user["score_list"]).count(6)

        Rules.update(client, os.getenv("DB_NAME"), "leaderboard", {"Name": user["profile_name"]}, exsisting_user)

        return
    else:
        total_score = sum(eval(user["score_list"]))
        if total_score >= int(user["target"]):
            won = True
        user_data = {}
        user_data["_id"] = ObjectId()
        user_data["Name"] = user["profile_name"]
        user_data["Matches"] = 1
        user_data["Won"] = 1 if won else 0
        user_data["Runs"] = total_score
        user_data["6s"] = eval(user["score_list"]).count(6)

        Rules.add(client, os.getenv("DB_NAME"), "leaderboard", user_data)
        return
    
@router.get("/leaderboard")
async def get_leaderboard():
    all_users = list(Rules.get_all(client, os.getenv("DB_NAME"), "leaderboard", {}))
    for user in all_users:
        user["_id"] = str(user["_id"])
        user["Rank"] = len(list(Rules.get_all(client, os.getenv("DB_NAME"), "leaderboard", {"Runs": {"$gt": user["Runs"]}}))) + 1
    all_users.sort(key=lambda x: x["Rank"], reverse=False)
    return all_users