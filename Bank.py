import json
from getpass import getpass
from time import sleep

count_failed = 0
action = 0
data_global = []
DATA_FILE_PATH = "user.json"
# Dữ liệu user mặc định
user_global = {
    "stk": "",
    "name": "",
    "amount": "",
    "password": ""
}


def load_data(path):
    with open(path, mode='r', encoding='utf8') as file:
        return json.load(file)


# Truyền vào users hiện tại, data file cũ, đường dẫn đến file để update
def update_data(users, data, path):
    # Duyệt data cũ nếu có users trùng stk thì thay bằng users hiện tại
    for index, us in enumerate(data):
        if us['stk'] == users['stk']:
            data[index] = users
    # Ghi data mới vào file
    with open(path, mode='w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# Hàm nhập stk trả về dữ liệu của user để dùng các chức năng
def enter_account(list_user):
    global count_failed
    for _ in range(3):
        stk = input("Nhập số tài khoản : ")
        for user in list_user:
            if user['stk'] == stk:
                count_failed = 0
                return user
        print("Số tài khoản không tồn tại. Vui lòng nhập lại.")
        count_failed += 1

    if count_failed >= 3:
        exits()


def validate_password(user):
    global count_failed
    password = getpass("Nhập mật khẩu : ")
    if user['password'] == password:
        count_failed = 0
        print("Đăng nhập thành công.")
        return True
    else:
        print(f"Sai mật khẩu. Bạn còn {2 - count_failed} lần nhập.")
        if count_failed >= 2:
            exits()
        else:
            count_failed += 1
            return False


# Tìm user bằng stk
def get_user_by_stk(stk, data_user):
    for user in data_user:
        if user['stk'] == stk:
            return user


# Rút tiền
# Truyền vào dữ liệu user đã đăng nhập
def take_amount(user, data_old):
    global user_global
    amount = int(user['amount'])
    get_amount = int(input("Nhập số tiền muốn rút (Nhập 0 để thoát): "))
    if get_amount == 0:
        return
    for _ in range(3):
        if amount >= get_amount:
            amount -= get_amount
            user['amount'] = amount
            update_data(user, data_old, DATA_FILE_PATH)  # Cập nhật lại dữ liệu
            print(f"Đã rút {get_amount}. Số dư còn lại {amount}")
            return user
        else:
            get_amount = int(input("Số dư không đủ. Vui lòng nhập lại : "))


# Chuyển tiền
def transfer(user, data):
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
        elif receive_bank == '1':
            path = "mbbank.json"
        elif receive_bank == '2':
            path = "techcombank.json"
        elif receive_bank == '3':
            path = "vietcombank.json"
        elif receive_bank == '4':
            path = "viettinbank.json"
        else:
            break

        data_receive_bank = load_data(path)  # Lấy danh sách user ngân hàng nhận
        while True:
            receive_stk = input("Nhập số tài khoản nhận : ")
            receive_user = check_exist(data_receive_bank, receive_stk)  # Dữ liệu người nhận
            if receive_user is not None:
                amount_send = int(input("Nhập số tiền chuyển : "))
                if amount_send <= int(user['amount']):
                    receive_amount_new = int(receive_user['amount']) + amount_send
                    receive_user['amount'] = receive_amount_new
                    user_amount_new = int(user['amount']) - amount_send
                    user['amount'] = user_amount_new
                    print(f"Chuyển thành công số tìền {amount_send} cho {receive_user['name']}.")
                    update_data(receive_user, data_receive_bank, path)
                    update_data(user, data, DATA_FILE_PATH)  # Cập nhật dữ liệu
                    return user
                else:
                    print("Số dư không đủ.")
            else:
                print("Số tài khoản nhận không tồn tại")


def check_exist(data, stk):
    for dt in data:
        if dt['stk'] == stk:
            return dt


def check_amount(user):
    print(f"Số dư của bạn là : {user['amount']}")


# Đổi mật khẩu
def change_password(user, data):
    pass_old = getpass("Nhập mật khẩu cũ : ")
    for _ in range(3):
        if user['password'] == pass_old:
            pass_new = getpass("Nhập mật khẩu mới : ")
            for _ in range(3):
                if len(pass_new) in range(6, 16):
                    user['password'] = pass_new
                    update_data(user, data, DATA_FILE_PATH)
                    print("Đổi mật khẩu thành công.")
                    return user
                else:
                    print("Yêu cầu độ dài 6-15 ký tự.")
                    pass_new = getpass("Vui lòng nhập lại mật khẩu mới : ")
        else:
            print("Sai mật khẩu. Vui lòng nhập lại.")
            pass_old = getpass("Mật khẩu cũ : ")

    return user


def exits():
    print("Bạn đã nhập sai quá 3 lần. Kết thúc sau 15 giây.")
    sleep(15)
    exit()


def main():
    global count_failed, action, user_global, data_global

    data_global = load_data(DATA_FILE_PATH)

    print("--- Chào mừng đến với ABC BANK ---")
    user_global = enter_account(data_global)
    if count_failed >= 3:
        exits()

    while count_failed != 3:

        if validate_password(user_global):
            count_failed = 0
            while True:
                # if user_global is None:
                #     user_global = enter_account(data_global)
                #     while True:
                #         if validate_password(user_global):
                #             break

                print("--- Chào mừng đến với ABC BANK ---")
                print(''' Chức năng : 
                1. Rút tiền
                2. Chuyển tiền
                3. Kiểm tra số dư
                4. Đổi mật khẩu
                5. Kết thúc
                ''')
                action = input("Nhập lựa chọn : ")
                # Đặt lại giá trị cho user và danh sách user sau mỗi thao tác
                if action == '1':
                    user_global = take_amount(user_global, data_global)
                    data_global = load_data(DATA_FILE_PATH)
                elif action == '2':
                    user_global = transfer(user_global, data_global)
                    data_global = load_data(DATA_FILE_PATH)
                elif action == '3':
                    check_amount(user_global)
                elif action == '4':
                    user_global = change_password(user_global, data_global)
                    data_global = load_data(DATA_FILE_PATH)
                # elif action == '5':
                #     user_global = None
                elif action == '5':
                    exit()
                else:
                    print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")


if __name__ == "__main__":
    main()
