# 메세지를 생성하는 함수 (txt에 저장하는 함수)
# 메세지를 내보내는 함수 (txt에서 읽어서 print하고 해당 str을 지우는 함수)
# 이 두가지가 반복되지만 그 총 반복수를 제어하는 부분도 필요.
# thread에 넣어서 thread 중간에도 생성했다가 종료했다가 할 수 있도록 구현
# 3개 3개로 나눠서 적용.
import random
import uuid
from datetime import datetime
from threading import Thread


class User:
    def __init__(self, name):
        self.name = name


class Chat:
    FILE_PATH = './chat.txt'
    COMPLETED_FILE_PATH = './completed_message.txt'

    def __init__(self, user):
        self.user = user

    def type_a_message(self, message=None, file_path=None):
        """메세지를 입력하는 함수

        Notes:
            message(str)혹은 random string을 txt파일에 적는 역할을하는 함수여서 따로 반환하지 않음

        Args:
            user (User)
            message (str)
            file_path (str)

        Returns:
            -

        """


        if file_path is None:
            file_path = self.FILE_PATH

        # TODO 1. str 생성 or message(str)를 인자로 받아서 txt에 저장.
        if message is None:
            message = str(uuid.uuid4())

        # TODO 2. 보낸사람과 Message내용을 dict로 취합해서 저장
        user_name = self.user.name
        message = {
            # 'id': None
            'user': str(user_name),
            'message': message,
            'time_stamp': None
        }

        # TODO 3. txt 파일로 저장
        text_file = open(file_path, 'a')

        # 보내기 txt 파일에 쓰기 직전에 현재시간을 찍는다.
        now = datetime.now()
        message['time_stamp'] = str(now)
        # txt에 저장
        text_file.write(str(message) + '\n')
        text_file.close()
        print(message)

    def send_the_message(self, file_path=None):

        if file_path is None:
            file_path = self.FILE_PATH
        # TODO 1. txt파일에서 message 읽기
        text_file = open(file_path, 'r+')
        all_messages = text_file.readlines()
        cur_message = all_messages[0]
        if len(cur_message) == 0:
            print("끝")
            return

        # TODO 2. message 보내기(+print)
        print(cur_message)

        # TODO 3. 보낸 message 삭제
        text_file.seek(0)
        del all_messages[0]
        text_file.write(all_messages)
        text_file.truncate()
        text_file.close()

        self.store_completed_the_message(cur_message)


    def store_completed_the_message(self, message, file_path=None):
        if file_path is None:
            file_path = self.COMPLETED_FILE_PATH
        text_file = open(file_path, 'a')
        text_file.write(message + '\n')
        text_file.close()


# class Simulator:
#     def __init__(self, )

# def simulate(chat):

# 어떻게 시뮬레이팅 할것인가?
# user들이 동시에 메세지를 작성하고(thread이용)
# thread를 세개에는 chat에 관련된 send메세지가 돌아가게 설정한다.

# 또 동시에 메세지를 처리해본다.

# 메세지를 여러개 생성하는 로직 필요.


class Simulator:

    def __init__(self, chat):
        self.chat = chat

    def type_messages(self, count):
        for i in range(count):
            self.chat.type_a_message()

    def send_messages(self, count):
        for i in range(count):
            self.chat.send_the_message()


def run_threads(chats):
    type_count = [2, 3, 4, 5]
    send_count = [1, 2, 3]
    threads = []

    for chat in chats:
        random.shuffle(type_count)
        args = (type_count[1],)
        simulator = Simulator(chat)
        thread = Thread(target=simulator.type_messages, args=args)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    user1 = User("신종민")
    user2 = User("홍석재")
    user3 = User("임정택")

    chat1 = Chat(user1)
    chat2 = Chat(user2)
    chat3 = Chat(user3)

    chats = [chat1, chat2, chat3]

    run_threads(chats)