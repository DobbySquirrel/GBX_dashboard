class ServicesProperties:
    def __init__(self):
        self.__services_properties = list()

    def add_service_property(self, service_id, property, value):
        # 查找是否已经存在相同的 service_id
        service = next((item for item in self.__services_properties if item["service_id"] == service_id), None)
        if service:
            # 如果已经存在，则添加新的属性到 properties
            service["properties"][property] = value
        else:
            # 如果不存在，创建一个新的 service_id 结构
            service_property_dict = {"service_id": service_id, "properties": {property: value}}
            self.__services_properties.append(service_property_dict)

    @property
    def service_property(self):
        return self.__services_properties
