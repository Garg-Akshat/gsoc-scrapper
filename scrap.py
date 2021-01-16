import requests

from bs4 import BeautifulSoup

from openpyxl import Workbook

URL =  "https://thealphadollar.me/GSoCOrgFrequency/"




class Org(object):
    def __init__(self, name, count, tech, topics, category, last_year):
        self.name = name
        self.count = count
        self.tech = tech
        self.topics = topics
        self.category = category
        self.last_year = last_year

    def __repr__(self):
        return f"organization({self.name})"

    def display(self):
        print(f"Name: {self.name}")
        print(f"Technologies: {self.tech}")
        print(f"Topics: {self.topics}")
        print(f"Category: {self.category}")
        print(f"Last Year: {self.last_year}")







content = requests.get(URL).content

soup = BeautifulSoup(content, "lxml")

organizations = []

for row in soup.findAll("tr")[1:]:
    data = list(row.findAll("td"))
    name = data[0].text
    count = int(data[1].text)
    tech = data[2].text.split(", ")
    topics = data[3].text.split(", ")
    category = data[4].text
    last_year = int(data[5].text)
    org = Org(name, count, tech, topics, category, last_year)

    organizations.append(org)

print(len(organizations))


def search(organizations, tech_name):
    orgs = list(filter(lambda org: tech_name in org.tech, organizations))
    return sorted(orgs, key=lambda x: (x.last_year, x.count, x.name), reverse=True)

def display(results):
    for i, org in enumerate(results, start=1):
        print(f"{i}. {org.name}")


def convert(lst):
    return ' , '.join(lst)


def addresultstoworkbook(results,tech_name):
    workbook_new = Workbook()
    sheet = workbook_new.active
    sheet["A1"] = "Name"
    sheet["B1"] = "Count"
    sheet["C1"] = "Tech"
    sheet["D1"] = "Topics"
    sheet["E1"] = "Category"
    sheet["F1"] = "Last year"
    for i in range(len(results)) :
        sheet[f'A{i+2}'] = results[i].name
        sheet[f'B{i + 2}'] = results[i].count
        sheet[f'C{i + 2}'] = convert(results[i].tech)
        sheet[f'D{i + 2}'] = convert(results[i].topics)
        sheet[f'E{i + 2}'] = results[i].category
        sheet[f'F{i + 2}'] = results[i].last_year
    workbook_new.save(filename=f'{tech_name}.xlsx')





temp_number = 1
while True:
    print("\n")
    print("Enter the name of a technology to search for (Enter 'exit' to exit)")
    user_input = input(">")
    if user_input == 'exit':
        break
    else:
        if user_input:
            tech_name = user_input
        else:
            tech_name = ""

    if tech_name:
        results = search(organizations, tech_name)
    else:
        results = organizations

    temp_number +=1

    display(results)
    addresultstoworkbook(results,tech_name)

    if results:
        while True:
            print("\n")
            print("Enter the Sr No. of an organization to know more about it. Press Enter to exit")
            try:
                org_number = int(input(">")) - 1
                results[org_number].display()
            except ValueError:
               break
    print("\n")
    print("Search again? (yN)")
    ans = input(">")
    if not (ans[0] == 'y' or ans[0] == 'Y'):
        break
