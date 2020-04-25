from django import forms
from bs4 import BeautifulSoup
from collections import OrderedDict
from urllib.request import urlopen


class MyForm(forms.Form):

    # extracting list of location from given url
    url = 'http://quickaid.com/airport-codes-canada/'
    page = urlopen(url)
    soup = BeautifulSoup(page, 'lxml')

    # Scrapping webpage to get specific list
    all_matches = str(soup.findAll('div', attrs={'class': ['entry']})[0].contents[7].text)
    list1 = all_matches.splitlines()

    # Removing unwanted data from the list
    list1.pop(0)
    templist = [sub[: -6] for sub in list1]

    newlist = []

    # Creating location list as per choicefield format
    for item in templist:
        if (item.find('–') != -1):
            temp = str(item).split('–')

            newlist.append(temp[0])
        else:
            newlist.append(item)

    res = list(OrderedDict.fromkeys(newlist))

    CITY_CHOICES = [tuple([x, x]) for x in res]

    JOB_TITLES = (
        ("Web Developer", "Web Developer"),
        ("Senior Web Developer", "Senior Web Developer"),
        ("Front End Developer", "Front End Developer"),
        ("Systems Software Engineer", "Systems Software Engineer"),
        ("Software Quality Assurance Analyst", "Software Quality Assurance Analyst"),
        ("Software Developer", "Software Developer"),
        ("Software Architect", "Software Architect"),
        ("System Designer", " System Designer"),
        ("Programmer Analyst", "Programmer Analyst"),
        ("Applications Engineer", "Applications Engineer"),
        ("Programmer", "Programmer"),
        (".NET Developer", ".NET Developer"),
        ("Associate Developer", "Associate Developer"),
        ("Application Developer", "Application Developer"),
        ("Support Analyst", "Support Analyst"),
        ("Data Quality Manager", "Data Quality Manager"),
        ("Database Administrator", "Database Administrator"),
        ("IT Analyst", "IT Analyst"),

    )

    name = forms.CharField(label='Enter your name', max_length=100)
    email = forms.EmailField(label='Enter your email', max_length=100)
    jobtitle = forms.TypedChoiceField(choices=JOB_TITLES, coerce=int, initial=1)
    state = forms.TypedChoiceField(choices=CITY_CHOICES, coerce=int, initial=1)


