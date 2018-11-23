# 메세지를 생성하는 함수 (txt에 저장하는 함수)
# 메세지를 내보내는 함수 (txt에서 읽어서 print하고 해당 str을 지우는 함수)
# 이 두가지가 반복되지만 그 총 반복수를 제어하는 부분도 필요.
# thread에 넣어서 thread 중간에도 생성했다가 종료했다가 할 수 있도록 구현
# 3개 3개로 나눠서 적용.
import random
import uuid
from threading import Thread, Lock
from file_handler import FileHandler
import ast

FILE_PATH = './chat.txt'


class User:
    def __init__(self, name):
        self.name = name


class Chat:
    FILE_PATH = './chat.txt'
    COMPLETED_FILE_PATH = './completed_message.txt'

    def __init__(self, user):
        self.user = user
        self.file_handler = FileHandler()

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
        # str 생성 or message_list를 인자로 받아서 txt에 저장.

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

        text_file, now = self.file_handler.access_text_file(file_path)
        message['time_stamp'] = now
        text_file.write(str(message) + '\n')
        text_file.close()

    def send_the_message(self, file_path=None):

        if file_path is None:
            file_path = self.FILE_PATH

        text_file, now = self.file_handler.access_text_file(file_path, 1)
        all_messages = text_file.readlines()

        if len(all_messages) == 0:
            text_file.close()
            print("끝")
            return
        cur_message = all_messages[0]
        print(cur_message)
        # self.store_completed_the_message(cur_message)

        text_file.seek(0)
        del all_messages[0]
        for message in all_messages:
            text_file.write(message)
        text_file.truncate()
        text_file.close()

    def run(self):

        self.type_a_message()
        self.send_the_message()


    # def store_completed_the_message(self, message, file_path=None):
    #     # with self.lock:
    #     if file_path is None:
    #         file_path = self.COMPLETED_FILE_PATH
    #     text_file = open(file_path, 'a')
    #     text_file.write(message)
    #     text_file.close()


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

    # def simulate_chat(self, count):
    #     for i in range(count):
    #         self.chat.run()


def compare_by_timestamp(file_path=None):
    if file_path is None:
        file_path = FILE_PATH
    text_file = open(file_path, 'r+')
    all_messages = text_file.readlines()
    num_messages = len(all_messages)

    if num_messages < 2:
        return

    for i in range(num_messages - 1):
        message1 = ast.literal_eval(all_messages[i])
        message2 = ast.literal_eval(all_messages[i + 1])

        time1 = message1['time_stamp']
        time2 = message2['time_stamp']
        if float(time1) < float(time2):
            print('True')
        else:
            print("threading이 잘못처리됐습니다.")


def run_threads(self, chats):
    type_count = [6, 7, 8, 9, 10, 11]
    threads = []

    for chat in chats:
        random.shuffle(type_count)
        args = (type_count[1],)
        simulator = Simulator(chat)
        thread = Thread(target=simulator., args=args)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    user1 = User("신종민")
    user2 = User("홍석재")
    user3 = User("임정택")
    user4 = User("신현종")
    user5 = User("주민건")

    chat1 = Chat(user1)
    chat2 = Chat(user2)
    chat3 = Chat(user3)
    chat4 = Chat(user4)
    chat5 = Chat(user5)

    chats = [chat1, chat2, chat3, chat4, chat5]

    run_threads(chats)

    compare_by_timestamp()
