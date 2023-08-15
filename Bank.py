import json
import sys
from getpass import getpass
from time import sleep

DATA_FILE_PATH = "user.json"
ERROR_MESSAGE = "Hệ thống lỗi!"


def load_data(path):
    try:
        with open(path, mode='r', encoding='utf8') as file:
            return json.load(file)
    except IOError:
        sys.exit(ERROR_MESSAGE)


def update_data(users, data, path):
    for index, us in enumerate(data):
        if us['stk'] == users['stk']:
            data[index] = users
    try:
        with open(path, mode='w', encoding='utf8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except IOError:
        sys.exit(ERROR_MESSAGE)


def display_message(message):
    print(message)


def get_positive_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Vui lòng nhập số nguyên dương.")
        except ValueError:
            print("Vui lòng nhập số nguyên dương.")


def enter_account(list_user):
    for _ in range(3):
        stk = input("Nhập số tài khoản: ")
        for user in list_user:
            if user['stk'] == stk:
                return user
        display_message("Số tài khoản không tồn tại. Vui lòng nhập lại.")
    exits()


def validate_password(user):
    for _ in range(3):
        password = getpass("Nhập mật khẩu: ")
        if user['password'] == password:
            return True
        display_message(f"Sai mật khẩu. Bạn còn {2 - _} lần nhập.")
        if _ >= 2:
            exits()
    return False


def take_amount(user, data):
    amount = int(user['amount'])
    get_amount = get_positive_integer_input("Nhập số tiền muốn rút (Nhập 0 để thoát): ")
    if get_amount == 0:
        return
    for _ in range(3):
        if amount >= get_amount:
            amount -= get_amount
            user['amount'] = amount
            update_data(user, data, DATA_FILE_PATH)
            display_message(f"Đã rút {get_amount}. Số dư còn lại {amount}")
            return user
        else:
            get_amount = get_positive_integer_input("Số dư không đủ. Vui lòng nhập lại: ")


def transfer_money(user, data):
    while True:
        receive_bank = input(''' Chọn ngân hàng nhận :
        1. MB
        2. Techcombank
        3. Vietcombank
        4. Viettinbank
        5. Thoát
        ''')

        if receive_bank == '0':
            path = DATA_FILE_PATH
        elif receive_bank in ('1', '2', '3', '4'):
            path = f"{receive_bank.lower()}bank.json"
        else:
            display_message("Ngân hàng không hợp lệ!")
            break

        data_receive_bank = load_data(path)
        while True:
            receive_stk = input("Nhập số tài khoản nhận: ")
            receive_user = check_exist(data_receive_bank, receive_stk)
            if receive_user:
                amount_send = get_positive_integer_input("Nhập số tiền chuyển: ")
                if amount_send <= int(user['amount']):
                    receive_user['amount'] += amount_send
                    user['amount'] -= amount_send
                    display_message(f"Chuyển thành công số tìền {amount_send} cho {receive_user['name']}.")
                    update_data(receive_user, data_receive_bank, path)
                    update_data(user, data, DATA_FILE_PATH)
                    return user
                else:
                    display_message("Số dư không đủ.")
            else:
                display_message("Số tài khoản nhận không tồn tại")


def check_exist(data, stk):
    for dt in data:
        if dt['stk'] == stk:
            return dt


def check_balance(user):
    display_message(f"Số dư của bạn là: {user['amount']}")


def change_password(user, data):
    for _ in range(3):
        pass_old = getpass("Nhập mật khẩu cũ: ")
        if user['password'] == pass_old:
            pass_new = getpass("Nhập mật khẩu mới: ")
            for _ in range(3):
                if 6 <= len(pass_new) <= 15:
                    user['password'] = pass_new
                    update_data(user, data, DATA_FILE_PATH)
                    display_message("Đổi mật khẩu thành công.")
                    return user
                else:
                    display_message("Yêu cầu độ dài 6-15 ký tự.")
                    pass_new = getpass("Vui lòng nhập lại mật khẩu mới: ")
        else:
            display_message("Sai mật khẩu. Vui lòng nhập lại.")

    return user


def exits():
    display_message("Bạn đã nhập sai quá 3 lần. Kết thúc sau 15 giây.")
    sleep(15)
    sys.exit("Kết thúc")


def main():
    data_global = load_data(DATA_FILE_PATH)

    display_message("--- Chào mừng đến với ABC BANK ---")
    user_global = enter_account(data_global)

    if validate_password(user_global):
        while True:
            display_message("--- Chào mừng đến với ABC BANK ---")
            display_message(''' Chức năng : 
            1. Rút tiền
            2. Chuyển tiền
            3. Kiểm tra số dư
            4. Đổi mật khẩu
            5. Kết thúc
            ''')
            action = input("Nhập lựa chọn: ")

            if action == '1':
                user_global = take_amount(user_global, data_global)
            elif action == '2':
                user_global = transfer_money(user_global, data_global)
            elif action == '3':
                check_balance(user_global)
            elif action == '4':
                user_global = change_password(user_global, data_global)
            elif action == '5':
                do_logout = input("Bạn có đồng ý thoát (y/n): ")
                if do_logout.lower() == 'y':
                    sys.exit("Kết thúc!")
                else:
                    display_message("Lựa chọn không hợp lệ. Vui lòng chọn lại.")


if __name__ == "__main__":
    main()
