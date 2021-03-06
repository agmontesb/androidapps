import pytest

from Android.content.Intent import Intent
from Android.content.Intent import ACTION_MAIN, ACTION_VIEW, ACTION_PICK
from Android.content.Intent import ACTION_GET_CONTENT, ACTION_EDIT, ACTION_INSERT
from Android.content.Intent import CATEGORY_LAUNCHER, CATEGORY_DEFAULT
from Android.content.IntentFilter import IntentFilter
from Android.content.IntentFilter import MATCH_CATEGORY_MASK, NO_MATCH_ACTION
from Android.Uri import Uri

manifestStr = \
'''<manifest xmlns:android="http://schemas.android.com/apk/res/android"
       package="com.android.notepad">
     <application android:icon="@drawable/app_notes"
             android:label="@string/app_name">

         <provider class=".NotePadProvider"
                 android:authorities="com.google.provider.NotePad" />

         <activity class=".NotesList" android:label="@string/title_notes_list">
             <intent-filter>
                 <action android:name="android.intent.action.MAIN" />
                 <category android:name="android.intent.category.LAUNCHER" />
             </intent-filter>
             <intent-filter>
                 <action android:name="android.intent.action.VIEW" />
                 <action android:name="android.intent.action.EDIT" />
                 <action android:name="android.intent.action.PICK" />
                 <category android:name="android.intent.category.DEFAULT" />
                 <data android:mimeType="vnd.android.cursor.dir/vnd.google.note" />
             </intent-filter>
             <intent-filter>
                 <action android:name="android.intent.action.GET_CONTENT" />
                 <category android:name="android.intent.category.DEFAULT" />
                 <data android:mimeType="vnd.android.cursor.item/vnd.google.note" />
             </intent-filter>
         </activity>

         <activity class=".NoteEditor" android:label="@string/title_note">
             <intent-filter android:label="@string/resolve_edit">
                 <action android:name="android.intent.action.VIEW" />
                 <action android:name="android.intent.action.EDIT" />
                 <category android:name="android.intent.category.DEFAULT" />
                 <data android:mimeType="vnd.android.cursor.item/vnd.google.note" />
             </intent-filter>

             <intent-filter>
                 <action android:name="android.intent.action.INSERT" />
                 <category android:name="android.intent.category.DEFAULT" />
                 <data android:mimeType="vnd.android.cursor.dir/vnd.google.note" />
             </intent-filter>

         </activity>

         <activity class=".TitleEditor" android:label="@string/title_edit_title"
                 android:theme="@android:style/Theme.Dialog">
             <intent-filter android:label="@string/resolve_title">
                 <action android:name="com.android.notepad.action.EDIT_TITLE" />
                 <category android:name="android.intent.category.DEFAULT" />
                 <category android:name="android.intent.category.ALTERNATIVE" />
                 <category android:name="android.intent.category.SELECTED_ALTERNATIVE" />
                 <data android:mimeType="vnd.android.cursor.item/vnd.google.note" />
             </intent-filter>
         </activity>

     </application>
 </manifest>'''

import xml.etree.ElementTree as ET
import StringIO
NS_MAP = "xmlns:map"


class ContentResolver(object):

    def getType(self, data):
        try:
            scheme = data.getScheme()
            if scheme == 'content':
                try:
                    int(data.getLastPathSegment())
                    return "vnd.android.cursor.item/*"
                except:
                    return "vnd.android.cursor.dir/*"
        except:
            pass


resolver = ContentResolver()


def parse_nsmap(file):
    events = "start", "start-ns", "end-ns"
    root = None
    ns_map = []
    for event, elem in ET.iterparse(file, events):
        if event == "start-ns":
            ns_map.append(elem)
        elif event == "end-ns":
            ns_map.pop()
        elif event == "start":
            if root is None:
                root = elem
            elem.set(NS_MAP, dict(ns_map))
    return ET.ElementTree(root)


def getMatchFilters(intentFilters, action, mimetype=None, data=None, category=None):
    intent = Intent(action)
    if category: intent.addCategory(category)
    if data:
        intent.setDataAndTypeAndNormalize(data, mimetype)
    else: intent.setTypeAndNormalize(mimetype)
    matches = []
    for k, intentfilter in enumerate(intentFilters):
        result = intentfilter.match(resolver, intent, True, '')
        if result < 0: continue
        matches.append(k)
    return matches


@pytest.fixture(scope='module')
def intentFiltersXml():
    fd = StringIO.StringIO(manifestStr)
    manifest =  parse_nsmap(fd).getroot()
    return manifest.findall('.//intent-filter')


@pytest.fixture(scope='module')
def intentFilters(intentFiltersXml):
    filters = []
    for filterXml in intentFiltersXml:
        filter = IntentFilter()
        filter.readFromXml(filterXml)
        filters.append(filter)
    return filters


def test_filterActionCategory(intentFilters):
    anIntentFilter = intentFilters[0]
    anAction = ACTION_MAIN
    aCategory = CATEGORY_LAUNCHER
    assert anIntentFilter.countActions() == 1, 'countActions: Bad countActions'
    assert anIntentFilter.getAction(0) == anAction, 'getAction: Bad action on index'
    assert anIntentFilter.countCategories() == 1, 'countCategories: Bad countCategories'
    assert anIntentFilter.getCategory(0) == aCategory, 'getCategory: Bad action on index'
    assert not anIntentFilter.hasDataPath('/'), 'hasDataPath: Bad hasDataPath'
    assert anIntentFilter.matchAction(anAction), 'matchAction: Not returning True'
    assert not anIntentFilter.matchAction('a' + anAction), 'matchAction: Not returning False'
    assert anIntentFilter.matchCategories([aCategory,]) is None, 'matchCategories: Not returning True'
    assert anIntentFilter.matchCategories([]) is None, 'matchCategories: Not returning True'
    assert anIntentFilter.matchCategories([aCategory, 'a' + aCategory]) == 'a' + aCategory, 'matchCategories: Not returning False'


def test_filterData(intentFilters):
    anIntentFilter = intentFilters[1]
    assert anIntentFilter.countActions() == 3, 'countActions: Bad countActions'
    required = ['android.intent.action.VIEW',
                'android.intent.action.EDIT',
                'android.intent.action.PICK']
    dataType = "vnd.android.cursor.dir/vnd.google.note"
    assert list(anIntentFilter.actionsIterator()) == required, 'actionsIterator: Bad actionsIterator'
    assert anIntentFilter.hasDataType(dataType), 'hasDataType: Bad hasDataType'
    assert anIntentFilter.countDataTypes() > 0, 'countDataTypes: Bad countDataTypes'
    assert anIntentFilter.getDataType(0) == dataType, "getDataType: Bad getDataType"


def test_filterResolution(intentFilters):
    action = ACTION_MAIN
    matches = getMatchFilters(intentFilters, action)
    assert matches == [0], 'match: Not match'

    action = ACTION_MAIN
    category = CATEGORY_LAUNCHER
    matches = getMatchFilters(intentFilters, action, category=category)
    assert matches == [0], 'match: Not match'

    action = ACTION_VIEW
    data = Uri.parse('content://com.google.provider.NotePad/notes')
    categories = ''
    matches = getMatchFilters(intentFilters, action, data=data)
    assert matches == [1], 'match: Not match'

    action = ACTION_PICK
    data = Uri.parse('content://com.google.provider.NotePad/notes')
    matches = getMatchFilters(intentFilters, action, data=data)
    assert matches == [1], 'match: Not match'

    action = ACTION_GET_CONTENT
    mimetype = 'vnd.android.cursor.item/vnd.google.note'
    matches = getMatchFilters(intentFilters, action, mimetype=mimetype)
    assert matches == [2], 'match: Not match'

    action = ACTION_VIEW
    data = Uri.parse('content://com.google.provider.NotePad/notes/1234')
    matches = getMatchFilters(intentFilters, action, data=data)
    assert matches == [3], 'match: Not match'

    action = ACTION_EDIT
    data = Uri.parse('content://com.google.provider.NotePad/notes/1234')
    matches = getMatchFilters(intentFilters, action, data=data)
    assert matches == [3], 'match: Not match'

    action = ACTION_INSERT
    data = Uri.parse('content://com.google.provider.NotePad/notes')
    matches = getMatchFilters(intentFilters, action, data=data)
    assert matches == [4], 'match: Not match'

    action = 'com.android.notepad.action.EDIT_TITLE'
    data = Uri.parse('content://com.google.provider.NotePad/notes/1234')
    matches = getMatchFilters(intentFilters, action, data=data)
    assert matches == [5], 'match: Not match'

