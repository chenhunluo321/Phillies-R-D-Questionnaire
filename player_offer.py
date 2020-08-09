import pandas as pd
from heapq import heappush, heappop

class Offer():
    def __init__(self, url):
        self.url = url

    def find_offer_players(self):
        # load the table from html and save to panda dataframe
        tables = pd.read_html(self.url)
        df = tables[0]
        df = df[df['Salary'].notna()]
        dic = {}

        # filter out the invalid date and store Player : Salary pair into a dictionary
        for index, row in df.iterrows():
            # detect and trim the invalid salary data and convert them into int type
            salary = self.cleaned_salary(row['Salary'])
            if salary != -1:
                dic[row['Player']] = salary
        # calculate avg salary of the 125 highest salaries
        avg = self.find_average(dic, 125)
        res_df = pd.DataFrame (columns = ['Player','Salary', '125_avg'])

        # find players who have salary higher than average
        for player, salary in dic.items():
            if salary >= avg:
                res_df = res_df.append({'Player': player, 'Salary': salary, '125_avg': avg}, ignore_index=True)

        # export players list to csv file
        res_df.to_csv("offer_players.csv", encoding='utf-8', index=False)


    # detect and trim the invalid salary data and convert them into int type
    def cleaned_salary(self, salary):
        if salary == "" or salary == "no salary data":
            return -1
        salary = salary.strip('$')
        salary = salary.replace(',', '')
        return int(salary)

    # calculate the average salary of the 125 highest salaries
    def find_average(self, lis, k):
        heap = []
        for salary in lis.values():
            heappush(heap, salary)
            if len(heap) > k:
                heappop(heap)
        return sum(heap) / k





url = r'https://questionnaire-148920.appspot.com/swe/data.html'
offer = Offer(url)
offer.find_offer_players()
