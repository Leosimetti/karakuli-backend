from bs4 import BeautifulSoup
from urllib import request
import pprint

WIKIPEDIA = r"https://en.wikipedia.org/wiki/List_of_j%C5%8Dy%C5%8D_kanji"

if __name__ == "__main__":
    words = {}
    with request.urlopen(WIKIPEDIA) as req:
        soup = BeautifulSoup(req.read().decode("utf-8"), features="html.parser")
        table = soup.find_all("table")[1]
        tbody = table.find_all("tbody")[0]

        for row in tbody.find_all("tr"):
            data = list(map(lambda tag: tag.text, row.find_all("td")))
            if len(data) == 9:
                word_entry = {
                    "id": data[0],
                    "new": data[1],
                    # "old": data[2],
                    "radical": data[3],
                    "strokes": data[4],
                    "grade": data[5],
                    # "year_added": data[6],
                    "meaning": data[7],
                    "readings": data[8].strip(),
                }

                words.setdefault(int(data[0]), word_entry)

        pprint.pprint(words)
