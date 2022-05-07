'''
예외처리 클래스
'''


class DBItemAlreadyExist(Exception):
    """DB에 이미 값이 있을경우 예외"""
    def __init__(self, message):
        self.error_code = 100
        self.status_code = 407
        self.message = message
