import socket


class BgColor:
    SUCCESS = '\033[92m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'
    ERROR = '\033[91m'

    @staticmethod
    def color_error_wrapper(string):
        return BgColor.ERROR + string + BgColor.ENDC

    @staticmethod
    def color_bold_wrapper(string):
        return BgColor.BOLD + string + BgColor.ENDC

    @staticmethod
    def color_success_wrapper(string):
        return BgColor.SUCCESS + string + BgColor.ENDC


SERVER_IP = 'localhost'
SERVER_PORT = 9999
LIST = ["Python DB Menu",
        "1. Find customer",
        "2. Add customer",
        "3. Delete customer",
        "4. Update customer's age",
        "5. Update customer's address",
        "6. Update customer's phone",
        "7. Print report", "8. Exit"]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def display_options():
    print(BgColor.color_bold_wrapper(('\n' + LIST[0] + '\n\n' +
                                      LIST[1] + '\n' +
                                      LIST[2] + '\n' +
                                      LIST[3] + '\n' +
                                      LIST[4] + '\n' + LIST[5] + '\n' + LIST[6] + '\n' +
                                      LIST[7] + '\n' +
                                      LIST[8] + '\n')))


def take_input():
    flag = True
    while flag:
        choice = input("Select: ")
        if not choice.isnumeric():
            print(BgColor.color_error_wrapper("Error: Only numbers are allowed"))
            continue
        choice = int(choice)
        if choice not in range(1, 9):
            print(BgColor.color_error_wrapper("Error: Enter Valid Number"))
            continue
        flag = not flag
    return choice


def switch(choice):
    switch_case = {
        1: find_customer,
        2: add_customer,
        3: delete_customer,
        4: update_customer_age,
        5: update_customer_address,
        6: update_customer_phone,
        7: print_report,
        8: exit_client,
    }
    return switch_case.get(choice)


def byte_to_string(byte_data):
    return byte_data.decode('utf_8')


def send_request(message):
    s.sendto(message.encode('utf_8'), (SERVER_IP, SERVER_PORT))


def receive_response():
    response, address = s.recvfrom(10000)
    return BgColor.color_success_wrapper(byte_to_string(response))


def generic_input(field):
    flag = True
    while flag:
        value = input("Enter " + field + " ")
        if (field is "age" or field is "phone") and (not value.isnumeric()):
            print(BgColor.color_error_wrapper("Error:  " + field + " can't have anything other than numbers."))
            continue
        if field is "phone" and len(value) != 10:
            print(BgColor.color_error_wrapper("Error: Invalid Phone number must be 10 digit long."))
            continue
        flag = False
    return value


def append_attributes(list_of_attribute):
    body = ''
    for attribute in list_of_attribute:
        body = body + attribute + '|'
    return body.strip('|')


def find_customer():
    name = generic_input("name")
    send_request(append_attributes(["1", name.lower()]))
    print("\nResponse from Server : " + receive_response())


def add_customer():
    name = generic_input("name")
    age = generic_input("age")
    address = generic_input("address")
    phone = generic_input("phone")
    send_request(append_attributes(["2", name.lower(), age, address, phone]))
    print("\nResponse from Server : " + receive_response())


def delete_customer():
    name = generic_input("name")
    send_request(append_attributes(["3", name.lower()]))
    print("\nResponse from Server : " + receive_response())


def update_customer_age():
    name = generic_input("name")
    age = generic_input("age")
    send_request(append_attributes(["4", name.lower(), age]))
    print("\nResponse from Server : " + receive_response())


def update_customer_address():
    name = generic_input("name")
    address = generic_input("address")
    send_request(append_attributes(["5", name.lower(), address]))
    print("\nResponse from Server : " + receive_response())


def update_customer_phone():
    name = generic_input("name")
    phone = generic_input("phone")
    send_request(append_attributes(["6", name.lower(), phone]))
    print("\nResponse from Server : " + receive_response())


def print_report():
    send_request(append_attributes(["7"]))
    print("\nResponse from Server: " + receive_response())


def exit_client():
    exit()


while True:
    display_options()
    fun = switch(take_input())
    fun()
