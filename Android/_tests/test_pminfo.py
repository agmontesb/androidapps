# -*- coding: utf-8 -*-
import importlib
import pytest

from Android.Os.Parcel import Parcel
from Android.content.pm.ActivityInfo import ActivityInfo
from Android.content.pm.PackageItemInfo import PackageItemInfo
from Android.content.pm.ApplicationInfo import ApplicationInfo
from Android.content.pm.ComponentInfo import ComponentInfo
from Android.content.pm.ProviderInfo import ProviderInfo

itemInfoData = [
    ('banner', 1001),
    ('icon', 1002),
    ('labelRes', 1003),
    ('logo', 1004),
    ('metaData', None),
    ('name', 'iteminfodata'),
    ('nonLocalizedLabel', 'label not localized'),
    ('packageName', 'Mi prueba'),
    ('_unclassifiedFields', None),
]

appInfoData = [
    ('appComponentFactory', 'app component factory'),
    ('backupAgentName', 'Este es el backup agent'),
    ('category', 3001),
    ('className', 'Esta es el class name'),
    ('compatibleWidthLimitDp', 3002),
    ('dataDir', 'data/dir/for/the/application'),
    ('descriptionRes', 3003),
    ('deviceProtectedDataDir', '/device/protected/data/dir'),
    ('enabled', False),
    ('flags', 3004),
    ('largestWidthLimitDp', 3005),
    ('manageSpaceActivityName', 'manage Space Activity Name'),
    ('minSdkVersion', 3006),
    ('nativeLibraryDir', 'native Library Dir'),
    ('permission', 'Permission'),
    ('processName', 'Process Name'),
    ('publicSourceDir', '/public/Source/Dir'),
    ('requiresSmallestWidthDp', 3007),
    ('sharedLibraryFiles', ['shared/lib/1', 'shared/lib/2']),
    ('sourceDir', '/source/Dir'),
    ('splitNames', ['/split/Name/1', '/split/Name/2', '/split/Name/3']),
    ('splitPublicSourceDirs', ['/split/Public/Source/Dirs']),
    ('splitSourceDirs', ['/splitSource/Dir/1', '/splitSource/Dir/20']),
    ('storageUuid', 3008),
    ('targetSdkVersion', 3009),
    ('taskAffinity', 'Task Affinity'),
    ('theme', 3010),
    ('uiOptions', 3011),
    ('uid', 3012)
]

componentInfoData = [
    ('applicationInfo', None),
    ('descriptionRes', 2001),
    ('directBootAware', False),
    ('enabled', True),
    ('exported', True),
    ('processName', 'Este process name'),
    ('splitName', 'Split Name 2000')
]

activityInfoData = [
    ('colorMode', 5001),
    ('configChanges', 5002),
    ('documentLaunchMode', 5003),
    ('flags', 5004),
    ('launchMode', 5005),
    ('maxRecents', 5006),
    ('parentActivityName', 'Parent Activity Name'),
    ('permission', 'Permission'),
    ('persistableMode', 5007),
    ('screenOrientation', 5008),
    ('softInputMode', 5009),
    ('targetActivity', 'Target Activity'),
    ('taskAffinity', 'Task Affinity'),
    ('theme', 5010),
    ('uiOptions', 5011),
]

providerInfoData = [
    ('authority', 'Authority'),
    ('flags', 6001),
    ('grantUriPermissions', True),
    ('initOrder', 6002),
    ('isSyncable', False),
    ('multiprocess', True),
    ('pathPermissions', [None, None]),
    ('readPermission', 'Read Permission'),
    ('uriPermissionPatterns', [None, None, None]),
    ('writePermission', 'Write Permission'),
]

@pytest.fixture
def componentInfo(request):
    def _componentInfo(componentType, varsc):
        aclassname = getattr(request.module, componentType, None)
        if aclassname is None:
            raise Exception('Not a known component')
        componente = aclassname()
        map(lambda x: setattr(componente, x[0], x[1]), varsc)
        return componente
    return _componentInfo

def test_componentInfo_creation(componentInfo):
    infoData = [
        ('PackageItemInfo', itemInfoData),
        ('ApplicationInfo', itemInfoData + appInfoData),
        ('ComponentInfo', itemInfoData + componentInfoData),
        ('ActivityInfo', itemInfoData + componentInfoData + activityInfoData),
        ('ProviderInfo', itemInfoData + componentInfoData + providerInfoData),
    ]
    for aclassname, varsc in infoData:
        obj = componentInfo(aclassname, varsc)
        cls = obj.__class__
        newobj = cls(obj)
        assert all(map(lambda x: getattr(newobj, x[0]) == x[1], varsc))
    pass

def test_ComponentInfo(componentInfo):
    appInfo = componentInfo('ApplicationInfo', itemInfoData + appInfoData)
    actInfo = componentInfo('ActivityInfo', componentInfoData + activityInfoData)
    actInfo.applicationInfo = appInfo

    for attr in ['banner', 'icon', 'logo']:
        method = 'get%sResource' % attr.title()
        assert getattr(actInfo, attr) == 0, 'ERROR: ComponentInfo.%s, retrieving' % attr
        assert getattr(actInfo, method)() == getattr(appInfo, attr), 'ERROR: ComponentInfo.%s' % method

        setattr(actInfo, attr, 2456)
        assert getattr(actInfo, method)() == 2456, 'ERROR: ComponentInfo.%s' % method

    appInfo.enabled = True
    actInfo.enabled = True
    assert actInfo.isEnabled(), 'ERROR: ApplicationInfo Enabled, ActivityInfo Enabled'
    actInfo.enabled = False
    assert not actInfo.isEnabled(), 'ERROR: ApplicationInfo Enabled, ActivityInfo NOT Enabled'
    appInfo.enabled = False
    actInfo.enabled = True
    assert not actInfo.isEnabled(), 'ERROR: ApplicationInfo not Enabled, ActivityInfo Enabled'
    actInfo.enabled = False
    assert not actInfo.isEnabled(), 'ERROR: ApplicationInfo not Enabled, ActivityInfo NOT Enabled'

