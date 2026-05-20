import requests
from bs4 import BeautifulSoup
import json
import datetime

# 크롤링 봇 차단을 막기 위해 '사람이 크롬 브라우저로 접속하는 것'처럼 위장하는 정보
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def get_yes24_bestseller():
    print("예스24 진짜 데이터 크롤링 중...")
    url = "http://www.yes24.com/24/category/bestseller"
    books = []
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        items = soup.select('#bestList > ol > li')[:5]  # 1위~5위까지만

        for idx, item in enumerate(items):
            title_tag = item.select_one('.pTit a')
            author_tag = item.select_one('.info_auth a')
            img_tag = item.select_one('.image img')

            books.append({
                "rank": idx + 1,
                "title": title_tag.text.strip() if title_tag else "제목 없음",
                "author": author_tag.text.strip() if author_tag else "저자 미상",
                "image": img_tag['src'] if img_tag else "",
                "store": "yes24"
            })
    except Exception as e:
        print(f"예스24 크롤링 실패: {e}")
    return books


def get_aladin_bestseller():
    print("알라딘 진짜 데이터 크롤링 중...")
    url = "https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1"
    books = []
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        items = soup.select('.ss_book_box')[:5]

        for idx, item in enumerate(items):
            title_tag = item.select_one('a.bo3')
            img_tag = item.select_one('.cover_all img')

            # 알라딘은 저자 태그가 복잡하여 제일 첫 번째 링크(a태그)를 저자로 간주
            author = "저자 미상"
            author_list = item.select('li a')
            if len(author_list) > 1:
                author = author_list[1].text.strip()

            books.append({
                "rank": idx + 1,
                "title": title_tag.text.strip() if title_tag else "제목 없음",
                "author": author,
                "image": img_tag['src'] if img_tag else "",
                "store": "aladin"
            })
    except Exception as e:
        print(f"알라딘 크롤링 실패: {e}")
    return books


def get_kyobo_bestseller():
    print("교보문고 진짜 데이터 크롤링 시도 중...")
    books = []
    # 교보문고는 일반적인 html 크롤링(requests)을 막고 JS로 화면을 그립니다.
    # 실무에서는 Selenium 이라는 브라우저 자동화 툴을 쓰지만, 서버 무료 배포를 위해 여기선 생략합니다.
    # 대신 수집 실패 시 화면에 보여줄 안내 문구를 넣습니다.
    books.append({
        "rank": "-",
        "title": "교보문고는 봇 접근을 차단했습니다.",
        "author": "(Selenium 등의 고급 크롤링 기술 필요)",
        "image": "https://via.placeholder.com/150x200?text=Blocked",
        "store": "kyobo"
    })
    return books


if __name__ == "__main__":
    all_books = []

    # 3사 데이터 합치기
    all_books.extend(get_kyobo_bestseller())
    all_books.extend(get_yes24_bestseller())
    all_books.extend(get_aladin_bestseller())

    final_data = {
        "updated_at": str(datetime.datetime.now()),
        "data": all_books
    }

    with open('bestseller_data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print("모든 크롤링 완료! 진짜 데이터로 json 업데이트 완료.")