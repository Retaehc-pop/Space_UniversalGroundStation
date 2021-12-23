import math


class GNSS:
    '''
    get latitude longitude altitude and magnetometer from ground station
    get latitude longitude and altutude from cansat
    '''

    def __init__(self, lat_g, lng_g, lat_c, lng_c, alt_g, alt_c, x, y, z):
        self.lat_g = math.radians(float(lat_g))
        self.lat_c = math.radians(float(lat_c))
        self.lng_g = math.radians(float(lng_g))
        self.lng_c = math.radians(float(lng_c))
        self.dlon = self.lng_c - self.lng_g
        self.dlat = self.lat_c - self.lat_g

        self.alt_g = float(alt_g)
        self.alt_c = float(alt_c)
        self.alt = self.alt_c - self.alt_g

        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def arc(self):
        '''
        return arc of the 2 given point'''
        a = (math.sin(self.dlat / 2) ** 2)
        a += (math.cos(self.lat_g) * math.cos(self.lat_c)
              * ((math.sin(self.dlon / 2)) ** 2))
        x = math.sqrt(a)
        y = math.sqrt(1 - a)
        c = 2 * math.atan2(x, y)
        return c

    def ground_distance(self):
        '''
        return ground distance in meters
        '''
        R0 = 6371000
        d = R0 * self.arc()
        return d

    def line_of_sight(self):
        ''' 
        return line of sight distance in meters
        '''
        R0 = 6371000
        R = R0 + self.alt_g
        baselength = 2 * R * math.cos((math.pi - self.arc()) / 2)
        heightlength = self.alt

        los = baselength ** 2 + heightlength ** 2 - 2 * baselength * \
            heightlength * math.cos((math.pi + self.arc()) / 2)
        los = math.fabs(los)
        los = math.sqrt(los)

        return los

    def azimuth(self):
        '''
        return azimuth in degree for locating cansat
        '''
        a = math.sin(self.dlon) * math.cos(self.lat_c)
        b = math.cos(self.lat_g) * math.sin(self.lat_c) - \
            math.sin(self.lat_g) * math.cos(self.lat_c) * math.cos(self.dlon)
        theta = math.atan2(a, b)
        theta = math.degrees(theta)
        return theta

    def heading(self):
        '''
        return heading in degree for locating cansat
        '''
        ht = self.azimuth() - self.z
        ht = ht % 360
        return ht

    def elevation(self):
        '''
        return elevation in degree for locating cansat
        '''
        elev = math.atan2(self.alt, self.ground_distance())
        elev = math.degrees(elev)
        elev = elev - self.x
        elev = elev % 360
        return elev

    def roll(self):
        ty = self.y
        ty = ty % 360
        return ty

    def pythagorus(self):
        '''
        find distance of the remaining pythagorus
        '''
        pyx = math.atan2((self.lng_c - self.lng_g), (self.lat_c-self.lat_g))
        return pyx * 180/math.pi
