from datetime import datetime


class FileHandler:
    def access_text_file(self, file_path, usage=None):
        """txt파일을 제어하는 함수.

        Args:
            file_path (str) : 파일 경로
            usage : 사용용도

        Returns:
            text_file , now (tuple)
        """

        now = None
        if usage is None:
            text_file = open(file_path, 'a', encoding="utf-8")
            now = str(datetime.now().timestamp())
            return text_file, now
        text_file = open(file_path, 'r+', encoding="utf-8")
        return text_file, now