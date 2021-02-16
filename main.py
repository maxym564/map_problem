import math
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium
from folium.plugins import MarkerCluster

def read_list(path,year,coordinates):
    '''
    reads the file and returns the data in the form of a dictionary,
    where the keys are a tuple with coordinates and distance, and the
    value of the movie name
    '''
    apr_loc_and_movies = {}
    with open(path,encoding='ISO-8859-1') as movie_info:
        for _ in range(14):
            next(movie_info)
        for line in movie_info:
            line = line[0:-2]
            line = line.split('\t')
            year_and_name = take_year_name(line)
            if not year_and_name:
                continue
            if year_and_name[0] == year:
                index = define_correct_adress(line)
                if not index:
                    continue
                key_coordinates = define_cordinates(line[index])
                if not key_coordinates:
                    continue
                distance = distance_between_dots(coordinates[1],key_coordinates[1],
                                                 coordinates[0],key_coordinates[0])
                movie_n = cool_name(year_and_name[1])
                apr_loc_and_movies[(key_coordinates,distance)] = apr_loc_and_movies.get((key_coordinates,distance),[]) + [movie_n]
    return apr_loc_and_movies

def take_year_name(line):
    '''
    return the tuple of year and name of movie from string
    '''
    try:
        name_year = line[0]
        for index in range(len(name_year)):
            if name_year[index] == '(':
                points = 0
                for elem in name_year[index+1:index+5]:
                    if elem.isdigit():
                        points += 1
                if points == 4:
                    year = name_year[index+1:index+5]
                    break
        name = name_year[:index]
        return int(year),name
    except:
        return False

def define_correct_adress(line):
    '''
    determines the movie address in the string
    '''
    try:
        index = -1
        while ',' not in line[index]:
            index -= 1
        return index
    except IndexError:
        return False

def cool_name(name:str):
    '''
    removes extra characters from the movie title
    '''
    bad_elem = ['#','"']
    for elem in bad_elem:
        name = name.replace(elem,'')
    return name

def distance_between_dots(lon_1,lon_2,lat_1,lat_2):
    '''
    determines the distance between two points on
    the globe using their latitude and longitude
    '''
    fs_dod = (math.sin((lat_2 - lat_1)/2))**2
    sec_dod = (math.sin((lon_2 - lon_1)/2))**2
    fst_ex = fs_dod + math.cos(lat_1)*math.cos(lat_2)*sec_dod
    result = 2 * 6371*math.asin(fst_ex)
    return result



def define_cordinates(adress):
    '''
    determines the coordinates of a particular location
    '''
    try:
        geolocator = Nominatim(user_agent='Maxym')
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

        location = geolocator.geocode(adress)
        return (location.latitude,location.longitude)
    except:
        return False


def get_10_points(all_cor:dict):
    '''
    selects at least the 10 closest coordinates from the dictionary
    '''
    lst = list(all_cor.keys())
    lst = sorted(lst,key=lambda info:info[1])
    new_dict = {key[0]:set(all_cor[key]) for key in lst[:10]}
    return new_dict

def create_map(info:dict,coordinates:list):
    '''
    creates a folder with movie tags as an htlm file
    '''
    map = folium.Map(location= coordinates,zoom_start=10)

    folium.Marker(location= list(coordinates),popup="your place",
                   icon=folium.Icon(color='blue')).add_to(map)
    mark_cluster = MarkerCluster(name='movie locations').add_to(map)
    for key in info:
        folium.Marker(location=key,
                      popup= str(info[key]),
                      icon=folium.Icon(color='red')).add_to(mark_cluster)
    map.save('map.html')

def main_func():
    '''
    main function that responce for the final process
    the dataset must be in the correct directory
    '''
    year = int(input('Enter your year: '))
    latitude = float(input('Enter your latitude: '))
    longitude = float(input('Enter your longitude: '))
    print('Please,wait...')
    info = read_list('prob_lst',year,(latitude,longitude))
    new_info = get_10_points(info)
    create_map(new_info,[latitude,longitude],)
    print('Finished')

main_func()

# if __name__ == '__main__':
#     line = read_list('prob_lst',2016,(49.83826,24.02324 ))
#     info = get_10_points(line)
#     print(info)
#     create_map(info,[49.83826,24.02324])
