#!/usr/bin/env python

import argparse
import subprocess

VPN_HOSTNAME = '<VPN hostname>'  # Имя хоста VPN-сервера
VPN_USERNAME = '<Your username>'  # Ваше имя пользователя
VPN_PASSWORD = '<Your password>'  # Ваш пароль
VPN_OTPLABEL = '<The name of the keyring you created in the previous step, e.g. VPN>'  # Имя хранилища ключей, созданного в предыдущем шаге, например, VPN

def connect():
    # Получение одноразового пароля
    vpn_otpcode_cmd = ['./otp-cli/otp-cli', 'show', '-1', VPN_OTPLABEL, '|', 'grep', '-E', '-o', '([0-9]){{6}}']
    vpn_otpcode_output = subprocess.check_output(' '.join(vpn_otpcode_cmd), shell=True)
    vpn_otpcode = vpn_otpcode_output.strip().decode('utf-8')

    # Создание команды подключения к VPN-серверу
    vpn_connect_cmd = ['/opt/cisco/anyconnect/bin/vpn', '-s']
    vpn_connect_input = 'connect {}\n{}\n{}\n{}\nEOF'.format(VPN_HOSTNAME, VPN_USERNAME, VPN_PASSWORD, vpn_otpcode)

    # Подключение к VPN-серверу
    subprocess.check_call(' '.join(vpn_connect_cmd), input=vpn_connect_input, shell=True)

def disconnect():
    # Отключение VPN
    subprocess.check_call(['/opt/cisco/anyconnect/bin/vpn', 'disconnect'])

def status():
    # Проверка состояния VPN
    subprocess.check_call(['/opt/cisco/anyconnect/bin/vpn', 'status'])

def main():
    parser = argparse.ArgumentParser(description='Connect to a VPN server')
    parser.add_argument('-d', '--disconnect', action='store_true', help='disconnect from VPN')
    parser.add_argument('-s', '--status', action='store_true', help='check VPN status')
    args = parser.parse_args()

    if args.disconnect:
        disconnect()
    elif args.status:
        status()
    else:
        connect()

if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as e:
        print('Error:', e)
