# -*- coding: utf-8 -*-
from Tools.aapt.Resource import ResourceType

def test_ParseResourceTypes():
    for name in ResourceType.types:
        type = ResourceType.parseResourceType(name)
        assert type is not None
        assert type == getattr(ResourceType, 'k' + name.title())

    type = ResourceType.parseResourceType(u"blahaha")
    assert type is None