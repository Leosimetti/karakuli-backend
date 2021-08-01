from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

WIKIPEDIA = r"https://en.wikipedia.org/wiki/List_of_j%C5%8Dy%C5%8D_kanji"
RADICALS = r"https://kanjialive.com/214-traditional-kanji-radicals/"


def kanji():
    with urlopen(WIKIPEDIA) as req:
        soup = BeautifulSoup(req.read().decode("utf-8"), features="html.parser")
        table = soup.find_all("table")[1]
        tbody = table.find_all("tbody")[0]

        # Todo make it add more radicals to kanji
        # Todo somehow integrate readings
        for row in tbody.find_all("tr"):
            data = list(map(lambda tag: tag.text, row.find_all("td")))
            if len(data) == 9:
                word_entry = {
                    # "id": int(data[0]),
                    "character": data[1],
                    # "old": data[2],
                    # "radical": data[3],
                    "strokes": data[4],
                    "jlpt_level": data[5],
                    # "year_added": data[6],
                    "meaning": data[7],
                    # "readings": data[8].strip(),
                    # "example": f"I like my {data[1]} - Я люблю сво(ю/й) {data[7]}"
                }

                yield word_entry


def radicals(no_variations=False):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(RADICALS, headers=hdr)
    with urlopen(req) as req:
        soup = BeautifulSoup(req.read().decode("utf-8"), features="html.parser")

        for row in soup.select(".row-hover tr"):
            data = list(map(lambda tag: tag.text, row.find_all("td")))

            # Check if the radical is a variation
            if no_variations and data[5]:
                continue

            radical = {
                "strokes": data[0],
                "radical": data[1],
                "meaning": data[3]
            }

            yield radical


if __name__ == "__main__":
    for word in radicals(no_variations=True):
        print(word)

