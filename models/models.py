##############          Eggwise       ##############
############## GENERATED MODELS START ##############

import copy


class FactoryBase():
    def __init__(self, schema, config, child_locals=None):

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
        # build bindings
        mapping_config = config['mapping']
        mapping = mapping_config
        if '_include' in mapping_config:
            include_config = mapping_config['_include']
            del (mapping['_include'])

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
        mapping = self.mapping
        if item not in mapping:
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
            err_msg = '{0} > No mappint to schema defined for: {1}\nAvailable bindings:\n {2}'.format(self, key,
                                                                                                      mapping)
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


class ActionMessage(FactoryBase):
    SCHEMA = {'list_template': {'type': 'object', 'value': {
        'message': {'name': 'message', 'type': 'object', 'enum': None, 'value': {
            'attachment': {'name': 'attachment', 'type': 'object', 'enum': None,
                           'value': {'type': {'name': 'type', 'type': 'string', 'enum': None, 'value': 'template'},
                                     'payload': {'name': 'payload', 'type': 'object', 'enum': None, 'value': {
                                         'elements': {'name': 'elements', 'type': 'list', 'enum': None, 'value': []},
                                         'template_type': {'name': 'template_type', 'type': 'string', 'enum': None,
                                                           'value': 'list'}}}}}}},
        'notification_type': {'name': 'notification_type', 'type': 'enum',
                              'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'value': None},
        'sender_action': {'name': 'sender_action', 'type': 'enum', 'enum': ['typing_on', 'typing_off', 'mark_seen'],
                          'value': None}, 'recipient': {'name': 'recipient', 'type': 'object', 'enum': None, 'value': {
            'phone_number': {'name': 'phone_number', 'type': 'string', 'enum': None, 'value': None},
            'id': {'name': 'id', 'type': 'string', 'enum': None, 'value': None}}}}},
              'generic_template': {'type': 'object', 'value': {
                  'message': {'name': 'message', 'type': 'object', 'enum': None, 'value': {
                      'attachment': {'name': 'attachment', 'type': 'object', 'enum': None, 'value': {
                          'type': {'name': 'type', 'type': 'string', 'enum': None, 'value': 'template'},
                          'payload': {'name': 'payload', 'type': 'object', 'enum': None, 'value': {
                              'elements': {'name': 'elements', 'type': 'list', 'enum': None, 'value': []},
                              'template_type': {'name': 'template_type', 'type': 'string', 'enum': None,
                                                'value': 'generic'}}}}}}},
                  'notification_type': {'name': 'notification_type', 'type': 'enum',
                                        'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'value': None},
                  'sender_action': {'name': 'sender_action', 'type': 'enum',
                                    'enum': ['typing_on', 'typing_off', 'mark_seen'], 'value': None},
                  'recipient': {'name': 'recipient', 'type': 'object', 'enum': None, 'value': {
                      'phone_number': {'name': 'phone_number', 'type': 'string', 'enum': None, 'value': None},
                      'id': {'name': 'id', 'type': 'string', 'enum': None, 'value': None}}}}}, 'type': 'object',
              'quickreply': {'type': 'object', 'value': {'message': {'name': 'message', 'type': 'object', 'enum': None,
                                                                     'value': {
                                                                         'text': {'name': 'text', 'type': 'string',
                                                                                  'enum': None, 'value': None},
                                                                         'quick_replies': {'name': 'quick_replies',
                                                                                           'type': 'list', 'enum': None,
                                                                                           'value': []}}},
                                                         'notification_type': {'name': 'notification_type',
                                                                               'type': 'enum',
                                                                               'enum': ['REGULAR', 'SILENT_PUSH',
                                                                                        'NO_PUSH'], 'value': None},
                                                         'sender_action': {'name': 'sender_action', 'type': 'enum',
                                                                           'enum': ['typing_on', 'typing_off',
                                                                                    'mark_seen'], 'value': None},
                                                         'recipient': {'name': 'recipient', 'type': 'object',
                                                                       'enum': None, 'value': {
                                                                 'phone_number': {'name': 'phone_number',
                                                                                  'type': 'string', 'enum': None,
                                                                                  'value': None},
                                                                 'id': {'name': 'id', 'type': 'string', 'enum': None,
                                                                        'value': None}}}}}, 'value': {
            'message': {'name': 'message', 'type': 'object', 'enum': None,
                        'value': {'attachment': {'name': 'attachment', 'type': 'object', 'enum': None, 'value': None},
                                  'text': {'name': 'text', 'type': 'string', 'enum': None, 'value': None}}},
            'notification_type': {'name': 'notification_type', 'type': 'enum',
                                  'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'value': None},
            'sender_action': {'name': 'sender_action', 'type': 'enum', 'enum': ['typing_on', 'typing_off', 'mark_seen'],
                              'value': None}, 'recipient': {'name': 'recipient', 'type': 'object', 'enum': None,
                                                            'value': {'phone_number': {'name': 'phone_number',
                                                                                       'type': 'string', 'enum': None,
                                                                                       'value': None},
                                                                      'id': {'name': 'id', 'type': 'string',
                                                                             'enum': None, 'value': None}}}}}
    CONFIG = {'mapping': {'action': 'sender_action', 'recipient': 'recipient.id'}, 'schema': 'message',
              'class_name': 'ActionMessage'}

    def __init__(self, action=None, recipient=None, ):
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


class GenericElement(FactoryBase):
    SCHEMA = {'type': 'object',
              'value': {'default_action': {'name': 'default_action', 'type': 'string', 'enum': None, 'value': None},
                        'image_url': {'name': 'image_url', 'type': 'string', 'enum': None, 'value': None},
                        'title': {'name': 'title', 'type': 'string', 'enum': None, 'value': None},
                        'item_url': {'name': 'item_url', 'type': 'string', 'enum': None, 'value': None},
                        'subtitle': {'name': 'subtitle', 'type': 'string', 'enum': None, 'value': None},
                        'buttons': {'name': 'buttons', 'type': 'list', 'enum': None, 'value': []}}}
    CONFIG = {'mapping': {'default_action': 'default_action', 'image_url': 'image_url', 'title': 'title',
                          'item_url': 'item_url', 'subtitle': 'subtitle', 'buttons': 'buttons'},
              'schema': 'generic.element', 'class_name': 'GenericElement'}

    def __init__(self, default_action=None, image_url=None, title=None, item_url=None, subtitle=None, buttons=None, ):
        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    @property
    def default_action(self):
        return self.__getattr__('action')

    @default_action.setter
    def default_action(self, value):
        self.__setattr__('default_action', value)

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
    def item_url(self):
        return self.__getattr__('action')

    @item_url.setter
    def item_url(self, value):
        self.__setattr__('item_url', value)

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


class GenericTemplate(FactoryBase):
    SCHEMA = {'type': 'object', 'value': {'type': {'name': 'type', 'type': 'string', 'enum': None, 'value': 'template'},
                                          'payload': {'name': 'payload', 'type': 'object', 'enum': None, 'value': {
                                              'elements': {'name': 'elements', 'type': 'list', 'enum': None,
                                                           'value': []},
                                              'template_type': {'name': 'template_type', 'type': 'string', 'enum': None,
                                                                'value': 'generic'}}}}}
    CONFIG = {'mapping': {'type': 'type', 'payload': 'payload'}, 'schema': 'generic.template',
              'class_name': 'GenericTemplate'}

    def __init__(self, type=None, payload=None, ):
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


class GenericTemplateMessage(FactoryBase):
    SCHEMA = {'type': 'object', 'value': {'message': {'name': 'message', 'type': 'object', 'enum': None, 'value': {
        'attachment': {'name': 'attachment', 'type': 'object', 'enum': None,
                       'value': {'type': {'name': 'type', 'type': 'string', 'enum': None, 'value': 'template'},
                                 'payload': {'name': 'payload', 'type': 'object', 'enum': None, 'value': {
                                     'elements': {'name': 'elements', 'type': 'list', 'enum': None, 'value': []},
                                     'template_type': {'name': 'template_type', 'type': 'string', 'enum': None,
                                                       'value': 'generic'}}}}}}},
                                          'notification_type': {'name': 'notification_type', 'type': 'enum',
                                                                'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'],
                                                                'value': None},
                                          'sender_action': {'name': 'sender_action', 'type': 'enum',
                                                            'enum': ['typing_on', 'typing_off', 'mark_seen'],
                                                            'value': None},
                                          'recipient': {'name': 'recipient', 'type': 'object', 'enum': None, 'value': {
                                              'phone_number': {'name': 'phone_number', 'type': 'string', 'enum': None,
                                                               'value': None},
                                              'id': {'name': 'id', 'type': 'string', 'enum': None, 'value': None}}}}}
    CONFIG = {'mapping': {'elements': 'message.attachment.payload.elements', 'recipient': 'recipient.id'},
              'schema': 'generic_template.message', 'class_name': 'GenericTemplateMessage'}

    def __init__(self, elements=None, recipient=None, ):
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


class ListElement(FactoryBase):
    SCHEMA = {'type': 'object',
              'value': {'default_action': {'name': 'default_action', 'type': 'string', 'enum': None, 'value': None},
                        'image_url': {'name': 'image_url', 'type': 'string', 'enum': None, 'value': None},
                        'subtitle': {'name': 'subtitle', 'type': 'string', 'enum': None, 'value': None},
                        'title': {'name': 'title', 'type': 'string', 'enum': None, 'value': None},
                        'buttons': {'name': 'buttons', 'type': 'list', 'enum': None, 'value': []}}}
    CONFIG = {'mapping': {'default_action': 'default_action', 'image_url': 'image_url', 'subtitle': 'subtitle',
                          'title': 'title', 'buttons': 'buttons'}, 'schema': 'list.element',
              'class_name': 'ListElement'}

    def __init__(self, default_action=None, image_url=None, subtitle=None, title=None, buttons=None, ):
        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    @property
    def default_action(self):
        return self.__getattr__('action')

    @default_action.setter
    def default_action(self, value):
        self.__setattr__('default_action', value)

    @property
    def image_url(self):
        return self.__getattr__('action')

    @image_url.setter
    def image_url(self, value):
        self.__setattr__('image_url', value)

    @property
    def subtitle(self):
        return self.__getattr__('action')

    @subtitle.setter
    def subtitle(self, value):
        self.__setattr__('subtitle', value)

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


class ListTemplate(FactoryBase):
    SCHEMA = {'type': 'object', 'value': {'type': {'name': 'type', 'type': 'string', 'enum': None, 'value': 'template'},
                                          'payload': {'name': 'payload', 'type': 'object', 'enum': None, 'value': {
                                              'elements': {'name': 'elements', 'type': 'list', 'enum': None,
                                                           'value': []},
                                              'template_type': {'name': 'template_type', 'type': 'string', 'enum': None,
                                                                'value': 'list'}}}}}
    CONFIG = {'mapping': {'type': 'type', 'payload': 'payload'}, 'schema': 'list.template',
              'class_name': 'ListTemplate'}

    def __init__(self, type=None, payload=None, ):
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


class ListTemplateMessage(FactoryBase):
    SCHEMA = {'type': 'object', 'value': {'message': {'name': 'message', 'type': 'object', 'enum': None, 'value': {
        'attachment': {'name': 'attachment', 'type': 'object', 'enum': None,
                       'value': {'type': {'name': 'type', 'type': 'string', 'enum': None, 'value': 'template'},
                                 'payload': {'name': 'payload', 'type': 'object', 'enum': None, 'value': {
                                     'elements': {'name': 'elements', 'type': 'list', 'enum': None, 'value': []},
                                     'template_type': {'name': 'template_type', 'type': 'string', 'enum': None,
                                                       'value': 'list'}}}}}}},
                                          'notification_type': {'name': 'notification_type', 'type': 'enum',
                                                                'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'],
                                                                'value': None},
                                          'sender_action': {'name': 'sender_action', 'type': 'enum',
                                                            'enum': ['typing_on', 'typing_off', 'mark_seen'],
                                                            'value': None},
                                          'recipient': {'name': 'recipient', 'type': 'object', 'enum': None, 'value': {
                                              'phone_number': {'name': 'phone_number', 'type': 'string', 'enum': None,
                                                               'value': None},
                                              'id': {'name': 'id', 'type': 'string', 'enum': None, 'value': None}}}}}
    CONFIG = {'mapping': {'elements': 'message.attachment.payload.elements', 'recipient': 'recipient.id'},
              'schema': 'list_template.message', 'class_name': 'ListTemplateMessage'}

    def __init__(self, elements=None, recipient=None, ):
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


class Message(FactoryBase):
    SCHEMA = {'list_template': {'type': 'object', 'value': {
        'message': {'name': 'message', 'type': 'object', 'enum': None, 'value': {
            'attachment': {'name': 'attachment', 'type': 'object', 'enum': None,
                           'value': {'type': {'name': 'type', 'type': 'string', 'enum': None, 'value': 'template'},
                                     'payload': {'name': 'payload', 'type': 'object', 'enum': None, 'value': {
                                         'elements': {'name': 'elements', 'type': 'list', 'enum': None, 'value': []},
                                         'template_type': {'name': 'template_type', 'type': 'string', 'enum': None,
                                                           'value': 'list'}}}}}}},
        'notification_type': {'name': 'notification_type', 'type': 'enum',
                              'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'value': None},
        'sender_action': {'name': 'sender_action', 'type': 'enum', 'enum': ['typing_on', 'typing_off', 'mark_seen'],
                          'value': None}, 'recipient': {'name': 'recipient', 'type': 'object', 'enum': None, 'value': {
            'phone_number': {'name': 'phone_number', 'type': 'string', 'enum': None, 'value': None},
            'id': {'name': 'id', 'type': 'string', 'enum': None, 'value': None}}}}},
              'generic_template': {'type': 'object', 'value': {
                  'message': {'name': 'message', 'type': 'object', 'enum': None, 'value': {
                      'attachment': {'name': 'attachment', 'type': 'object', 'enum': None, 'value': {
                          'type': {'name': 'type', 'type': 'string', 'enum': None, 'value': 'template'},
                          'payload': {'name': 'payload', 'type': 'object', 'enum': None, 'value': {
                              'elements': {'name': 'elements', 'type': 'list', 'enum': None, 'value': []},
                              'template_type': {'name': 'template_type', 'type': 'string', 'enum': None,
                                                'value': 'generic'}}}}}}},
                  'notification_type': {'name': 'notification_type', 'type': 'enum',
                                        'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'value': None},
                  'sender_action': {'name': 'sender_action', 'type': 'enum',
                                    'enum': ['typing_on', 'typing_off', 'mark_seen'], 'value': None},
                  'recipient': {'name': 'recipient', 'type': 'object', 'enum': None, 'value': {
                      'phone_number': {'name': 'phone_number', 'type': 'string', 'enum': None, 'value': None},
                      'id': {'name': 'id', 'type': 'string', 'enum': None, 'value': None}}}}}, 'type': 'object',
              'quickreply': {'type': 'object', 'value': {'message': {'name': 'message', 'type': 'object', 'enum': None,
                                                                     'value': {
                                                                         'text': {'name': 'text', 'type': 'string',
                                                                                  'enum': None, 'value': None},
                                                                         'quick_replies': {'name': 'quick_replies',
                                                                                           'type': 'list', 'enum': None,
                                                                                           'value': []}}},
                                                         'notification_type': {'name': 'notification_type',
                                                                               'type': 'enum',
                                                                               'enum': ['REGULAR', 'SILENT_PUSH',
                                                                                        'NO_PUSH'], 'value': None},
                                                         'sender_action': {'name': 'sender_action', 'type': 'enum',
                                                                           'enum': ['typing_on', 'typing_off',
                                                                                    'mark_seen'], 'value': None},
                                                         'recipient': {'name': 'recipient', 'type': 'object',
                                                                       'enum': None, 'value': {
                                                                 'phone_number': {'name': 'phone_number',
                                                                                  'type': 'string', 'enum': None,
                                                                                  'value': None},
                                                                 'id': {'name': 'id', 'type': 'string', 'enum': None,
                                                                        'value': None}}}}}, 'value': {
            'message': {'name': 'message', 'type': 'object', 'enum': None,
                        'value': {'attachment': {'name': 'attachment', 'type': 'object', 'enum': None, 'value': None},
                                  'text': {'name': 'text', 'type': 'string', 'enum': None, 'value': None}}},
            'notification_type': {'name': 'notification_type', 'type': 'enum',
                                  'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'value': None},
            'sender_action': {'name': 'sender_action', 'type': 'enum', 'enum': ['typing_on', 'typing_off', 'mark_seen'],
                              'value': None}, 'recipient': {'name': 'recipient', 'type': 'object', 'enum': None,
                                                            'value': {'phone_number': {'name': 'phone_number',
                                                                                       'type': 'string', 'enum': None,
                                                                                       'value': None},
                                                                      'id': {'name': 'id', 'type': 'string',
                                                                             'enum': None, 'value': None}}}}}
    CONFIG = {'mapping': {'text': 'message.text', 'action': 'sender_action', 'recipient': 'recipient.id'},
              'schema': 'message', 'class_name': 'Message'}

    def __init__(self, text=None, action=None, recipient=None, ):
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


class QuickReply(FactoryBase):
    SCHEMA = {'type': 'object',
              'value': {'image_url': {'name': 'image_url', 'type': 'string', 'enum': None, 'value': None},
                        'title': {'name': 'title', 'type': 'string', 'enum': None, 'value': None},
                        'content_type': {'name': 'content_type', 'type': 'enum', 'enum': ['text', 'location'],
                                         'value': None},
                        'payload': {'name': 'payload', 'type': 'string', 'enum': None, 'value': None}},
              'location': {'type': 'object', 'value': {
                  'content_type': {'name': 'content_type', 'type': 'string', 'enum': None, 'value': 'location'}}}}
    CONFIG = {
        'mapping': {'image_url': 'image_url', 'title': 'title', 'content_type': 'content_type', 'payload': 'payload'},
        'schema': 'quickreply', 'class_name': 'QuickReply'}

    def __init__(self, image_url=None, title=None, content_type=None, payload=None, ):
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
    def title(self):
        return self.__getattr__('action')

    @title.setter
    def title(self, value):
        self.__setattr__('title', value)

    @property
    def content_type(self):
        return self.__getattr__('action')

    @content_type.setter
    def content_type(self, value):
        self.__setattr__('content_type', value)

    @property
    def payload(self):
        return self.__getattr__('action')

    @payload.setter
    def payload(self, value):
        self.__setattr__('payload', value)

    class CONTENT_TYPE:
        TEXT = 'text'
        LOCATION = 'location'


class QuickReplyMessage(FactoryBase):
    SCHEMA = {'type': 'object', 'value': {'message': {'name': 'message', 'type': 'object', 'enum': None, 'value': {
        'text': {'name': 'text', 'type': 'string', 'enum': None, 'value': None},
        'quick_replies': {'name': 'quick_replies', 'type': 'list', 'enum': None, 'value': []}}},
                                          'notification_type': {'name': 'notification_type', 'type': 'enum',
                                                                'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'],
                                                                'value': None},
                                          'sender_action': {'name': 'sender_action', 'type': 'enum',
                                                            'enum': ['typing_on', 'typing_off', 'mark_seen'],
                                                            'value': None},
                                          'recipient': {'name': 'recipient', 'type': 'object', 'enum': None, 'value': {
                                              'phone_number': {'name': 'phone_number', 'type': 'string', 'enum': None,
                                                               'value': None},
                                              'id': {'name': 'id', 'type': 'string', 'enum': None, 'value': None}}}}}
    CONFIG = {
        'mapping': {'text': 'message.text', 'quick_replies': 'message.quick_replies', 'recipient': 'recipient.id'},
        'schema': 'quickreply.message', 'class_name': 'QuickReplyMessage'}

    def __init__(self, text=None, quick_replies=None, recipient=None, ):
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


class CallButton(FactoryBase):
    SCHEMA = {'type': 'object',
              'value': {'type': {'name': 'type', 'type': 'string', 'enum': None, 'value': 'phone_number'},
                        'title': {'name': 'title', 'type': 'string', 'enum': None, 'value': None},
                        'payload': {'name': 'payload', 'type': 'string', 'enum': None, 'value': None}}}
    CONFIG = {'mapping': {'type': 'type', 'title': 'title', 'payload': 'payload'}, 'schema': 'call.button',
              'class_name': 'CallButton'}

    def __init__(self, type=None, title=None, payload=None, ):
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


class PostBackButton(FactoryBase):
    SCHEMA = {'type': 'object', 'value': {'type': {'name': 'type', 'type': 'string', 'enum': None, 'value': 'postback'},
                                          'title': {'name': 'title', 'type': 'string', 'enum': None, 'value': None},
                                          'payload': {'name': 'payload', 'type': 'string', 'enum': None,
                                                      'value': None}}}
    CONFIG = {'mapping': {'type': 'type', 'title': 'title', 'payload': 'payload'}, 'schema': 'postback.button',
              'class_name': 'PostBackButton'}

    def __init__(self, type=None, title=None, payload=None, ):
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


class ShareButton(FactoryBase):
    SCHEMA = {'type': 'object',
              'value': {'type': {'name': 'type', 'type': 'string', 'enum': None, 'value': 'element_share'},
                        'title': {'name': 'title', 'type': 'string', 'enum': None, 'value': None},
                        'payload': {'name': 'payload', 'type': 'string', 'enum': None, 'value': None}}}
    CONFIG = {'mapping': {'type': 'type', 'title': 'title', 'payload': 'payload'}, 'schema': 'share.button',
              'class_name': 'ShareButton'}

    def __init__(self, type=None, title=None, payload=None, ):
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


class UrlButton(FactoryBase):
    SCHEMA = {'type': 'object', 'value': {'url': {'name': 'url', 'type': 'string', 'enum': None, 'value': None},
                                          'type': {'name': 'type', 'type': 'string', 'enum': None, 'value': 'web_url'},
                                          'title': {'name': 'title', 'type': 'string', 'enum': None, 'value': None},
                                          'messenger_extensions': {'name': 'messenger_extensions', 'type': 'boolean',
                                                                   'enum': None, 'value': None},
                                          'fallback_url': {'name': 'fallback_url', 'type': 'string', 'enum': None,
                                                           'value': None},
                                          'webview_height_ratio': {'name': 'webview_height_ratio', 'type': 'enum',
                                                                   'enum': ['compact', 'tall', 'full'], 'value': None}}}
    CONFIG = {
        'mapping': {'url': 'url', 'type': 'type', 'title': 'title', 'messenger_extensions': 'messenger_extensions',
                    'webview_height_ratio': 'webview_height_ratio', 'fallback_url': 'fallback_url'},
        'schema': 'url.button', 'class_name': 'UrlButton'}

    def __init__(self, url=None, type=None, title=None, messenger_extensions=None, webview_height_ratio=None,
                 fallback_url=None, ):
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
    def title(self):
        return self.__getattr__('action')

    @title.setter
    def title(self, value):
        self.__setattr__('title', value)

    @property
    def messenger_extensions(self):
        return self.__getattr__('action')

    @messenger_extensions.setter
    def messenger_extensions(self, value):
        self.__setattr__('messenger_extensions', value)

    @property
    def webview_height_ratio(self):
        return self.__getattr__('action')

    @webview_height_ratio.setter
    def webview_height_ratio(self, value):
        self.__setattr__('webview_height_ratio', value)

    @property
    def fallback_url(self):
        return self.__getattr__('action')

    @fallback_url.setter
    def fallback_url(self, value):
        self.__setattr__('fallback_url', value)

    class WEBVIEW_HEIGHT_RATIO:
        COMPACT = 'compact'
        TALL = 'tall'
        FULL = 'full'


##############  GENERATED MODELS END  ##############
##############          Eggwise       ##############
