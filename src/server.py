import socket

SERVER_IP = 'localhost'
SERVER_PORT = 9999
DATASET = {}


def byte_to_string(byte_data):
    return byte_data.decode('utf_8')


def string_to_byte(string_data):
    return string_data.encode('utf_8')


def read_file_store_in_dictionary():
    file = open("data.txt", encoding="ISO-8859-1")
    lines = file.readlines()
    for line in lines:
        attribute_list = line.split('|')
        attribute_list = [item.strip() for item in attribute_list]
        name = attribute_list[0].strip().lower()
        if name not in DATASET.keys():
            DATASET[name] = attribute_list[1:]


def switch(choice):
    switch_case = {
        1: find_customer,
        2: add_customer,
        3: delete_customer,
        4: update_customer_age,
        5: update_customer_address,
        6: update_customer_phone,
        7: print_report,
    }
    return switch_case.get(choice)


def get_attribute_from_request(request):
    attribute_list = request.split('|')
    return attribute_list[1:]


def format_single_record_line(list):
    record = "\n-----------------------------------------------"
    record = record + "\nName: " + list[0] + "\nAge: " + list[1] + "\nAddress: " + list[2] + "\nPhone: " + list[3]
    record = record + "\n-----------------------------------------------"
    return record


# Business logic

def find_customer(request):
    name, = get_attribute_from_request(request)
    if name in DATASET.keys():
        response = format_single_record_line([name] + DATASET[name])
        return response
    else:
        return "Customer not found"


def add_customer(request):
    name, age, address, phone = get_attribute_from_request(request)
    if name not in DATASET.keys():
        DATASET[name] = [age, address, phone]
        return "Customer has been added"
    else:
        return "Customer already exists"


def delete_customer(request):
    name, = get_attribute_from_request(request)
    if name in DATASET.keys():
        del DATASET[name]
        return name + "'s record has been successfully deleted"
    else:
        return "Customer does not exist"


def update_customer_age(request):
    name, age = get_attribute_from_request(request)
    if name in DATASET.keys():
        DATASET[name][0] = age
        return name + "'s age has been successfully updated"
    else:
        return "Customer not found"


def update_customer_address(request):
    name, address = get_attribute_from_request(request)
    if name in DATASET.keys():
        DATASET[name][1] = address
        return name + "'s address has been successfully updated"
    else:
        return "Customer not found"


def update_customer_phone(request):
    name, phone = get_attribute_from_request(request)
    if name in DATASET.keys():
        DATASET[name][2] = phone
        return name + "'s phone has been successfully updated"
    else:
        return "Customer not found"


def print_report(request):
    response = ''
    for key in DATASET.keys():
        response = response + format_single_record_line([key] + DATASET[key])
    return response


def main():
    read_file_store_in_dictionary()
    print("\nDataset loaded successfully")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((SERVER_IP, SERVER_PORT))

        print("\nServer is up and running. ")

        while True:
            request, address = s.recvfrom(1000)
            request = byte_to_string(request).strip()
            choice = int(request[0])
            func_to_execute = switch(choice)
            response = func_to_execute(request)
            s.sendto(string_to_byte(response), address)

    except (RuntimeError, OSError) as error:
        print("\nError occurred: ", error)
    finally:
        print('Closing the socket')
        s.close()


main()
