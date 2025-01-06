def find_suffix(stem: str, form: str) -> list:
    # form 은 'end', 'con' 중에 하나임
    idx = ord(stem[-1])

    if (idx - 44032) % 28 == 0:
        # 어간의 마지막 글자에 종성이 없을 때
        if form == "end":  # 종결 어미: -ㄴ다, -기, -ㅁ, -자
            return [
                stem[:-1] + chr(idx + 4) + "다",
                stem + "기",
                stem[:-1] + chr(idx + 16),
                stem + "자",
            ]

        if form == "con":  # 연결 어미: -고 -(으)며
            return [stem + "고", stem + "며"]
    else:
        # 종성이 있을 때
        if form == "end":
            return [stem + "는다", stem + "기", stem + "음", stem + "자"]

        if form == "con":
            return [stem + "고", stem + "으며"]


# 가: 44032 / 힣: 55203
