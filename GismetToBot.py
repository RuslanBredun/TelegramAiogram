import requests
from bs4 import BeautifulSoup
import datetime
from fake_useragent import UserAgent
import numpy as np


def get_html_code(city='киев'):
    if city.lower() == 'днепр':
        city = 'днепр-303007131'
    day = datetime.datetime.today().strftime("%Y-%m-%d")
    html_code = requests.get(f'http://sinoptik.ua/погода-{city}/{day}', headers={'User-agent': UserAgent().random})
    html_code.encoding = 'utf-8'
    soup = BeautifulSoup(html_code.content, 'html.parser')
    if soup.find(attrs={'class': 'ru p404'}):
        return False
    else:
        return html_code.content


def get_week_info(city='киев'):
    # Checking for 404 error
    if get_html_code(city):
        html_doc = get_html_code(city)
    else:
        return False
    # Parsing site
    soup = BeautifulSoup(html_doc, 'html.parser')
    soup_result = np.array(soup.find(id='blockDays').find(attrs={'class': 'tabs'}).text.split())
    soup_result = soup_result.reshape((int(soup_result.shape[0]/7), 7))
    img_result = soup.find(id='blockDays').find(attrs={'class': 'tabs'}).find_all(attrs={'class': 'weatherIco'})

    # Take images info from parser
    img_list, img_url, gifs = [], [], []
    for image in img_result:
        img_list.append(str(image).split('"')[3])
        # img_url.append(str(image).split('"')[-2])

    # TODO: download images to decorate answers
    # Take gif from url
    # for idx, url in enumerate(img_url):
    #     with open(f'/tmp/{idx}.gif', 'wb') as f:
    #         f.write(requests.get(url).content)
    #     gifs.append(requests.get(url).content)
    soup_result = np.column_stack((soup_result, img_list))
    result = []
    for row in soup_result:
        result.append({'day': row[0] + ' - ' + row[1] + ' ' + row[2],
                       'min_temp': row[4],
                       'max_temp': row[6],
                       'description': row[7]})
    return result


def get_now_weather(city="киев"):
    response = get_html_code(city)
    soup = BeautifulSoup(response, "lxml")
    now = {}
    index_time = int(float(datetime.datetime.now().strftime("%H")) / 3)
    now['time'] = datetime.datetime.now().strftime("%H:%M")
    now['temp'] = soup.find('table', class_="weatherDetails").find_all('tr')[3].find_all('td')[index_time].text
    now['temp_sens'] = soup.find('table', class_="weatherDetails").find_all('tr')[4].find_all('td')[index_time].text
    now['pressure'] = soup.find('table', class_="weatherDetails").find_all('tr')[5].find_all('td')[index_time].text
    now['humidity'] = soup.find('table', class_="weatherDetails").find_all('tr')[6].find_all('td')[index_time].text
    now['wind'] = soup.find('table', class_="weatherDetails").find_all('tr')[7].find_all('td')[index_time].text
    now['precipitation'] = soup.find('table', class_="weatherDetails").find_all('tr')[8].find_all('td')[index_time].text
    now['sunrise_time'] = soup.find('div', class_='infoDaylight').find_all('span')[0].text
    now['sunset_time'] = soup.find('div', class_='infoDaylight').find_all('span')[1].text
    return now


def get_today_weather(city='киев'):
    if get_html_code(city):
        html_doc = get_html_code(city)
    else:
        return False
    soup = BeautifulSoup(html_doc, 'html.parser')
    soup_result = np.array(soup.find(attrs={'class': 'weatherDetails'}).text.split())
    ind_f = np.where(soup_result == ':00')[-1][-1]
    soup_result = np.array(soup_result[ind_f+1:])
    soup_result = soup_result.reshape((6, int(np.size(soup_result)/6)))
    result_list = []
    result_list.append(min(soup_result[0].tolist()))
    result_list.append(max(soup_result[0].tolist()))
    result_list.append(min(soup_result[1].tolist()))
    result_list.append(max(soup_result[1].tolist()))
    result_list.append(soup_result[2, 0])
    result_list.append(min(soup_result[3].tolist()))
    result_list.append(max(soup_result[3].tolist()))
    result_list.append(min(soup_result[4].tolist()))
    result_list.append(max(soup_result[4].tolist()))
    result_list.append(max(soup_result[5].tolist()))
    columns_list = ['min_temp', 'max_temp', 'min_temp_sense', 'max_temp_sense', 'pressure', 'min_humidity',
                    'max_humidity', 'min_wind', 'max_wind', 'max_precipitation']
    result = dict(zip(columns_list, result_list))
    return result


def get_3d_weather(city='киев'):
    return get_week_info(city=city)[:3]


def get_7d_weather(city='киев'):
    return get_week_info(city=city)[:7]


if __name__ == "__name__":
    get_week_info()
