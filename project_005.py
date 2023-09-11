import json
# 引入會員資料
global user_data
with open('user_data.json','r') as f:
    user_data = json.load(f)
    
# 引入商品資料
global product_list
with open('product.json','r') as f:
    product_list = json.load(f)

global login_status
login_status = True

global cart
cart = []

# 【系統功能-檢查帳號】
def is_user(username:str) -> bool:
    """
    根據給予的帳號，逐項檢查是否存在於資料集中。
    """
    for user in user_data:
        if user["username"] == username:
            return True
    return False

# 【系統功能-檢查電子郵件】
def check_email(email:str) -> bool:
    """
    根據給予的電子郵件，逐項檢查是否與資料集中的電子郵件重複。
    """
    for user in user_data:
        if user["email"] == email:
            return True
    return False

# 【系統功能-檢查電子郵件格式】
def is_valid_email(email:str) -> bool:
    """
    1. 輸入的電子郵件中只能有一個@，並且@不能出現在開頭或結尾。
    2. 以 @ 拆成兩個部分，前面的部分是「使用者名稱」，後面的部分是「域名」。
    3. @ 前後的「使用者名稱」、「域名」都要存在。
    4. 「域名」的部分要包含至少一個句點。
    """
    if email.count('@') != 1:
        return False
    
    name, domain = email.split('@')
    
    if not name or not domain:
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
    if len(pwd) < 8:
        return False
    has_upper, has_lower, has_digit = False, False, False
    
    # 檢查每個字符
    for char in pwd:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
            
    return has_upper and has_lower and has_digit
     
# 【系統功能-確認密碼】
def check_password(username:str, pwd:str) -> bool:
    """
    根據給予的帳號與密碼，逐項檢查是否與資料集中的帳號與密碼相符。
    """
    for user in user_data:
        if username == user["username"] and pwd == user["password"]:
            return True
    
    return False

# 【系統功能-檢查商品是否存在】
def is_product(item:str) -> bool:
    for product in product_list:
        if product['name'] == item:
            return True

# 【系統功能-檢查商品庫存是否足夠】
def is_sufficient(item:str, number:int) -> bool:
    for product in product_list:
        if product['name'] == item:
            if product['stock'] >= number:
                return True

# 【功能限制-登入後才能用的項目】
def check_login(func):
    def wrapper(*args, **kwargs):
        if login_status:
            func(*args, **kwargs)
        else:
            print("【請先登入】")
    return wrapper

# 【系統功能-加入購物車】
def add_to_cart(item:str, number:int):
    """
    1. 檢查商品是否存在。
    2. 檢查商品庫存是否足夠。
    3. 如果檢查都通過，則顯示「【{item}*{number} 已加入購物車!】」。
    """
    if not is_product(item):
        print("【我們沒有這個商品喔!】")
        return
    
    if not is_sufficient(item, number):
        print(f"【很抱歉，我們的庫存不足{number}份!> <】")
        return
    
    cart.append((item, number))
    print(f"【{item}*{number} 已加入購物車!】")
    pass

# 【系統功能-產生商品資訊】
def generate_product_info(page_number: int, page_size=10) -> str:
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size

    yield "|    商品名稱    |  售價  |   折扣  |  剩餘庫存  |        備註        |"
    yield "-" * 70
    for product in product_list[start_index:end_index]:
        name = product['name']
        price = f"{product['price']}元"
        discount = product['discount']
        stock = product['stock']
        remark = product['remark']

        # 處理打折名稱
        if discount == 1:
            discount_str = "　-"
        elif discount * 100 % 10 == 0:
            discount_str = f"{int(discount * 10)}折"
        else:
            discount_str = f"{int(discount * 100)}折"

        yield f"|{name:{chr(12288)}>8}|{price:>7}|{discount_str:>8}|{stock:>12}|{remark:{chr(12288)}>10}|"
    yield "-" * 70

# 【服務功能-會員註冊】
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
    # 設定帳號
    while True:
        new_username = input("設定帳號: ")
        if new_username == "q":
            return
        
        if is_user(new_username):
            print("【此帳號已被註冊！】")
        else:
            break
    # 設定電子郵件
    while True:
        
        new_email = input("設定電子郵件: ")
        if new_email == "q":
            return
        
        if not is_valid_email(new_email):
            print("【電子郵件格式錯誤！】")
            continue
            
        if check_email(new_email):
            print("【此電子郵件已被使用！】")
            continue
            
        else:
            break

    # 設定密碼
    while True:
        new_password = input("設定密碼: ")
        if new_password == "q":
            return
        if not is_valid_password(new_password):
            print("密碼安全性不足，長度需大於8個字元，且需包含大小寫字母與數字")
            continue
        else:
            check_email_password = input("確認密碼: ")
            if new_password != check_email_password:
                print("密碼不一致!請重新設定密碼")
                continue
            else:
                break
    
    # 建立新會員資料
    new_user_data = {"username": new_username, "email": new_email, "password": new_password}
    
    # 寫入資料庫
    with open('user_data.json','w') as f:
        user_data.append(new_user_data)
        json.dump(user_data, f)
    
    print("【註冊成功】")

# 【服務功能-會員登入】
def login():
    """
    1. 輸入帳號。如果帳號不存在，則顯示「查無此帳號，請先註冊再登入」。
    2. 輸入密碼。如果密碼錯誤，則顯示「密碼錯誤，請重新輸入一次(還有{chance}次機會)」，機會最多三次。
    3. 如果密碼錯誤超過三次，則顯示「密碼錯誤超過三次，請重新登入」。
    """
    while True:
        username = input("帳號: ")
        if not is_user(username):
            print("【查無此帳號，請先註冊再登入】")
            return
        else:
            break
    
    chance = 3
    while True:
        password_input = input("密碼: ")
        
        if check_password(username, password_input):
            print("【登入成功】")
            global login_status
            login_status = True
            return
        else:
            chance -= 1
            if chance == 0:
                print("密碼錯誤超過三次，請重新登入")
                return
            print(f"密碼錯誤，請重新輸入一次(還有{chance}次機會)")
            continue

# 【服務功能-會員登出】
@check_login
def logout():
    """
    將全域變數 login_status 設為 False，表示登出。
    """
    global login_status
    login_status = False
    print("【登出成功】")

# 【服務功能-查看商城清單】
def show_product_list():
    page_number = 1
    while True:
        for line in generate_product_info(page_number):
            print(line)
        
        print(f"第 {page_number} 頁，輸入 [p] 查看上一頁，輸入 [n] 查看下一頁，輸入 [q] 返回主目錄")
        user_input = input("請輸入指令: ")
        
        if user_input == "q":
            break
        elif user_input == "p":
            page_number -= 1
            if page_number < 1:
                page_number = 1
        elif user_input == "n":
            page_number += 1

# 【服務功能-開始購物】
@check_login
def shopping():
    print("【開始買東西!】")
    
    page_number = 1
    while True:
        for line in generate_product_info(page_number):
            print(line)
        print(f"第 {page_number} 頁，輸入 [p] 查看上一頁，輸入 [n] 查看下一頁，輸入 [q] 返回主目錄")
        print("🛒 加入購物車，請輸入商品名稱與數量，格式為「商品名稱 數量」，例如: 蘋果 3")
        
        user_input = input("我要: ")
        if user_input == "q":
            break
        elif user_input == "p":
            page_number -= 1
            if page_number < 1:
                page_number = 1
                continue
        elif user_input == "n":
            page_number += 1
            continue
        
        # 例外檢查
        try:
            item, number = user_input.split()
            number = int(number)
        except:
            print("輸入格式似乎有問題喔~ 請重新輸入一次")
            continue
        
        # 加入購物車
        add_to_cart(item, number)
    
    pass

# 【服務功能-查看購物車】
@check_login
def show_cart():
    """
    1. 若購物車是空的，則顯示「【購物車是空的喔!】」。
    2. 若購物車不是空的，則顯示購物車內容，格式如下：
    |    商品名稱    |  售價  |  數量  |   折扣  |  價格  |
    3. 商品名稱與備註的欄位，使用全形空白填滿。
    """
    if not cart:
        print("【購物車是空的喔!】")
        return
    
    print("【購物車內容】")
    print("-"*56)
    print("|    商品名稱    |  售價  |  數量  |   折扣  |   價格  |")
    print("-"*56)
    total = 0
    for item, number in cart:
        for product in product_list:
            if product['name'] == item:
                name = product['name']
                price = product['price']
                discount = product['discount']
                
                # 處理打折名稱
                if discount == 1:
                    discount = "　-"
                elif discount*100%10 == 0:
                    show_discount = str(int(discount*10))+"折"
                else:
                    show_discount = str(int(discount*100))+"折"
                
                # 計算價格
                sub_total = round(price*number*discount)
                total += sub_total
                sub_total = str(sub_total)+"元"
                print(f"|{name:{chr(12288)}>8}|{price:>8}|{number:>8}|{show_discount:>8}|{sub_total:>8}|")
    print("-"*56)
    print(f"|{'總計 '+str(total):>50}元|")
    print("-"*56)

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