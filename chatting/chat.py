# 메세지를 파일에 저장

# 메세지를 파일에서 읽어서 보냄.

# 읽은 메세지를 파일에서 삭제

# 메세지를 확인해서 next_message와 맞으면 처리.

# next_message와 맞지 않으면, 되돌아간다.

# message를 만들어내는 함수 정의

# 멀티쓰레드방식으로 처리하는 함수도 정의

# 테스트코드 작성

import ast
import time
import uuid
from threading import Thread
from threading import Lock
import os

FILE_PATH = './chat.txt'
COMPLETED_FILE_PATH = './completed_message.txt'

class Chatting_with_lock:
    """Chatting을 위한 앱

    Attributes:
        FILE_PATH : txt파일이 생성되는 경로
    """

    def __init__(self, next_message=None):
        """

        Args:
            next_message: FIFO를 위한 구분자
        """
        self.lock = Lock()
        self.next_message = next_message

    def get_all_messages(self, file_path=None):
        if file_path is None:
            file_path = FILE_PATH

        text_file = open(file_path, 'r')
        all_messages = text_file.readlines()
        return all_messages

    def get_checked_the_message_id(self, file_path=None):
        if file_path is None:
            file_path = FILE_PATH

        text_file = open(file_path, 'r')
        all_messages = text_file.readlines()
        message_id = 0
        if len(all_messages) == 0:
            return message_id
        last_line = all_messages[-1]

        # String을 Dict로 바꾸기위해서 ast를 import해서 사용
        last_message = ast.literal_eval(last_line)
        message_id = last_message['id']
        text_file.close()
        return message_id

    def store_message(self, message, file_path=None):
        if file_path is None:
            file_path = FILE_PATH

        text_file = open(file_path, 'a')
        data = {
            'id': self.get_checked_the_message_id() + 1,
            'message': message,
        }
        # print(str(data))
        text_file.write(str(data) + '\n')
        text_file.close()

    def store_completed_message(self, message, file_path=None):

        text_file = open(file_path, 'a')
        text_file.write(message)
        text_file.close()

    def send_message(self, file_path=None):
        """메세지를 파일에서 받아서 처리하는 메소드

        Args:
            file_path:

        """
        if file_path is None:
            file_path = FILE_PATH

        text_file = open(file_path, 'r+')
        all_messages = text_file.readlines()

        cur_message = all_messages[0]
        if self.next_message is None:
            if len(all_messages) > 1:
                self.next_message = all_messages[1]
            print(cur_message)
            self.store_completed_message(cur_message, COMPLETED_FILE_PATH)

            text_file.seek(0)
            for message in all_messages:
                if message != cur_message:
                    text_file.write(message)
            text_file.truncate()
            text_file.close()
        else:
            if self.next_message == cur_message:
                print(cur_message)
                self.store_completed_message(cur_message, COMPLETED_FILE_PATH)
                text_file.seek(0)
                for message in all_messages:
                    if message != cur_message:
                        text_file.write(message)
                text_file.truncate()
                text_file.close()
                text_file_2 = open(file_path, 'r+')
                self.next_message = text_file_2.readline()
            else:
                return

    def do(self):
        with self.lock:
            while len(self.get_all_messages()) > 0:
                self.send_message()
                if len(self.get_all_messages()) == 0:
                    print('끝')

def make_messages(num_of_messages):
    '''다수의 메세지를 생성함으로써 테스트를 할 수 있는 환경 구성

    Args:
        num_of_messages (int): 생성할 메세지의 숫자
    Return
        messages (list)
    '''

    messages = []
    for i in range(1, num_of_messages):
        randomString = str(uuid.uuid4())
        messages.append(randomString)
    return messages


def run_threads(func):
    threads = []
    for i in range(5):
        thread = Thread(target=func)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    while True:
        number_of_messages = input("몇 개의 메세지를 생성할까요?")
        if not number_of_messages.isnumeric():
            print("정수만 입력 가능합니다.")
            continue
        number_of_messages = int(number_of_messages)

        if number_of_messages == 0:
            print("0이상의 정수를 입력해주세요.")
            continue
        break
    print('-----message 생성시작')
    s_time = time.time()
    # 갯수를 넣어서 message를 만든다.
    messages = make_messages(number_of_messages)
    print("message making time = ", time.time() - s_time)
    print("-----message들을 생성했습니다.")

    while True:
        answer = input("메세지를 저장할까요??(Y/n)")
        if len(answer) == 0:
            answer = True
            break

        if answer.upper() == 'Y':
            answer = True
        elif answer.upper() == 'N':
            answer = False
        else:
            print("'y' 또는 'n'을 입력해주세요.")
            continue
        break
        exit()

    chat = Chatting_with_lock()
    if answer:
        print('-----txt파일로 저장시작')
        s_time = time.time()
        for message in messages:
            # Char class를 통해서 txt파일로 저장시킨다.
            chat.store_message(message)
        print("message store time = ", time.time() - s_time)
        print("-----message들을 저장했습니다.")
    else:
        exit()

    while True:
        answer = input(
            '''message를 처리할 방식을 선택해주세요.
            
    1) 단일 쓰레드 방식
    2) 멀티 쓰레드 방식
            
            '''
        )

        if not answer.isnumeric():
            print("정수만 입력 가능합니다.")
            continue

        if not 0< int(answer)< 3 :
            print("1 또는 2를 입력해주세요.")
            continue

        if int(answer) == 1:
            print('-----단일 쓰레드 방식으로 처리시작')
            s_time = time.time()
            chat.do()
            print('single thread time = ', time.time() - s_time)
            print("-----message들을 처리했습니다.")
            os.remove(FILE_PATH)
            os.remove(COMPLETED_FILE_PATH)
        else:
            print('-----멀티 쓰레드 방식으로 처리시작')
            s_time = time.time()
            run_threads(chat.do())
            print('ㅡmulti thread time = ', time.time() - s_time)
            print("-----message들을 처리했습니다.")
            os.remove(FILE_PATH)
            os.remove(COMPLETED_FILE_PATH)
        exit()




    # chat.send_message()
    # chat.do()

    # 그냥 실행 시켰을때
    # chat.do()

    # Multi thread 방식
    # send_with_multithread(chat.do())

    # send_with_multithread(chat.do_something())
    # print('time = ', time.time() - s_time)
