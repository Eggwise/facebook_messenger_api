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
    def __init__(self,  payload = None,  type = None,  title = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass


class GenericElement(GenericElementBase):
    def __init__(self,  image_url = None,  item_url = None,  title = None,  subtitle = None,  default_action = None,  buttons = None, ):
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
    def __init__(self,  elements = None,  recipient = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass


class ListElement(ListElementBase):
    def __init__(self,  image_url = None,  title = None,  subtitle = None,  default_action = None,  buttons = None, ):
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
    def __init__(self,  elements = None,  recipient = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass


class Message(MessageBase):
    def __init__(self,  recipient = None,  action = None,  text = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        if self.text is None and self.action is None:
            msg = 'Non action message needs text'
            raise ValidationError(msg)


class PostBackButton(PostBackButtonBase):
    def __init__(self,  payload = None,  type = None,  title = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        if self.title is None:
            raise ValidationError('PostBackButton needs a title')
        if self.payload is None:
            raise ValidationError('PostBackButton needs a payload')
        pass


class QuickReply(QuickReplyBase):
    def __init__(self,  image_url = None,  content_type = None,  title = None,  payload = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)

        # default value
        if self.content_type is None:
            self.content_type = self.CONTENT_TYPE.TEXT

        self.validate()

    def validate(self):

        if self.content_type is None:
            raise ValidationError('Quickreply must have a content type')

        if self.title is None:
            raise ValidationError('No title for quick reply')

        if self.content_type == self.CONTENT_TYPE.TEXT:
            if self.payload is None:
                raise ValidationError('Text QuickReply needs a payload')


class QuickReplyMessage(QuickReplyMessageBase):
    def __init__(self,  quick_replies = None,  recipient = None,  text = None, ):
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
    def __init__(self,  webview_height_ratio = None,  url = None,  fallback_url = None,  title = None,  type = None,  messenger_extensions = None, ):
        super_args = Utils._get_super_args(locals())

        super().__init__(**super_args)
        self.validate()

    def validate(self):
        # TODO
        pass