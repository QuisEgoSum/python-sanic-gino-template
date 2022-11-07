from pydantic import BaseModel, BaseConfig


class Schema(BaseModel):

    class Config(BaseConfig):
        error_msg_templates = {
            # 'value_error.missing': ''
        }
