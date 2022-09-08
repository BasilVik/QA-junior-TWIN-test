import csv
import requests
import os.path

def check_operator_field_in_file(path_file_input, path_file_output):
    if not os.path.exists(path_file_input):
        print('Не найден файл с входными данными!')
        return

    if not os.path.exists(path_file_output):
        print('Не найден файл для записи выходных данных!')
        return

    with open(path_file_input, encoding='utf-8', mode='r') as r_file:
        fieldnames = ('phone_number', 'operator',)
        file_data = csv.DictReader(r_file, fieldnames=fieldnames)
        
        with open(path_file_output, mode='w', newline='', encoding='utf-8') as w_file:
            fieldnames = (
                'phone_number',
                'operator_in_file',
                'operator_in_rosreestr',
                'data_match'
            )
            writer = csv.DictWriter(w_file, fieldnames=fieldnames)
            writer.writeheader()
           
            for elem in file_data:
                phone_number_and_operator = dict(elem)
                phone_number = phone_number_and_operator['phone_number']
                operator_in_file = phone_number_and_operator['operator']
                operator_in_rosreestr = get_operator_in_rosreestr(phone_number)

                if operator_in_rosreestr == '':
                    writer.writerow(
                        {
                            'phone_number': phone_number,
                            'operator_in_file': operator_in_file,
                            'operator_in_rosreestr': operator_in_rosreestr,
                            'data_match': 2
                        }
                    )
                elif operator_in_rosreestr.lower().strip() == operator_in_file.lower().strip():
                    writer.writerow(
                        {
                            'phone_number': phone_number,
                            'operator_in_file': operator_in_file,
                            'operator_in_rosreestr': operator_in_rosreestr,
                            'data_match': 1
                        }
                    )
                else:
                    writer.writerow(
                        {
                            'phone_number': phone_number,
                            'operator_in_file': operator_in_file,
                            'operator_in_rosreestr': operator_in_rosreestr,
                            'data_match': 0
                        }
                    )


def get_operator_in_rosreestr(phone_number):
    req = requests.get(
        f'http://rosreestr.subnets.ru/?get=num&num={phone_number}&format=json'
    )
    req_data = req.json()
    if '0' in req_data.keys():
        if 'operator' in req_data['0'].keys():
            return req_data['0']['operator']
    return ''

path_file_input = input('Введите путь к файлу с входными данными: ')
path_file_output = input('Введите путь к файлу с выходными данными: ')

check_operator_field_in_file(path_file_input, path_file_output)
