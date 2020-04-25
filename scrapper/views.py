from django.shortcuts import render

from scrapper.forms import MyForm
from django.template import loader
from django.http import HttpResponse
from bs4 import BeautifulSoup
import urllib
import re
import pandas as pd
import requests
from urllib.request import urlopen
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from scrapper import settings

# Created views here.


def responseform(request):
    # if form is submitted

    if request.method == 'POST':

        myForm = MyForm(request.POST)

        if myForm.is_valid():

            # returing the template
            return render(request, 'index.html')
    else:
        form = MyForm()
        # returning form with validation message
        return render(request, 'form.html', {'form': form})


def postrequest(request):
    if request.method == 'POST':

        settings.JOBTITLE = request.POST.get('jobtitle')
        state = request.POST.get('state')
        settings.STATE = state
        return render(request, 'index.html')


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class SkillData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        #Initailizing all counters
        sum_py = 0
        sum_C = 0
        sum_Cplus = 0
        sum_Csharp = 0
        sum_php = 0
        sum_java = 0
        sum_javascript = 0
        sum_r = 0
        sum_sql = 0
        sum_hadoop = 0


        sum_spark = 0
        sum_aws = 0
        sum_tableau = 0

        i = 0

        # get global parameters
        searchstate = settings.STATE
        jobtitle = settings.JOBTITLE

        # build url as per indeed format
        jobtitle = jobtitle.replace(" ", "%20")
        statecity = searchstate.split(',')
        url = 'https://www.indeed.ca/jobs?q=' + str(jobtitle) + '&l=' + str(statecity[0]) +'%2C+' + str(statecity[1])[1:]

        # Data extraction and analysis
        for i in range(1):
            try:
                #Requesting joblisting data from url and parsing it into html using html parser
                page = urlopen(url)
                soup = BeautifulSoup(page, 'lxml')
                all_matches = soup.findAll(attrs={'rel': ['noopener nofollow']})

                # Requesting each job description data from url and parsing it into html using html parser
                for i in all_matches:
                    jd_url = 'http://www.indeed.ca/' + i['href']
                    response = requests.get(jd_url,timeout=5)
                    jd_page = response.text
                    jd_soup = BeautifulSoup(jd_page, 'lxml')
                    jd_desc = jd_soup.findAll('div', attrs={'id': ['jobDescriptionText']})  ## find the structure like: <div id="desc"></>

                    # searching and counting skill keyword found in job decription page
                    C = re.findall(r'[\b\s\/]C\b[\/\s,]', str(jd_desc))
                    sum_C = sum_C + len(C)

                    c_plus = re.findall(r'[\b\/\s]?[Cc]\+\+[\s,]?', str(jd_desc))
                    sum_Cplus = sum_Cplus + len(c_plus)

                    java = re.findall(r'[\/\b\s]?[Jj]ava[\b,\/]?', str(jd_desc))
                    sum_java = sum_java + len(java)

                    javascript = re.findall(r'[\/\s\b][Jj]ava[Ss]cript[\/\b\s,]?', str(jd_desc))
                    sum_javascript = sum_javascript + len(javascript)

                    python = re.findall(r'[\/\b]?[Pp]ython[\s\/,]?', str(jd_desc))
                    sum_py = sum_py + len(python)

                    R = re.findall(r'[\s\/\b]?R[\b\s\/,]', str(jd_desc))
                    sum_r = sum_r + len(R)

                    sql = re.findall(r'[\/\b]?[Ss][Qq][Ll][\s\/,]?', str(jd_desc))
                    sum_sql = sum_sql + len(sql)

                    hadoop = re.findall(r'[\/\b]?Hadoop[\s\/,]?', str(jd_desc))
                    sum_hadoop = sum_hadoop + len(hadoop)

                    csharp = re.findall(r'[\/\b]?[Cc]\#[\s\/,]?', str(jd_desc))
                    sum_Csharp = sum_Csharp + len(csharp)

                    php = re.findall(r'[\/\b]?P[Hh][Pp][\s\/,]?', str(jd_desc))
                    sum_php = sum_php + len(php)

                    spark = re.findall(r'[\/\b]?Spark[\s\/,]?', str(jd_desc))
                    sum_spark = sum_spark + len(spark)

                    aws = re.findall(r'[\/\b]?AWS[\s\/,]?', str(jd_desc))
                    sum_aws = sum_aws + len(aws)

                    tableau = re.findall(r'[\/\b\/]?Tableau[\s\/,]?', str(jd_desc))
                    sum_tableau = sum_tableau + len(tableau)

            except:
                print("An exception occurred")

            url_all = soup.findAll(attrs={'rel': ['next']})

            if(len(url_all) > 0):
                url = 'http://www.indeed.ca/' + str(url_all[0]['href'])

        # Loading chart with labels and data
        labels = ["C", "C++", "Java", "Javascript", "Python", "R", "SQL", "Hadoop", "C#", "PHP",
                                    "Spark", "AWS", "Tableau"]
        chartLabel = "skills"
        chartdata = [sum_C, sum_Cplus, sum_java, sum_javascript, sum_py, sum_r, sum_sql, sum_hadoop,
                                 sum_Csharp,
                                 sum_php, sum_spark, sum_aws, sum_tableau]
        data = {
            "labels": labels,
            "chartLabel": chartLabel,
            "chartdata": chartdata,
        }

        return Response(data)

