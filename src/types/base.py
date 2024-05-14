from pydantic import BaseModel, ConfigDict


class DTO(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        use_enum_values=True,
        from_attributes=True,
        allow_inf_nan=False,
        ser_json_timedelta="float",
        ser_json_bytes="utf8",
        regex_engine="python-re"
    )

    