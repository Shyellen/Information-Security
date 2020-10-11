from string import ascii_lowercase
from itertools import permutations
import operator


def getCipher():
    fname = input("input file name?: ")
    try:
        file = open(fname, "r", encoding='UTF8')
    except FileNotFoundError:
        print("[ERROR] Type file name correctly.")
        exit(1)

    text = ""
    for line in file:
        text += line.lower()  # 소문자로 저장
    file.close()

    return text


def getFrequency(text):
    global alpha_list
    get_freq = {string: 0 for string in alpha_list}

    for char in text:
        try:
            if char.isalpha():
                get_freq[char] += 1
        except KeyError:
            pass

    # 알파벳 빈도 수로 딕셔너리 정렬
    get_freq = dict(sorted(get_freq.items(), key=operator.itemgetter(1), reverse=True))

    return get_freq


def RedundancyCheck(key_dict, expect_dict):
    # 추측 중인 알파벳 수만큼 반복: 추측 중인 알파벳 전체 확인
    for i in range(len(expect_dict)):
        # expect_dict 에서 가장 빈도수 점수가 높은 것을 선택
        expect = max(expect_dict.items(), key=operator.itemgetter(1))[0]

        try:
            # expect가 이미 매칭된 key_dict에 없다면 리턴해줌.
            if expect not in key_dict.values():
                return expect
            else:  # 이미 매치된 알파벳이 맞다면 제외 후
                del (expect_dict[expect])
                #  다시 for문으로 돌아가서 빈도수 높은 걸 선택
        except KeyError:
            # 가끔 발생하길래 예외처리 해줬음
            pass
    return


def decryptionA(key_dict):  # A 탐색
    global word_list
    A_dict = {}

    for word in word_list:  # 한 글자는 A와 I
        if len(word) == 1 and word.isalpha():
            if word in A_dict:
                A_dict[word] += 1
            else:
                A_dict[word] = 1

    A_list = list(A_dict.keys())  # A로 예상되는 알파벳 리스트

    # 3글자인 단어를 봤을 때 더 많은 게 A임. I는 잘 없음
    # ex) and, say, can, all, has, was, add, art, ...
    for word in word_list:
        if len(word) == 3:
            for i in range(len(A_list)):  # A로 예상되는 알파벳 전체 확인
                if A_list[i] in word:  # 단어에 A가 들어가면 점수 추가
                    A_dict[A_list[i]] += 1

    if A_dict:
        expect = RedundancyCheck(key_dict, A_dict)
        key_dict['a'] = expect

    print("[DEBUG] A:", key_dict['a'])
    decryptionTHE(key_dict)
    return


def decryptionTHE(key_dict):  # THE 탐색
    global word_list
    global freq_dict
    THE_dict = {}
    freq_list = list(freq_dict.keys())

    for word in word_list:  # a가 없는 세 글자 단어 탐색
        if len(word) == 3 and word.isalpha():
            if key_dict['a'] not in word:
                flag = 0
                for i in range(6):  # 빈도 수 상위 6위까지의 알파벳 포함 여부 확인
                    if freq_list[i] in word:
                        flag += 1  # 빈도 수가 높은 알파벳이 포함되어 있다면 flag++
                if flag >= 2:  # 빈도 수가 높은 알파벳이 두 개 이상 있으면
                    if word in THE_dict:  # 점수++
                        THE_dict[word] += 1
                    else:
                        THE_dict[word] = 1

    if len(THE_dict) > 4:
        top = 4
    else:
        top = len(THE_dict)

    for i in range(top):
        expect = max(THE_dict.items(), key=operator.itemgetter(1))[0]
        key_dict['t'] = expect[0]
        key_dict['h'] = expect[1]
        key_dict['e'] = expect[2]
        del (THE_dict[expect])
        print("*****************************************************")
        print("[DEBUG] THE:", expect, end=", ")
        decryptionO(key_dict)

    return


def decryptionO(key_dict):  # O 탐색
    global word_list
    O_dict = {}

    for word in word_list:
        if len(word) == 2 and word.isalpha():
            if word[0] == key_dict['t']:  # T_
                if word[1] in O_dict:
                    O_dict[word[1]] += 1
                else:
                    O_dict[word[1]] = 1

    if O_dict:
        expect = RedundancyCheck(key_dict, O_dict)
        key_dict['o'] = expect
    print("O:", key_dict['o'], end=", ")
    decryptionI(key_dict)
    return


def decryptionI(key_dict):  # I 탐색
    global word_list
    I_dict = {}

    for word in word_list:
        if len(word) == 1 and word.isalpha():  # 한 글자 짜리는 A와 I밖에 없음.
            if word != key_dict['a']:
                if word in I_dict:
                    I_dict[word] += 1
                else:
                    I_dict[word] = 1
        elif len(word) == 2 and word.isalpha():
            if word[1] == key_dict['t']:  # at이 아니면 반드시 it이다.
                if word[0] != key_dict['a']:
                    if word[0] in I_dict:
                        I_dict[word[0]] += 5
                    else:
                        I_dict[word[0]] = 5
        elif len(word) == 5 and word.isalpha():
            if word[0] == key_dict['t']:  # the__ 단, the_e 제외. their 저격
                if word[1] == key_dict['h']:
                    if word[2] == key_dict['e']:
                        if word[4] != key_dict['e']:
                            if word[3] in I_dict:
                                I_dict[word[3]] += 5
                            else:
                                I_dict[word[3]] = 5

    if I_dict:
        expect = RedundancyCheck(key_dict, I_dict)
        key_dict['i'] = expect
    print("I:", key_dict['i'], end=", ")
    decryptionS(key_dict)
    return


def decryptionS(key_dict):  # S 탐색
    global word_list
    S_dict = {}

    for word in word_list:
        if len(word) == 3 and word.isalpha():
            if word[0] == key_dict['i']:  # its
                if word[1] == key_dict['t']:
                    if word[2] in S_dict:
                        S_dict[word[2]] += 5
                    else:
                        S_dict[word[2]] = 5
        elif len(word) == 4 and word.isalpha():  # this
            if word[0] == key_dict['t']:
                if word[1] == key_dict['h']:
                    if word[2] == key_dict['i']:
                        if word[3] in S_dict:
                            S_dict[word[3]] += 5
                        else:
                            S_dict[word[3]] = 5
        elif len(word) == 5 and word.isalpha():  # these
            if word[0] == key_dict['t']:
                if word[1] == key_dict['h']:
                    if word[2] == key_dict['e']:
                        if word[4] == key_dict['e']:
                            if word[3] in S_dict:
                                S_dict[word[3]] += 1
                            else:
                                S_dict[word[3]] = 1

    if S_dict:
        expect = RedundancyCheck(key_dict, S_dict)
        key_dict['s'] = expect
    print("S:", key_dict['s'], end=", ")
    decryptionR(key_dict)
    return


def decryptionR(key_dict):  # R 찾기
    global word_list
    R_dict = {}

    for word in word_list:
        if len(word) == 3 and word.isalpha():
            if word[0] == key_dict['a']:  # a_e
                if word[2] == key_dict['e']:
                    if word[1] in R_dict:
                        R_dict[word[1]] += 1
                    else:
                        R_dict[word[1]] = 1
        elif len(word) == 4 and word.isalpha():
            if word[0] == key_dict['a']:  # a_ea
                if word[2] == key_dict['e']:
                    if word[3] == key_dict['a']:
                        if word[1] in R_dict:
                            R_dict[word[1]] += 1
                        else:
                            R_dict[word[1]] = 1
            if word[1] == key_dict['e']:  # _e_e, were, here 저격
                if word[3] == key_dict['e']:
                        if word[2] in R_dict:
                            R_dict[word[2]] += 1
                        else:
                            R_dict[word[2]] = 1
        elif len(word) >= 5 and word.isalpha():
            if word[0] == key_dict['o']:  # othe_
                if word[1] == key_dict['t']:
                    if word[2] == key_dict['h']:
                        if word[3] == key_dict['e']:
                            if word[4] in R_dict:
                                R_dict[word[4]] += 5
                            else:
                                R_dict[word[4]] = 5

    if R_dict:
        expect = RedundancyCheck(key_dict, R_dict)
        key_dict['r'] = expect
    print("R:", key_dict['r'], end=", ")
    decryptionD(key_dict)
    return


def decryptionD(key_dict):  # D 탐색
    global word_list
    D_dict = {}

    for word in word_list:
        if len(word) == 3 and word.isalpha():  # ha_. had 저격
            if word[0] == key_dict['h']:
                if word[1] == key_dict['a']:
                    if word[2] != key_dict['s']:
                        if word[2] != key_dict['t']:
                            if word[2] in D_dict:
                                D_dict[word[2]] += 5
                            else:
                                D_dict[word[2]] = 5
        elif len(word) == 4 and word.isalpha():  # said
            if word[0] == key_dict['s']:
                if word[1] == key_dict['a']:
                    if word[2] == key_dict['i']:
                        if word[3] in D_dict:
                            D_dict[word[3]] += 10
                        else:
                            D_dict[word[3]] = 10
    if D_dict:
        expect = RedundancyCheck(key_dict, D_dict)
        key_dict['d'] = expect
    print("D:", key_dict['d'], end=", ")
    decryptionN(key_dict)
    return


def decryptionN(key_dict):  # N 탐색
    global word_list
    N_dict = {}

    for word in word_list:
        if len(word) == 2 and word.isalpha():
            if word[0] == key_dict['a']:  # a_. an 저격
                if word[1] != key_dict['t']:
                    if word[1] != key_dict['s']:
                        if word[1] in N_dict:
                            N_dict[word[1]] += 1
                        else:
                            N_dict[word[1]] = 1
        elif len(word) == 3 and word.isalpha():
            if word[0] == key_dict['o']:  # o_e. one 저격
                if word[2] == key_dict['e']:
                    if word[1] != key_dict['r']:
                        if word[1] in N_dict:
                            N_dict[word[1]] += 1
                        else:
                            N_dict[word[1]] = 1
            elif word[1] == key_dict['o']:  # _ot. not 저격
                if word[2] == key_dict['t']:
                    if word[0] != key_dict['h']:
                        if word[0] != key_dict['d']:
                            if word[0] in N_dict:
                                N_dict[word[0]] += 1
                            else:
                                N_dict[word[0]] = 1
            elif word[0] == key_dict['a']:  # a_d. and 저격
                if word[2] == key_dict['d']:
                    if word[1] != key_dict['i']:
                        if word[1] in N_dict:
                            N_dict[word[1]] += 5
                        else:
                            N_dict[word[1]] = 5

    if N_dict:
        expect = RedundancyCheck(key_dict, N_dict)
        key_dict['n'] = expect
    print("N:", key_dict['n'], end=", ")
    decryptionF(key_dict)
    return


def decryptionF(key_dict):  # FOR, OF에서 f 골라내기
    global word_list
    F_dict = {}

    for word in word_list:
        if len(word) == 2 and word.isalpha():  # o_
            if word[0] == key_dict['o']:
                if word[1] != key_dict['r']:
                    if word[1] != key_dict['h']:
                        if word[1] != key_dict['n']:
                            if word[1] in F_dict:
                                F_dict[word[1]] += 1
                            else:
                                F_dict[word[1]] = 1
        elif len(word) == 3 and word.isalpha():  # _or
            if word[1] == key_dict['o']:
                if word[2] == key_dict['r']:
                    if word[0] != key_dict['n']:
                        if word[0] in F_dict:
                            F_dict[word[0]] += 1
                        else:
                            F_dict[word[0]] = 1

    if F_dict:
        expect = RedundancyCheck(key_dict, F_dict)
        key_dict['f'] = expect

    print("F:", key_dict['f'], end=", ")
    decryptionW(key_dict)
    return


def decryptionW(key_dict):  # W 탐색
    global word_list
    W_dict = {}

    for word in word_list:
        if len(word) == 3 and word.isalpha():
            if word[1] == key_dict['a']:  # was
                if word[2] == key_dict['s']:
                    if word[0] != key_dict['h']:
                        if word[0] in W_dict:
                            W_dict[word[0]] += 3
                        else:
                            W_dict[word[0]] = 3
            elif word[0] == key_dict['n']:
                if word[1] == key_dict['e']:  # new
                    if word[2] != key_dict['t']:
                        if word[2] in W_dict:
                            W_dict[word[2]] += 1
                        else:
                            W_dict[word[2]] = 1
                elif word[1] == key_dict['o']:  # now
                    if word[2] != key_dict['t']:
                        if word[2] in W_dict:
                            W_dict[word[2]] += 1
                        else:
                            W_dict[word[2]] = 1
        elif len(word) >= 4 and word.isalpha():
            if word[1] == key_dict['i']:  # with
                if word[2] == key_dict['t']:
                    if word[3] == key_dict['h']:
                        if word[0] in W_dict:
                            W_dict[word[0]] += 3
                        else:
                            W_dict[word[0]] = 3
            if word[1] == key_dict['e']:  # were
                if word[2] == key_dict['r']:
                    if word[3] == key_dict['e']:
                        if word[0] in W_dict:
                            W_dict[word[0]] += 2
                        else:
                            W_dict[word[0]] = 2

    if W_dict:
        expect = RedundancyCheck(key_dict, W_dict)
        key_dict['w'] = expect
    print("W:", key_dict['w'], end=", ")
    decryptionV(key_dict)
    return


def decryptionV(key_dict):  # V 탐색
    global word_list
    V_dict = {}

    for word in word_list:
        if len(word) == 4 and word.isalpha():  # have
            if word[0] == key_dict['h']:
                if word[1] == key_dict['a']:
                    if word[3] == key_dict['e']:
                        if word[2] in V_dict:
                            V_dict[word[2]] += 3
                        else:
                            V_dict[word[2]] = 3
            elif word[0] == key_dict['o']:  # over
                if word[2] == key_dict['e']:
                    if word[3] == key_dict['r']:
                        if word[1] in V_dict:
                            V_dict[word[1]] += 2
                        else:
                            V_dict[word[1]] = 2
        if len(word) >= 4 and word.isalpha():
            if word[0] == key_dict['e']:  # even
                if word[2] == key_dict['e']:
                    if word[3] == key_dict['n']:
                        if word[1] in V_dict:
                            V_dict[word[1]] += 1
                        else:
                            V_dict[word[1]] = 1
        if len(word) >= 5 and word.isalpha():
            if word[-4] == key_dict['t']:  # ____tive
                if word[-3] == key_dict['i']:
                    if word[-1] == key_dict['e']:
                        if word[-2] in V_dict:
                            V_dict[word[-2]] += 1
                        else:
                            V_dict[word[-2]] = 1

    if V_dict:
        expect = RedundancyCheck(key_dict, V_dict)
        key_dict['v'] = expect

    print("V:", key_dict['v'], end=", ")
    decryptionB(key_dict)
    return


def decryptionB(key_dict):  # B 탐색
    global word_list
    B_dict = {}

    for word in word_list:
        if len(word) == 2 and word.isalpha(): # be, by
            if word[0] != key_dict['i']:
                if word[0] != key_dict['t']:
                    if word[0] != key_dict['o']:
                        if word[0] != key_dict['a']:
                            if word[0] != key_dict['h']:
                                if word[0] != key_dict['w']:
                                    if word[1] != key_dict['o']:
                                        if word[1] != key_dict['s']:
                                            if word[0] in B_dict:
                                                B_dict[word[0]] += 4
                                            else:
                                                B_dict[word[0]] = 4
        elif len(word) == 4 and word.isalpha():  # been
            if word[1] == key_dict['e']:
                if word[2] == key_dict['e']:
                    if word[3] == key_dict['n']:
                        if word[0] != key_dict['s']:
                            if word[0] in B_dict:
                                B_dict[word[0]] += 8
                            else:
                                B_dict[word[0]] = 8

    if B_dict:
        expect = RedundancyCheck(key_dict, B_dict)
        key_dict['b'] = expect
    print("B:", key_dict['b'], end=", ")
    decryptionG(key_dict)
    return


def decryptionG(key_dict):  # G 탐색
    global word_list
    G_dict = {}

    for word in word_list:
        if len(word) >= 5 and word.isalpha():  # ___ing
            if word[-3] == key_dict['i']:
                if word[-2] == key_dict['n']:
                    if word[-1] != key_dict['e']:
                        if word[-1] != key_dict['s']:
                            if word[-1] != key_dict['a']:
                                if word[-1] in G_dict:
                                    G_dict[word[-1]] += 1
                                else:
                                    G_dict[word[-1]] = 1

    if G_dict:
        expect = RedundancyCheck(key_dict, G_dict)
        key_dict['g'] = expect
    print("G:", key_dict['g'], end=", ")
    decryptionM(key_dict)
    return


def decryptionM(key_dict):  # M 탐색
    global word_list
    M_dict = {}

    for word in word_list:
        if len(word) == 4 and word.isalpha():
            if word[0] == key_dict['f']:  # fro_
                if word[1] == key_dict['r']:
                    if word[2] == key_dict['o']:
                        if word[3] != key_dict['g']:
                            if word[3] in M_dict:
                                M_dict[word[3]] += 10
                            else:
                                M_dict[word[3]] = 10
            elif word[1] == key_dict['o']:  # _ost
                if word[2] == key_dict['s']:
                    if word[3] == key_dict['t']:
                        if word[0] != key_dict['h']:
                            if word[0] in M_dict:
                                M_dict[word[0]] += 1
                            else:
                                M_dict[word[0]] = 1
            elif word[0] == key_dict['s']:  # so_e
                if word[1] == key_dict['o']:
                    if word[3] == key_dict['e']:
                        if word[2] in M_dict:
                            M_dict[word[2]] += 2
                        else:
                            M_dict[word[2]] = 2
        elif len(word) >= 7 and word.isalpha(): # america
            if word[0] == key_dict['a']:
                if word[2] == key_dict['e']:
                    if word[3] == key_dict['r']:
                        if word[4] == key_dict['i']:
                            if word[6] == key_dict['a']:
                                if word[1] in M_dict:
                                    M_dict[word[1]] += 10
                                else:
                                    M_dict[word[1]] = 10
    if M_dict:
        expect = RedundancyCheck(key_dict, M_dict)
        key_dict['m'] = expect
    print("M:", key_dict['m'], end=", ")
    decryptionK(key_dict)
    return


def decryptionK(key_dict):  # K 탐색
    global word_list
    K_dict = {}

    for word in word_list:
        if len(word) >= 4 and word.isalpha():
            if word[1] == key_dict['n']:  # know
                if word[2] == key_dict['o']:
                    if word[3] == key_dict['w']:
                        if word[0] != key_dict['s']:
                            if word[0] in K_dict:
                                K_dict[word[0]] += 1
                            else:
                                K_dict[word[0]] = 1
            elif word[0] == key_dict['t']:  # take
                if word[1] == key_dict['a']:
                    if word[3] == key_dict['e']:
                        if word[2] in K_dict:
                            K_dict[word[2]] += 2
                        else:
                            K_dict[word[2]] = 2
        if len(word) == 4 and word.isalpha():
            if word[0] == key_dict['m']:  # make
                if word[1] == key_dict['a']:
                    if word[3] == key_dict['e']:
                        if word[2] != key_dict['d']:
                            if word[2] != key_dict['t']:
                                if word[2] in K_dict:
                                    K_dict[word[2]] += 1
                                else:
                                    K_dict[word[2]] = 1
    if K_dict:
        expect = RedundancyCheck(key_dict, K_dict)
        key_dict['k'] = expect
    print("K:", key_dict['k'], end=", ")
    decryptionY(key_dict)
    return


def decryptionY(key_dict):  # Y 탐색
    global word_list
    Y_dict = {}

    for word in word_list:
        if len(word) == 2 and word.isalpha():
            if word[0] == key_dict['b']:
                if word[1] != key_dict['e']:
                    if word[1] != key_dict['i']:
                        if word[1] in Y_dict:
                            Y_dict[word[1]] += 10
                        else:
                            Y_dict[word[1]] = 10
        elif len(word) == 3 and word.isalpha():
            if word[0] == key_dict['t']:  # try
                if word[1] == key_dict['r']:
                    if word[2] in Y_dict:
                        Y_dict[word[2]] += 1
                    else:
                        Y_dict[word[2]] = 1
            elif word[0] == key_dict['w']:  # way
                if word[1] == key_dict['a']:
                    if word[2] != key_dict['s']:
                        if word[2] in Y_dict:
                            Y_dict[word[2]] += 1
                        else:
                            Y_dict[word[2]] = 1
            elif word[0] == key_dict['s']:  # say
                if word[1] == key_dict['a']:
                    if word[2] in Y_dict:
                        Y_dict[word[2]] += 1
                    else:
                        Y_dict[word[2]] = 1
        elif len(word) == 4 and word.isalpha():
            if word[0] == key_dict['m']:  # many
                if word[1] == key_dict['a']:
                    if word[2] == key_dict['n']:
                        if word[3] in Y_dict:
                            Y_dict[word[3]] += 1
                        else:
                            Y_dict[word[3]] = 1
            elif word[0] == key_dict['t']:  # they
                if word[1] == key_dict['h']:
                    if word[2] == key_dict['e']:
                        if word[3] != key_dict['m']:
                            if word[3] in Y_dict:
                                Y_dict[word[3]] += 1
                            else:
                                Y_dict[word[3]] = 1

    if Y_dict:
        expect = RedundancyCheck(key_dict, Y_dict)
        key_dict['y'] = expect
    print("Y:", key_dict['y'], end=", ")
    decryptionL(key_dict)
    return


def decryptionL(key_dict):  # L 탐색
    global word_list
    L_dict = {}

    for word in word_list:
        if len(word) >= 3 and word.isalpha():  # ___ll
            if word[-2] == word[-1]:
                if word[-1] != key_dict['s']:
                    if word[-1] != key_dict['o']:
                        if word[-1] != key_dict['f']:
                            if word[-1] != key_dict['e']:
                                if word[-1] in L_dict:
                                    L_dict[word[-1]] += 5
                                else:
                                    L_dict[word[-1]] = 5
            elif word[-1] == key_dict['y']:  # ___ly
                if word[-2] != key_dict['a']:
                    if word[-2] != key_dict['r']:
                        if word[-2] != key_dict['n']:
                            if word[-2] != key_dict['g']:
                                if word[-2] in L_dict:
                                    L_dict[word[-2]] += 5
                                else:
                                    L_dict[word[-2]] = 5
        elif len(word) == 4 and word.isalpha():
            if word[0] == key_dict['a']:  # a_so
                if word[2] == key_dict['s']:
                    if word[3] == key_dict['o']:
                        if word[1] in L_dict:
                            L_dict[word[1]] += 1
                        else:
                            L_dict[word[1]] = 1
            elif word[1] == key_dict['i']:  # _ike
                if word[2] == key_dict['k']:
                    if word[3] == key_dict['e']:
                        if word[0] != key_dict['h']:
                            if word[0] != key_dict['b']:
                                if word[0] != key_dict['n']:
                                    if word[1] in L_dict:
                                        L_dict[word[1]] += 1
                                    else:
                                        L_dict[word[1]] = 1

    if L_dict:
        expect = RedundancyCheck(key_dict, L_dict)
        key_dict['l'] = expect
    print("L:", key_dict['l'], end=", ")
    decryptionU(key_dict)
    return


def decryptionU(key_dict):  # U 탐색
    global word_list
    U_dict = {}

    for word in word_list:
        if len(word) == 3 and word.isalpha():
            if word[1] == key_dict['s']:  # use
                if word[2] == key_dict['e']:
                    if word[0] in U_dict:
                        U_dict[word[0]] += 1
                    else:
                        U_dict[word[0]] = 1
            elif word[0] == key_dict['b']:  # but
                if word[2] == key_dict['t']:
                    if word[1] in U_dict:
                        U_dict[word[1]] += 1
                    else:
                        U_dict[word[1]] = 1
            elif word[0] == key_dict['o']:  # out
                if word[2] == key_dict['t']:
                    if word[1] in U_dict:
                        U_dict[word[1]] += 1
                    else:
                        U_dict[word[1]] = 1
        elif len(word) == 5 and word.isalpha():
            if word[0] == key_dict['a']:  #abo_t
                if word[1] == key_dict['b']:
                    if word[2] == key_dict['o']:
                        if word[4] == key_dict['t']:
                            if word[3] in U_dict:
                                U_dict[word[3]] += 10
                            else:
                                U_dict[word[3]] = 10

    if U_dict:
        expect = RedundancyCheck(key_dict, U_dict)
        key_dict['u'] = expect
    print("U:", key_dict['u'], end=", ")
    decryptionQ(key_dict)
    return


def decryptionQ(key_dict):  # Q 탐색. 거의 없음.
    global word_list
    Q_dict = {}

    for word in word_list:
        if len(word) >= 5 and word.isalpha():
            if word[1] == key_dict['u']:
                if word[2] == key_dict['i']:  # qui
                    if word[0] != key_dict['b']:
                        if word[0] in Q_dict:
                            Q_dict[word[0]] += 1
                        else:
                            Q_dict[word[0]] = 1
                elif word[2] == key_dict['e']:  # que
                    if word[0] in Q_dict:
                        Q_dict[word[0]] += 1
                    else:
                        Q_dict[word[0]] = 1

    if Q_dict:
        expect = RedundancyCheck(key_dict, Q_dict)
        key_dict['q'] = expect
    print("Q:", key_dict['q'], end=", ")
    decryptionC(key_dict)
    return


def decryptionC(key_dict):  # C 탐색
    global word_list
    C_dict = {}

    for word in word_list:
        if len(word) == 3 and word.isalpha():  # _an
            if word[1] == key_dict['a']:
                if word[2] == key_dict['n']:
                    if word[0] in C_dict:
                        C_dict[word[0]] += 5
                    else:
                        C_dict[word[0]] = 5
        if len(word) >= 3 and word.isalpha():  # a_t
            if word[0] == key_dict['a']:
                if word[2] == key_dict['t']:
                    if word[1] != key_dict['r']:
                        if word[1] != key_dict['l']:
                            if word[1] in C_dict:
                                C_dict[word[1]] += 5
                            else:
                                C_dict[word[1]] = 5
        if len(word) == 4 and word.isalpha():
            if word[0] == key_dict['e']:  # ea_h
                if word[1] == key_dict['a']:
                    if word[3] == key_dict['h']:
                        if word[2] in C_dict:
                            C_dict[word[2]] += 1
                        else:
                            C_dict[word[2]] = 1
            elif word[0] == key_dict['m']:  # mu_h
                if word[1] == key_dict['u']:
                    if word[3] == key_dict['h']:
                        if word[2] in C_dict:
                            C_dict[word[2]] += 1
                        else:
                            C_dict[word[2]] = 1
            elif word[0] == key_dict['s']:  # su_h
                if word[1] == key_dict['u']:
                    if word[3] == key_dict['h']:
                        if word[2] in C_dict:
                            C_dict[word[2]] += 1
                        else:
                            C_dict[word[2]] = 1
        elif len(word) == 5 and word.isalpha():  # which
            if word[0] == key_dict['w']:
                if word[1] == key_dict['h']:
                    if word[2] == key_dict['i']:
                        if word[4] == key_dict['h']:
                            if word[3] in C_dict:
                                C_dict[word[3]] += 1
                            else:
                                C_dict[word[3]] = 1
        if len(word) == 5 and word.isalpha():  # could
            if word[1] == key_dict['o']:
                if word[2] == key_dict['u']:
                    if word[3] == key_dict['l']:
                        if word[4] == key_dict['d']:
                            if word[0] in C_dict:
                                C_dict[word[0]] += 1
                            else:
                                C_dict[word[0]] = 1
    if C_dict:
        expect = RedundancyCheck(key_dict, C_dict)
        key_dict['c'] = expect
    print("C:", key_dict['c'], end=", ")
    decryptionJ(key_dict)
    return


def decryptionJ(key_dict):  # J 탐색
    global word_list
    J_dict = {}

    for word in word_list:
        if 3 <= len(word) <= 4 and word.isalpha():  # _ob
            if word[1] == key_dict['o']:
                if word[2] == key_dict['b']:
                    if word[0] != key_dict['m']:
                        if word[0] in J_dict:
                            J_dict[word[0]] += 1
                        else:
                            J_dict[word[0]] = 1
        if len(word) >= 4 and word:
            ust = str(key_dict['u'])+str(key_dict['s'])+str(key_dict['t'])
            ects = str(key_dict['e'])+str(key_dict['c'])+str(key_dict['t'])+str(key_dict['s'])
            if ust in word:  # ___ust___
                i = word.find(ust)
                if i != 0:
                    if word[i-1] in J_dict:
                        J_dict[word[i-1]] += 1
                    else:
                        J_dict[word[i-1]] = 1
            elif ects in word:  # ___ects
                i = word.find(ects)
                if i != 0:
                    if word[i - 1] in J_dict:
                        J_dict[word[i - 1]] += 1
                    else:
                        J_dict[word[i - 1]] = 1

    if J_dict:
        expect = RedundancyCheck(key_dict, J_dict)
        key_dict['j'] = expect
    print("J:", key_dict['j'], end=", ")
    decryptionP(key_dict)
    return


def decryptionP(key_dict):  # P 탐색
    global word_list
    P_dict = {}

    for word in word_list:
        if len(word) == 2 and word.isalpha():  # up
            if word[0] == key_dict['u']:
                if word[1] != key_dict['k']:
                    if word[1] != key_dict['s']:
                        if word[1] != key_dict['n']:
                            if word[1] in P_dict:
                                P_dict[word[1]] += 1
                            else:
                                P_dict[word[1]] = 1
        if len(word) >= 4:
            shi = str(key_dict['s']) + str(key_dict['h']) + str(key_dict['i'])
            hel = str(key_dict['h']) + str(key_dict['e']) + str(key_dict['l'])
            if shi in word:  # ___ship_
                i = word.find(shi)
                if len(word) != i+3:
                    if word[i+3] in P_dict:
                        P_dict[word[i+3]] += 1
                    else:
                        P_dict[word[i+3]] = 1
            elif hel in word:  # hel____
                    i = word.find(shi)
                    if len(word) != i + 3:
                        if word[i + 3] in P_dict:
                            P_dict[word[i + 3]] += 1
                        else:
                            P_dict[word[i + 3]] = 1
        if len(word) >= 6 and word.isalpha():  # people
            if word[0] == word[4]:
                if word[1] == key_dict['e']:
                    if word[2] == key_dict['o']:
                        if word[4] == key_dict['l']:
                            if word[5] == key_dict['e']:
                                if word[0] in P_dict:
                                    P_dict[word[0]] += 5
                                else:
                                    P_dict[word[0]] = 5

    if P_dict:
        expect = RedundancyCheck(key_dict, P_dict)
        key_dict['p'] = expect
    print("P:", key_dict['p'], end=", ")
    decryptionX(key_dict)
    return


def decryptionX(key_dict):  # X 탐색
    global word_list
    X_dict = {}

    for word in word_list:
        if len(word) >= 5 and word.isalpha():
            if word[0] == key_dict['e']:
                if word[2] == key_dict['t']:  # e_t___
                    if word[1] in X_dict:
                        X_dict[word[1]] += 1
                    else:
                        X_dict[word[1]] = 1
                elif word[2] == key_dict['p']:  # e_p___
                    if word[1] in X_dict:
                        X_dict[word[1]] += 1
                    else:
                        X_dict[word[1]] = 1
                elif word[2] == key_dict['e']:  # e_e___
                    if word[1] in X_dict:
                        X_dict[word[1]] += 1
                    else:
                        X_dict[word[1]] = 1
            elif word[0] == key_dict['a']:  # an_i___
                if word[1] == key_dict['n']:
                    if word[3] == key_dict['i']:
                        if word[2] in X_dict:
                            X_dict[word[2]] += 5
                        else:
                            X_dict[word[2]] = 5

    if X_dict:
        expect = RedundancyCheck(key_dict, X_dict)
        key_dict['x'] = expect
    print("X:", key_dict['x'], end=", ")

    decryptionZ(key_dict)
    return


def decryptionZ(key_dict):  # Z 탐색
    global word_list
    Z_dict = {}

    for word in word_list:
        if len(word) >= 4 and word.isalpha():
            if word[-1] == key_dict['e']:  # _____i_e
                if word[-3] == key_dict['i']:
                    if word[-2] in Z_dict:
                        Z_dict[word[-2]] += 1
                    else:
                        Z_dict[word[-2]] = 1

    if Z_dict:
        expect = RedundancyCheck(key_dict, Z_dict)
        key_dict['z'] = expect
    print("Z:", key_dict['z'])
    ReliabilityCheck(key_dict)
    return


def ReliabilityCheck(key_dict):
    cnt = 0
    for value in key_dict.values():
        if value is None:
            cnt += 1
    if cnt > 4:
        return
    else:
        ZeroNoneCheck(key_dict)
        return


def ZeroNoneCheck(key_dict):
    global alpha_list
    global freq_dict

    # key_dict 중 아직 매치된 알파벳이 없으면 추출
    empty_key_list = []
    for k, v in key_dict.items():
        if v == 0 or v is None:
            empty_key_list.append(k)
    length = len(empty_key_list)
    if length == 0:  # 안 비었으면 바로 진행
        makePlain(key_dict)
        return

    none_list = []  # 매치되지 못한 알파벳
    exist_list = []  # 암호문에 등장했으나! 매치되지 못한 알파벳

    for k, v in freq_dict.items():
        if k not in key_dict.values():
            none_list.append(k)
            if v != 0:
                exist_list.append(k)

    if length == 1:  # 한 자리만 비었으면 또 바로 진행
        key_dict[empty_key_list[0]] = none_list[0]
        makePlain(key_dict)
        return

    # fill_dict(key_dict, empty_key_list, exist_list)

    for i in range(length):
        for j in range(length):
            key_dict[empty_key_list[(i+j)%length]] = none_list[j]
        makePlain(key_dict)
    return


'''
# 경우의 수가 너무 많이 나옴.
def fill_dict(key_dict, key_list, left_items):
    while len(key_list) > len(left_items):
        left_items += '0'

    print(key_list)
    print(left_items)

    perm = list(map(''.join, permutations(left_items)))

    temp = key_dict
    for i in perm:
        key_dict = temp
        print(i)
        flag = 0
        for k in key_list:
            if i[flag].isalpha():
                key_dict[k] = i[flag]
            flag += 1
        print(key_dict)
    return
'''


def makePlain(key_dict):
    global cipher
    global out_count
    plain = ""

    for char in cipher:
        if char.isalpha():
            for k, v in key_dict.items():
                if v == char:
                    plain += k
        else:
            plain += char

    out_count += 1
    # 원문 파일 생성
    fname = "plain" + str(out_count) + ".txt"
    f = open(fname, 'w', encoding="UTF8")
    f.write(plain)
    f.close()

    # 키 파일 생성
    fname = "key" + str(out_count) + ".txt"
    f = open(fname, 'w', encoding="UTF8")
    for v in key_dict.values():
        f.write(str(v))
    f.close()
    print("[DEBUG] %d번째 복호화 파일이 생성되었습니다."%out_count)
    return


# ---------- MAIN CODE ---------- #
alpha_list = list(ascii_lowercase)  # a~z 리스트

out_count = 0  # 현재까지 복호화 시도 수: 복호화 파일 저장에 사용

cipher = getCipher()  # 암호문 전체: 최종 복호화에 사용
word_list = cipher.split()  # 암호문을 띄어쓰기 단위로 저장: 복호화 과정에 사용

freq_dict = getFrequency(cipher)  # 알파벳 빈도 수 저장: 복호화 과정에 사용
key_dict_init = {string: 0 for string in alpha_list}  # Key 매치 딕셔너리 틀

decryptionA(key_dict_init)



