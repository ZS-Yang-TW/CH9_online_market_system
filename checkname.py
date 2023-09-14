# def check_email(input_email: str):

#     email_data = [
#         {"username": "JessicaChen", "email": "jennifernguyen@email.com"},
#         {"username": "LindaMiller", "email": "danieljohnson@email.com"},
#         {"username": "StevenYang", "email": "tmsycomtw@gmail.com"}
#     ]
#     for user_email in email_data:
#         if user_email["email"] == input_email:
#             return True
#     return False


# # 測試程式碼
# if __name__ == "__main__":
#     print(check_email("jennifernguyen@email.com"))
#     print(check_email("danieljohnson@email.com"))
#     print(check_email("tmsycomtw@gmail.com"))
#     print(check_email(""))


def is_valid_email(input_email: str) -> bool:

    if input_email.count('@') != 1:
        return False

    name, domain = input_email.split('@')

    if not name and not domain:
        return False

    if domain.count('.') < 1:
        return False

    return True


if __name__ == "__main__":
    print(is_valid_email("jennifernguyen@email.com"))  # 输出 True
    print(is_valid_email("danieljohnson@email.com"))  # 输出 True
    print(is_valid_email("tmsycomtw@gmail.com"))       # 输出 True
    print(is_valid_email("invalid.email.com"))         # 输出 False
    print(is_valid_email("invalid@.com"))              # 输出 False
    print(is_valid_email("invalid.com"))               # 输出 False
