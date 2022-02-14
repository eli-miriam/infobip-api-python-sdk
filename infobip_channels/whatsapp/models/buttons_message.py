from enum import Enum
from typing import Literal, Optional, Union

from pydantic import AnyHttpUrl, conlist, constr, validator

from infobip_channels.whatsapp.models.core import (
    CamelCaseModel,
    MessageBody,
    ValidateUrlLengthMixin,
)


class ButtonTypeEnum(str, Enum):
    REPLY = "REPLY"


class Footer(CamelCaseModel):
    text: constr(min_length=1, max_length=60)


class HeaderDocument(ValidateUrlLengthMixin, CamelCaseModel):
    type: Literal["DOCUMENT"]
    media_url: AnyHttpUrl
    filename: Optional[constr(max_length=240)] = None

    @validator("media_url", pre=True)
    def validate_url_length(cls, value: str) -> str:
        return super().validate_url_length(value)


class HeaderVideo(ValidateUrlLengthMixin, CamelCaseModel):
    type: Literal["VIDEO"]
    media_url: AnyHttpUrl

    @validator("media_url", pre=True)
    def validate_url_length(cls, value: str) -> str:
        return super().validate_url_length(value)


class HeaderImage(ValidateUrlLengthMixin, CamelCaseModel):
    type: Literal["IMAGE"]
    media_url: AnyHttpUrl

    @validator("media_url", pre=True)
    def validate_url_length(cls, value: str) -> str:
        return super().validate_url_length(value)


class HeaderText(CamelCaseModel):
    type: Literal["TEXT"]
    text: constr(min_length=1, max_length=60)


class Button(CamelCaseModel):
    type: ButtonTypeEnum
    id: constr(min_length=1, max_length=256)
    title: constr(min_length=1, max_length=20)


class Action(CamelCaseModel):
    buttons: conlist(Button, min_items=1, max_items=3)


class Body(CamelCaseModel):
    text: constr(min_length=1, max_length=1024)


class Content(CamelCaseModel):
    body: Body
    action: Action
    header: Optional[Union[HeaderText, HeaderImage, HeaderDocument, HeaderVideo]] = None
    footer: Optional[Footer] = None


class ButtonsMessageBody(MessageBody):
    content: Content