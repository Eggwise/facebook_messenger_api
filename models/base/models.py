##############          Eggwise       ##############
############## GENERATED MODELS START ##############

import copy



class FactoryBase():

    @staticmethod
    def __get_super_args(locals):
        super_args = {}

        for k, v in locals.items():
            if k.startswith('__'):
                continue
            if k == 'self':
                continue
            super_args[k] = v
        return super_args

    def __init__(self, schema, config, child_locals = None):

        self.__dict__['config'] = config
        self.__dict__['schema'] = schema

        if 'mapping' not in config:
            raise Exception('no mapping defined for {0}'.format(self))
        self._setup_mapping(config, schema)

        if child_locals is not None:
            for key, val in child_locals.items():
                if key.startswith('_') or key == 'self':
                    continue
                if val is None:
                    continue
                self.__setattr__(key, val)


    def _setup_mapping(self, config, schema):
        #build bindings
        mapping_config = config['mapping']
        mapping = mapping_config
        if '_include' in mapping_config:
            include_config = mapping_config['_include']
            del(mapping['_include'])

            included_keys = []
            if include_config == 'all':

                schema_type_config = schema['type']
                if schema_type_config == 'object':
                    included_keys = schema['value'].keys()
                else:
                    included_keys = [schema['name']]

            elif isinstance(include_config, list):
                included_keys = include_config

            for i in included_keys:
                mapping[i] = i

        self.__dict__['mapping'] = mapping

    @property
    def _enums(self):
        enums = {}
        for k, path in self.mapping.items():

            attr_config = self._get_by_path(path, self.schema)

            if attr_config['type'] == 'enum':
                attr_enums = attr_config['enum']
                enums[k] = attr_enums

        return enums
    @property
    def _attributes(self):
        return self.mapping.keys()

    @staticmethod
    def _get_by_path(path, schema):
        path_split = path.split('.')
        scoped_object = schema
        for i in path_split:
            assert schema['type'] == 'object'
            try:
                scoped_object = scoped_object['value'][i]
            except KeyError as e:
                print('COuld not find key {0} in {1}'.format(e, scoped_object))
                raise

        return scoped_object

    @staticmethod
    def _set_by_path(path, schema, val):
        path_split = path.split('.')
        scoped_object = schema
        for i in path_split:
            assert schema['type'] == 'object'
            scoped_object = scoped_object['value'][i]
        type_config = scoped_object['type']

        if type_config == 'enum':
            valid_values = scoped_object['enum']
            if val not in valid_values:
                raise AttributeError('invalid value, must be one of {0}'.format(valid_values))
            type_config = 'str'

        elif type_config == 'object':
            type_config = 'dict'
        elif type_config == 'string':
            type_config = 'str'

        value_type = type(val).__name__
        if type_config != value_type:
            err_msg = 'invalid type for {0}, was: {1}, must be {2}'.format(val, value_type, type_config)
            raise AttributeError(err_msg)

        scoped_object['value'] = val
        return scoped_object

    def __getattr__(self, item):
        if item == '__get_super_args':
            return self.__get_super_args
        mapping = self.mapping
        if item not in mapping :
            err_msg = '{0} > No mapping to schema defined for: {1}\nAvailable bindings:\n {2}'.format(self, item,
                                                                                                      mapping)
            raise AttributeError(err_msg)
        path = mapping[item]
        proxy_val = self._get_by_path(path, self.schema)
        return_val = proxy_val['value']
        return return_val



    def __setattr__(self, key, value):
        mapping = self.mapping
        if key not in mapping:
            err_msg = '{0} > No mappint to schema defined for: {1}\nAvailable bindings:\n {2}'.format(self, key, mapping)
            raise AttributeError(err_msg)
        path = mapping[key]
        self._set_by_path(path, self.schema, value)

    @classmethod
    def _build(cls, schema):

        if isinstance(schema, FactoryBase):
            return schema.build()

        if isinstance(schema, list):

            return [cls._build(i) for i in schema]

        if not isinstance(schema, dict):
            return schema

        tree = {

        }
        if 'type' in schema:
            if schema['type'] == 'object':
                schema = schema['value']

        for k, v in schema.items():
            value = v['value']
            if value is None:
                continue

            # if v['type'] == 'object':
            value = cls._build(value)

            if value is None:
                continue

            if len(value) == 0:
                continue

            tree[k] = value

        if len(tree) == 0:
            return None
        return tree

    def build(self):
        return self._build(self.schema)

class ActionMessageBase (FactoryBase):

    SCHEMA =  {'quickreply': {'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum', 'value': None}, 'message': {'name': 'message', 'enum': None, 'type': 'object', 'value': {'text': {'name': 'text', 'enum': None, 'type': 'string', 'value': None}, 'quick_replies': {'name': 'quick_replies', 'enum': None, 'type': 'list', 'value': []}}}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum', 'value': None}, 'recipient': {'name': 'recipient', 'enum': None, 'type': 'object', 'value': {'phone_number': {'name': 'phone_number', 'enum': None, 'type': 'string', 'value': None}, 'id': {'name': 'id', 'enum': None, 'type': 'string', 'value': None}}}}, 'type': 'object'}, 'list_template': {'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum', 'value': None}, 'message': {'name': 'message', 'enum': None, 'type': 'object', 'value': {'attachment': {'name': 'attachment', 'enum': None, 'type': 'object', 'value': {'type': {'name': 'type', 'enum': None, 'type': 'string', 'value': 'template'}, 'payload': {'name': 'payload', 'enum': None, 'type': 'object', 'value': {'template_type': {'name': 'template_type', 'enum': None, 'type': 'string', 'value': 'list'}, 'elements': {'name': 'elements', 'enum': None, 'type': 'list', 'value': []}}}}}}}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum', 'value': None}, 'recipient': {'name': 'recipient', 'enum': None, 'type': 'object', 'value': {'phone_number': {'name': 'phone_number', 'enum': None, 'type': 'string', 'value': None}, 'id': {'name': 'id', 'enum': None, 'type': 'string', 'value': None}}}}, 'type': 'object'}, 'generic_template': {'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum', 'value': None}, 'message': {'name': 'message', 'enum': None, 'type': 'object', 'value': {'attachment': {'name': 'attachment', 'enum': None, 'type': 'object', 'value': {'type': {'name': 'type', 'enum': None, 'type': 'string', 'value': 'template'}, 'payload': {'name': 'payload', 'enum': None, 'type': 'object', 'value': {'template_type': {'name': 'template_type', 'enum': None, 'type': 'string', 'value': 'generic'}, 'elements': {'name': 'elements', 'enum': None, 'type': 'list', 'value': []}}}}}}}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum', 'value': None}, 'recipient': {'name': 'recipient', 'enum': None, 'type': 'object', 'value': {'phone_number': {'name': 'phone_number', 'enum': None, 'type': 'string', 'value': None}, 'id': {'name': 'id', 'enum': None, 'type': 'string', 'value': None}}}}, 'type': 'object'}, 'type': 'object', 'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum', 'value': None}, 'message': {'name': 'message', 'enum': None, 'type': 'object', 'value': {'text': {'name': 'text', 'enum': None, 'type': 'string', 'value': None}, 'attachment': {'name': 'attachment', 'enum': None, 'type': 'object', 'value': None}}}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum', 'value': None}, 'recipient': {'name': 'recipient', 'enum': None, 'type': 'object', 'value': {'phone_number': {'name': 'phone_number', 'enum': None, 'type': 'string', 'value': None}, 'id': {'name': 'id', 'enum': None, 'type': 'string', 'value': None}}}}}
    CONFIG = {'mapping': {'action': 'sender_action', 'recipient': 'recipient.id'}, 'schema': 'message', 'class_name': 'ActionMessage'}

    def __init__(self,  action = None,  recipient = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def action(self):
        return self.__getattr__('action')

    @action.setter
    def action(self, value):
        self.__setattr__('action', value)
    
    @property
    def recipient(self):
        return self.__getattr__('action')

    @recipient.setter
    def recipient(self, value):
        self.__setattr__('recipient', value)
    

    class ACTION:
        TYPING_ON = 'typing_on'
        TYPING_OFF = 'typing_off'
        MARK_SEEN = 'mark_seen'
class GenericElementBase (FactoryBase):

    SCHEMA =  {'value': {'image_url': {'name': 'image_url', 'enum': None, 'type': 'string', 'value': None}, 'default_action': {'name': 'default_action', 'enum': None, 'type': 'string', 'value': None}, 'subtitle': {'name': 'subtitle', 'enum': None, 'type': 'string', 'value': None}, 'item_url': {'name': 'item_url', 'enum': None, 'type': 'string', 'value': None}, 'title': {'name': 'title', 'enum': None, 'type': 'string', 'value': None}, 'buttons': {'name': 'buttons', 'enum': None, 'type': 'list', 'value': []}}, 'type': 'object'}
    CONFIG = {'mapping': {'image_url': 'image_url', 'default_action': 'default_action', 'subtitle': 'subtitle', 'item_url': 'item_url', 'title': 'title', 'buttons': 'buttons'}, 'schema': 'generic.element', 'class_name': 'GenericElement'}

    def __init__(self,  image_url = None,  default_action = None,  subtitle = None,  item_url = None,  title = None,  buttons = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def image_url(self):
        return self.__getattr__('action')

    @image_url.setter
    def image_url(self, value):
        self.__setattr__('image_url', value)
    
    @property
    def default_action(self):
        return self.__getattr__('action')

    @default_action.setter
    def default_action(self, value):
        self.__setattr__('default_action', value)
    
    @property
    def subtitle(self):
        return self.__getattr__('action')

    @subtitle.setter
    def subtitle(self, value):
        self.__setattr__('subtitle', value)
    
    @property
    def item_url(self):
        return self.__getattr__('action')

    @item_url.setter
    def item_url(self, value):
        self.__setattr__('item_url', value)
    
    @property
    def title(self):
        return self.__getattr__('action')

    @title.setter
    def title(self, value):
        self.__setattr__('title', value)
    
    @property
    def buttons(self):
        return self.__getattr__('action')

    @buttons.setter
    def buttons(self, value):
        self.__setattr__('buttons', value)
    

class GenericTemplateBase (FactoryBase):

    SCHEMA =  {'value': {'type': {'name': 'type', 'enum': None, 'type': 'string', 'value': 'template'}, 'payload': {'name': 'payload', 'enum': None, 'type': 'object', 'value': {'template_type': {'name': 'template_type', 'enum': None, 'type': 'string', 'value': 'generic'}, 'elements': {'name': 'elements', 'enum': None, 'type': 'list', 'value': []}}}}, 'type': 'object'}
    CONFIG = {'mapping': {'type': 'type', 'payload': 'payload'}, 'schema': 'generic.template', 'class_name': 'GenericTemplate'}

    def __init__(self,  type = None,  payload = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def type(self):
        return self.__getattr__('action')

    @type.setter
    def type(self, value):
        self.__setattr__('type', value)
    
    @property
    def payload(self):
        return self.__getattr__('action')

    @payload.setter
    def payload(self, value):
        self.__setattr__('payload', value)
    

class GenericTemplateMessageBase (FactoryBase):

    SCHEMA =  {'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum', 'value': None}, 'message': {'name': 'message', 'enum': None, 'type': 'object', 'value': {'attachment': {'name': 'attachment', 'enum': None, 'type': 'object', 'value': {'type': {'name': 'type', 'enum': None, 'type': 'string', 'value': 'template'}, 'payload': {'name': 'payload', 'enum': None, 'type': 'object', 'value': {'template_type': {'name': 'template_type', 'enum': None, 'type': 'string', 'value': 'generic'}, 'elements': {'name': 'elements', 'enum': None, 'type': 'list', 'value': []}}}}}}}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum', 'value': None}, 'recipient': {'name': 'recipient', 'enum': None, 'type': 'object', 'value': {'phone_number': {'name': 'phone_number', 'enum': None, 'type': 'string', 'value': None}, 'id': {'name': 'id', 'enum': None, 'type': 'string', 'value': None}}}}, 'type': 'object'}
    CONFIG = {'mapping': {'elements': 'message.attachment.payload.elements', 'recipient': 'recipient.id'}, 'schema': 'generic_template.message', 'class_name': 'GenericTemplateMessage'}

    def __init__(self,  elements = None,  recipient = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def elements(self):
        return self.__getattr__('action')

    @elements.setter
    def elements(self, value):
        self.__setattr__('elements', value)
    
    @property
    def recipient(self):
        return self.__getattr__('action')

    @recipient.setter
    def recipient(self, value):
        self.__setattr__('recipient', value)
    

class ListElementBase (FactoryBase):

    SCHEMA =  {'value': {'image_url': {'name': 'image_url', 'enum': None, 'type': 'string', 'value': None}, 'default_action': {'name': 'default_action', 'enum': None, 'type': 'string', 'value': None}, 'buttons': {'name': 'buttons', 'enum': None, 'type': 'list', 'value': []}, 'subtitle': {'name': 'subtitle', 'enum': None, 'type': 'string', 'value': None}, 'title': {'name': 'title', 'enum': None, 'type': 'string', 'value': None}}, 'type': 'object'}
    CONFIG = {'mapping': {'image_url': 'image_url', 'default_action': 'default_action', 'subtitle': 'subtitle', 'buttons': 'buttons', 'title': 'title'}, 'schema': 'list.element', 'class_name': 'ListElement'}

    def __init__(self,  image_url = None,  default_action = None,  subtitle = None,  buttons = None,  title = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def image_url(self):
        return self.__getattr__('action')

    @image_url.setter
    def image_url(self, value):
        self.__setattr__('image_url', value)
    
    @property
    def default_action(self):
        return self.__getattr__('action')

    @default_action.setter
    def default_action(self, value):
        self.__setattr__('default_action', value)
    
    @property
    def subtitle(self):
        return self.__getattr__('action')

    @subtitle.setter
    def subtitle(self, value):
        self.__setattr__('subtitle', value)
    
    @property
    def buttons(self):
        return self.__getattr__('action')

    @buttons.setter
    def buttons(self, value):
        self.__setattr__('buttons', value)
    
    @property
    def title(self):
        return self.__getattr__('action')

    @title.setter
    def title(self, value):
        self.__setattr__('title', value)
    

class ListTemplateBase (FactoryBase):

    SCHEMA =  {'value': {'type': {'name': 'type', 'enum': None, 'type': 'string', 'value': 'template'}, 'payload': {'name': 'payload', 'enum': None, 'type': 'object', 'value': {'template_type': {'name': 'template_type', 'enum': None, 'type': 'string', 'value': 'list'}, 'elements': {'name': 'elements', 'enum': None, 'type': 'list', 'value': []}}}}, 'type': 'object'}
    CONFIG = {'mapping': {'type': 'type', 'payload': 'payload'}, 'schema': 'list.template', 'class_name': 'ListTemplate'}

    def __init__(self,  type = None,  payload = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def type(self):
        return self.__getattr__('action')

    @type.setter
    def type(self, value):
        self.__setattr__('type', value)
    
    @property
    def payload(self):
        return self.__getattr__('action')

    @payload.setter
    def payload(self, value):
        self.__setattr__('payload', value)
    

class ListTemplateMessageBase (FactoryBase):

    SCHEMA =  {'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum', 'value': None}, 'message': {'name': 'message', 'enum': None, 'type': 'object', 'value': {'attachment': {'name': 'attachment', 'enum': None, 'type': 'object', 'value': {'type': {'name': 'type', 'enum': None, 'type': 'string', 'value': 'template'}, 'payload': {'name': 'payload', 'enum': None, 'type': 'object', 'value': {'template_type': {'name': 'template_type', 'enum': None, 'type': 'string', 'value': 'list'}, 'elements': {'name': 'elements', 'enum': None, 'type': 'list', 'value': []}}}}}}}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum', 'value': None}, 'recipient': {'name': 'recipient', 'enum': None, 'type': 'object', 'value': {'phone_number': {'name': 'phone_number', 'enum': None, 'type': 'string', 'value': None}, 'id': {'name': 'id', 'enum': None, 'type': 'string', 'value': None}}}}, 'type': 'object'}
    CONFIG = {'mapping': {'elements': 'message.attachment.payload.elements', 'recipient': 'recipient.id'}, 'schema': 'list_template.message', 'class_name': 'ListTemplateMessage'}

    def __init__(self,  elements = None,  recipient = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def elements(self):
        return self.__getattr__('action')

    @elements.setter
    def elements(self, value):
        self.__setattr__('elements', value)
    
    @property
    def recipient(self):
        return self.__getattr__('action')

    @recipient.setter
    def recipient(self, value):
        self.__setattr__('recipient', value)
    

class MessageBase (FactoryBase):

    SCHEMA =  {'quickreply': {'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum', 'value': None}, 'message': {'name': 'message', 'enum': None, 'type': 'object', 'value': {'text': {'name': 'text', 'enum': None, 'type': 'string', 'value': None}, 'quick_replies': {'name': 'quick_replies', 'enum': None, 'type': 'list', 'value': []}}}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum', 'value': None}, 'recipient': {'name': 'recipient', 'enum': None, 'type': 'object', 'value': {'phone_number': {'name': 'phone_number', 'enum': None, 'type': 'string', 'value': None}, 'id': {'name': 'id', 'enum': None, 'type': 'string', 'value': None}}}}, 'type': 'object'}, 'list_template': {'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum', 'value': None}, 'message': {'name': 'message', 'enum': None, 'type': 'object', 'value': {'attachment': {'name': 'attachment', 'enum': None, 'type': 'object', 'value': {'type': {'name': 'type', 'enum': None, 'type': 'string', 'value': 'template'}, 'payload': {'name': 'payload', 'enum': None, 'type': 'object', 'value': {'template_type': {'name': 'template_type', 'enum': None, 'type': 'string', 'value': 'list'}, 'elements': {'name': 'elements', 'enum': None, 'type': 'list', 'value': []}}}}}}}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum', 'value': None}, 'recipient': {'name': 'recipient', 'enum': None, 'type': 'object', 'value': {'phone_number': {'name': 'phone_number', 'enum': None, 'type': 'string', 'value': None}, 'id': {'name': 'id', 'enum': None, 'type': 'string', 'value': None}}}}, 'type': 'object'}, 'generic_template': {'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum', 'value': None}, 'message': {'name': 'message', 'enum': None, 'type': 'object', 'value': {'attachment': {'name': 'attachment', 'enum': None, 'type': 'object', 'value': {'type': {'name': 'type', 'enum': None, 'type': 'string', 'value': 'template'}, 'payload': {'name': 'payload', 'enum': None, 'type': 'object', 'value': {'template_type': {'name': 'template_type', 'enum': None, 'type': 'string', 'value': 'generic'}, 'elements': {'name': 'elements', 'enum': None, 'type': 'list', 'value': []}}}}}}}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum', 'value': None}, 'recipient': {'name': 'recipient', 'enum': None, 'type': 'object', 'value': {'phone_number': {'name': 'phone_number', 'enum': None, 'type': 'string', 'value': None}, 'id': {'name': 'id', 'enum': None, 'type': 'string', 'value': None}}}}, 'type': 'object'}, 'type': 'object', 'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum', 'value': None}, 'message': {'name': 'message', 'enum': None, 'type': 'object', 'value': {'text': {'name': 'text', 'enum': None, 'type': 'string', 'value': None}, 'attachment': {'name': 'attachment', 'enum': None, 'type': 'object', 'value': None}}}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum', 'value': None}, 'recipient': {'name': 'recipient', 'enum': None, 'type': 'object', 'value': {'phone_number': {'name': 'phone_number', 'enum': None, 'type': 'string', 'value': None}, 'id': {'name': 'id', 'enum': None, 'type': 'string', 'value': None}}}}}
    CONFIG = {'mapping': {'text': 'message.text', 'action': 'sender_action', 'recipient': 'recipient.id'}, 'schema': 'message', 'class_name': 'Message'}

    def __init__(self,  text = None,  action = None,  recipient = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def text(self):
        return self.__getattr__('action')

    @text.setter
    def text(self, value):
        self.__setattr__('text', value)
    
    @property
    def action(self):
        return self.__getattr__('action')

    @action.setter
    def action(self, value):
        self.__setattr__('action', value)
    
    @property
    def recipient(self):
        return self.__getattr__('action')

    @recipient.setter
    def recipient(self, value):
        self.__setattr__('recipient', value)
    

    class ACTION:
        TYPING_ON = 'typing_on'
        TYPING_OFF = 'typing_off'
        MARK_SEEN = 'mark_seen'
class QuickReplyBase (FactoryBase):

    SCHEMA =  {'location': {'value': {'content_type': {'name': 'content_type', 'enum': None, 'type': 'string', 'value': 'location'}}, 'type': 'object'}, 'value': {'content_type': {'name': 'content_type', 'enum': ['text', 'location'], 'type': 'enum', 'value': None}, 'image_url': {'name': 'image_url', 'enum': None, 'type': 'string', 'value': None}, 'title': {'name': 'title', 'enum': None, 'type': 'string', 'value': None}, 'payload': {'name': 'payload', 'enum': None, 'type': 'string', 'value': None}}, 'type': 'object'}
    CONFIG = {'mapping': {'content_type': 'content_type', 'image_url': 'image_url', 'title': 'title', 'payload': 'payload'}, 'schema': 'quickreply', 'class_name': 'QuickReply'}

    def __init__(self,  content_type = None,  image_url = None,  title = None,  payload = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def content_type(self):
        return self.__getattr__('action')

    @content_type.setter
    def content_type(self, value):
        self.__setattr__('content_type', value)
    
    @property
    def image_url(self):
        return self.__getattr__('action')

    @image_url.setter
    def image_url(self, value):
        self.__setattr__('image_url', value)
    
    @property
    def title(self):
        return self.__getattr__('action')

    @title.setter
    def title(self, value):
        self.__setattr__('title', value)
    
    @property
    def payload(self):
        return self.__getattr__('action')

    @payload.setter
    def payload(self, value):
        self.__setattr__('payload', value)
    

    class CONTENT_TYPE:
        TEXT = 'text'
        LOCATION = 'location'
class QuickReplyMessageBase (FactoryBase):

    SCHEMA =  {'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum', 'value': None}, 'message': {'name': 'message', 'enum': None, 'type': 'object', 'value': {'text': {'name': 'text', 'enum': None, 'type': 'string', 'value': None}, 'quick_replies': {'name': 'quick_replies', 'enum': None, 'type': 'list', 'value': []}}}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum', 'value': None}, 'recipient': {'name': 'recipient', 'enum': None, 'type': 'object', 'value': {'phone_number': {'name': 'phone_number', 'enum': None, 'type': 'string', 'value': None}, 'id': {'name': 'id', 'enum': None, 'type': 'string', 'value': None}}}}, 'type': 'object'}
    CONFIG = {'mapping': {'text': 'message.text', 'quick_replies': 'message.quick_replies', 'recipient': 'recipient.id'}, 'schema': 'quickreply.message', 'class_name': 'QuickReplyMessage'}

    def __init__(self,  text = None,  quick_replies = None,  recipient = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def text(self):
        return self.__getattr__('action')

    @text.setter
    def text(self, value):
        self.__setattr__('text', value)
    
    @property
    def quick_replies(self):
        return self.__getattr__('action')

    @quick_replies.setter
    def quick_replies(self, value):
        self.__setattr__('quick_replies', value)
    
    @property
    def recipient(self):
        return self.__getattr__('action')

    @recipient.setter
    def recipient(self, value):
        self.__setattr__('recipient', value)
    

class CallButtonBase (FactoryBase):

    SCHEMA =  {'value': {'title': {'name': 'title', 'enum': None, 'type': 'string', 'value': None}, 'type': {'name': 'type', 'enum': None, 'type': 'string', 'value': 'phone_number'}, 'payload': {'name': 'payload', 'enum': None, 'type': 'string', 'value': None}}, 'type': 'object'}
    CONFIG = {'mapping': {'title': 'title', 'type': 'type', 'payload': 'payload'}, 'schema': 'call.button', 'class_name': 'CallButton'}

    def __init__(self,  title = None,  type = None,  payload = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def title(self):
        return self.__getattr__('action')

    @title.setter
    def title(self, value):
        self.__setattr__('title', value)
    
    @property
    def type(self):
        return self.__getattr__('action')

    @type.setter
    def type(self, value):
        self.__setattr__('type', value)
    
    @property
    def payload(self):
        return self.__getattr__('action')

    @payload.setter
    def payload(self, value):
        self.__setattr__('payload', value)
    

class PostBackButtonBase (FactoryBase):

    SCHEMA =  {'value': {'title': {'name': 'title', 'enum': None, 'type': 'string', 'value': None}, 'type': {'name': 'type', 'enum': None, 'type': 'string', 'value': 'postback'}, 'payload': {'name': 'payload', 'enum': None, 'type': 'string', 'value': None}}, 'type': 'object'}
    CONFIG = {'mapping': {'title': 'title', 'type': 'type', 'payload': 'payload'}, 'schema': 'postback.button', 'class_name': 'PostBackButton'}

    def __init__(self,  title = None,  type = None,  payload = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def title(self):
        return self.__getattr__('action')

    @title.setter
    def title(self, value):
        self.__setattr__('title', value)
    
    @property
    def type(self):
        return self.__getattr__('action')

    @type.setter
    def type(self, value):
        self.__setattr__('type', value)
    
    @property
    def payload(self):
        return self.__getattr__('action')

    @payload.setter
    def payload(self, value):
        self.__setattr__('payload', value)
    

class ShareButtonBase (FactoryBase):

    SCHEMA =  {'value': {'type': {'name': 'type', 'enum': None, 'type': 'string', 'value': 'element_share'}}, 'type': 'object'}
    CONFIG = {'mapping': {'type': 'type'}, 'schema': 'share.button', 'class_name': 'ShareButton'}

    def __init__(self,  type = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def type(self):
        return self.__getattr__('action')

    @type.setter
    def type(self, value):
        self.__setattr__('type', value)
    

class UrlButtonBase (FactoryBase):

    SCHEMA =  {'value': {'url': {'name': 'url', 'enum': None, 'type': 'string', 'value': None}, 'type': {'name': 'type', 'enum': None, 'type': 'string', 'value': 'web_url'}, 'fallback_url': {'name': 'fallback_url', 'enum': None, 'type': 'string', 'value': None}, 'messenger_extensions': {'name': 'messenger_extensions', 'enum': None, 'type': 'boolean', 'value': None}, 'title': {'name': 'title', 'enum': None, 'type': 'string', 'value': None}, 'webview_height_ratio': {'name': 'webview_height_ratio', 'enum': ['compact', 'tall', 'full'], 'type': 'enum', 'value': None}}, 'type': 'object'}
    CONFIG = {'mapping': {'url': 'url', 'type': 'type', 'fallback_url': 'fallback_url', 'messenger_extensions': 'messenger_extensions', 'title': 'title', 'webview_height_ratio': 'webview_height_ratio'}, 'schema': 'url.button', 'class_name': 'UrlButton'}

    def __init__(self,  url = None,  type = None,  fallback_url = None,  messenger_extensions = None,  title = None,  webview_height_ratio = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def url(self):
        return self.__getattr__('action')

    @url.setter
    def url(self, value):
        self.__setattr__('url', value)
    
    @property
    def type(self):
        return self.__getattr__('action')

    @type.setter
    def type(self, value):
        self.__setattr__('type', value)
    
    @property
    def fallback_url(self):
        return self.__getattr__('action')

    @fallback_url.setter
    def fallback_url(self, value):
        self.__setattr__('fallback_url', value)
    
    @property
    def messenger_extensions(self):
        return self.__getattr__('action')

    @messenger_extensions.setter
    def messenger_extensions(self, value):
        self.__setattr__('messenger_extensions', value)
    
    @property
    def title(self):
        return self.__getattr__('action')

    @title.setter
    def title(self, value):
        self.__setattr__('title', value)
    
    @property
    def webview_height_ratio(self):
        return self.__getattr__('action')

    @webview_height_ratio.setter
    def webview_height_ratio(self, value):
        self.__setattr__('webview_height_ratio', value)
    

    class WEBVIEW_HEIGHT_RATIO:
        COMPACT = 'compact'
        TALL = 'tall'
        FULL = 'full'



##############  GENERATED MODELS END  ##############
##############          Eggwise       ##############