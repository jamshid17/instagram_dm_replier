import sqlite3




# conn = sqlite3.connect('data.db')
# c = conn.cursor()
# # c.execute(""" DELETE FROM users """)
# # c.execute("INSERT INTO users VALUES (:tm_id, :name, :ig_username, :ig_password, :step)", 
# #     {"tm_id":1, "name":'jame', 'ig_username':'jamejame', 'ig_password':'None', 'step':'username'})
# user_id = 1
# c.execute("SELECT * FROM users WHERE tm_id=:user_id;", {'user_id':user_id})

# # conn.commit()

# x = c.fetchall()
# print(x)
# conn.close()


def get_user_data(message=None, call=None):
    if message:
        user_id = message.from_user.id
        name = message.from_user.first_name
    else:
        user_id = call.from_user.id
        name = call.from_user.first_name
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE tm_id=:user_id;", {'user_id':user_id})
    result = c.fetchall()
    if result == []:
        c.execute("INSERT INTO users VALUES (:tm_id, :name, :step);", {"tm_id":user_id, "name":name, "step":"password"})
        c.execute("SELECT * FROM users WHERE tm_id=:user_id;", {'user_id':user_id})
        result = c.fetchall()
    conn.close()
    result = {'tm_id':result[0][0], 'name':result[0][1], 'ig_username':result[0][2], 
        'ig_password':result[0][3], 'step':result[0][4]}
    return result


def update_user_data(update_dict, message=None, call=None):
    if message:
        user_id = message.from_user.id
    else:
        user_id = call.from_user.id 
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    for key, value in update_dict.items():
        c.execute(f"UPDATE users SET {key}='{value}' WHERE tm_id='{user_id}';")
    conn.close()