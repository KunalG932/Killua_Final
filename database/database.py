import pymongo, os
from config import DB_URL, DB_NAME, ADMINS, OWNER_ID

dbclient = pymongo.MongoClient(DB_URL)
database = dbclient[DB_NAME]
user_data = database['users']
admin_data = database['admins']

# Initialize admins collection with owner if it's empty
if admin_data.count_documents({}) == 0 and OWNER_ID:
    admin_data.insert_one({'_id': int(OWNER_ID), 'status': 'owner'})

req_one = database['req_one']  
req_two = database['req_two']




async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

# Admin management functions
async def is_admin(user_id: int):
    if user_id == OWNER_ID:
        return True, 'owner'
    admin = admin_data.find_one({'_id': user_id})
    return (True, admin['status']) if admin else (False, None)

async def add_admin(user_id: int, status='admin'):
    if user_id == OWNER_ID:
        return False, 'User is the owner'
    if (await is_admin(user_id))[0]:
        return False, 'User is already an admin'
    admin_data.insert_one({'_id': user_id, 'status': status})
    return True, f'Successfully added as {status}'

async def remove_admin(user_id: int):
    if user_id == OWNER_ID:
        return False, 'Cannot remove owner'
    result = admin_data.delete_one({'_id': user_id})
    return (True, 'Admin removed successfully') if result.deleted_count > 0 else (False, 'User is not an admin')

async def list_admins():
    admins = list(admin_data.find({}))
    return [(admin['_id'], admin.get('status', 'admin')) for admin in admins]

async def is_requested_one(message):
    user = await get_req_one(message.from_user.id)
    if user:
        return True
    if message.from_user.id in ADMINS:
        return True
    return False
    
async def is_requested_two(message):
    user = await get_req_two(message.from_user.id)
    if user:
        return True
    if message.from_user.id in ADMINS:
        return True
    return False

async def add_req_one(user_id):
    try:
        if not await get_req_one(user_id):
            await req_one.insert_one({"user_id": int(user_id)})
            return
    except:
        pass
        
async def add_req_two(user_id):
    try:
        if not await get_req_two(user_id):
            await req_two.insert_one({"user_id": int(user_id)})
            return
    except:
        pass

async def get_req_one(user_id):
    return req_one.find_one({"user_id": int(user_id)})

async def get_req_two(user_id):
    return req_two.find_one({"user_id": int(user_id)})

async def delete_all_one():
    req_one.delete_many({})

async def delete_all_two():
    req_two.delete_many({})










# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
