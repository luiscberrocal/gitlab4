from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel


class ProjectVariable(BaseModel):
    variable_type: str
    key: str
    value: str
    protected: bool
    masked: bool
    raw: bool
    environment_scope: str
    description: str | None
