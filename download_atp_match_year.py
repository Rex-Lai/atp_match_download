# -*- coding: utf-8 -*-
from lxml import html
from bs4 import BeautifulSoup
import requests
import re
import json
import csv
import sys

#def html_parse(url, xpath):
#    page = requests.get(url)
#    tree = html.fromstring(page.content)
#    result = tree.xpath(xpath)
#    return result
    
def html_download(url):
    page = requests.get(url)
    return page.text
    #tree = html.fromstring(page.content)
    #return tree

def html_parse(data, xpath):
    result = data.xpath(xpath)
    return result

def regex_strip_string(string):
    string = re.sub('\n', '', string)
    string = re.sub('\r', '', string)
    string = re.sub('\t', '', string)
    return string

def regex_strip_space(string):
    string = re.sub(' ', '', string)
    return string
    
def regex_strip_array(array):
    for i in xrange(0, len(array)):
        array[i] = regex_strip_string(array[i])
    return array

def parse_atp_year(url):
    #Tournament title
    year_page = html_download(year_url)
    soup = BeautifulSoup(year_page, "lxml")
    tourney_result_parsed = soup.find_all("tr")
    tourney_count = len(tourney_result_parsed)
    for i in xrange(0, tourney_count):
        cells = tourney_result_parsed[i].find_all("td")
        if len(cells) > 4:
            tourney_badge = cells[1].find("img")["src"].split("?")[0].split("/")[5].split("_")[1]
            tourney_title = regex_strip_string(cells[2].find("span", class_="tourney-title").get_text().encode("UTF-8"))
            tourney_location = regex_strip_string(cells[2].find("span", class_="tourney-location").get_text().encode("UTF-8"))
            tourney_dates = regex_strip_string(cells[2].find("span", class_="tourney-dates").get_text().encode("UTF-8"))
            tourney_condition_surface = regex_strip_string(cells[4].find("div", class_="item-details").get_text().encode("UTF-8")).split(" ")
            tourney_condition = tourney_condition_surface[0]
            tourney_surface = tourney_condition_surface[1]
            tourney_draws = cells[3].find_all("span", class_="item-value")
            tourney_single_draws = regex_strip_space(regex_strip_string(tourney_draws[0].get_text().encode("UTF-8")))
            year_array = [tourney_title, tourney_badge, tourney_location, tourney_dates, tourney_condition, tourney_surface, tourney_single_draws]
            for a in cells[7].find_all("a", href=True):
                current_url = a["href"]
            print( str(year) + "-" + str(i) + ": " + tourney_title + "," + tourney_badge + "," + tourney_location + "," + tourney_dates + "," + tourney_surface)
            #parse_tournaement(year_array, url_prefix + current_url)
            #print( url_prefix + current_url)
    
def parse_atp_year2(url):
    year_page = html_download(year_url)
    print(year_page)
    soup = BeautifulSoup(year_page, "lxml")
    tourney_result_parsed = soup.find_all("tr")
    tourney_count = len(tourney_result_parsed)
    print(tourney_count)
    for i in xrange(0, tourney_count):
        cells = tourney_result_parsed[i].find_all("td")
        if len(cells) > 4:
            for a in cells[7].find_all("a", href=True):
                current_url = a["href"]
            print( str(year) + "-" + str(i) + ": " )#+ tourney_title + "," + tourney_badge + "," + tourney_location + "," + tourney_dates + "," + tourney_surface
            print( url_prefix + current_url)
            parse_tournaement(url_prefix + current_url)

def parse_tournaement(url):
    #get tournament page
    tournament_page = html_download(url)
    soup_tournament = BeautifulSoup(tournament_page, "lxml")
    
    #get tournament info
    tourney_info = soup_tournament.find("table", class_="tourney-results-wrapper")
    cells = tourney_info.find_all("td")
    tourney_badge = cells[0].find("img")["src"].split("?")[0].split("/")[5].replace("-","_").split("_")[1]
    try:
        tourney_title = regex_strip_string(cells[1].find("a", class_="tourney-title").get_text().encode("UTF-8"))
    except:
        tourney_title = regex_strip_string(cells[1].find("span", class_="tourney-title").get_text().encode("UTF-8"))
    tourney_location = regex_strip_string(cells[1].find("span", class_="tourney-location").get_text().encode("UTF-8"))
    tourney_dates = regex_strip_string(cells[1].find("span", class_="tourney-dates").get_text().encode("UTF-8")).split(" - ")
    tourney_details = cells[2].find_all("td", class_="tourney-details")
    tourney_single_draws = regex_strip_space(regex_strip_string(tourney_details[0].find("span", class_="item-value").get_text()))
    tourney_surface = regex_strip_space(regex_strip_string(tourney_details[1].find("span", class_="item-value").get_text()))
    #year_array = [tourney_title, tourney_badge, tourney_location, tourney_dates, tourney_condition, tourney_surface, tourney_single_draws]
    #print str(year) + "-" + str(i) + ": " + tourney_title + "," + tourney_badge + "," + tourney_location + "," + tourney_dates + "," + tourney_surface
    year_array = [tourney_title,tourney_badge,tourney_location,tourney_dates[0],tourney_dates[1],tourney_surface,tourney_single_draws]
    
    #get tournament detail
    tournament_table = soup_tournament.find("table", class_="day-table")
    table_headers = tournament_table.find_all("th")
    table_bodys = tournament_table.find_all("tbody")
    #output tournament rounds
    for i in xrange(0, len(table_headers)):
        tournament_round = table_headers[i].get_text()
        rows = table_bodys[i].find_all("tr")
        for j in xrange(0, len(rows)):
            cols = rows[j].find_all("td")
            #player seed No.
            #player_no = regex_strip_string(cols[0].find("span").get_text())
            #player name
            player_name = regex_strip_string(cols[2].find("a").get_text().encode("UTF-8"))
            #opponent seed No.
            #opponent_no = regex_strip_string(cols[4].find("span").get_text())
            #opponent name
            opponent_name = regex_strip_string(cols[6].find("a").get_text().encode("UTF-8"))
            #scores
            scores = cols[7].get_text().split(" ")
            round_no = str(i+1)
            print( round_no + "-" + str(j) + " | "+ tournament_round + " | " + player_name + " def. " + opponent_name + " | " + regex_strip_string(cols[7].get_text()))
            set_length = 0
            total_set = []
            for k in xrange(0, len(scores)):
                set_score = regex_strip_string(scores[k])
                if set_score == "(RET)" or set_score == "(W/O)":
                    total_set.append(set_score)
                elif len(set_score) > 2: #tiebreak
                    total_set.append(set_score[0:2] + "(" + set_score[2:] + ")")
                    set_length += 1
                elif len(set_score) == 0:
                    continue
                else:
                    total_set.append(set_score)
                    set_length += 1
            #match details
            
            tournament_array = year_array + [tournament_round, round_no, player_name, opponent_name, str(set_length)]
            tournament_array += total_set
            tournament_array2 = []
            tournament_array2.append(year_array + [tournament_round, round_no, player_name, "win", opponent_name, str(set_length)] + total_set)
            tournament_array2.append(year_array + [tournament_round, round_no, opponent_name, "lose", player_name, str(set_length)]+ total_set)
            for m in range(0, 5-set_length):
                tournament_array += [""]
                tournament_array2[0] += [""]
                tournament_array2[1] += [""]
            scores_url = cols[7].find("a", href=True)
            try:
                match_detail_url = scores_url["href"]
                match_result = parse_match(url_prefix + match_detail_url)
                csv_array.append(tournament_array + match_result[0] + match_result[1])
                csv_array2.append(tournament_array2[0] + match_result[0])
                match_time = [match_result[0][0]]
                csv_array2.append(tournament_array2[1] + match_time + match_result[1])
            except:
                print( "no match detail url")
                continue
        # Output to CSV file
        print( "save to file")
        print( year_array)
        csv_out1 = open("new_" + year + ".csv", 'wb')
        mywriter1 = csv.writer(csv_out1)
        for row in csv_array:
            mywriter1.writerow(row)
        csv_out1.close()
        # Save file2
        csv_out2 = open("new2_" + year + ".csv", 'wb')
        mywriter2 = csv.writer(csv_out2)
        for row in csv_array2:
            mywriter2.writerow(row)
        csv_out2.close()
        
def parse_match(url):
    tournament_id = url.split("/")[6]
    #match_id = url.split("/")[12]
    match_page = html_download(url)
    soup_match = BeautifulSoup(match_page, "html.parser")
    match_time = regex_strip_string(soup_match.find("td", class_="time").get_text()).split(" ")[1]
	#get stats json data
    match_stats = soup_match.find("script", id="matchStatsData").get_text()
    #print match_stats
    match_stats_json = json.loads(match_stats)
    #winner_ace = match_stats_json[0]['playerStats']['Aces']
    player_match_data = [match_time]
    opponent_match_data = []
    for s in match_header:
        player_match_data.append(str(match_stats_json[0]['playerStats'][s]))
        opponent_match_data.append(str(match_stats_json[0]['opponentStats'][s]))
    
    match_result = []
    match_result.append(player_match_data)
    match_result.append(opponent_match_data)
    return match_result
    #print match_stats_json[0]['opponentStats']
    #print match_stats_json[0]['playerStats']
    
year_header = ['tourney_title','tourney_badge','tourney_location','tourney_dates','tourney_dates1','tourney_surface','tourney_single_draws']
tournament_header = ['tournament_round','round_no','player_name','opponent_name','set_length','set1','set2','set3','set4','set5','match_time']
tournament_header2 = ['tournament_round','round_no','player_name','win/lose','opponent_name','set_length','set1','set2','set3','set4','set5','match_time']
#match_header = ['Aces','AcesPercentage','DoubleFaults','DoubleFaultsPercentage','FirstServePercentage','FirstServeDividend','FirstServeDivisor','FirstServePointsWonPercentage','FirstServePointsWonDividend','FirstServePointsWonDivisor','SecondServePointsWonPercentage','SecondServePointsWonDividend','SecondServePointsWonDivisor','BreakPointsSavedPercentage','BreakPointsSavedDividend','BreakPointsSavedDivisor','ServiceGamesPlayed','ServiceGamesPlayedPercentage','FirstServeReturnPointsPercentage','FirstServeReturnPointsDividend','FirstServeReturnPointsDivisor','SecondServePointsPercentage','SecondServePointsDividend','SecondServePointsDivisor','BreakPointsConvertedPercentage','BreakPointsConvertedDividend','BreakPointsConvertedDivisor','ReturnGamesPlayed','ReturnGamesPlayedPercentage','TotalServicePointsWonPercentage','TotalServicePointsWonDividend','TotalServicePointsWonDivisor','TotalReturnPointsWonPercentage','TotalReturnPointsWonDividend','TotalReturnPointsWonDivisor','TotalPointsWonPercentage','TotalPointsWonDividend','TotalPointsWonDivisor']
match_header = ['AcesPercentage','DoubleFaultsPercentage','FirstServePercentage','FirstServePointsWonPercentage','SecondServePointsWonPercentage','BreakPointsSavedPercentage',
'FirstServeReturnPointsPercentage','SecondServePointsPercentage','BreakPointsConvertedPercentage',
'TotalServicePointsWonPercentage','TotalReturnPointsWonPercentage','TotalPointsWonPercentage',
'Aces','DoubleFaults','FirstServeDividend','FirstServeDivisor',
'FirstServePointsWonDividend','FirstServePointsWonDivisor',
'SecondServePointsWonDividend','SecondServePointsWonDivisor',
'BreakPointsSavedDividend','BreakPointsSavedDivisor',
'ServiceGamesPlayed','ServiceGamesPlayedPercentage',
'FirstServeReturnPointsDividend','FirstServeReturnPointsDivisor',
'SecondServePointsDividend','SecondServePointsDivisor',
'BreakPointsConvertedDividend','BreakPointsConvertedDivisor',
'ReturnGamesPlayed','ReturnGamesPlayedPercentage',
'TotalServicePointsWonDividend','TotalServicePointsWonDivisor',
'TotalReturnPointsWonDividend','TotalReturnPointsWonDivisor',
'TotalPointsWonDividend','TotalPointsWonDivisor']

# Command line input
year = str(sys.argv[1])

# Setup
year_url = "http://www.atpworldtour.com/en/scores/results-archive?year=" + year
url_prefix = "http://www.atpworldtour.com"
year_current = "http://www.atpworldtour.com/en/scores/current"

player_match_header = []
opponent_match_header = []
for s in match_header:
    player_match_header.append("player" + s)
    opponent_match_header.append("opponent" + s)

all_header = year_header + tournament_header + player_match_header + opponent_match_header
all_header2 = year_header + tournament_header2 + match_header

csv_array = []
csv_array2 = []

csv_array.append(all_header)
csv_array2.append(all_header2)

parse_atp_year2(year_url)
#parse_tournaement(year_current)
#parse_tournaement("http://www.atpworldtour.com/en/scores/archive/bucharest/773/2016/results")
#parse_match("http://www.atpworldtour.com/en/tournaments/nitto-atp-finals/605/2016/match-stats/MC10/R975/live/MS002/match-stats")
#http://www.atpworldtour.com/en/tournaments/nitto-atp-finals/605/2016/match-stats/mc10/r975/match-stats
#http://www.atpworldtour.com/en/tournaments/nitto-atp-finals/605/2016/match-stats/MC10/R975/live/MS002/match-stats
