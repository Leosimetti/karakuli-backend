import pickle
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

WIKIPEDIA = r"https://en.wikipedia.org/wiki/List_of_j%C5%8Dy%C5%8D_kanji"

RADICALS = r"https://kanjialive.com/214-traditional-kanji-radicals/"
ALTERNATIVE_RADICALS = (
    r"https://en.wikipedia.org/wiki/List_of_kanji_radicals_by_frequency"
)


# Todo @todo create a funtion that takes a generator and make all other functions use it


def kanji():
    try:
        with open("kanji.pickle", "rb") as f:
            data = pickle.load(f)

            for k in data:
                yield k

    except FileNotFoundError:
        with urlopen(WIKIPEDIA) as req:
            soup = BeautifulSoup(req.read().decode("utf-8"), features="html.parser")
            table = soup.find_all("table")[1]
            tbody = table.find_all("tbody")[0]

            results = []
            for row in tbody.find_all("tr"):
                data = list(map(lambda tag: tag.text, row.find_all("td")))
                if len(data) == 9:
                    word_entry = {
                        # "id": int(data[0]),
                        "character": data[1],
                        # "old": data[2],
                        # "radical": data[3],
                        "strokes": int(data[4]),
                        "jlpt_level": data[5],
                        # "year_added": data[6],
                        "meaning": data[7],
                        "readings": data[8].strip(),
                        # "example": f"I like my {data[1]} - Я люблю сво(ю/й) {data[7]}"
                    }
                    results.append(word_entry)
            with open("kanji.pickle", "wb") as f:
                pickle.dump(results, f)

            return results


def radicals(no_variations=False):
    try:
        with open("radicals.pickle", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        hdr = {"User-Agent": "Mozilla/5.0"}
        req = Request(RADICALS, headers=hdr)
        with urlopen(req) as req:
            soup = BeautifulSoup(req.read().decode("utf-8"), features="html.parser")

            results = []
            for row in soup.select(".row-hover tr"):
                data = list(map(lambda tag: tag.text, row.find_all("td")))

                # Check if the radical is a variation
                if no_variations and data[5]:
                    continue

                radical = {
                    "strokes": int(data[0]),
                    "radical": data[1],
                    "meaning": data[3],
                }

                results.append(radical)

            with open("radicals.pickle", "wb") as f:
                pickle.dump(results, f)

            return results
