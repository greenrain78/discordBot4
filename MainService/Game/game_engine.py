import random

from MainService.Point.point_DB import PointDB


class Gameboard:

    @staticmethod
    def odd_even(user, point, args):
        # 인자 확인
        check = GameUtil.check_wrong_args(args, 1)
        if check:
            return check
        input_num = args[0]
        if input_num != "홀" and input_num != "짝":
            text = f"홀짝 게임에서는 홀 짝 둘중 하나만 선택할 수 있어요.\n 알겠나요?"
            return text
        # init
        text = ""
        pt = 0
        # 홀짝
        rand = random.randrange(0, 100)
        num = int(rand % 2)
        # 홀
        if num == 1:
            text = f"정답은 [홀]!!! \n"
            if input_num == "홀":
                text += f"정답입니다!!\n"
                pt = point
            elif input_num == "짝":
                text += f"틀렸습니다ㅠㅠ\n"
                pt = -point

        # 짝
        elif num == 0:
            text = f"정답은 [짝]!!! \n"
            if input_num == "홀":
                text += f"틀렸습니다ㅠㅠ\n"
                pt = -point
            elif input_num == "짝":
                text += f"정답입니다!!\n"
                pt = point

        # 점수 처리
        text += f"나온 숫자: {rand}\n"
        text += GameUtil.update_point("홀짝 게임", user, pt)
        return text

    @staticmethod
    def coin(user, point, args):
        # 인자 확인
        check = GameUtil.check_wrong_args(args, 1)
        if check:
            return check
        input_num = args[0]
        if input_num != "앞" and input_num != "뒤":
            text = f"동전 게임에서는 앞 뒤 둘중 하나만 선택할 수 있어요.\n 알겠나요?"
            return text

        # init
        text = ""
        pt = 0

        # 홀짝
        rand = random.randrange(1, 3)
        # 홀
        if rand == 1:
            text = f"정답은 [앞면]!!! \n"
            if input_num == "앞":
                text += f"정답입니다!!\n"
                pt = point
            elif input_num == "뒤":
                text += f"틀렸습니다ㅠㅠ\n"
                pt = -point

        # 짝
        elif rand == 2:
            text = f"정답은 [뒷면]!!! \n"
            if input_num == "앞":
                text += f"틀렸습니다ㅠㅠ\n"
                pt = -point
            elif input_num == "뒤":
                text += f"정답입니다!!\n"
                pt = point

        # 점수 처리
        text += GameUtil.update_point("동전 게임", user, pt)
        return text


class GameUtil:
    @staticmethod
    def check_wrong_args(args, num):
        if len(args) != num:
            text = f"odd 게임의 인자가 잘못 입력되었습니다.\n{len(args)}개가 입력되어 있네요^^\n 정상적으로 입력해 주세요 ^^\n"
            return text
        return False

    @staticmethod
    def update_point(game_name, user, point):
        reason = f"게임({game_name})으로 포인트:{point}만큼 획득하셨습니다."
        PointDB.earn_point_user(user, point, reason)
        PointDB.update_game_count_user(user)
        text = f"{user}의 획득 포인트: {point}"
        return text
