from datetime import datetime, date, timedelta
import calendar
from datetime import date


def all_categories():
    return [
        {
            "sub_id": 0,
            "name": "식사",
            "icon": "assets/images/icons/food.svg",
            "color": "0xFF9FCE7C",
        },
        {
            "sub_id": 1,
            "name": "카페",
            "icon": "assets/images/icons/cafe.svg",
            "color": "0xFF8197BC",
        },
        {
            "sub_id": 2,
            "name": "교통",
            "icon": "assets/images/icons/subway.svg",
            "color": "0xFFBE684E",
        },
        {
            "sub_id": 3,
            "name": "여행",
            "icon": "assets/images/icons/suitcase.svg",
            "color": "0xFFC9B699",
        },
        {
            "sub_id": 4,
            "name": "여가/취미",
            "icon": "assets/images/icons/happy.svg",
            "color": "0xFF406A21",
        },
        {
            "sub_id": 5,
            "name": "의류/쇼핑",
            "icon": "assets/images/icons/shopping.svg",
            "color": "0xFF6D96DC",
        },
        {
            "sub_id": 6,
            "name": "건강/의료",
            "icon": "assets/images/icons/health.svg",
            "color": "0xFFA5AA6C",
        },
        {
            "sub_id": 7,
            "name": "뷰티",
            "icon": "assets/images/icons/beauty.svg",
            "color": "0xFFD9A048",
        },
        {
            "sub_id": 8,
            "name": "교육",
            "icon": "assets/images/icons/book.svg",
            "color": "0xFF67A6C6",
        },
        {
            "sub_id": 9,
            "name": "주거",
            "icon": "assets/images/icons/home.svg",
            "color": "0xFFA683B5",
        },
        {
            "sub_id": 10,
            "name": "보험",
            "icon": "assets/images/icons/shield.svg",
            "color": "0xFF7A7062",
        },
        {
            "sub_id": 11,
            "name": "통신",
            "icon": "assets/images/icons/phone.svg",
            "color": "0xFF3B6A82",
        },
        {
            "sub_id": 12,
            "name": "생활비",
            "icon": "assets/images/icons/cart.svg",
            "color": "0xFFB58395",
        },
        {
            "sub_id": 13,
            "name": "선물/기념일",
            "icon": "assets/images/icons/gift.svg",
            "color": "0xFFE2B5D1",
        },
        {
            "sub_id": 14,
            "name": "문화생활",
            "icon": "assets/images/icons/movie.svg",
            "color": "0xFFC58170",
        },
    ]


def get_current_month_range():
    today = date.today()
    first_day_of_month = today.replace(day=1)

    if today.month == 12:
        last_day_of_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        last_day_of_month = today.replace(month=today.month + 1, day=1)

    last_day_of_month = last_day_of_month.toordinal() - 1
    last_day_of_month = date.fromordinal(last_day_of_month)

    first_day_str = first_day_of_month.strftime("%Y-%m-%d")
    last_day_str = last_day_of_month.strftime("%Y-%m-%d")

    return first_day_str, last_day_str


def get_current_week_range():
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    start_of_week_str = start_of_week.strftime("%Y-%m-%d")
    end_of_week_str = end_of_week.strftime("%Y-%m-%d")

    return start_of_week_str, end_of_week_str


def get_today_range():
    today = date.today()

    formatted_today = today.strftime("%Y-%m-%d")

    return formatted_today, formatted_today


def get_3month_range(year: int, month: int):
    if year == 0 or month == 0:
        today = datetime.today()
        year = today.year
        month = today.month

    two_months_ago = month - 2 if month > 2 else 12 + (month - 2)
    two_months_ago_year = year if month > 2 else year - 1

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1

    two_months_ago_start = datetime(two_months_ago_year, two_months_ago, 1)
    two_months_ago_end = datetime(
        two_months_ago_year,
        two_months_ago,
        calendar.monthrange(two_months_ago_year, two_months_ago)[1],
    )

    prev_start = datetime(prev_year, prev_month, 1)
    prev_end = datetime(
        prev_year, prev_month, calendar.monthrange(prev_year, prev_month)[1]
    )

    curr_start = datetime(year, month, 1)
    curr_end = datetime(year, month, calendar.monthrange(year, month)[1])

    return [
        two_months_ago_start.strftime("%Y-%m-%d"),
        two_months_ago_end.strftime("%Y-%m-%d"),
        prev_start.strftime("%Y-%m-%d"),
        prev_end.strftime("%Y-%m-%d"),
        curr_start.strftime("%Y-%m-%d"),
        curr_end.strftime("%Y-%m-%d"),
    ]


def date_converter(o):
    if isinstance(o, date):
        return o.strftime("%Y-%m-%d")
    raise TypeError(f"Type {o} not serializable")
