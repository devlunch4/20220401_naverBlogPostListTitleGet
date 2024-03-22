from bs4 import BeautifulSoup


# input type yyyy. mm.dd
def modify_date_text(date_text):
    parts = date_text.split('.')
    modified_parts = [f'{int(part):02d}' if part.strip().isdigit() else part for part in parts]
    date_text = '-'.join(modified_parts)
    return date_text[:-1]


def main(account_id):
    # Read HTML file
    with open("tbody.html", "r", encoding="utf-8") as file:
        html = file.read()

    list = []
    soup = BeautifulSoup(html, 'html.parser')

    tbody = soup.find('tbody')
    if tbody:
        tr_elements = tbody.find_all('tr')
        for tr in tr_elements:
            title = ""
            date = ""
            link = ""

            # title
            title_td = tr.find('td', class_='title')
            if title_td:
                a_element = title_td.find('a', class_='pcol2 _setTop _setTopListUrl')
                if a_element:
                    title = a_element.text.strip()

            # date
            date_td = tr.find('td', class_='date')
            if date_td:
                span_element = date_td.find("span", class_="date pcol2")
                if span_element:
                    date = span_element.text
                    date = modify_date_text(date).strip()
            # link
            read_td = tr.find('td', class_='read')
            if read_td:
                a_href_element = read_td.find("a")
                link = a_href_element.get("href")
                link = link.replace("stat.", "").replace("blog/article", account_id).replace("/cv", "").strip()
            if title != "":
                list.append(date + "\t" + title + "\t" + link)

    list.reverse()
    print()
    for new_item in list:
        print(new_item)


if __name__ == '__main__':
    account_name = 'id'
    main(account_name)
