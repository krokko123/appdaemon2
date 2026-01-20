dev = {
    "ergerg":"ergerger",
    "kykykytktk":"hrthrthrthrthrt",
     "eswrggewrerg": ["wef","efgewfwef"]
}
data = {
    "ent_id" : "entuddd",
    "topic" : "topiczek",
    "friendly_name_of_entity" : "friendlik"

}
T_NUMBER = {
    "topic": "homeassistant/number/{app_name}/{ent_id}/config",
    "params":{
      "app_name":"app_name",
      "ent_id":"ent_id",
      "unique_id":"unique_id",
      "st_topic":"st_topic",
      "friendly_name_of_entity": "friendly_name",
      "dev":"dev"
    },
    "data": {
         "command_topic": "{st_topic}",
         "state_topic": "{st_topic}/set",
         "availability_topic": "{st_topic}/av",
         "unique_id": "{unique_id}",
         "name": "{friendly_name_of_entity}",
         "mode": "slider",
         "dev": {}
    }
}

T_SENSOR = {
    "topic":"homeassistant/sensor/{app_name}/{ent_id}/config",
    "params":{
        "app_name": "app_name",
        "ent_id": "ent_id",
        "unique_id": "unique_id",
        "st_topic": "st_topic",
        "friendly_name_of_entity": "friendly_name_of_entity",
        "fwewefefwfwe" : "fwewefefwfwe",
        "states":"states",
        "dev":"dev"
     },
    "data":{
        "command_topic": "{st_topic}",
        "state_topic": "{st_topic}/set",
        "availability_topic": "{st_topic}/av",
        "unique_id": "{ent_id}",
        "name":"{friendly_name_of_entity}",
        "dewewdwe": "{fwewefefwfwe}",
        "states" : "{states}",
        "dev":{}
    }
}
T_SWITCH = {
    "topic":"homeassistant/switch/{app_name}/{ent_id}/config",
    "params":{
        "app_name": "app_name",
        "ent_id": "ent_id",
        "unique_id": "unique_id",
        "st_topic": "st_topic",
        "friendly_name_of_entity": "friendly_name",
        "dev":"dev"
     },
    "data":{
         "command_topic": "{st_topic}",
         "state_topic": "{st_topic}/set",
         "availability_topic": "{st_topic}/av",
         "mode": "box",
         "unique_id": "{ent_id}",
         "name": "{friendly_name_of_entity}",
         "friendly_name": "2137",
        "dev":{}
    }
}