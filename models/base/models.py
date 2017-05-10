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

    SCHEMA =  {'generic_template': {'value': {'message': {'value': {'attachment': {'value': {'payload': {'value': {'elements': {'value': [], 'name': 'elements', 'enum': None, 'type': 'list'}, 'template_type': {'value': 'generic', 'name': 'template_type', 'enum': None, 'type': 'string'}}, 'name': 'payload', 'enum': None, 'type': 'object'}, 'type': {'value': 'template', 'name': 'type', 'enum': None, 'type': 'string'}}, 'name': 'attachment', 'enum': None, 'type': 'object'}}, 'name': 'message', 'enum': None, 'type': 'object'}, 'sender_action': {'value': None, 'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}, 'recipient': {'value': {'id': {'value': None, 'name': 'id', 'enum': None, 'type': 'string'}, 'phone_number': {'value': None, 'name': 'phone_number', 'enum': None, 'type': 'string'}}, 'name': 'recipient', 'enum': None, 'type': 'object'}, 'notification_type': {'value': None, 'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}}, 'type': 'object'}, 'list_template': {'value': {'message': {'value': {'attachment': {'value': {'payload': {'value': {'elements': {'value': [], 'name': 'elements', 'enum': None, 'type': 'list'}, 'template_type': {'value': 'list', 'name': 'template_type', 'enum': None, 'type': 'string'}}, 'name': 'payload', 'enum': None, 'type': 'object'}, 'type': {'value': 'template', 'name': 'type', 'enum': None, 'type': 'string'}}, 'name': 'attachment', 'enum': None, 'type': 'object'}}, 'name': 'message', 'enum': None, 'type': 'object'}, 'sender_action': {'value': None, 'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}, 'recipient': {'value': {'id': {'value': None, 'name': 'id', 'enum': None, 'type': 'string'}, 'phone_number': {'value': None, 'name': 'phone_number', 'enum': None, 'type': 'string'}}, 'name': 'recipient', 'enum': None, 'type': 'object'}, 'notification_type': {'value': None, 'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}}, 'type': 'object'}, 'quickreply': {'value': {'message': {'value': {'quick_replies': {'value': [], 'name': 'quick_replies', 'enum': None, 'type': 'list'}, 'text': {'value': None, 'name': 'text', 'enum': None, 'type': 'string'}}, 'name': 'message', 'enum': None, 'type': 'object'}, 'sender_action': {'value': None, 'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}, 'recipient': {'value': {'id': {'value': None, 'name': 'id', 'enum': None, 'type': 'string'}, 'phone_number': {'value': None, 'name': 'phone_number', 'enum': None, 'type': 'string'}}, 'name': 'recipient', 'enum': None, 'type': 'object'}, 'notification_type': {'value': None, 'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}}, 'type': 'object'}, 'type': 'object', 'value': {'message': {'value': {'text': {'value': None, 'name': 'text', 'enum': None, 'type': 'string'}, 'attachment': {'value': None, 'name': 'attachment', 'enum': None, 'type': 'object'}}, 'name': 'message', 'enum': None, 'type': 'object'}, 'sender_action': {'value': None, 'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}, 'recipient': {'value': {'id': {'value': None, 'name': 'id', 'enum': None, 'type': 'string'}, 'phone_number': {'value': None, 'name': 'phone_number', 'enum': None, 'type': 'string'}}, 'name': 'recipient', 'enum': None, 'type': 'object'}, 'notification_type': {'value': None, 'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}}}
    CONFIG = {'class_name': 'ActionMessage', 'mapping': {'recipient': 'recipient.id', 'action': 'sender_action'}, 'schema': 'message'}

    def __init__(self,  recipient = None,  action = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def recipient(self):
        return self.__getattr__('recipient')

    @recipient.setter
    def recipient(self, value):
        self.__setattr__('recipient', value)
    
    @property
    def action(self):
        return self.__getattr__('action')

    @action.setter
    def action(self, value):
        self.__setattr__('action', value)
    

    class ACTION:
        TYPING_ON = 'typing_on'
        TYPING_OFF = 'typing_off'
        MARK_SEEN = 'mark_seen'
class GenericElementBase (FactoryBase):

    SCHEMA =  {'value': {'image_url': {'value': None, 'name': 'image_url', 'enum': None, 'type': 'string'}, 'item_url': {'value': None, 'name': 'item_url', 'enum': None, 'type': 'string'}, 'title': {'value': None, 'name': 'title', 'enum': None, 'type': 'string'}, 'subtitle': {'value': None, 'name': 'subtitle', 'enum': None, 'type': 'string'}, 'default_action': {'value': None, 'name': 'default_action', 'enum': None, 'type': 'string'}, 'buttons': {'value': [], 'name': 'buttons', 'enum': None, 'type': 'list'}}, 'type': 'object'}
    CONFIG = {'class_name': 'GenericElement', 'mapping': {'image_url': 'image_url', 'item_url': 'item_url', 'title': 'title', 'subtitle': 'subtitle', 'default_action': 'default_action', 'buttons': 'buttons'}, 'schema': 'generic.element'}

    def __init__(self,  image_url = None,  item_url = None,  title = None,  subtitle = None,  default_action = None,  buttons = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def image_url(self):
        return self.__getattr__('image_url')

    @image_url.setter
    def image_url(self, value):
        self.__setattr__('image_url', value)
    
    @property
    def item_url(self):
        return self.__getattr__('item_url')

    @item_url.setter
    def item_url(self, value):
        self.__setattr__('item_url', value)
    
    @property
    def title(self):
        return self.__getattr__('title')

    @title.setter
    def title(self, value):
        self.__setattr__('title', value)
    
    @property
    def subtitle(self):
        return self.__getattr__('subtitle')

    @subtitle.setter
    def subtitle(self, value):
        self.__setattr__('subtitle', value)
    
    @property
    def default_action(self):
        return self.__getattr__('default_action')

    @default_action.setter
    def default_action(self, value):
        self.__setattr__('default_action', value)
    
    @property
    def buttons(self):
        return self.__getattr__('buttons')

    @buttons.setter
    def buttons(self, value):
        self.__setattr__('buttons', value)
    

class GenericTemplateBase (FactoryBase):

    SCHEMA =  {'value': {'payload': {'value': {'elements': {'value': [], 'name': 'elements', 'enum': None, 'type': 'list'}, 'template_type': {'value': 'generic', 'name': 'template_type', 'enum': None, 'type': 'string'}}, 'name': 'payload', 'enum': None, 'type': 'object'}, 'type': {'value': 'template', 'name': 'type', 'enum': None, 'type': 'string'}}, 'type': 'object'}
    CONFIG = {'class_name': 'GenericTemplate', 'mapping': {'payload': 'payload', 'type': 'type'}, 'schema': 'generic.template'}

    def __init__(self,  payload = None,  type = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def payload(self):
        return self.__getattr__('payload')

    @payload.setter
    def payload(self, value):
        self.__setattr__('payload', value)
    
    @property
    def type(self):
        return self.__getattr__('type')

    @type.setter
    def type(self, value):
        self.__setattr__('type', value)
    

class GenericTemplateMessageBase (FactoryBase):

    SCHEMA =  {'value': {'message': {'value': {'attachment': {'value': {'payload': {'value': {'elements': {'value': [], 'name': 'elements', 'enum': None, 'type': 'list'}, 'template_type': {'value': 'generic', 'name': 'template_type', 'enum': None, 'type': 'string'}}, 'name': 'payload', 'enum': None, 'type': 'object'}, 'type': {'value': 'template', 'name': 'type', 'enum': None, 'type': 'string'}}, 'name': 'attachment', 'enum': None, 'type': 'object'}}, 'name': 'message', 'enum': None, 'type': 'object'}, 'sender_action': {'value': None, 'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}, 'recipient': {'value': {'id': {'value': None, 'name': 'id', 'enum': None, 'type': 'string'}, 'phone_number': {'value': None, 'name': 'phone_number', 'enum': None, 'type': 'string'}}, 'name': 'recipient', 'enum': None, 'type': 'object'}, 'notification_type': {'value': None, 'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}}, 'type': 'object'}
    CONFIG = {'class_name': 'GenericTemplateMessage', 'mapping': {'elements': 'message.attachment.payload.elements', 'recipient': 'recipient.id'}, 'schema': 'generic_template.message'}

    def __init__(self,  elements = None,  recipient = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def elements(self):
        return self.__getattr__('elements')

    @elements.setter
    def elements(self, value):
        self.__setattr__('elements', value)
    
    @property
    def recipient(self):
        return self.__getattr__('recipient')

    @recipient.setter
    def recipient(self, value):
        self.__setattr__('recipient', value)
    

class ListElementBase (FactoryBase):

    SCHEMA =  {'value': {'image_url': {'value': None, 'name': 'image_url', 'enum': None, 'type': 'string'}, 'subtitle': {'value': None, 'name': 'subtitle', 'enum': None, 'type': 'string'}, 'default_action': {'value': None, 'name': 'default_action', 'enum': None, 'type': 'string'}, 'buttons': {'value': [], 'name': 'buttons', 'enum': None, 'type': 'list'}, 'title': {'value': None, 'name': 'title', 'enum': None, 'type': 'string'}}, 'type': 'object'}
    CONFIG = {'class_name': 'ListElement', 'mapping': {'image_url': 'image_url', 'title': 'title', 'subtitle': 'subtitle', 'default_action': 'default_action', 'buttons': 'buttons'}, 'schema': 'list.element'}

    def __init__(self,  image_url = None,  title = None,  subtitle = None,  default_action = None,  buttons = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def image_url(self):
        return self.__getattr__('image_url')

    @image_url.setter
    def image_url(self, value):
        self.__setattr__('image_url', value)
    
    @property
    def title(self):
        return self.__getattr__('title')

    @title.setter
    def title(self, value):
        self.__setattr__('title', value)
    
    @property
    def subtitle(self):
        return self.__getattr__('subtitle')

    @subtitle.setter
    def subtitle(self, value):
        self.__setattr__('subtitle', value)
    
    @property
    def default_action(self):
        return self.__getattr__('default_action')

    @default_action.setter
    def default_action(self, value):
        self.__setattr__('default_action', value)
    
    @property
    def buttons(self):
        return self.__getattr__('buttons')

    @buttons.setter
    def buttons(self, value):
        self.__setattr__('buttons', value)
    

class ListTemplateBase (FactoryBase):

    SCHEMA =  {'value': {'payload': {'value': {'elements': {'value': [], 'name': 'elements', 'enum': None, 'type': 'list'}, 'template_type': {'value': 'list', 'name': 'template_type', 'enum': None, 'type': 'string'}}, 'name': 'payload', 'enum': None, 'type': 'object'}, 'type': {'value': 'template', 'name': 'type', 'enum': None, 'type': 'string'}}, 'type': 'object'}
    CONFIG = {'class_name': 'ListTemplate', 'mapping': {'payload': 'payload', 'type': 'type'}, 'schema': 'list.template'}

    def __init__(self,  payload = None,  type = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def payload(self):
        return self.__getattr__('payload')

    @payload.setter
    def payload(self, value):
        self.__setattr__('payload', value)
    
    @property
    def type(self):
        return self.__getattr__('type')

    @type.setter
    def type(self, value):
        self.__setattr__('type', value)
    

class ListTemplateMessageBase (FactoryBase):

    SCHEMA =  {'value': {'message': {'value': {'attachment': {'value': {'payload': {'value': {'elements': {'value': [], 'name': 'elements', 'enum': None, 'type': 'list'}, 'template_type': {'value': 'list', 'name': 'template_type', 'enum': None, 'type': 'string'}}, 'name': 'payload', 'enum': None, 'type': 'object'}, 'type': {'value': 'template', 'name': 'type', 'enum': None, 'type': 'string'}}, 'name': 'attachment', 'enum': None, 'type': 'object'}}, 'name': 'message', 'enum': None, 'type': 'object'}, 'sender_action': {'value': None, 'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}, 'recipient': {'value': {'id': {'value': None, 'name': 'id', 'enum': None, 'type': 'string'}, 'phone_number': {'value': None, 'name': 'phone_number', 'enum': None, 'type': 'string'}}, 'name': 'recipient', 'enum': None, 'type': 'object'}, 'notification_type': {'value': None, 'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}}, 'type': 'object'}
    CONFIG = {'class_name': 'ListTemplateMessage', 'mapping': {'elements': 'message.attachment.payload.elements', 'recipient': 'recipient.id'}, 'schema': 'list_template.message'}

    def __init__(self,  elements = None,  recipient = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def elements(self):
        return self.__getattr__('elements')

    @elements.setter
    def elements(self, value):
        self.__setattr__('elements', value)
    
    @property
    def recipient(self):
        return self.__getattr__('recipient')

    @recipient.setter
    def recipient(self, value):
        self.__setattr__('recipient', value)
    

class MessageBase (FactoryBase):

    SCHEMA =  {'generic_template': {'value': {'message': {'value': {'attachment': {'value': {'payload': {'value': {'elements': {'value': [], 'name': 'elements', 'enum': None, 'type': 'list'}, 'template_type': {'value': 'generic', 'name': 'template_type', 'enum': None, 'type': 'string'}}, 'name': 'payload', 'enum': None, 'type': 'object'}, 'type': {'value': 'template', 'name': 'type', 'enum': None, 'type': 'string'}}, 'name': 'attachment', 'enum': None, 'type': 'object'}}, 'name': 'message', 'enum': None, 'type': 'object'}, 'sender_action': {'value': None, 'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}, 'recipient': {'value': {'id': {'value': None, 'name': 'id', 'enum': None, 'type': 'string'}, 'phone_number': {'value': None, 'name': 'phone_number', 'enum': None, 'type': 'string'}}, 'name': 'recipient', 'enum': None, 'type': 'object'}, 'notification_type': {'value': None, 'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}}, 'type': 'object'}, 'list_template': {'value': {'message': {'value': {'attachment': {'value': {'payload': {'value': {'elements': {'value': [], 'name': 'elements', 'enum': None, 'type': 'list'}, 'template_type': {'value': 'list', 'name': 'template_type', 'enum': None, 'type': 'string'}}, 'name': 'payload', 'enum': None, 'type': 'object'}, 'type': {'value': 'template', 'name': 'type', 'enum': None, 'type': 'string'}}, 'name': 'attachment', 'enum': None, 'type': 'object'}}, 'name': 'message', 'enum': None, 'type': 'object'}, 'sender_action': {'value': None, 'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}, 'recipient': {'value': {'id': {'value': None, 'name': 'id', 'enum': None, 'type': 'string'}, 'phone_number': {'value': None, 'name': 'phone_number', 'enum': None, 'type': 'string'}}, 'name': 'recipient', 'enum': None, 'type': 'object'}, 'notification_type': {'value': None, 'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}}, 'type': 'object'}, 'quickreply': {'value': {'message': {'value': {'quick_replies': {'value': [], 'name': 'quick_replies', 'enum': None, 'type': 'list'}, 'text': {'value': None, 'name': 'text', 'enum': None, 'type': 'string'}}, 'name': 'message', 'enum': None, 'type': 'object'}, 'sender_action': {'value': None, 'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}, 'recipient': {'value': {'id': {'value': None, 'name': 'id', 'enum': None, 'type': 'string'}, 'phone_number': {'value': None, 'name': 'phone_number', 'enum': None, 'type': 'string'}}, 'name': 'recipient', 'enum': None, 'type': 'object'}, 'notification_type': {'value': None, 'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}}, 'type': 'object'}, 'type': 'object', 'value': {'message': {'value': {'text': {'value': None, 'name': 'text', 'enum': None, 'type': 'string'}, 'attachment': {'value': None, 'name': 'attachment', 'enum': None, 'type': 'object'}}, 'name': 'message', 'enum': None, 'type': 'object'}, 'sender_action': {'value': None, 'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}, 'recipient': {'value': {'id': {'value': None, 'name': 'id', 'enum': None, 'type': 'string'}, 'phone_number': {'value': None, 'name': 'phone_number', 'enum': None, 'type': 'string'}}, 'name': 'recipient', 'enum': None, 'type': 'object'}, 'notification_type': {'value': None, 'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}}}
    CONFIG = {'class_name': 'Message', 'mapping': {'recipient': 'recipient.id', 'action': 'sender_action', 'text': 'message.text'}, 'schema': 'message'}

    def __init__(self,  recipient = None,  action = None,  text = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def recipient(self):
        return self.__getattr__('recipient')

    @recipient.setter
    def recipient(self, value):
        self.__setattr__('recipient', value)
    
    @property
    def action(self):
        return self.__getattr__('action')

    @action.setter
    def action(self, value):
        self.__setattr__('action', value)
    
    @property
    def text(self):
        return self.__getattr__('text')

    @text.setter
    def text(self, value):
        self.__setattr__('text', value)
    

    class ACTION:
        TYPING_ON = 'typing_on'
        TYPING_OFF = 'typing_off'
        MARK_SEEN = 'mark_seen'
class QuickReplyBase (FactoryBase):

    SCHEMA =  {'value': {'image_url': {'value': None, 'name': 'image_url', 'enum': None, 'type': 'string'}, 'content_type': {'value': None, 'name': 'content_type', 'enum': ['text', 'location'], 'type': 'enum'}, 'payload': {'value': None, 'name': 'payload', 'enum': None, 'type': 'string'}, 'title': {'value': None, 'name': 'title', 'enum': None, 'type': 'string'}}, 'type': 'object', 'location': {'value': {'content_type': {'value': 'location', 'name': 'content_type', 'enum': None, 'type': 'string'}}, 'type': 'object'}}
    CONFIG = {'class_name': 'QuickReply', 'mapping': {'image_url': 'image_url', 'content_type': 'content_type', 'title': 'title', 'payload': 'payload'}, 'schema': 'quickreply'}

    def __init__(self,  image_url = None,  content_type = None,  title = None,  payload = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def image_url(self):
        return self.__getattr__('image_url')

    @image_url.setter
    def image_url(self, value):
        self.__setattr__('image_url', value)
    
    @property
    def content_type(self):
        return self.__getattr__('content_type')

    @content_type.setter
    def content_type(self, value):
        self.__setattr__('content_type', value)
    
    @property
    def title(self):
        return self.__getattr__('title')

    @title.setter
    def title(self, value):
        self.__setattr__('title', value)
    
    @property
    def payload(self):
        return self.__getattr__('payload')

    @payload.setter
    def payload(self, value):
        self.__setattr__('payload', value)
    

    class CONTENT_TYPE:
        TEXT = 'text'
        LOCATION = 'location'
class QuickReplyMessageBase (FactoryBase):

    SCHEMA =  {'value': {'message': {'value': {'quick_replies': {'value': [], 'name': 'quick_replies', 'enum': None, 'type': 'list'}, 'text': {'value': None, 'name': 'text', 'enum': None, 'type': 'string'}}, 'name': 'message', 'enum': None, 'type': 'object'}, 'sender_action': {'value': None, 'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}, 'recipient': {'value': {'id': {'value': None, 'name': 'id', 'enum': None, 'type': 'string'}, 'phone_number': {'value': None, 'name': 'phone_number', 'enum': None, 'type': 'string'}}, 'name': 'recipient', 'enum': None, 'type': 'object'}, 'notification_type': {'value': None, 'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}}, 'type': 'object'}
    CONFIG = {'class_name': 'QuickReplyMessage', 'mapping': {'quick_replies': 'message.quick_replies', 'recipient': 'recipient.id', 'text': 'message.text'}, 'schema': 'quickreply.message'}

    def __init__(self,  quick_replies = None,  recipient = None,  text = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def quick_replies(self):
        return self.__getattr__('quick_replies')

    @quick_replies.setter
    def quick_replies(self, value):
        self.__setattr__('quick_replies', value)
    
    @property
    def recipient(self):
        return self.__getattr__('recipient')

    @recipient.setter
    def recipient(self, value):
        self.__setattr__('recipient', value)
    
    @property
    def text(self):
        return self.__getattr__('text')

    @text.setter
    def text(self, value):
        self.__setattr__('text', value)
    

class CallButtonBase (FactoryBase):

    SCHEMA =  {'value': {'payload': {'value': None, 'name': 'payload', 'enum': None, 'type': 'string'}, 'type': {'value': 'phone_number', 'name': 'type', 'enum': None, 'type': 'string'}, 'title': {'value': None, 'name': 'title', 'enum': None, 'type': 'string'}}, 'type': 'object'}
    CONFIG = {'class_name': 'CallButton', 'mapping': {'payload': 'payload', 'type': 'type', 'title': 'title'}, 'schema': 'call.button'}

    def __init__(self,  payload = None,  type = None,  title = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def payload(self):
        return self.__getattr__('payload')

    @payload.setter
    def payload(self, value):
        self.__setattr__('payload', value)
    
    @property
    def type(self):
        return self.__getattr__('type')

    @type.setter
    def type(self, value):
        self.__setattr__('type', value)
    
    @property
    def title(self):
        return self.__getattr__('title')

    @title.setter
    def title(self, value):
        self.__setattr__('title', value)
    

class PostBackButtonBase (FactoryBase):

    SCHEMA =  {'value': {'payload': {'value': None, 'name': 'payload', 'enum': None, 'type': 'string'}, 'type': {'value': 'postback', 'name': 'type', 'enum': None, 'type': 'string'}, 'title': {'value': None, 'name': 'title', 'enum': None, 'type': 'string'}}, 'type': 'object'}
    CONFIG = {'class_name': 'PostBackButton', 'mapping': {'payload': 'payload', 'type': 'type', 'title': 'title'}, 'schema': 'postback.button'}

    def __init__(self,  payload = None,  type = None,  title = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def payload(self):
        return self.__getattr__('payload')

    @payload.setter
    def payload(self, value):
        self.__setattr__('payload', value)
    
    @property
    def type(self):
        return self.__getattr__('type')

    @type.setter
    def type(self, value):
        self.__setattr__('type', value)
    
    @property
    def title(self):
        return self.__getattr__('title')

    @title.setter
    def title(self, value):
        self.__setattr__('title', value)
    

class ShareButtonBase (FactoryBase):

    SCHEMA =  {'value': {'type': {'value': 'element_share', 'name': 'type', 'enum': None, 'type': 'string'}}, 'type': 'object'}
    CONFIG = {'class_name': 'ShareButton', 'mapping': {'type': 'type'}, 'schema': 'share.button'}

    def __init__(self,  type = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def type(self):
        return self.__getattr__('type')

    @type.setter
    def type(self, value):
        self.__setattr__('type', value)
    

class UrlButtonBase (FactoryBase):

    SCHEMA =  {'value': {'webview_height_ratio': {'value': None, 'name': 'webview_height_ratio', 'enum': ['compact', 'tall', 'full'], 'type': 'enum'}, 'type': {'value': 'web_url', 'name': 'type', 'enum': None, 'type': 'string'}, 'fallback_url': {'value': None, 'name': 'fallback_url', 'enum': None, 'type': 'string'}, 'title': {'value': None, 'name': 'title', 'enum': None, 'type': 'string'}, 'url': {'value': None, 'name': 'url', 'enum': None, 'type': 'string'}, 'messenger_extensions': {'value': None, 'name': 'messenger_extensions', 'enum': None, 'type': 'boolean'}}, 'type': 'object'}
    CONFIG = {'class_name': 'UrlButton', 'mapping': {'webview_height_ratio': 'webview_height_ratio', 'url': 'url', 'fallback_url': 'fallback_url', 'title': 'title', 'type': 'type', 'messenger_extensions': 'messenger_extensions'}, 'schema': 'url.button'}

    def __init__(self,  webview_height_ratio = None,  url = None,  fallback_url = None,  title = None,  type = None,  messenger_extensions = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def webview_height_ratio(self):
        return self.__getattr__('webview_height_ratio')

    @webview_height_ratio.setter
    def webview_height_ratio(self, value):
        self.__setattr__('webview_height_ratio', value)
    
    @property
    def url(self):
        return self.__getattr__('url')

    @url.setter
    def url(self, value):
        self.__setattr__('url', value)
    
    @property
    def fallback_url(self):
        return self.__getattr__('fallback_url')

    @fallback_url.setter
    def fallback_url(self, value):
        self.__setattr__('fallback_url', value)
    
    @property
    def title(self):
        return self.__getattr__('title')

    @title.setter
    def title(self, value):
        self.__setattr__('title', value)
    
    @property
    def type(self):
        return self.__getattr__('type')

    @type.setter
    def type(self, value):
        self.__setattr__('type', value)
    
    @property
    def messenger_extensions(self):
        return self.__getattr__('messenger_extensions')

    @messenger_extensions.setter
    def messenger_extensions(self, value):
        self.__setattr__('messenger_extensions', value)
    

    class WEBVIEW_HEIGHT_RATIO:
        COMPACT = 'compact'
        TALL = 'tall'
        FULL = 'full'



##############  GENERATED MODELS END  ##############
##############          Eggwise       ##############