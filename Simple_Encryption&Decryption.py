import random


def generate_key():
    key = ""
    while 1:
        if len(key) == 26:
            break;
        ran_num = random.randint(97, 122)
        if chr(ran_num) not in key:
            key += chr(ran_num)
    print("[KEY]", key)

    try:
        file = open("KEY.txt", "w", encoding='UTF8')
    except FileNotFoundError:
        print("[ERROR] File open error.")
        exit(-1)
    file.write(key)
    file.close()
    print("[SUCCESS] KEY.txt created.")
    return


def encryption():
    # key 파일 읽어들이기
    try:
        key_file = open("KEY.txt", "r", encoding='UTF8')
    except FileNotFoundError:
        print("[ERROR] There is no KEY.txt.")
        return
    key = ""
    for line in key_file:
        key += line
    key_file.close()

    # 원문 파일 읽어들이기
    fname = input("Plain File Name: ")
    try:
        plain_file = open(fname, "r", encoding='UTF8')
    except FileNotFoundError:
        print("[ERROR] Plain file open error.")
        exit(-1)
    plain_text = ""
    for line in plain_file:
        plain_text += line.lower()  # 소문자로 저장
    plain_file.close()
    
    # 암호문 파일 생성하기
    try:
        cipher_file = open("Cipher.txt", "w", encoding='UTF8')
    except FileNotFoundError:
        print("[ERROR] Cipher file open error.")
        exit(-1)
        
    # 암호화하기
    for char in plain_text:
        if char.isalpha():
            cipher_file.write(key[ord(char)-97])
        else:
            cipher_file.write(char)
    cipher_file.close()

    print("[SUCCESS] Cipher.txt created.")
    return


def decryption():
    # key 파일 읽어들이기
    try:
        key_file = open("KEY.txt", "r", encoding='UTF8')
    except FileNotFoundError:
        print("[ERROR] There is no KEY.txt.")
        return
    key = ""
    for line in key_file:
        key += line
    key_file.close()
    print("[KEY]", key)

    # 암호문 파일 읽어들이기
    try:
        cipher_file = open("Cipher.txt", "r", encoding='UTF8')
    except FileNotFoundError:
        print("[ERROR] Cipher file open error.")
        exit(-1)
    cipher_text = ""
    for line in cipher_file:
        cipher_text += line.lower()  # 소문자로 저장
    cipher_file.close()

    # 원문 파일 생성하기
    try:
        plain_file = open("Plain.txt", "w", encoding='UTF8')
    except FileNotFoundError:
        print("[ERROR] Plain file open error.")
        exit(-1)

    # 복호화하기
    for char in cipher_text:
        if char.isalpha():
            i = key.find(char)
            plain_file.write(chr(i+97))
        else:
            plain_file.write(char)
    plain_file.close()

    print("[SUCCESS] Plain.txt created.")
    return


while 1:
    print("[MENU] 1: Key Generation, 2: Encryption, 3: Decryption, 4: Exit")
    menu = input("Your input: ")
    if menu == '1':
        generate_key()
    elif menu == '2':
        encryption()
    elif menu == '3':
        decryption()
    elif menu == '4':
        exit(0)
    else:
        print("error")
