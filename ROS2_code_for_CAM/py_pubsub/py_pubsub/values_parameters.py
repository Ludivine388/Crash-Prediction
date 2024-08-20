# ------------------------------------------------------------------------------------------------------------------
# Script to define all specific parameters of each value 
# documentation in : https://www.etsi.org/deliver/etsi_ts/102800_102899/10289402/01.02.01_60/ts_10289402v010201p.pdf
# ------------------------------------------------------------------------------------------------------------------

# Availabality Fontion
def get_boolean(unit_value):
    if int(unit_value)==1:
        availability = True
    else:
        availability = False
    return availability

# StationType & VehicleLengthConfidenceIndication 
type_parameters = {'unknown': 0 , 'pedestrian': 1, 'cyclist': 2, 'moped': 3, 'motorcycle' :  4, 'passengerCar': 5, 'bus': 6,
                    'lightTruck' : 7, 'heavyTruck' : 8, 'trailer': 9, 'specialVehicles' : 10, 'tram' : 11, 
                    'roadSideUnit' : 15}
lenConf_parameters = {'unavailable' : 4, 'noTrailerPresent' : 0 ,'trailerPresentWithKnownLength':1, 'trailerPresentWithUnknownLength':2,
                       'trailerPresenceIsUnknown':3}

calcMode_parameters = {'unavailable' : 2, 'yawRateUsed' : 0 ,'yawRateNotUsed':1}

veh_role_parameters = {'default' : 0, 'publicTransport' : 1, 'specialTransport' : 2, 'dangerousGoods' : 3, 'roadWork' : 4, 'rescue' : 5,
            'emergency' : 6, 'safetyCar' : 7,'agriculture' : 8, 'commercial' : 9,'military' : 10,
            'roadOperator' : 11, 'taxi' : 12, 'reserved1' : 13, 'reserved2' : 14, 'reserved3' : 15} 


def get_value_from_param(unit_value, parameters):
    if unit_value in parameters.keys():
        return parameters[unit_value]
    # for calcMode and lenConf
    elif unit_value=='unavailble':
        return parameters['unavailable']
    # for vehicle role, when value is 'none', return default
    elif unit_value=='none':
        return parameters['default']
    # for type
    else:
        return parameters['unknown']

# PosConfidenceEllipse-SemiAxisLength
def get_semi_confidence(unit_value):
    if unit_value=='NaN':
        return 4095                  # Information not available
    else :
        unit_value = float(unit_value)
        if 1 < unit_value <= 4093:
            return int(unit_value)       # n (n > 1 and n < 4 093) if the accuracy is equal to or less than n cm
        else:
            return 4094                  # out of range

#HeadingValue
def get_heading_value(unit_value):
    if unit_value=='NaN':
        return 3601                 # Information not available
    else:
        return int(float(unit_value))
    
# AltitudeConfidence & CurvatureConfidence
altConf_parameters = [(0.01, 0), (0.02, 1), (0.05, 2), (0.1, 3), (0.2, 4), (0.5, 5), (1, 6), (2, 7),
                       (5, 8), (10, 9), (20, 10), (50, 11), (100, 12), (200, 13)]
altConf_unavail = 15
altConf_out_of_range = 14

curVal_conf_parameters = [(0.00002, 0), (0.0001, 1), (0.0005 , 2), (0.002, 3), (0.01, 4), (0.1, 5)]
curVal_conf_unavail = 7
curVal_conf_out_of_range = 6

yawRate_conf_parameters = [(0.01, 0), (0.05, 1), (0.1 , 2), (1, 3), (5, 4), (10, 5), (100, 6)]
yawRate_conf_unavail = 8
yawRate_conf_out_of_range = 7

def get_Conf(unit_value, parameters, unavail, out_of_range):
    # no information
    if unit_value=='NaN':
        return unavail
    # check for value with parameters
    for max_value, level in parameters:
        if float(unit_value) <= max_value:
            return level
    return out_of_range    

#HeadingConfidence
def get_heading_confidence(unit_value):
    if unit_value=='NaN':
        return 127  # Information not available
    elif float(unit_value) <= 0.1:
        return 1    # 1 if the heading accuracy is equal to or less than 0.1 degree
    elif 0.1 < float(unit_value) < 12.5:
        return int(float(unit_value))
    elif float(unit_value) == 12.5:
        return 125  # 125 if the heading accuracy is equal to 12.5 degrees
    else:
        return 126  # Out of range, greater than 12.5 degrees
    
# SpeedValue
def get_speed_value(unit_value):
    if unit_value=='NaN':
        return 16383       # Information not available                            
    else:
        unit_value = float(unit_value) * 100          # unit_value is given in m/s, unit in CAM : oneCentimeterPerSec(1)
        if unit_value < 16382:
            return int(unit_value)                    
        else:
            return 16382   # out of range values
        
# SpeedConf
def get_speed_confidence(unit_value):
    if unit_value=='NaN':
        return 127       # Information not available                            
    else:
        unit_value = float(unit_value) * 100          # unit_value is given in m/s, unit in CAM : oneCentimeterPerSec(1)
        if unit_value <= 1:
            return 1                    
        elif 1 < unit_value <= 125:
            return int(unit_value)
        else:
            return 126   # out of range

# VehicleLength
def get_veh_len(unit_value):
    if unit_value=='NaN':
        return 1023       # Information not available                            
    else:
        unit_value = float(unit_value) * 10          # unit_value is given in m, unit in CAM : tenCentimeters(1)                
        if 1022 <= unit_value:
            return 1022  # out of range
        else:
            return int(unit_value)
        
# VehicleWidth
def get_veh_wid(unit_value):
    if unit_value=='NaN':
        return 62       # Information not available                            
    else:
        unit_value = float(unit_value) * 10          # unit_value is given in m, unit in CAM : tenCentimeters(1)                
        if 61 <= unit_value:
            return 61  # out of range
        else:
            return int(unit_value)
        
#Acceleration Value & Confidence
def get_Acc_value(unit_value):
    if unit_value=='NaN':
        return 161       # Information not available                            
    else:
        unit_value = float(unit_value) * 10          # unit_value is given in m/s^2, unit in CAM : pointOneMeterPerSecSquared(1)
        # out of range
        if 160 < unit_value:
            return 160
        elif unit_value < -160:
            return -160
        # else
        else:
            return int(unit_value)
        
def get_Acc_conf(unit_value):
    if unit_value=='NaN':
        return 102       # Information not available                            
    else:
        unit_value = float(unit_value) * 10          # unit_value is given in m/s^2, unit in CAM : pointOneMeterPerSecSquared(1)
        if 100 < unit_value:
            return 101  # out of range
        elif unit_value <= 0.1:
            return 1
        else:
            return int(unit_value)
        
#YawRate
def get_yawRate_value(unit_value):
    if unit_value=='NaN':
        return 32767       # Information not available                            
    else:
        unit_value = float(unit_value) * 100          # unit_value is given in deg/s, unit in CAM : 0.01 degree per second
        # out of range
        if 32766 < unit_value:
            return 32766
        elif unit_value < -32766:
            return -32766
        # else
        else:
            return int(unit_value)

# AccelerationControl & ExteriorLights
list_keys_acc_control = ['brakeEng', 'gasEng', 'emergBrakeEng', 'collWarnEng', 'accEng', 'cruiseContEng', 'speedLimEng']
list_keys_extLight = ['lowBeam', 'highBeam', 'leftTurn', 'rightTurn', 'daytime', 'reverse', 'fog', 'parking']

def get_bit_string(unit_key, list_keys):
    conditions = []
    for key in list_keys:
        if int(unit_key[key])==1:
            # if breakEng is engaged bit shall be set to 1
            conditions.append(True)
        else:
            conditions.append(False)
    # create bit string from condition (True fro engaged (1) and False from not engaged (0))
    bit_string = ''.join(['1' if condition else '0' for condition in conditions])
    return int(bit_string)

# SteeringWheelAngle
# TODO: rework needed
steerWhAngl_val_unavail = 512
steerWhAngl_conf_unavail = 127
def get_steerWhAngl_data(unit_value, unavailable_int):
    if unit_value=='NaN':
        return unavailable_int       # Information not available                            
    else:
        unit_value = float(unit_value)
        return int(unit_value)
