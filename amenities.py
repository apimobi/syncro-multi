from aaaApi import AaaApi
import math
import json

class Amenities(object):
    """Amenities entity"""
    api = None
    rooms = []
    amenities = [
        {
            "amenity_type_id": "9",
            "amenity_type_name": "Common Areas",
            "amenities": [
                {
                    "name": "TV",
                    "id": "1", 
                    "sb": 57
                },
                {
                    "name": "VCR",
                    "id": "2"
                },
                {
                    "name": "DVD",
                    "id": "3",
                    "sb": 59
                },
                {
                    "name": "Cable",
                    "id": "4",
                    "sb":58
                },
                {
                    "name": "Satellite",
                    "id": "5"
                },
                {
                    "name": "Stereo",
                    "id": "10",
                    "sb":60
                },
                {
                    "name": "Ceiling Fans",
                    "id": "12",
                    "sb":40
                },
                {
                    "name": "Home Gym",
                    "id": "54",
                    "sb": 28
                },
                {
                    "name": "Home Cinema",
                    "id": "66"
                },
                {
                    "name": "Piano",
                    "id": "67"
                },
                {
                    "name": "Elevator",
                    "id": "78",
                    "sb": 87
                },
                {
                    "name": "Fireplace",
                    "id": "89",
                    "sb":56
                },
                {
                    "name": "Music Library",
                    "id": "92",
                    "sb":77
                },
                {
                    "name": "Video Library",
                    "id": "93",
                    "sb":78
                },
                {
                    "name": "Ipod Docking Station",
                    "id": "108"
                },
                {
                    "name": "Air-conditioning",
                    "id": "124",
                    "sb": 39
                }
            ]
        },
        {
            "amenity_type_id": "10",
            "amenity_type_name": "Kitchen",
            "amenities": [
                {
                    "name": "Blender",
                    "id": "17"
                },
                {
                    "name": "Coffeemaker",
                    "id": "18",
                    "sb": 9
                },
                {
                    "name": "Microwave",
                    "id": "19",
                    "sb": 4
                },
                {
                    "name": "Dishwasher",
                    "id": "20",
                    "sb" : 5
                },
                {
                    "name": "Ice Maker",
                    "id": "21",
                    "sb" : 15
                },
                {
                    "name": "Toaster",
                    "id": "30",
                    "sb" : 13
                },
                {
                    "name": "Espresso Machine",
                    "id": "41",
                    "sb" : 84
                },
                {
                    "name": "Oven",
                    "id": "44",
                    "sb":8
                },
                {
                    "name": "Stove",
                    "id": "45",
                    "sb":76
                },
                {
                    "name": "Refrigerator",
                    "id": "46",
                    "sb":10
                },
                {
                    "name": "Freezer",
                    "id": "47",
                    "sb":11
                },
                {
                    "name": "Kettle",
                    "id": "48",
                    "sb":14
                },
                {
                    "name": "Juicer",
                    "id": "73",
                    "sb":17
                }
            ]
        },
        {
            "amenity_type_id": "12",
            "amenity_type_name": "Office",
            "amenities": [
                {
                    "name": "Telephone",
                    "id": "6",
                    "sb":55
                },
                {
                    "name": "Computer",
                    "id": "7"
                },
                {
                    "name": "FAX",
                    "id": "8"
                },
                {
                    "name": "Answering Machine",
                    "id": "9"
                },
                {
                    "name": "Cell Phone",
                    "id": "53"
                },
                {
                    "name": "Printer",
                    "id": "112"
                }
            ]
        },
        {
            "amenity_type_id": "13",
            "amenity_type_name": "Bathrooms",
            "amenities": [
                {
                    "name": "Hair Dryer",
                    "id": "22",
                    "sb":21
                },
                {
                    "name": "Bath Tub",
                    "id": "23",
                    "sb": 80
                },
                {
                    "name": "Shower",
                    "id": "28",
                    "sb":66
                },
                {
                    "name": "Jacuzzi Tub",
                    "id": "68"
                },
                {
                    "name": "Steam Room",
                    "id": "110"
                }
            ]
        },
        {
            "amenity_type_id": "14",
            "amenity_type_name": "Patio/Pool Area",
            "amenities": [
                {
                    "name": "BBQ",
                    "id": "16",
                    "sb":86
                },
                {
                    "name": "Pool Toys",
                    "id": "24"
                },
                {
                    "name": "Beach Chairs",
                    "id": "26",
                    "sb" : 68
                },
                {
                    "name": "Pool - Heated ",
                    "id": "63"
                },
                {
                    "name": "Hot Tub",
                    "id": "64"
                },
                {
                    "name": "Jacuzzi",
                    "id": "65"
                },
                {
                    "name": "Pool",
                    "id": "70",
                    "sb":1
                },
                {
                    "name": "Pool - Plunge ",
                    "id": "71"
                },
                {
                    "name": "Pool - Children's",
                    "id": "72"
                },
                {
                    "name": "Pool - Indoor ",
                    "id": "75",
                    "sb":23
                },
                {
                    "name": "Shower - Outdoor ",
                    "id": "76",
                    "sb":34
                },
                {
                    "name": "Pool - Child Friendly ",
                    "id": "95"
                },
                {
                    "name": "Pool - Non Chlorinated/Salt water",
                    "id": "97"
                },
                {
                    "name": "Pool - Infinity ",
                    "id": "100"
                },
                {
                    "name": "Firepit",
                    "id": "101"
                },
                {
                    "name": "Stereo - Outdoor ",
                    "id": "106",
                    "sb":60
                },
                {
                    "name": "Fireplace - Outdoor ",
                    "id": "107",
                    "sb":56
                },
                {
                    "name": "Outdoor/Summer Kitchen",
                    "id": "109"
                },
                {
                    "name": "Pool Fence",
                    "id": "118"
                }
            ]
        },
        {
            "amenity_type_id": "15",
            "amenity_type_name": "Laundry Room",
            "amenities": [
                {
                    "name": "Washer",
                    "id": "13",
                    "sb":16
                },
                {
                    "name": "Dryer",
                    "id": "14",
                    "sb": 18
                },
                {
                    "name": "Iron",
                    "id": "29",
                    "sb": 20
                },
                {
                    "name": "Ironing Board",
                    "id": "69",
                    "sb": 19
                }
            ]
        },
        {
            "amenity_type_id": "16",
            "amenity_type_name": "Bedrooms",
            "amenities": [
                {
                    "name": "Safe",
                    "id": "15"
                },
                {
                    "name": "Alarm ",
                    "id": "42",
                    "sb":50
                },
                {
                    "name": "Mini Fridge",
                    "id": "43"
                },
                {
                    "name": "Air-conditioning",
                    "id": "49",
                    "sb":39
                },
                {
                    "name": "Ceiling Fans",
                    "id": "52",
                    "sb":40
                },
                {
                    "name": "Mosquito Nets",
                    "id": "77",
                    "sb":36
                },
                {
                    "name": "Fireplace",
                    "id": "116",
                    "sb":56
                },
                {
                    "name": "Air-conditioning (Master Bedroom)",
                    "id": "119"
                },
                {
                    "name": "Steam Room",
                    "id": "123"
                }
            ]
        },
        {
            "amenity_type_id": "17",
            "amenity_type_name": "Theme",
            "amenities": [
                {
                    "name": "Views",
                    "id": "32"
                },
                {
                    "name": "Beach Access",
                    "id": "33"
                },
                {
                    "name": "Honeymoon",
                    "id": "34"
                },
                {
                    "name": "Corporate",
                    "id": "35"
                },
                {
                    "name": "Ultra Luxury",
                    "id": "37"
                },
                {
                    "name": "Ski In/Ski Out",
                    "id": "38"
                },
                {
                    "name": "Holiday",
                    "id": "39"
                },
                {
                    "name": "Newsletter",
                    "id": "40"
                }
            ]
        },
        {
            "amenity_type_id": "19",
            "amenity_type_name": "Community",
            "amenities": [
                {
                    "name": "Pool - Indoor ",
                    "id": "36"
                },
                {
                    "name": "Gym",
                    "id": "61"
                },
                {
                    "name": "Pool - Heated ",
                    "id": "62"
                },
                {
                    "name": "Pool",
                    "id": "96"
                },
                {
                    "name": "Gated Community",
                    "id": "104"
                },
                {
                    "name": "Jacuzzi",
                    "id": "115"
                },
                {
                    "name": "Tennis Court",
                    "id": "117"
                }
            ]
        },
        {
            "amenity_type_id": "21",
            "amenity_type_name": "Baby Equipment",
            "amenities": [
                {
                    "name": "High Chair",
                    "id": "80",
                    "sb": 42
                },
                {
                    "name": "PackNPlay",
                    "id": "81"
                },
                {
                    "name": "Baby Bed",
                    "id": "82",
                    "sb":43
                }
            ]
        },
        {
            "amenity_type_id": "22",
            "amenity_type_name": "General Information",
            "amenities": [
                {
                    "name": "Workout Equipment",
                    "id": "11"
                },
                {
                    "name": "Tennis Court",
                    "id": "25",
                    "sb":32
                },
                {
                    "name": "Air Conditioning",
                    "id": "50"
                },
                {
                    "name": "Air Conditioning (Central )",
                    "id": "57"
                },
                {
                    "name": "Herb Garden",
                    "id": "74",
                    "sb":75
                },
                {
                    "name": "WiFi",
                    "id": "79",
                    "sb": 74
                },
                {
                    "name": "Handicap Accessible",
                    "id": "83"
                },
                {
                    "name": "Pets Allowed",
                    "id": "84",
                    "sb":46
                },
                {
                    "name": "Window Screens",
                    "id": "85"
                },
                {
                    "name": "Smoking - Indoors",
                    "id": "86",
                    "sb":47
                },
                {
                    "name": "Smoking - Outdoors",
                    "id": "87"
                },
                {
                    "name": "Children Accepted",
                    "id": "88",
                    "sb":48
                },
                {
                    "name": "Massage Room",
                    "id": "91",
                    "sb":69
                },
                {
                    "name": "Water Purification System",
                    "id": "103"
                },
                {
                    "name": "Gated Property",
                    "id": "105"
                },
                {
                    "name": "Steam Room",
                    "id": "111"
                },
                {
                    "name": "Smoking - Designated Areas",
                    "id": "113"
                },
                {
                    "name": "Jacuzzi",
                    "id": "114"
                }
            ]
        },
        {
            "amenity_type_id": "23",
            "amenity_type_name": "Parking",
            "amenities": [
                {
                    "name": "Parking  - Covered",
                    "id": "55"
                },
                {
                    "name": "Parking - Off Street",
                    "id": "56"
                },
                {
                    "name": "Garage",
                    "id": "102"
                },
                {
                    "name": "Parking - Street",
                    "id": "122"
                },
                {
                    "name": "Parking Garage",
                    "id": "126",
                    "sb": 72
                }
            ]
        }
    ]

    roomsId = {
        "9"  : 2,
        "10" : 1,
        "13" : 12,
        "12" : 16,
        "14" : 239,
        "15" : 13,
        "16" : 5,
        "23" : 245,
        "22" : 246,
        "21" : 3,
    }

    medias = []

    def __init__(self, data, api, propertyId, medias, logger):
        self.api = api
        self.logger = logger
        self.medias.clear()
        self.medias = medias
        self.rooms.clear()
        self.rooms = []

        try :
            self.createPropertyRooms(data, propertyId)
        except Exception as e:
            self.logger.error(e, exc_info=True)
        
    def createPropertyRooms(self, data, propertyId):
        print(data['amenities'])
        needKitchen = True
        
        print('>>>>>> propertyId '+str(propertyId))
        for amenity in data['amenities']:
            if amenity["amenity_type_id"] == "10":
                needKitchen = False
            if amenity["amenity_type_id"] in self.roomsId and amenity["amenity_type_id"] != "16" :
                room = self.createRoom(propertyId, amenity, amenity["amenity_type_id"])
                if amenity["amenity_type_id"] == "13" :
                    for index in range(int(data['bathrooms'])):
                        self.rooms.append(room)
                else :
                    self.rooms.append(room)
                    
        if needKitchen:
            self.rooms.append(self.createKitchen(propertyId))
        
        # bedrooms around 3 beds per room
        for index in range(math.ceil((int(data['max_occupancy'])/3))):
            self.rooms.append(self.createBedroom(propertyId))

        for room in self.rooms:
            self.api.callRequest("/properties/property-room", json.dumps(room))
        
        
    def createBedroom(self, propertyId):
        return {
            "property" : propertyId,
            "room" : 5
        }

        
    def createKitchen(self, propertyId):
        return {
            "property" : propertyId,
            "room" : 1,
            "propertyMedia" : self.medias
        }
        
    def createRoom(self, propertyId, data, id):

        propertyAmenityRoom = []
        amenities = self.getAmenityGroup(id)
        
        for amenity in data['amenities']:
            for ame in amenities["amenities"] :
                if ame['id'] == amenity['id'] and 'sb' in ame:
                     propertyAmenityRoom.append({
                         "amenity" : ame['sb']
                     })

        propertyMedias = []
        if id == "10":
            propertyMedias = self.medias

        return {
            "property" : propertyId,
            "room" : self.roomsId[id],
            "propertyAmenityRoom" : propertyAmenityRoom,
            "propertyMedia" : propertyMedias
        }

    def getAmenityGroup(self, id):
        for ame in self.amenities :
            if ame['amenity_type_id'] == id:
                return ame
        
        return None         
