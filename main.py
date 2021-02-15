import math
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def read_list(path,year):
    apr_loc_and_movies = {}
    with open(path,encoding='ISO-8859-1') as movie_info:
        for _ in range(14):
            next(movie_info)
        for line in movie_info:
            line = line[0:-2]
            line = line.split('\t')
            year_and_name = take_year_name(line)
            if year_and_name[0] == year:
                index = define_correct_adress(line)
                if index == ' ':
                    continue
                apr_loc_and_movies[line[index]] = apr_loc_and_movies.get(line[index],[]) + [year_and_name[1]]
    return apr_loc_and_movies

def take_year_name(line):
    '''
    return the year and name of movie from str
    '''
    name_year = line[0]
    year_index = name_year.find('" (')
    year = name_year[year_index:]
    name = name_year[:year_index+1]
    year = int(year[3:7])
    return year,name

def define_correct_adress(line):
    try:
        index = -1
        while ',' not in line[index]:
            index -= 1
        return index
    except IndexError:
        return ' '

def distance_between_dots(lon_1,lon_2,lat_1,lat_2):
    fs_dod = (math.sin((lat_2 - lat_1)/2))**2
    sec_dod = (math.sin((lon_2 - lon_1)/2))**2
    fst_ex = fs_dod + math.cos(lat_1)*math.cos(lat_2)*sec_dod
    result = 2 * 6000*math.asin(fst_ex)
    return result



def define_cordinates(adress):
    geolocator = Nominatim(user_agent='Maxym')
    location = geolocator.geocode(adress)
    return (location.latitude,location.longitude)

# def 

if __name__ == '__main__':
    # print(define_correct_adress(['"#Fuga" (2016)', '', '', '', '', '', 'Barra da Tijuca, Rio de Janeiro, Rio de Janeiro, Brazil', '(location']))
    print(read_list('prob_lst',2016))
    # print(define_cordinates('New York City, New York, US'))
    # print(distance_between_dots(24.02324,-74.0060152,49.83826,40.7127281))
