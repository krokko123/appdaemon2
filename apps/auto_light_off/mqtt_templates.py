import json
import copy
import functools
import templates as t

# if __name__ == "__main__":
    # print(json.dumps(T_NUMBER))

class mqtt_templates():
    def __init__(self,hass_object):
        self.hass_object = hass_object
        # print(self.hass_object)

    @staticmethod
    def prepare_params(template=None,
                       data=None,
                       obj=None):
        cpy_template = copy.deepcopy(template.get('params', {}))

        res_params = {}

        for key, param in cpy_template.items():
            # if param in data:
            res_params[key] = data[param] if param in data else "Empty"
            # else:
            #     obj.log(f"No {param} in data dictionary for Mqtt payload",level="WARNING")
        return res_params
    @staticmethod
    def send_mqtt(self,data):
        self.hass_object.mqtt.mqqt_publish()
    def prepare_mqtt_payload(template):

        def prepare_mqtt_payload_wrapper(func):

            def wrapper(*args, **kwargs):
                # print(f"ARGS={args},KWARGS={kwargs}")

                # print(func(*args))
                dataa_cpy = func(*args)

                cpy_template = copy.deepcopy(template)
                res_params = mqtt_templates.prepare_params(template=cpy_template,
                                                           data=dataa_cpy,
                                                           obj=args[0].hass_object)
                mqtt_data = dict()
                mqtt_data['topic'] = cpy_template.get('topic').format(**dataa_cpy)
                template_data = cpy_template.get('data')
                print(res_params)

                formatted_data = dict()
                # # print(json.dumps(template,indent=4),json.dumps(template_data,indent=4))
                # print(template_data)
                for key, param in template_data.items():
                    # pass
                #     # print (param.format(**data))
                #     # print(dataa_cpy[param])
                    if isinstance(template_data[key], str):
                        formatted_data[key] = param.format(**res_params)
                    elif isinstance(template_data[key], dict):
                        print("sssssssssssssssssssssS",dataa_cpy[key])
                        # formatted_data[key] = dataa_cpy[key]
                #     # if key == 'unique_id':
                #             # print (dataa_cpy[key],key, param)
                            #if key in dataa_cpy:
                            #print('freferref')

                    # print(dataa_cpy,key,param)
                # print(json.dumps(template,indent=4))
                # print(json.dumps(dataa,indent=4))
                # print(data)
                # print(json.dumps(template_data,indent=4))
                # print(json.dumps(template_topic,indent=4))
                mqtt_data['data'] = formatted_data
                print(json.dumps(mqtt_data,indent=4))

            return wrapper

        return prepare_mqtt_payload_wrapper

            # template["topic"] = template.get("topic").format(**data)
            #
            # env_data = T_NUMBER.get("data", {})
            # for key,env in env_data.items():
            #     env_data[key] = env.format(**data)
            #
            # T_NUMBER["data"]["dev"] = dev
            #
            # print(T_NUMBER['topic'])
            # print(json.dumps(T_NUMBER['data'],indent=5))

    @prepare_mqtt_payload(template=t.T_SENSOR)
    def register_mqtt_sensors(self, data):
        # print(data)
        # print(obj)

        # data = {}
        # data['ent_id'] = "jakis_szalter"
        # data['unique_id'] = "jakisefefe_szalter"
        # data['ent_topic'] = "egrgeegrgernt_topic"
        # data['friendly_name'] = "friendly_name"
        # data['app_name'] = "kirigistan"
        # data['st_topic'] = f"{data['app_name']}/{data['ent_id']}"
        # data['dev'] = {"Appname":"SuchyStefan"}
        # print(data)
        return data

    @prepare_mqtt_payload(template=t.T_SWITCH)
    def register_mqtt_switches(self, data):
        # print(data)
        # print(obj)

        # data = {}
        # data['ent_id'] = "jakis_szalter"
        # data['unique_id'] = "jakisefefe_szalter"
        # data['ent_topic'] = "egrgeegrgernt_topic"
        # data['friendly_name'] = "friendly_name"
        # data['app_name'] = "kirigistan"
        # data['st_topic'] = f"{data['app_name']}/{data['ent_id']}"
        # data['dev'] = {"Appname":"SuchyStefan"}
        # print(data)
        return data

    # mqtt.mqtt_publish(topic="tt", payload="ww")

    #print(blebleble())

    #prepare_mqtt_payload(template=T_NUMBER)


mqt = mqtt_templates('yyy')
print(type(mqt))

mqt.register_mqtt_switches({'app_name':"eddede","ent_id":"werfwefr"})
