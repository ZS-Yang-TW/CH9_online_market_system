import json

# 引入會員資料
global user_data
with open('user_data.json','r', encoding="utf-8") as f:
    user_data = json.load(f)

# 引入商品資料
global product_list
with open('product.json','r',encoding='utf-8') as f:
    product_list = json.load(f)

global login_status
login_status = False

global login_user
login_user = {}

global cart
cart = []

global register_data
register_data = {
    "username": "",
    "email": "",
    "password": "",
}

#print(user_data)
# 【系統功能-檢查帳號】
# 定义一个函数来检查用户名是否存在于用户数据中


def is_user(username: str):
    """
    根據給予的帳號，逐項檢查是否存在於資料集中。
    """
    for user in user_data:
        if user["username"] == username:
            return True
    return False

# 【系統功能-檢查電子郵件】
def check_email(email: str):
    """
    根據給予的帳號，逐項檢查是否存在於資料集中。
    """
    for user in user_data:
        if user["email"] == email:
            return True
    return False

# 【系統功能-檢查電子郵件格式】
def is_valid_email(email: str) -> bool:
    if email.count('@') != 1:
        return False

    name, domain = email.split('@')

    if not name and not domain:
        return False

    if domain.count('.') < 1:
        return False
    return True

# 【系統功能-檢查密碼安全性】
def is_valid_password(pwd:str) -> bool:
    """
    1. 密碼長度需大於8個字元。
    2. 密碼需包含大小寫字母與數字。
    """
    if len(pwd) < 8 :
        return False
    p_upper = False
    p_lower = False
    p_digit = False 
    for p in pwd :
        if all([p_upper, p_lower, p_digit]): 
            # 已滿足條件，不用繼續檢查
            break
        if p.isupper():
            p_upper = True
        if p.islower():
            p_lower = True
        if p.isdigit():
            p_digit = True 
    return p_upper and p_lower and p_digit

# 【系統功能-確認密碼】
def check_password(username:str, pwd:str) -> bool:
    """
    根據給予的帳號與密碼，逐項檢查是否與資料集中的帳號與密碼相符。
    若相同，回傳user資料
    """
    for data in user_data : 
        if username == data['username'] and pwd == data['password']:
            return data
    return False

# 【系統功能-檢查商品是否存在】
def is_product(item: str) -> bool or dict:
    """
    根據給予的商品名稱，逐項檢查是否存在於資料集中。
    若有值，回傳product資料
    """
    for product in product_list:
        if item ==  product['name']:
            return product
    return False

# 【系統功能-檢查商品庫存是否足夠】
def is_sufficient(item:str, number:int) -> bool:
    """
    根據給予的商品名稱，逐項檢查是否存在於資料集中。

    註: 此函式會檢查number是否為正整數，若不是則會拋出TypeError例外。
    例外訊息為「商品數量必須為正整數」。
    """
    try:
        if number <= 0:
            raise ValueError('商品數量需大於0')
        if type(number) != int:
            raise TypeError
        for product in product_list:
            if item ==  product['name'] and number <= product['stock']:
                return True     
        return False
    except TypeError:
        print("商品數量必須為正整數")
    except ValueError as err:
        print(err)
# 【功能限制-登入後才能用的項目】
def check_login(func):
    """
    此函式為裝飾器，需接收一個函式作為參數。

    這個裝飾器會使被裝飾的函式，只有在登入後才能執行。

    如果有登入，則執行原函式；如果沒有登入，則顯示「【請先登入】」。
    """
    def wrapper():
        if login_status:
            func()
            return
        print("【請先登入】")
    return wrapper

# 【系統功能-加入購物車】
def add_to_cart(item: str, number: int):
    """
    1. 檢查商品是否存在。如果不存在，則顯示「【我們沒有這個商品喔!】」。
    2. 檢查商品庫存是否足夠。如果不足，則顯示「【很抱歉，我們的庫存不足{number}份!> <】」。
    3. 如果檢查都通過，則以tuple的方式將商品及數量加入購物車串列，並顯示「【{item}*{number} 已加入購物車!】」。
    """
    product = is_product(item)
    if(not product):
        print('【我們沒有這個商品喔!】')
        return
    
    haveStock = is_sufficient(item, number)
    if(haveStock is None):
        return
    if(not haveStock):
        print('很抱歉，我們的庫存不足{number}份!> <】')
        return
    else:
        cart.append((product, number))
        print(f"【{item}*{number} 已加入購物車!】")

# 【系統功能-產生商品資訊】
def generate_product_info(page_number: int, page_size=10) -> str:
    """
    此函式是一個產生器，根據提供的頁數來產生商品資訊。
    1. 計算商品資料的起始索引與結束索引。
    2. 以yield的方式回傳商品資訊。
    3. 商品名稱與備註的欄位，使用全形空白填滿。
    4. 商品資訊的格式如下：
    |    商品名稱    |  售價  |   折扣  |  剩餘庫存  |        備註        |
    """
    startIndex = (page_number - 1) * page_size
    endIndex = startIndex + page_size
    
    yield "|    商品名稱    |  售價  |   折扣  |  剩餘庫存  |        備註        |"
    yield "-"*71
    for product in product_list[startIndex : endIndex]:
        name = product['name']
        price = f"{product['price']}元"
        discount = product['discount']
        stock = product['stock']
        remark = product['remark']

        if discount == 1:
            discountStr = "　-"
        elif discount * 100 % 10 == 0:
            discountStr = f"{int(discount * 10)}折"
        else:
             discountStr = f"{int(discount * 100)}折"

        yield f"|{name:{chr(12288)}>8}|{price:>7}|{discountStr:>8}|{stock:>12}|{remark:{chr(12288)}>10}|"   
    yield "-"*71
    pass

# 【服務功能[1]-會員註冊】
def register():
    """
    1. 設定帳號。如果帳號已存在，則顯示「【此帳號已被註冊!】」。
    2. 設定電子郵件。如果電子郵件格式錯誤，則顯示「【電子郵件格式錯誤】」。如果電子郵件已被使用，則顯示「【此電子郵件已被使用】」。
    3. 設定密碼。如果密碼安全性不足，則顯示「【密碼安全性不足，長度需大於8個字元，且需包含大小寫字母與數字】」。
       確認密碼。如果與密碼不一致，則顯示「【密碼不一致!請重新設定密碼】」。
    4. 如果以上檢查都通過，則建立新會員資料，並寫入資料庫。
    5. 寫入資料庫後，顯示「【註冊成功】」。

    備註:1~3的功能，輸入"q"即返為主目錄。
    """
    global register_data
    username = register_data["username"]
    email = register_data["email"]
    password = register_data["password"]
    # step 1
    if(username):
        print(f"設定帳號：{username}")
    else:
        username = input("設定帳號：")

    if is_user(username):
        print("【此帳號已被註冊!】")
        register_data["username"] = ""
        register()

    register_data["username"] = username
    # step 2
    if(email):
        print(f"設定電子郵件：{email}")
    else:
        email = input("設定電子郵件：")
    
    if not is_valid_email(email):
        print("【電子郵件格式錯誤】")
        register_data["email"] = ""
        register()
    else:
        if check_email(email):
            print("【此電子郵件已被使用】")
            register_data["email"] = ""
            register()
            
    register_data["email"] = email
    # step 3
    if(password):
        print(f"設定密碼：{password}")
    else:
        password = input("設定密碼：")
    
    if not is_valid_password(password):
        print("【密碼安全性不足，長度需大於8個字元，且需包含大小寫字母與數字】")
        register_data["password"] = ""
        register()
    else:
        register_data["password"] = password
        password_confirm = input("確認密碼：")
        if password != password_confirm:
            print("【密碼不一致!請重新設定密碼】")
            register()
            
    # step 4
    user_data.append(register_data)
    
    json_object = json.dumps(user_data, indent=4)
    with open("user_data.json", "w") as outfile:
        outfile.write(json_object)
    
    if is_user(username):
        print("【註冊成功】")
        register_data = {
            "username": "",
            "email": "",
            "password": "",
        }
    else:
        print("註冊發生錯誤，請稍後重試")
        register()

# 【服務功能[2]-會員登入】
def login():
    """
    1. 輸入帳號。如果帳號不存在，則顯示「【查無此帳號，請先註冊再登入】」。
    2. 輸入密碼。如果密碼錯誤，則顯示「【密碼錯誤，請重新輸入一次(還有{chance}次機會)】」，機會最多三次。
    3. 如果密碼錯誤超過三次，則顯示「【密碼錯誤超過三次，請重新登入】」。
    """
    global login_status
    global login_user

    if login_status:
        print("您已登入，請先登入")
        return

    # step 1 enter username
    username = input("帳號：")
    if not is_user(username):
        print("【查無此帳號，請先註冊再登入】")
        return
    
    # step 2 ender password (3 chances)
    chance = 2
    while(chance >= 0):
        password = input("密碼：")
        user = check_password(username, password)
        if user:
            login_status = True
            login_user = user
            print("【登入成功】")
            return
        else:
            print(f"【密碼錯誤，請重新輸入一次(還有{chance}次機會)】")
            chance -= 1
            
    print("【密碼錯誤超過三次，請重新登入】")
    return

# 【服務功能[3]-會員登出】
@check_login
def logout():
    """
    1. 詢問「【確定要登出嗎? [y/n]】」。
    2. 如果輸入y，則清空購物車，並將全域變數 login_status 設為 False，最後顯示「【登出成功】」。
    3. 如果輸入n，則不做任何事情。直接返回主目錄。
    """
    global login_status
    global login_user
    global cart
    user_input = input("【確定要登出嗎? [y/n]】")
    if user_input.lower() == 'y':
        login_status = False
        login_user = {}
        cart = []
        print("【登出成功】")
    elif user_input.lower() == 'n':
        return
    else:
        print("請輸入有效指令")
        logout()

# 【服務功能[4]-查看商城清單】
def show_product_list():
    """
    此函式會呼叫 generate_product_info 產生器，並顯示商品資訊。
    1. 請先設定頁數為1。
    2. 系統訊息為:「第 {page_number} 頁，輸入 [p] 查看上一頁，輸入 [n] 查看下一頁，輸入 [q] 返回主目錄」"
    """
    pass

# 【服務功能[5]-開始購物】
@check_login
def shopping():
    """
    此函式要經過check_login檢查，確認使用者是否登入。
    1. 先顯示「【開始買東西!】」。
    2. 請先設定頁數為1。
    3. 第一條系統訊息為:"第 {page_number} 頁，輸入 [p] 查看上一頁，輸入 [n] 查看下一頁，輸入 [q] 返回主目錄"
    4. 第二條系統訊息為:"🛒 加入購物車，請輸入商品名稱與數量，格式為「商品名稱 數量」，例如: 蘋果 3"
    5. 使用者輸入時，如果有輸入格式錯誤，則顯示「【輸入格式似乎有問題喔~ 請重新輸入一次】」。(請使用try except)
    6. 如果格式正確，則呼叫 add_to_cart 函式，將商品加入購物車。
    """
    pass

# 【服務功能[6]-查看購物車】
@check_login
def show_cart():
    """
    此函式要經過check_login檢查，確認使用者是否登入。
    1. 若購物車是空的，則顯示「【購物車是空的喔!】」。
    2. 若購物車不是空的，則顯示購物車內容，格式如下：
    |    商品名稱    |  售價  |  數量  |   折扣  |  價格  |
    3. 商品名稱與備註的欄位，使用全形空白填滿。
    4. 最後顯示總計多少錢。

    備註: 價格的計算方式為「售價*數量*折扣」，並四捨五入。
    """
    pass

# 【服務功能-主目錄】
def main():
    user_menu = """
歡迎來到「好頂線上生鮮超市」!
請輸入數字選擇服務項目:
    [1] 註冊
    [2] 登入
    [3] 登出
    [4] 商城清單
    [5] 開始買東西!
    [6] 查看購物車
"""

    while True:
        print(user_menu)

        user_input = input("請輸入指令: ")
        if user_input == "q":
            break

        if user_input == "1":
            register()

        elif user_input == "2":
            login()

        elif user_input == "3":
            logout()

        elif user_input == "4":
            show_product_list()

        elif user_input == "5":
            shopping()

        elif user_input == "6":
            show_cart()

if __name__ == "__main__":
    main()