# 전ㅊ 센서 네트워크에서 밝기 단계를 샘플링
# 여러 대상을 카운트하는 프로그램
# 시간에 따른 밝기 샘플의 전체 개수를 알고 싶다면 새 클래스로 개수를 모으면 됨.

from threading import Thread


class Counter:
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


# 센서에서 읽는 작업은 블로킹 I/O가 필요하므로 각 센서별로 고유한 작업 스레드가 있다고 가정
# 각 센서 측정값을 읽고 나면 작업 스레드는 읽으려는 최대 개수에 이를 때까지 카운터 증가

def worker(sensor_index, how_many, counter):
    # how_many를 for문으로 돌려서
    for _ in range(how_many):
        # Couter의 instance에 증가함수를 실행시킴
        counter.increment(1)


# 센서별로 작업 스레드를 시작하고 읽기를 모두 마칠때까지 기다리는 함수
def run_threads(func, how_many, counter):
    # 빈리스트를 선언
    threads = []
    for i in range(5):
        args = (i, how_many, counter)
        thread = Thread(target=func, args=args)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    how_many = 10 ** 5
    counter = Counter()
    run_threads(worker, how_many, counter)
    print("Counter should be {}, found {}".format(5 * how_many, counter.count))
