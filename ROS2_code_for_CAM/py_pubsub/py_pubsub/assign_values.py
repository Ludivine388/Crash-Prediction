from datetime import datetime, timezone
from py_pubsub.get_values import get_root, get_values
from py_pubsub.values_parameters import *
import cam_msg.msg 
# import *         # import all messages from cam_msg

# to be change for xml output of Station_Details
file_unit = 'py_pubsub/py_pubsub/ucuMyItsData.xml'

# get values from unit and return data in a dictionary
unit_data = {}
unit_xml = get_root(file_unit)
unit_data[unit_xml.tag] = unit_xml.attrib
get_values(unit_xml, unit_data)
# to check output
# print(unit_data) 

# Assign values of data to variables (values from unit_data are str)

# -----------------------------------------------------------
# Constant variables
# -----------------------------------------------------------

# ItsPduHeader 
prot_vers = 1                                            # currentVersion is 1 (ETSI TS 102 894-2 V1.2.1)
msg_id = 2                                                  # MESSAGE_ID_CAM = 2

# DriveDirection
drive_dir = 2                                            # forward = 0, backaward = 1, unavailable = 2

# AccelerationControl
bits_unused = 0

#LanePosition
laneNum_present = True

#PerformanceClass
perfClass = 0
perfClass_present = False

# -----------------------------------------------------------
# Unconstant variables
# -----------------------------------------------------------

# ItsPduHeader/StationID
staId = int(unit_data['ucuMyItsData']['staId'])

# CoopAwareness/GenerationDeltaTime
#TimestampIts represents an integer value in milliseconds since 2004-01-01T00:00:00:000Z as defined in ETSI TS 102 894-2 [2]
dt_value = unit_data['ucuMyItsData']['dt']
dt_object = datetime.fromisoformat(dt_value[:-1]).replace(tzinfo=timezone.utc)      #timestamp string into a datetime object
# Convert to Unix timestamp (seconds since epoch)
unix_timestamp = int(dt_object.timestamp())     # Convert to Unix timestamp (seconds since epoch)
# Calculate the remainder when divided by 65,536
dt = unix_timestamp % 65536

#CoopAwareness/CamParameters/BasicContainer/StationType
type = get_value_from_param(unit_data['obuIts']['type'], type_parameters)

#CoopAwareness/CamParameters/BasicContainer/ReferencePosition/Latitude&Longitude
# INTEGER {oneMicrodegreeNorth (10), oneMicrodegreeSouth (-10), unavailable(900000001) }
if unit_data['pos']['lat']=='NaN':
    lat = 900000001                       
else:
    lat = int(float(unit_data['pos']['lat'])*1e7)

if unit_data['pos']['lng']=='NaN':
    lng = 1800000001                      # unavailable
else:
    lng = int(float(unit_data['pos']['lng'])*1e7)

#CoopAwareness/CamParameters/BasicContainer/ReferencePosition/PosConfidenceEllipse
posConfMinAx = get_semi_confidence(unit_data['pos']['posConfMinAx'])
posConfMajAx = get_semi_confidence(unit_data['pos']['posConfMajAx'])
posConfElOr = get_heading_value(unit_data['pos']['posConfElOr'])          # Headingvalue (semi_major_orientation & heading_value)  

# CoopAwareness/CamParameters/BasicContainer/ReferencePosition/AltitudeValue&AltitudeConfidence
alt = int(float(unit_data['pos']['alt']))
altConf = get_Conf(unit_data['pos']['altConf'], altConf_parameters, altConf_unavail, altConf_out_of_range)

# CoopAwareness/CamParameters/HighFrequencyContainer/BasicVehicleContainerHighFrequency/Heading
heading_val = get_heading_value(unit_data['heading']['value'])
heading_conf = get_heading_confidence(unit_data['heading']['conf'])

# CoopAwareness/CamParameters/HighFrequencyContainer/BasicVehicleContainerHighFrequency/Speed
speed_val = get_speed_value(unit_data['speed']['value'])
speed_conf = get_speed_confidence(unit_data['speed']['conf'])

# CoopAwareness/CamParameters/HighFrequencyContainer/BasicVehicleContainerHighFrequency/VehicleLength
len = get_veh_len(unit_data['dim']['len'])
veh_lenConf = get_value_from_param(unit_data['dim']['lenConf'], lenConf_parameters)
wid = get_veh_wid(unit_data['dim']['wid'])

# CoopAwareness/CamParameters/HighFrequencyContainer/BasicVehicleContainerHighFrequency/LongitudinalAcceleration
lngAcc_val = get_Acc_value(unit_data['lngAcc']['value'])
lngAcc_conf = get_Acc_conf(unit_data['lngAcc']['conf'])

# CoopAwareness/CamParameters/HighFrequencyContainer/BasicVehicleContainerHighFrequency/Curvature
curVal_val = int(float(unit_data['curVal']['value']))
curVal_conf = get_Conf(unit_data['curVal']['conf'], curVal_conf_parameters, curVal_conf_unavail, curVal_conf_out_of_range)
curVal_calcMode = get_value_from_param(unit_data['curVal']['calcMode'], calcMode_parameters)

# CoopAwareness/CamParameters/HighFrequencyContainer/BasicVehicleContainerHighFrequency/YawRate
yawRate_val = get_yawRate_value(unit_data['yawRate']['value'])
yawRate_conf = get_Conf(unit_data['yawRate']['conf'], yawRate_conf_parameters, yawRate_conf_unavail, yawRate_conf_out_of_range)

# CoopAwareness/CamParameters/HighFrequencyContainer/BasicVehicleContainerHighFrequency/AccelerationControl
accControl_present = get_boolean(unit_data['accControl']['avail'])
accControl = get_bit_string(unit_data['accControl'], list_keys_acc_control)

# CoopAwareness/CamParameters/HighFrequencyContainer/BasicVehicleContainerHighFrequency/LanePosition
laneNum = int(unit_data['lanePositionDef']['laneNum'])         # offTheRoad(-1), hardShoulder(0), outermostDrivingLane(1), secondLaneFromOutside(2),...

# CoopAwareness/CamParameters/HighFrequencyContainer/BasicVehicleContainerHighFrequency/SteeringWheel
steerWhAngl_present = get_boolean(unit_data['steerWhAngle']['avail'])
if steerWhAngl_present:
    steerWhAngle_val = get_steerWhAngl_data(unit_data['steerWhAngle']['value'], steerWhAngl_val_unavail)
    steerWhAngle_conf = get_steerWhAngl_data(unit_data['steerWhAngle']['conf'], steerWhAngl_conf_unavail)
else:
    steerWhAngle_val = steerWhAngl_val_unavail
    steerWhAngle_conf = steerWhAngl_conf_unavail

# CoopAwareness/CamParameters/HighFrequencyContainer/BasicVehicleContainerHighFrequency/LateralAcceleration
latAcc_present = get_boolean(unit_data['latAcc']['avail'])
latAcc_val = get_Acc_value(unit_data['latAcc']['value'])
latAcc_conf = get_Acc_conf(unit_data['latAcc']['conf'])

# CoopAwareness/CamParameters/HighFrequencyContainer/BasicVehicleContainerHighFrequency/VerticalAcceleration
vertAcc_val = get_Acc_value(unit_data['vertAcc']['value'])
vertAcc_conf = get_Acc_conf(unit_data['vertAcc']['conf'])
vertAcc_present = get_boolean(unit_data['vertAcc']['avail'])

# CoopAwareness/CamParameters/HighFrequencyContainer/BasicVehicleContainerHighFrequency/CenDsrcTollingZone
if unit_data['cenDsrcZone']['lat']=='NaN':
    cenDsrcZone_lat  = 900000001                       
else:
    cenDsrcZone_lat  = int(float(unit_data['cenDsrcZone']['lat'])*1e7)

if unit_data['cenDsrcZone']['lng']=='NaN':
    cenDsrcZone_lng  = 900000001                       
else:
    cenDsrcZone_lng  = int(float(unit_data['cenDsrcZone']['lng'])*1e7)
prot_zone_id = int(unit_data['cenDsrcZone']['id'])

# CoopAwareness/CamParameters/LowFrequencyContainer/BasicVehicleContainerLowFrequency/VehicleRole
veh_role = get_value_from_param(unit_data['obuIts']['role'], veh_role_parameters)

# CoopAwareness/CamParameters/LowFrequencyContainer/BasicVehicleContainerLowFrequency/ExteriorLights
extLight = get_bit_string(unit_data['extLight'], list_keys_extLight)

cam_2_pub = cam_msg.msg.CAM(
                header=cam_msg.msg.ItsPduHeader(
                    protocol_version=prot_vers, 
                    message_id=msg_id, 
                    station_id=cam_msg.msg.StationID(value=staId)), 
                cam=cam_msg.msg.CoopAwareness(
                    generation_delta_time=cam_msg.msg.GenerationDeltaTime(value=dt), 
                    cam_parameters=cam_msg.msg.CamParameters(
                        basic_container=cam_msg.msg.BasicContainer(
                            station_type=cam_msg.msg.StationType(value=type), 
                            reference_position=cam_msg.msg.ReferencePosition(
                                latitude=cam_msg.msg.Latitude(value=lat), 
                                longitude=cam_msg.msg.Longitude(value=lng), 
                                position_confidence_ellipse=cam_msg.msg.PosConfidenceEllipse(
                                    semi_major_confidence=cam_msg.msg.SemiAxisLength(value=posConfMajAx),
                                    semi_minor_confidence=cam_msg.msg.SemiAxisLength(value=posConfMinAx), 
                                    semi_major_orientation=cam_msg.msg.HeadingValue(value=posConfElOr)),
                                altitude=cam_msg.msg.Altitude(
                                    altitude_value=cam_msg.msg.AltitudeValue(value=alt), 
                                    altitude_confidence=cam_msg.msg.AltitudeConfidence(value=altConf)))), 
                        high_frequency_container=cam_msg.msg.HighFrequencyContainer(choice=0, 
                            basic_vehicle_container_high_frequency=cam_msg.msg.BasicVehicleContainerHighFrequency(
                                heading=cam_msg.msg.Heading(
                                    heading_value=cam_msg.msg.HeadingValue(value=heading_val),
                                    heading_confidence=cam_msg.msg.HeadingConfidence(value=heading_conf)), 
                                speed=cam_msg.msg.Speed(
                                    speed_value=cam_msg.msg.SpeedValue(value=speed_val),
                                    speed_confidence=cam_msg.msg.SpeedConfidence(value=speed_conf)), 
                                drive_direction=cam_msg.msg.DriveDirection(value=drive_dir), 
                                vehicle_length=cam_msg.msg.VehicleLength(
                                    vehicle_length_value=cam_msg.msg.VehicleLengthValue(value=len), 
                                    vehicle_length_confidence_indication=cam_msg.msg.VehicleLengthConfidenceIndication(value=veh_lenConf)), 
                                    vehicle_width=cam_msg.msg.VehicleWidth(value=wid), 
                                longitudinal_acceleration=cam_msg.msg.LongitudinalAcceleration(
                                    longitudinal_acceleration_value=cam_msg.msg.LongitudinalAccelerationValue(value=lngAcc_val),
                                    longitudinal_acceleration_confidence=cam_msg.msg.AccelerationConfidence(value=lngAcc_conf)),
                                curvature=cam_msg.msg.Curvature(
                                    curvature_value=cam_msg.msg.CurvatureValue(value=curVal_val),
                                    curvature_confidence=cam_msg.msg.CurvatureConfidence(value=curVal_conf)), 
                                curvature_calculation_mode=cam_msg.msg.CurvatureCalculationMode(value=curVal_calcMode), 
                                yaw_rate=cam_msg.msg.YawRate(
                                    yaw_rate_value=cam_msg.msg.YawRateValue(value=yawRate_val),
                                    yaw_rate_confidence=cam_msg.msg.YawRateConfidence(value=yawRate_conf)), 
                                acceleration_control=cam_msg.msg.AccelerationControl(value=[accControl], bits_unused=0),
                                acceleration_control_is_present=accControl_present, 
                                lane_position=cam_msg.msg.LanePosition(value=laneNum),
                                lane_position_is_present=laneNum_present,
                                steering_wheel_angle=cam_msg.msg.SteeringWheelAngle(
                                    steering_wheel_angle_value=cam_msg.msg.SteeringWheelAngleValue(value=steerWhAngle_val), 
                                    steering_wheel_angle_confidence=cam_msg.msg.SteeringWheelAngleConfidence(value=steerWhAngle_conf)),
                                steering_wheel_angle_is_present=steerWhAngl_present, 
                                lateral_acceleration=cam_msg.msg.LateralAcceleration(
                                    lateral_acceleration_value=cam_msg.msg.LateralAccelerationValue(value=latAcc_val),
                                    lateral_acceleration_confidence=cam_msg.msg.AccelerationConfidence(value=latAcc_conf)),
                                lateral_acceleration_is_present=latAcc_present,
                                vertical_acceleration=cam_msg.msg.VerticalAcceleration(
                                    vertical_acceleration_value=cam_msg.msg.VerticalAccelerationValue(value=vertAcc_val), 
                                    vertical_acceleration_confidence=cam_msg.msg.AccelerationConfidence(value=vertAcc_conf)), 
                                vertical_acceleration_is_present=vertAcc_present, 
                                performance_class=cam_msg.msg.PerformanceClass(value=perfClass), 
                                performance_class_is_present=perfClass_present, 
                                cen_dsrc_tolling_zone=cam_msg.msg.CenDsrcTollingZone(
                                    protected_zone_latitude=cam_msg.msg.Latitude(value=cenDsrcZone_lat),
                                    protected_zone_longitude=cam_msg.msg.Longitude(value=cenDsrcZone_lng),
                                    cen_dsrc_tolling_zone_id=cam_msg.msg.CenDsrcTollingZoneID(value=cam_msg.msg.ProtectedZoneID(value=prot_zone_id)), 
                                cen_dsrc_tolling_zone_id_is_present=False),
                                cen_dsrc_tolling_zone_is_present=False)), 
                        low_frequency_container=cam_msg.msg.LowFrequencyContainer(choice=0,
                            basic_vehicle_container_low_frequency=cam_msg.msg.BasicVehicleContainerLowFrequency(
                                vehicle_role=cam_msg.msg.VehicleRole(value=veh_role),
                                exterior_lights=cam_msg.msg.ExteriorLights(value=[extLight], bits_unused=0))), 
                            low_frequency_container_is_present=False)))
