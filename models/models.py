##############          Eggwise       ##############
############## GENERATED MODELS START ##############


from facebook_messenger_api.models.base import *


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
    def __init__(self,  type = None,  payload = None,  title = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass


class GenericElement(GenericElementBase):
    def __init__(self,  subtitle = None,  title = None,  buttons = None,  default_action = None,  image_url = None,  item_url = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass



class GenericTemplateMessage(GenericTemplateMessageBase):
    def __init__(self,  elements = None,  recipient = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass


class ListElement(ListElementBase):
    def __init__(self,  image_url = None,  subtitle = None,  title = None,  buttons = None,  default_action = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        if len(self.buttons) > 1:
            self.raise_validation_error('Too many buttons for list element, max is 1')

        # TODO
        pass


class ListTemplateMessage(ListTemplateMessageBase):
    def __init__(self,  elements = None,  buttons = None,  recipient = None,  top_element_style = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()


    def validate(self):
        if len(self.elements) < 2:
            self.raise_validation_error('Too few elements, min 2, max 4')
        if len(self.elements) > 4:
            self.raise_validation_error('Too many elements, max 4, min 2')
        if len(self.buttons) > 1:
            self.raise_validation_error('Too many many global buttons, max 1')

#TODO figure out how to add properties
    # @property
    # def global_button(self):
    #     if len(self.buttons) == 0:
    #         return None
    #     return self.buttons[0]
    #
    # @global_button.setter
    # def global_button(self, value):
    #     print('set global button')
    #     if self.buttons is None:
    #         self.buttons = []
    #     self.buttons[1] = value


class Message(MessageBase):
    def __init__(self,  recipient = None,  action = None,  text = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        if self.text is None and self.action is None:
            msg = 'Non action message needs text'
            self.raise_validation_error(msg)


class PostBackButton(PostBackButtonBase):
    def __init__(self,  type = None,  payload = None,  title = None, ):
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
    def __init__(self,  image_url = None,  payload = None,  content_type = None,  title = None, ):
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
    def __init__(self,  title = None,  type = None,  webview_height_ratio = None,  url = None,  fallback_url = None,  messenger_extensions = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass