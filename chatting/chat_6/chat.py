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

FILE_PATH = "./chat.txt"
COMPLETED_FILE_PATH = "./completed_message.txt"

# thread를 제어하기위한 Lock
lock = Lock()


class User:
    """사용자 class

        Attributes:
            name (str) : 이름

    """
    def __init__(self, name):
        self.name = name


class Chat:
    """채팅(?)에 대한 class

        Attributes:
            user (User)
            file_handler (FileHandler)
    """

    def __init__(self, user):
        self.user = user
        self.file_handler = FileHandler()

    def type_a_message(self, message=None, file_path=None):
        """메세지를 입력하는 함수

        Notes:
            message(str)혹은 random string을 txt파일에 적는 역할을하는 함수여서 따로 반환하지 않음

        Args:
            message (str)
            file_path (str)

        Returns:
            -

        """
        if file_path is None:
            file_path = FILE_PATH

        # TODO 1. str 생성 or message(str)를 인자로 받아서 txt에 저장.
        if message is None:
            message = str(uuid.uuid4())

        # TODO 2. 보낸사람과 Message내용을 dict로 취합해서 저장
        user_name = self.user.name
        message = {
            # 'id': None
            "user": str(user_name),
            "message": message,
            "time_stamp": None
        }

        text_file, now = self.file_handler.access_text_file(file_path)
        message['time_stamp'] = now
        text_file.write(str(message) + "\n")
        text_file.close()

    def send_the_message(self, file_path=None):
        """메세지를 보내는 함수

        Notes:
            txt파일에 저장된 message를 전송하는(print) 함수여서 따로 반환하지않음.
            print 후 complete_message.txt 파일에 다시 기록함.

        Args:
            file_path (str)

        Returns:
            -

        """

        if file_path is None:
            file_path = FILE_PATH
        text_file, now = self.file_handler.access_text_file(file_path, 1)
        all_messages = text_file.readlines()

        if len(all_messages) == 0:
            text_file.close()
            return

        cur_message = all_messages[0]
        print(cur_message)
        self.store_completed_the_message(cur_message)

        text_file.seek(0)
        del all_messages[0]
        for message in all_messages:
            text_file.write(message)
        text_file.truncate()
        text_file.close()

    def store_completed_the_message(self, message, file_path=None):
        """전송이 완료된 message를 또다른 txt에 적어놓는 함수

        Notes:
            전송된 message(str)를 받아서 complete txt에 적어놓는 함수라 따로 반환하지 않음.

        Args:
            message (str)
            file_path (str)

        Returns:
            -

        """
        if file_path is None:
            file_path = COMPLETED_FILE_PATH
        text_file, now = self.file_handler.access_text_file(file_path)
        text_file.write(message)
        text_file.close()

class Simulator:
    """chat을 시뮬레이팅하기 위한 class / Lock으로 제어

    Attribute:
        chat (Chat)

    """
    def __init__(self, chat):
        self.chat = chat

    # TODO Lock을 이용해서 thread간의 접근을 제어한다.
    def type_messages(self, count):
        for i in range(count):
            # lock.acquire()
            with lock:
                self.chat.type_a_message()
            # lock.release()

    def send_messages(self, count):
        for i in range(count):
            with lock:
                self.chat.send_the_message()
            # lock.release()


def compare_by_timestamp(file_path=None):
    """전송된 메세지들의 timestamp를 비교하는 함수

    Note:
        typing된 순서대로 now를 FIFO를 잘 지켰는지 확인하는 함수

    Args:
        file_path (str)

    Returns:
        message (str) : 처리에 결과에 따라 메세지를 반환한다.

    """
    if file_path is None:
        file_path = COMPLETED_FILE_PATH
    text_file = open(file_path, "r+")
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
            pass
        else:
            message = "threading이 잘못처리됐습니다."
            return  message
    message = "threading이 잘 처리되었습니다."
    return message


def run_threads(chats):
    """thread를 위한 함수

    Notes:
        chat_count는 대화를 주고받는 사이클을 얼마나 할것인가에 대한 제한.
        typing_or_sending_count는 메세지의 갯수에 대한 제한.

    Args:
        chats (Chat)

    Returns:
        -
    """

    chat_count = [i for i in range(5, 8)]
    typing_or_sending_count = [i for i in range(1, 4)]
    threads = []

    for i in range(chat_count[2]):
        random.shuffle(chats)
        for chat in chats:
            random.shuffle(typing_or_sending_count)
            args = (typing_or_sending_count[1],)
            simulator = Simulator(chat)
            thread = Thread(target=simulator.type_messages, args=args)
            thread2 = Thread(target=simulator.send_messages, args=args)
            threads.append(thread)
            threads.append(thread2)

    for thread in threads:
        thread.start()
        thread.join()


if __name__ == "__main__":
    user_name_list = ["신종민", "홍석재", "임정택", "신현종", "주민건", "조승리"]

    # for i in range(3):
    #     new_user_name_list = [name + str(i) for name in user_name_list]
    #     user_name_list += new_user_name_list

    chats = []

    for user_name in user_name_list:
        user = User(user_name)
        chat = Chat(user)
        chats.append(chat)

    run_threads(chats)

    print(compare_by_timestamp())
