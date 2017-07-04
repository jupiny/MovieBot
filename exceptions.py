class NaverMoviePageAcessDeniedError(Exception):

    def __str__(self):
        return "해당 영화 정보 페이지에 접근할 수 없습니다."
