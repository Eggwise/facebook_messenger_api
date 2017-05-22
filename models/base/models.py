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

    SCHEMA =  {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions', 'list_template': {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template', 'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'value': None, 'type': 'enum'}, 'recipient': {'name': 'recipient', 'enum': None, 'value': {'id': {'name': 'id', 'enum': None, 'value': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'value': None, 'type': 'enum'}, 'message': {'name': 'message', 'enum': None, 'value': {'attachment': {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template', 'enum': None, 'value': {'type': {'name': 'type', 'enum': None, 'value': 'template', 'type': 'string'}, 'payload': {'name': 'payload', 'enum': None, 'value': {'template_type': {'name': 'template_type', 'enum': None, 'value': 'list', 'type': 'string'}, 'top_element_style': {'name': 'top_element_style', 'enum': None, 'value': 'compact', 'type': 'string'}, 'elements': {'name': 'elements', 'enum': None, 'value': [], 'type': 'list'}}, 'type': 'object'}}, 'name': 'attachment', 'type': 'object'}}, 'type': 'object'}}, 'type': 'object'}, 'generic_template': {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template', 'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'value': None, 'type': 'enum'}, 'recipient': {'name': 'recipient', 'enum': None, 'value': {'id': {'name': 'id', 'enum': None, 'value': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'value': None, 'type': 'enum'}, 'message': {'name': 'message', 'enum': None, 'value': {'attachment': {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template', 'enum': None, 'value': {'type': {'name': 'type', 'enum': None, 'value': 'template', 'type': 'string'}, 'payload': {'name': 'payload', 'enum': None, 'value': {'template_type': {'name': 'template_type', 'enum': None, 'value': 'generic', 'type': 'string'}, 'elements': {'name': 'elements', 'enum': None, 'value': [], 'type': 'list'}}, 'type': 'object'}}, 'name': 'attachment', 'type': 'object'}}, 'type': 'object'}}, 'type': 'object'}, 'type': 'object', 'quickreply': {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions', 'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'value': None, 'type': 'enum'}, 'recipient': {'name': 'recipient', 'enum': None, 'value': {'id': {'name': 'id', 'enum': None, 'value': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'value': None, 'type': 'enum'}, 'message': {'name': 'message', 'enum': None, 'value': {'quick_replies': {'name': 'quick_replies', 'enum': None, 'value': [], 'type': 'list'}, 'text': {'name': 'text', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}}, 'type': 'object'}, 'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'value': None, 'type': 'enum'}, 'recipient': {'name': 'recipient', 'enum': None, 'value': {'id': {'name': 'id', 'enum': None, 'value': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'value': None, 'type': 'enum'}, 'message': {'name': 'message', 'enum': None, 'value': {'attachment': {'name': 'attachment', 'enum': None, 'value': None, 'type': 'object'}, 'text': {'name': 'text', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}}}
    CONFIG = {'schema': 'message', 'class_name': 'ActionMessage', 'mapping': {'recipient': 'recipient.id', 'action': 'sender_action'}}
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

    SCHEMA =  {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template', 'value': {'buttons': {'name': 'buttons', 'enum': None, 'value': [], 'type': 'list'}, 'item_url': {'name': 'item_url', 'enum': None, 'value': None, 'type': 'string'}, 'image_url': {'name': 'image_url', 'enum': None, 'value': None, 'type': 'string'}, 'default_action': {'name': 'default_action', 'enum': None, 'value': None, 'type': 'string'}, 'title': {'name': 'title', 'enum': None, 'value': None, 'type': 'string'}, 'subtitle': {'name': 'subtitle', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}
    CONFIG = {'schema': 'generic.element', 'class_name': 'GenericElement', 'mapping': {'buttons': 'buttons', 'item_url': 'item_url', 'image_url': 'image_url', 'default_action': 'default_action', 'title': 'title', 'subtitle': 'subtitle'}}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template'
    def __init__(self,  buttons = None,  item_url = None,  image_url = None,  default_action = None,  title = None,  subtitle = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def buttons(self):
        return self.__getattr__('buttons')

    @buttons.setter
    def buttons(self, value):
        self.__setattr__('buttons', value)
    
    @property
    def item_url(self):
        return self.__getattr__('item_url')

    @item_url.setter
    def item_url(self, value):
        self.__setattr__('item_url', value)
    
    @property
    def image_url(self):
        return self.__getattr__('image_url')

    @image_url.setter
    def image_url(self, value):
        self.__setattr__('image_url', value)
    
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
    def subtitle(self):
        return self.__getattr__('subtitle')

    @subtitle.setter
    def subtitle(self, value):
        self.__setattr__('subtitle', value)
    

class GenericTemplateMessageBase (FactoryBase):

    SCHEMA =  {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template', 'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'value': None, 'type': 'enum'}, 'recipient': {'name': 'recipient', 'enum': None, 'value': {'id': {'name': 'id', 'enum': None, 'value': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'value': None, 'type': 'enum'}, 'message': {'name': 'message', 'enum': None, 'value': {'attachment': {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template', 'enum': None, 'value': {'type': {'name': 'type', 'enum': None, 'value': 'template', 'type': 'string'}, 'payload': {'name': 'payload', 'enum': None, 'value': {'template_type': {'name': 'template_type', 'enum': None, 'value': 'generic', 'type': 'string'}, 'elements': {'name': 'elements', 'enum': None, 'value': [], 'type': 'list'}}, 'type': 'object'}}, 'name': 'attachment', 'type': 'object'}}, 'type': 'object'}}, 'type': 'object'}
    CONFIG = {'schema': 'generic_template.message', 'class_name': 'GenericTemplateMessage', 'mapping': {'recipient': 'recipient.id', 'elements': 'message.attachment.payload.elements'}}
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

    SCHEMA =  {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template', 'value': {'buttons': {'name': 'buttons', 'enum': None, 'value': [], 'type': 'list'}, 'subtitle': {'name': 'subtitle', 'enum': None, 'value': None, 'type': 'string'}, 'default_action': {'name': 'default_action', 'enum': None, 'value': None, 'type': 'string'}, 'title': {'name': 'title', 'enum': None, 'value': None, 'type': 'string'}, 'image_url': {'name': 'image_url', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}
    CONFIG = {'schema': 'list.element', 'class_name': 'ListElement', 'mapping': {'buttons': 'buttons', 'image_url': 'image_url', 'default_action': 'default_action', 'title': 'title', 'subtitle': 'subtitle'}}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template'
    def __init__(self,  buttons = None,  image_url = None,  default_action = None,  title = None,  subtitle = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def buttons(self):
        return self.__getattr__('buttons')

    @buttons.setter
    def buttons(self, value):
        self.__setattr__('buttons', value)
    
    @property
    def image_url(self):
        return self.__getattr__('image_url')

    @image_url.setter
    def image_url(self, value):
        self.__setattr__('image_url', value)
    
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
    def subtitle(self):
        return self.__getattr__('subtitle')

    @subtitle.setter
    def subtitle(self, value):
        self.__setattr__('subtitle', value)
    

class ListTemplateMessageBase (FactoryBase):

    SCHEMA =  {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template', 'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'value': None, 'type': 'enum'}, 'recipient': {'name': 'recipient', 'enum': None, 'value': {'id': {'name': 'id', 'enum': None, 'value': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'value': None, 'type': 'enum'}, 'message': {'name': 'message', 'enum': None, 'value': {'attachment': {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template', 'enum': None, 'value': {'type': {'name': 'type', 'enum': None, 'value': 'template', 'type': 'string'}, 'payload': {'name': 'payload', 'enum': None, 'value': {'template_type': {'name': 'template_type', 'enum': None, 'value': 'list', 'type': 'string'}, 'top_element_style': {'name': 'top_element_style', 'enum': None, 'value': 'compact', 'type': 'string'}, 'elements': {'name': 'elements', 'enum': None, 'value': [], 'type': 'list'}}, 'type': 'object'}}, 'name': 'attachment', 'type': 'object'}}, 'type': 'object'}}, 'type': 'object'}
    CONFIG = {'schema': 'list_template.message', 'class_name': 'ListTemplateMessage', 'mapping': {'recipient': 'recipient.id', 'top_element_style': 'message.attachment.payload.top_element_style', 'elements': 'message.attachment.payload.elements'}}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template'
    def __init__(self,  recipient = None,  top_element_style = None,  elements = None, ):

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
    def top_element_style(self):
        return self.__getattr__('top_element_style')

    @top_element_style.setter
    def top_element_style(self, value):
        self.__setattr__('top_element_style', value)
    
    @property
    def elements(self):
        return self.__getattr__('elements')

    @elements.setter
    def elements(self, value):
        self.__setattr__('elements', value)
    

class MessageBase (FactoryBase):

    SCHEMA =  {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions', 'list_template': {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template', 'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'value': None, 'type': 'enum'}, 'recipient': {'name': 'recipient', 'enum': None, 'value': {'id': {'name': 'id', 'enum': None, 'value': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'value': None, 'type': 'enum'}, 'message': {'name': 'message', 'enum': None, 'value': {'attachment': {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template', 'enum': None, 'value': {'type': {'name': 'type', 'enum': None, 'value': 'template', 'type': 'string'}, 'payload': {'name': 'payload', 'enum': None, 'value': {'template_type': {'name': 'template_type', 'enum': None, 'value': 'list', 'type': 'string'}, 'top_element_style': {'name': 'top_element_style', 'enum': None, 'value': 'compact', 'type': 'string'}, 'elements': {'name': 'elements', 'enum': None, 'value': [], 'type': 'list'}}, 'type': 'object'}}, 'name': 'attachment', 'type': 'object'}}, 'type': 'object'}}, 'type': 'object'}, 'generic_template': {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template', 'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'value': None, 'type': 'enum'}, 'recipient': {'name': 'recipient', 'enum': None, 'value': {'id': {'name': 'id', 'enum': None, 'value': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'value': None, 'type': 'enum'}, 'message': {'name': 'message', 'enum': None, 'value': {'attachment': {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template', 'enum': None, 'value': {'type': {'name': 'type', 'enum': None, 'value': 'template', 'type': 'string'}, 'payload': {'name': 'payload', 'enum': None, 'value': {'template_type': {'name': 'template_type', 'enum': None, 'value': 'generic', 'type': 'string'}, 'elements': {'name': 'elements', 'enum': None, 'value': [], 'type': 'list'}}, 'type': 'object'}}, 'name': 'attachment', 'type': 'object'}}, 'type': 'object'}}, 'type': 'object'}, 'type': 'object', 'quickreply': {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions', 'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'value': None, 'type': 'enum'}, 'recipient': {'name': 'recipient', 'enum': None, 'value': {'id': {'name': 'id', 'enum': None, 'value': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'value': None, 'type': 'enum'}, 'message': {'name': 'message', 'enum': None, 'value': {'quick_replies': {'name': 'quick_replies', 'enum': None, 'value': [], 'type': 'list'}, 'text': {'name': 'text', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}}, 'type': 'object'}, 'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'value': None, 'type': 'enum'}, 'recipient': {'name': 'recipient', 'enum': None, 'value': {'id': {'name': 'id', 'enum': None, 'value': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'value': None, 'type': 'enum'}, 'message': {'name': 'message', 'enum': None, 'value': {'attachment': {'name': 'attachment', 'enum': None, 'value': None, 'type': 'object'}, 'text': {'name': 'text', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}}}
    CONFIG = {'schema': 'message', 'class_name': 'Message', 'mapping': {'recipient': 'recipient.id', 'text': 'message.text', 'action': 'sender_action'}}
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

    SCHEMA =  {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/quick-replies', 'value': {'image_url': {'name': 'image_url', 'enum': None, 'value': None, 'type': 'string'}, 'payload': {'name': 'payload', 'enum': None, 'value': None, 'type': 'string'}, 'title': {'name': 'title', 'enum': None, 'value': None, 'type': 'string'}, 'content_type': {'name': 'content_type', 'enum': ['text', 'location'], 'value': None, 'type': 'enum'}}, 'location': {'type': 'object', 'value': {'content_type': {'name': 'content_type', 'enum': None, 'value': 'location', 'type': 'string'}}}, 'type': 'object'}
    CONFIG = {'schema': 'quickreply', 'class_name': 'QuickReply', 'mapping': {'title': 'title', 'payload': 'payload', 'image_url': 'image_url', 'content_type': 'content_type'}}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/quick-replies'
    def __init__(self,  title = None,  payload = None,  image_url = None,  content_type = None, ):

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
    def payload(self):
        return self.__getattr__('payload')

    @payload.setter
    def payload(self, value):
        self.__setattr__('payload', value)
    
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
    

    class CONTENT_TYPE:
        TEXT = 'text'
        LOCATION = 'location'
class QuickReplyMessageBase (FactoryBase):

    SCHEMA =  {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions', 'value': {'sender_action': {'name': 'sender_action', 'enum': ['typing_on', 'typing_off', 'mark_seen'], 'value': None, 'type': 'enum'}, 'recipient': {'name': 'recipient', 'enum': None, 'value': {'id': {'name': 'id', 'enum': None, 'value': None, 'type': 'string'}, 'phone_number': {'name': 'phone_number', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}, 'notification_type': {'name': 'notification_type', 'enum': ['REGULAR', 'SILENT_PUSH', 'NO_PUSH'], 'value': None, 'type': 'enum'}, 'message': {'name': 'message', 'enum': None, 'value': {'quick_replies': {'name': 'quick_replies', 'enum': None, 'value': [], 'type': 'list'}, 'text': {'name': 'text', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}}, 'type': 'object'}
    CONFIG = {'schema': 'quickreply.message', 'class_name': 'QuickReplyMessage', 'mapping': {'recipient': 'recipient.id', 'text': 'message.text', 'quick_replies': 'message.quick_replies'}}
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

    SCHEMA =  {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/call-button', 'value': {'type': {'name': 'type', 'enum': None, 'value': 'phone_number', 'type': 'string'}, 'payload': {'name': 'payload', 'enum': None, 'value': None, 'type': 'string'}, 'title': {'name': 'title', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}
    CONFIG = {'schema': 'call.button', 'class_name': 'CallButton', 'mapping': {'type': 'type', 'title': 'title', 'payload': 'payload'}}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/call-button'
    def __init__(self,  type = None,  title = None,  payload = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
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
    
    @property
    def payload(self):
        return self.__getattr__('payload')

    @payload.setter
    def payload(self, value):
        self.__setattr__('payload', value)
    

class PostBackButtonBase (FactoryBase):

    SCHEMA =  {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/postback-button', 'value': {'type': {'name': 'type', 'enum': None, 'value': 'postback', 'type': 'string'}, 'payload': {'name': 'payload', 'enum': None, 'value': None, 'type': 'string'}, 'title': {'name': 'title', 'enum': None, 'value': None, 'type': 'string'}}, 'type': 'object'}
    CONFIG = {'schema': 'postback.button', 'class_name': 'PostBackButton', 'mapping': {'type': 'type', 'title': 'title', 'payload': 'payload'}}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/postback-button'
    def __init__(self,  type = None,  title = None,  payload = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
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
    
    @property
    def payload(self):
        return self.__getattr__('payload')

    @payload.setter
    def payload(self, value):
        self.__setattr__('payload', value)
    

class ShareButtonBase (FactoryBase):

    SCHEMA =  {'_doc': 'https://developers.facebook.com/docs/messenger-platform/send-api-reference/share-button', 'value': {'type': {'name': 'type', 'enum': None, 'value': 'element_share', 'type': 'string'}}, 'type': 'object'}
    CONFIG = {'schema': 'share.button', 'class_name': 'ShareButton', 'mapping': {'type': 'type'}}
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

    SCHEMA =  {'type': 'object', 'value': {'type': {'name': 'type', 'enum': None, 'value': 'web_url', 'type': 'string'}, 'url': {'name': 'url', 'enum': None, 'value': None, 'type': 'string'}, 'fallback_url': {'name': 'fallback_url', 'enum': None, 'value': None, 'type': 'string'}, 'webview_height_ratio': {'name': 'webview_height_ratio', 'enum': ['compact', 'tall', 'full'], 'value': None, 'type': 'enum'}, 'messenger_extensions': {'name': 'messenger_extensions', 'enum': None, 'value': None, 'type': 'boolean'}, 'title': {'name': 'title', 'enum': None, 'value': None, 'type': 'string'}}}
    CONFIG = {'schema': 'url.button', 'class_name': 'UrlButton', 'mapping': {'type': 'type', 'url': 'url', 'fallback_url': 'fallback_url', 'webview_height_ratio': 'webview_height_ratio', 'messenger_extensions': 'messenger_extensions', 'title': 'title'}}
    DOC_URL = 'https://developers.facebook.com/docs/messenger-platform'
    def __init__(self,  type = None,  url = None,  fallback_url = None,  webview_height_ratio = None,  messenger_extensions = None,  title = None, ):

        _schema = copy.deepcopy(self.SCHEMA)
        _config = copy.deepcopy(self.CONFIG)
        super().__init__(_schema, _config, locals())

    
    @property
    def type(self):
        return self.__getattr__('type')

    @type.setter
    def type(self, value):
        self.__setattr__('type', value)
    
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
    def webview_height_ratio(self):
        return self.__getattr__('webview_height_ratio')

    @webview_height_ratio.setter
    def webview_height_ratio(self, value):
        self.__setattr__('webview_height_ratio', value)
    
    @property
    def messenger_extensions(self):
        return self.__getattr__('messenger_extensions')

    @messenger_extensions.setter
    def messenger_extensions(self, value):
        self.__setattr__('messenger_extensions', value)
    
    @property
    def title(self):
        return self.__getattr__('title')

    @title.setter
    def title(self, value):
        self.__setattr__('title', value)
    

    class WEBVIEW_HEIGHT_RATIO:
        COMPACT = 'compact'
        TALL = 'tall'
        FULL = 'full'



##############  GENERATED MODELS END  ##############
##############          Eggwise       ##############