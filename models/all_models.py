##############          Eggwise       ##############
############## GENERATED MODELS START ##############

import copy

class ValidationError(Exception):
    pass


class FactoryBase():

    def raise_validation_error(self, msg):
        msg = '\n=======\n{0}\n=======\n'.format(msg)
        msg += 'Check the api documentation:\n\n' \
               '{0}\n======'.format(self.doc)
        raise ValidationError(msg)

    def __init__(self, schema, config, child_locals = None):

        self.__dict__['config'] = config
        self.__dict__['schema'] = schema

        if '_doc' in schema:
            doc_url = schema['_doc']
        else:
            doc_url = 'https://developers.facebook.com/docs/messenger-platform'
        self.__dict__['doc'] = doc_url

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

    SCHEMA =  {'quickreply': {'value': {'message': {'name': 'message', 'value': {'quick_replies': {'name': 'quick_replies', 'value': [], 'enum': None, 'type': 'list'}, 'text': {'name': 'text', 'value': None, 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'recipient': {'name': 'recipient', 'value': {'id': {'name': 'id', 'value': None, 'enum': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'value': None, 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'value': None, 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}, 'sender_action': {'name': 'sender_action', 'value': None, 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions', 'type': 'object'}, 'generic_template': {'value': {'message': {'name': 'message', 'value': {'attachment': {'name': 'attachment', '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template', 'value': {'payload': {'name': 'payload', 'value': {'elements': {'name': 'elements', 'value': [], 'enum': None, 'type': 'list'}, 'template_type': {'name': 'template_type', 'value': 'generic', 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'type': {'name': 'type', 'value': 'template', 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}}, 'enum': None, 'type': 'object'}, 'recipient': {'name': 'recipient', 'value': {'id': {'name': 'id', 'value': None, 'enum': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'value': None, 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'value': None, 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}, 'sender_action': {'name': 'sender_action', 'value': None, 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template', 'type': 'object'}, 'type': 'object', 'list_template': {'value': {'message': {'name': 'message', 'value': {'attachment': {'name': 'attachment', '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template', 'value': {'payload': {'name': 'payload', 'value': {'elements': {'name': 'elements', 'value': [], 'enum': None, 'type': 'list'}, 'template_type': {'name': 'template_type', 'value': 'list', 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'type': {'name': 'type', 'value': 'template', 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}}, 'enum': None, 'type': 'object'}, 'recipient': {'name': 'recipient', 'value': {'id': {'name': 'id', 'value': None, 'enum': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'value': None, 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'value': None, 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}, 'sender_action': {'name': 'sender_action', 'value': None, 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template', 'type': 'object'}, 'value': {'message': {'name': 'message', 'value': {'attachment': {'name': 'attachment', 'value': None, 'enum': None, 'type': 'object'}, 'text': {'name': 'text', 'value': None, 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'recipient': {'name': 'recipient', 'value': {'id': {'name': 'id', 'value': None, 'enum': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'value': None, 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'value': None, 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}, 'sender_action': {'name': 'sender_action', 'value': None, 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions'}
    CONFIG = {'class_name': 'ActionMessage', 'mapping': {'recipient': 'recipient.id', 'action': 'sender_action'}, 'schema': 'message'}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions'
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

    SCHEMA =  {'value': {'title': {'name': 'title', 'value': None, 'enum': None, 'type': 'string'}, 'image_url': {'name': 'image_url', 'value': None, 'enum': None, 'type': 'string'}, 'subtitle': {'name': 'subtitle', 'value': None, 'enum': None, 'type': 'string'}, 'item_url': {'name': 'item_url', 'value': None, 'enum': None, 'type': 'string'}, 'default_action': {'name': 'default_action', 'value': None, 'enum': None, 'type': 'string'}, 'buttons': {'name': 'buttons', 'value': [], 'enum': None, 'type': 'list'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template', 'type': 'object'}
    CONFIG = {'class_name': 'GenericElement', 'mapping': {'title': 'title', 'image_url': 'image_url', 'subtitle': 'subtitle', 'item_url': 'item_url', 'default_action': 'default_action', 'buttons': 'buttons'}, 'schema': 'generic.element'}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template'
    def __init__(self,  title = None,  image_url = None,  subtitle = None,  item_url = None,  default_action = None,  buttons = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def title(self):
        return self.__getattr__('title')

    @title.setter
    def title(self, value):
        self.__setattr__('title', value)
    
    @property
    def image_url(self):
        return self.__getattr__('image_url')

    @image_url.setter
    def image_url(self, value):
        self.__setattr__('image_url', value)
    
    @property
    def subtitle(self):
        return self.__getattr__('subtitle')

    @subtitle.setter
    def subtitle(self, value):
        self.__setattr__('subtitle', value)
    
    @property
    def item_url(self):
        return self.__getattr__('item_url')

    @item_url.setter
    def item_url(self, value):
        self.__setattr__('item_url', value)
    
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

    SCHEMA =  {'value': {'payload': {'name': 'payload', 'value': {'elements': {'name': 'elements', 'value': [], 'enum': None, 'type': 'list'}, 'template_type': {'name': 'template_type', 'value': 'generic', 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'type': {'name': 'type', 'value': 'template', 'enum': None, 'type': 'string'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template', 'type': 'object'}
    CONFIG = {'class_name': 'GenericTemplate', 'mapping': {'payload': 'payload', 'type': 'type'}, 'schema': 'generic.template'}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template'
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

    SCHEMA =  {'value': {'message': {'name': 'message', 'value': {'attachment': {'name': 'attachment', '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template', 'value': {'payload': {'name': 'payload', 'value': {'elements': {'name': 'elements', 'value': [], 'enum': None, 'type': 'list'}, 'template_type': {'name': 'template_type', 'value': 'generic', 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'type': {'name': 'type', 'value': 'template', 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}}, 'enum': None, 'type': 'object'}, 'recipient': {'name': 'recipient', 'value': {'id': {'name': 'id', 'value': None, 'enum': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'value': None, 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'value': None, 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}, 'sender_action': {'name': 'sender_action', 'value': None, 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template', 'type': 'object'}
    CONFIG = {'class_name': 'GenericTemplateMessage', 'mapping': {'recipient': 'recipient.id', 'elements': 'message.attachment.payload.elements'}, 'schema': 'generic_template.message'}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template'
    def __init__(self,  recipient = None,  elements = None, ):

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
    def elements(self):
        return self.__getattr__('elements')

    @elements.setter
    def elements(self, value):
        self.__setattr__('elements', value)
    

class ListElementBase (FactoryBase):

    SCHEMA =  {'value': {'default_action': {'name': 'default_action', 'value': None, 'enum': None, 'type': 'string'}, 'title': {'name': 'title', 'value': None, 'enum': None, 'type': 'string'}, 'image_url': {'name': 'image_url', 'value': None, 'enum': None, 'type': 'string'}, 'subtitle': {'name': 'subtitle', 'value': None, 'enum': None, 'type': 'string'}, 'buttons': {'name': 'buttons', 'value': [], 'enum': None, 'type': 'list'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template', 'type': 'object'}
    CONFIG = {'class_name': 'ListElement', 'mapping': {'default_action': 'default_action', 'title': 'title', 'image_url': 'image_url', 'subtitle': 'subtitle', 'buttons': 'buttons'}, 'schema': 'list.element'}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template'
    def __init__(self,  default_action = None,  title = None,  image_url = None,  subtitle = None,  buttons = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def default_action(self):
        return self.__getattr__('default_action')

    @default_action.setter
    def default_action(self, value):
        self.__setattr__('default_action', value)
    
    @property
    def title(self):
        return self.__getattr__('title')

    @title.setter
    def title(self, value):
        self.__setattr__('title', value)
    
    @property
    def image_url(self):
        return self.__getattr__('image_url')

    @image_url.setter
    def image_url(self, value):
        self.__setattr__('image_url', value)
    
    @property
    def subtitle(self):
        return self.__getattr__('subtitle')

    @subtitle.setter
    def subtitle(self, value):
        self.__setattr__('subtitle', value)
    
    @property
    def buttons(self):
        return self.__getattr__('buttons')

    @buttons.setter
    def buttons(self, value):
        self.__setattr__('buttons', value)
    

class ListTemplateBase (FactoryBase):

    SCHEMA =  {'value': {'payload': {'name': 'payload', 'value': {'elements': {'name': 'elements', 'value': [], 'enum': None, 'type': 'list'}, 'template_type': {'name': 'template_type', 'value': 'list', 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'type': {'name': 'type', 'value': 'template', 'enum': None, 'type': 'string'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template', 'type': 'object'}
    CONFIG = {'class_name': 'ListTemplate', 'mapping': {'payload': 'payload', 'type': 'type'}, 'schema': 'list.template'}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template'
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

    SCHEMA =  {'value': {'message': {'name': 'message', 'value': {'attachment': {'name': 'attachment', '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template', 'value': {'payload': {'name': 'payload', 'value': {'elements': {'name': 'elements', 'value': [], 'enum': None, 'type': 'list'}, 'template_type': {'name': 'template_type', 'value': 'list', 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'type': {'name': 'type', 'value': 'template', 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}}, 'enum': None, 'type': 'object'}, 'recipient': {'name': 'recipient', 'value': {'id': {'name': 'id', 'value': None, 'enum': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'value': None, 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'value': None, 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}, 'sender_action': {'name': 'sender_action', 'value': None, 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template', 'type': 'object'}
    CONFIG = {'class_name': 'ListTemplateMessage', 'mapping': {'recipient': 'recipient.id', 'elements': 'message.attachment.payload.elements'}, 'schema': 'list_template.message'}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template'
    def __init__(self,  recipient = None,  elements = None, ):

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
    def elements(self):
        return self.__getattr__('elements')

    @elements.setter
    def elements(self, value):
        self.__setattr__('elements', value)
    

class MessageBase (FactoryBase):

    SCHEMA =  {'quickreply': {'value': {'message': {'name': 'message', 'value': {'quick_replies': {'name': 'quick_replies', 'value': [], 'enum': None, 'type': 'list'}, 'text': {'name': 'text', 'value': None, 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'recipient': {'name': 'recipient', 'value': {'id': {'name': 'id', 'value': None, 'enum': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'value': None, 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'value': None, 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}, 'sender_action': {'name': 'sender_action', 'value': None, 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions', 'type': 'object'}, 'generic_template': {'value': {'message': {'name': 'message', 'value': {'attachment': {'name': 'attachment', '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template', 'value': {'payload': {'name': 'payload', 'value': {'elements': {'name': 'elements', 'value': [], 'enum': None, 'type': 'list'}, 'template_type': {'name': 'template_type', 'value': 'generic', 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'type': {'name': 'type', 'value': 'template', 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}}, 'enum': None, 'type': 'object'}, 'recipient': {'name': 'recipient', 'value': {'id': {'name': 'id', 'value': None, 'enum': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'value': None, 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'value': None, 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}, 'sender_action': {'name': 'sender_action', 'value': None, 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template', 'type': 'object'}, 'type': 'object', 'list_template': {'value': {'message': {'name': 'message', 'value': {'attachment': {'name': 'attachment', '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template', 'value': {'payload': {'name': 'payload', 'value': {'elements': {'name': 'elements', 'value': [], 'enum': None, 'type': 'list'}, 'template_type': {'name': 'template_type', 'value': 'list', 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'type': {'name': 'type', 'value': 'template', 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}}, 'enum': None, 'type': 'object'}, 'recipient': {'name': 'recipient', 'value': {'id': {'name': 'id', 'value': None, 'enum': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'value': None, 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'value': None, 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}, 'sender_action': {'name': 'sender_action', 'value': None, 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template', 'type': 'object'}, 'value': {'message': {'name': 'message', 'value': {'attachment': {'name': 'attachment', 'value': None, 'enum': None, 'type': 'object'}, 'text': {'name': 'text', 'value': None, 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'recipient': {'name': 'recipient', 'value': {'id': {'name': 'id', 'value': None, 'enum': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'value': None, 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'value': None, 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}, 'sender_action': {'name': 'sender_action', 'value': None, 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions'}
    CONFIG = {'class_name': 'Message', 'mapping': {'recipient': 'recipient.id', 'text': 'message.text', 'action': 'sender_action'}, 'schema': 'message'}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions'
    def __init__(self,  recipient = None,  text = None,  action = None, ):

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
    def text(self):
        return self.__getattr__('text')

    @text.setter
    def text(self, value):
        self.__setattr__('text', value)
    
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
class QuickReplyBase (FactoryBase):

    SCHEMA =  {'value': {'payload': {'name': 'payload', 'value': None, 'enum': None, 'type': 'string'}, 'content_type': {'name': 'content_type', 'value': None, 'enum': ['text', 'location'], 'type': 'enum'}, 'title': {'name': 'title', 'value': None, 'enum': None, 'type': 'string'}, 'image_url': {'name': 'image_url', 'value': None, 'enum': None, 'type': 'string'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/quick-replies', 'type': 'object', 'location': {'value': {'content_type': {'name': 'content_type', 'value': 'location', 'enum': None, 'type': 'string'}}, 'type': 'object'}}
    CONFIG = {'class_name': 'QuickReply', 'mapping': {'payload': 'payload', 'content_type': 'content_type', 'title': 'title', 'image_url': 'image_url'}, 'schema': 'quickreply'}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/quick-replies'
    def __init__(self,  payload = None,  content_type = None,  title = None,  image_url = None, ):

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
    def image_url(self):
        return self.__getattr__('image_url')

    @image_url.setter
    def image_url(self, value):
        self.__setattr__('image_url', value)
    

    class CONTENT_TYPE:
        TEXT = 'text'
        LOCATION = 'location'
class QuickReplyMessageBase (FactoryBase):

    SCHEMA =  {'value': {'message': {'name': 'message', 'value': {'quick_replies': {'name': 'quick_replies', 'value': [], 'enum': None, 'type': 'list'}, 'text': {'name': 'text', 'value': None, 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'recipient': {'name': 'recipient', 'value': {'id': {'name': 'id', 'value': None, 'enum': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'value': None, 'enum': None, 'type': 'string'}}, 'enum': None, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'value': None, 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'type': 'enum'}, 'sender_action': {'name': 'sender_action', 'value': None, 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'type': 'enum'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions', 'type': 'object'}
    CONFIG = {'class_name': 'QuickReplyMessage', 'mapping': {'recipient': 'recipient.id', 'text': 'message.text', 'quick_replies': 'message.quick_replies'}, 'schema': 'quickreply.message'}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions'
    def __init__(self,  recipient = None,  text = None,  quick_replies = None, ):

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
    def text(self):
        return self.__getattr__('text')

    @text.setter
    def text(self, value):
        self.__setattr__('text', value)
    
    @property
    def quick_replies(self):
        return self.__getattr__('quick_replies')

    @quick_replies.setter
    def quick_replies(self, value):
        self.__setattr__('quick_replies', value)
    

class CallButtonBase (FactoryBase):

    SCHEMA =  {'value': {'payload': {'name': 'payload', 'value': None, 'enum': None, 'type': 'string'}, 'title': {'name': 'title', 'value': None, 'enum': None, 'type': 'string'}, 'type': {'name': 'type', 'value': 'phone_number', 'enum': None, 'type': 'string'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/call-button', 'type': 'object'}
    CONFIG = {'class_name': 'CallButton', 'mapping': {'payload': 'payload', 'title': 'title', 'type': 'type'}, 'schema': 'call.button'}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/call-button'
    def __init__(self,  payload = None,  title = None,  type = None, ):

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
    

class PostBackButtonBase (FactoryBase):

    SCHEMA =  {'value': {'payload': {'name': 'payload', 'value': None, 'enum': None, 'type': 'string'}, 'title': {'name': 'title', 'value': None, 'enum': None, 'type': 'string'}, 'type': {'name': 'type', 'value': 'postback', 'enum': None, 'type': 'string'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/postback-button', 'type': 'object'}
    CONFIG = {'class_name': 'PostBackButton', 'mapping': {'payload': 'payload', 'title': 'title', 'type': 'type'}, 'schema': 'postback.button'}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/postback-button'
    def __init__(self,  payload = None,  title = None,  type = None, ):

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
    

class ShareButtonBase (FactoryBase):

    SCHEMA =  {'value': {'type': {'name': 'type', 'value': 'element_share', 'enum': None, 'type': 'string'}}, '_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/share-button', 'type': 'object'}
    CONFIG = {'class_name': 'ShareButton', 'mapping': {'type': 'type'}, 'schema': 'share.button'}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/share-button'
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

    SCHEMA =  {'value': {'fallback_url': {'name': 'fallback_url', 'value': None, 'enum': None, 'type': 'string'}, 'url': {'name': 'url', 'value': None, 'enum': None, 'type': 'string'}, 'title': {'name': 'title', 'value': None, 'enum': None, 'type': 'string'}, 'messenger_extensions': {'name': 'messenger_extensions', 'value': None, 'enum': None, 'type': 'boolean'}, 'type': {'name': 'type', 'value': 'web_url', 'enum': None, 'type': 'string'}, 'webview_height_ratio': {'name': 'webview_height_ratio', 'value': None, 'enum': ['compact', 'tall', 'full'], 'type': 'enum'}}, 'type': 'object'}
    CONFIG = {'class_name': 'UrlButton', 'mapping': {'fallback_url': 'fallback_url', 'url': 'url', 'title': 'title', 'messenger_extensions': 'messenger_extensions', 'type': 'type', 'webview_height_ratio': 'webview_height_ratio'}, 'schema': 'url.button'}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform'
    def __init__(self,  fallback_url = None,  url = None,  title = None,  messenger_extensions = None,  type = None,  webview_height_ratio = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def fallback_url(self):
        return self.__getattr__('fallback_url')

    @fallback_url.setter
    def fallback_url(self, value):
        self.__setattr__('fallback_url', value)
    
    @property
    def url(self):
        return self.__getattr__('url')

    @url.setter
    def url(self, value):
        self.__setattr__('url', value)
    
    @property
    def title(self):
        return self.__getattr__('title')

    @title.setter
    def title(self, value):
        self.__setattr__('title', value)
    
    @property
    def messenger_extensions(self):
        return self.__getattr__('messenger_extensions')

    @messenger_extensions.setter
    def messenger_extensions(self, value):
        self.__setattr__('messenger_extensions', value)
    
    @property
    def type(self):
        return self.__getattr__('type')

    @type.setter
    def type(self, value):
        self.__setattr__('type', value)
    
    @property
    def webview_height_ratio(self):
        return self.__getattr__('webview_height_ratio')

    @webview_height_ratio.setter
    def webview_height_ratio(self, value):
        self.__setattr__('webview_height_ratio', value)
    

    class WEBVIEW_HEIGHT_RATIO:
        COMPACT = 'compact'
        TALL = 'tall'
        FULL = 'full'



##############  GENERATED MODELS END  ##############
##############          Eggwise       ############################          Eggwise       ##############
############## GENERATED MODELS START ##############





class ValidationError(Exception):
    pass


class Utils():
    @staticmethod
    def _get_super_args(locals):
        super_args = {}

        for k, v in locals.items():
            if k.startswith('__'):
                continue
            if k == 'self':
                continue
            super_args[k] = v
        return super_args


class ActionMessage(ActionMessageBase):
    def __init__(self,  recipient = None,  action = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass


class CallButton(CallButtonBase):
    def __init__(self,  payload = None,  title = None,  type = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass


class GenericElement(GenericElementBase):
    def __init__(self,  title = None,  image_url = None,  subtitle = None,  item_url = None,  default_action = None,  buttons = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass


class GenericTemplate(GenericTemplateBase):
    def __init__(self,  payload = None,  type = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass


class GenericTemplateMessage(GenericTemplateMessageBase):
    def __init__(self,  recipient = None,  elements = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass


class ListElement(ListElementBase):
    def __init__(self,  default_action = None,  title = None,  image_url = None,  subtitle = None,  buttons = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass


class ListTemplate(ListTemplateBase):
    def __init__(self,  payload = None,  type = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass


class ListTemplateMessage(ListTemplateMessageBase):
    def __init__(self,  recipient = None,  elements = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass


class Message(MessageBase):
    def __init__(self,  recipient = None,  text = None,  action = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        if self.text is None and self.action is None:
            msg = 'Non action message needs text'
            self.raise_validation_error(msg)


class PostBackButton(PostBackButtonBase):
    def __init__(self,  payload = None,  title = None,  type = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        if self.title is None:
            self.raise_validation_error('PostBackButton needs a title')
        if self.payload is None:
            self.raise_validation_error('PostBackButton needs a payload')
        pass


class QuickReply(QuickReplyBase):
    def __init__(self,  payload = None,  content_type = None,  title = None,  image_url = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)

        # default value
        if self.content_type is None:
            self.content_type = self.CONTENT_TYPE.TEXT

        self.validate()

    def validate(self):

        if self.content_type is None:
            self.raise_validation_error('Quickreply must have a content type')

        if self.title is None:
            self.raise_validation_error('No title for quick reply')


        if self.content_type == self.CONTENT_TYPE.TEXT:
            if self.payload is None:
                self.raise_validation_error('Text QuickReply needs a payload')


class QuickReplyMessage(QuickReplyMessageBase):
    def __init__(self,  recipient = None,  text = None,  quick_replies = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass


class ShareButton(ShareButtonBase):
    def __init__(self,  type = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass


class UrlButton(UrlButtonBase):
    def __init__(self,  fallback_url = None,  url = None,  title = None,  messenger_extensions = None,  type = None,  webview_height_ratio = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass