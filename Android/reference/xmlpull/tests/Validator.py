# -*- coding: utf-8 -*-
import StringIO
import xml.parsers.expat

XML_CQUANT_NONE = 0
XML_CQUANT_OPT = 1
XML_CQUANT_PLUS = 3
XML_CQUANT_REP = 2
XML_CTYPE_ANY = 2
XML_CTYPE_CHOICE = 5
XML_CTYPE_EMPTY = 1
XML_CTYPE_MIXED = 3
XML_CTYPE_NAME = 4
XML_CTYPE_SEQ = 6

REQ = 1


class ValidatorBuilder(object):

    def __init__(self, root=None):
        super(ValidatorBuilder, self).__init__()
        self._elements = {}
        if root:
            self.setRoot(root)

    def setRoot(self, root):
        self.root = root
        return self

    def setElement(self, entityname, value):
        ptype, pquant, pname, pchildren = value
        ndx = 0
        self._elements[entityname] = (ptype, pquant, entityname, ndx, pchildren)
        return self

    def build(self):
        validator = Validator()
        validator.stack = [(6, 0, 'root', 0, ((4, 0, self.root, ()),))]
        validator.elements = self._elements
        return validator


class Validator(object):
    def start_tag(self, tag):
        while True:
            ptype, pquant, pname, pndx, pchildren = self.stack[-1]
            if ptype == XML_CTYPE_EMPTY:
                raise Exception('"%s" tag, is an empty tag, "%s" tag can not be a child' % (pname, tag))
            if ptype == XML_CTYPE_ANY and self.elements.get(tag):
                break
            else:
                try:
                    ctype = pchildren[pndx][0]
                except IndexError:
                    raise Exception('All tags for "%s" has been processed' % pname)
                if ctype in [XML_CTYPE_SEQ, XML_CTYPE_CHOICE]:
                    ctype, cquant, cname, children = pchildren[pndx]
                    self.stack.append((ctype, cquant, cname, 0, children))
                else:
                    answ, pndx = self.checkStartTag(ptype, pchildren, pndx, tag)
                    if answ == -1:
                        while True:
                            ptype, pquant, pname, pndx, pchildren = self.stack[-1]
                            if pname:
                                break
                            self.stack.pop()
                        if ptype == XML_CTYPE_SEQ or \
                                (ptype == XML_CTYPE_CHOICE and pndx == len(pchildren) - 1):
                            raise Exception('Tag "%s" not in sequence or a valid option for "%s"' % (tag, pname))
                        pndx += 1
                    self.stack[-1] = (ptype, pquant, pname, pndx, pchildren)
                    if answ != -1:
                        break
        try:
            self.stack.append(self.elements[tag])
        except:
            raise Exception('Element "%s" is not defined' % tag)
        pass

    def checkStartTag(self, ptype, pchildren, pndx, tag):
        while pndx < len(pchildren):
            ctype, cquant, cname, children = pchildren[pndx]
            if cname == tag:
                if cquant in [XML_CQUANT_NONE, XML_CQUANT_OPT]:
                    answ = 1
                elif cquant == XML_CQUANT_REP:  # '*'
                    answ = 2
                elif cquant == XML_CQUANT_PLUS:  # '+'
                    answ = 3
                pndx = pndx if ptype != XML_CTYPE_MIXED else 0
                return answ, pndx
            if cquant == XML_CQUANT_PLUS:
                return -1, pndx
            if ptype == XML_CTYPE_SEQ and cquant == XML_CQUANT_NONE:
                return -1, pndx
            pndx += 1
        return -1, pndx

    def end_tag(self, tag):
        ptype, pquant, pname, pndx, pchildren = self.stack.pop()
        if pname != tag:
            raise Exception('Expecting end tag for "%s" instead receive end tag for "%s"' % (pname, tag))
        if ptype != XML_CTYPE_MIXED and pchildren[pndx:] and not all(map(lambda x: x[1] in (XML_CQUANT_OPT, XML_CQUANT_REP), pchildren[pndx:])):
            tags = ', '.join(map(lambda x: x[2], pchildren[pndx:]))
            raise Exception('Tag "%s" requires "%s" tag(s)' % (pname, tags))
        while True:
            ptype, pquant, pname, pndx, pchildren = self.stack[-1]
            if ptype == XML_CTYPE_MIXED:
                pass
            elif ptype == XML_CTYPE_CHOICE:
                pndx = len(pchildren)
            elif ptype == XML_CTYPE_SEQ:
                if pndx < len(pchildren) and pchildren[pndx][1] in [XML_CQUANT_NONE, XML_CQUANT_OPT]:
                    pndx += 1
            if pname or (pname is None and pndx < len(pchildren)):
                break
            self.stack.pop()
        self.stack[-1] = (ptype, pquant, pname, pndx, pchildren)

    def others(self, other):
        pass


builder = None
validator = None


# handler functions
def start_element(name, attrs):
    print 'Start element:', name, attrs
    pass


def end_element(name):
    print 'End element:', name
    pass


def char_data(data):
    print 'Character data:', repr(data)


def default_handler(data):
    print 'default handler', '*', data, '*'


def default_handler_expand(data):
    print 'default_handler_expand', '*', data, '*'


def xml_decl(version, encoding, standalone):
    print 'xml', version, encoding, standalone
    return 1


def start_doctype(doctypeName, systemId, publicId, has_internal_subset):
    global builder
    print 'start_doctype', doctypeName, systemId, publicId, has_internal_subset
    builder = ValidatorBuilder(doctypeName)
    return 1


def end_doctype():
    global validator, builder
    print 'end_doctype'
    validator = builder.build()
    return 1


def element(name, *model):
    print 'element', name, model
    builder.setElement(name, model)


def attlist(elname, attname, atype, default, required):
    print 'attlist', elname, attname, atype, default, required
    return 1


def processing_instruction(target, data):
    print 'processing_instruction', target, data


def unparsed_entity(entityName, base, systemId, publicId, notationName):
    print 'unparsed_entity', entityName, base, systemId, publicId, notationName


def entity(entityName, is_parameter_entity, value, base, systemId, publicId, notationName):
    print 'entity', entityName, is_parameter_entity, value, base, systemId, publicId, notationName
    return is_parameter_entity


def notation(notationName, base, systemId, publicId):
    print 'notation', notationName, base, systemId, publicId


def start_namespace(prefix, uri):
    print 'start_namespace', prefix, uri


def end_namespace(prefix):
    print 'end_namespace', (prefix)


def comment(data):
    print 'comment', (data)


def start_cdata_section():
    print 'start_cdata_section'


def end_cdata_section():
    print 'end_cdata_section'


def not_stand_alone():
    print 'not_stand_alone'
    return 0


def external_entity_ref(context, base, systemId, publicId):
    print 'external_entity_ref', context, base, systemId, publicId
    return 1


def skipped_entity(*args):
    print 'skipped_entity', args
    return 1

def initValidatorBuilder(doctypeStr):
    builder = ValidatorBuilder()
    xml_param = xml.parsers.expat.XML_PARAM_ENTITY_PARSING_ALWAYS

    p = xml.parsers.expat.ParserCreate()
    p.ordered_attributes = True
    p.UseForeignDTD(True)
    p.SetParamEntityParsing(xml_param)
    p.buffer_text = 1

    def start_doctype(doctypeName, systemId, publicId, has_internal_subset, builder=builder):
        print 'start_doctype', doctypeName, systemId, publicId, has_internal_subset
        builder.setRoot(doctypeName)
    p.StartDoctypeDeclHandler = start_doctype

    def end_doctype():
        print 'end_doctype'
    p.EndDoctypeDeclHandler = end_doctype

    def element(name, model, builder=builder):
        print 'element', name, model
        builder.setElement(name, model)
    p.ElementDeclHandler = element

    data = StringIO.StringIO(doctypeStr)
    try:
        p.ParseFile(data)
    except xml.parsers.expat.ExpatError as e:
        print 'ExpatError', e.args, e.code
    except Exception as e:
        print 'Exception', e.message
    return builder



def initParser():
    xml_param = xml.parsers.expat.XML_PARAM_ENTITY_PARSING_ALWAYS

    p = xml.parsers.expat.ParserCreate()
    p.ordered_attributes = True
    p.UseForeignDTD(True)
    p.SetParamEntityParsing(xml_param)
    p.buffer_text = 1

    p.XmlDeclHandler = xml_decl
    if xml_param:
        p.StartDoctypeDeclHandler = start_doctype
        p.EndDoctypeDeclHandler = end_doctype
        p.ElementDeclHandler = element
        p.AttlistDeclHandler = attlist
        p.NotationDeclHandler = notation
    p.EntityDeclHandler = entity
    p.StartElementHandler = start_element
    p.EndElementHandler = end_element
    p.ProcessingInstructionHandler = processing_instruction
    p.CharacterDataHandler = char_data
    p.UnparsedEntityDeclHandler = unparsed_entity
    p.StartNamespaceDeclHandler = start_namespace
    p.EndNamespaceDeclHandler = end_namespace
    p.StartCdataSectionHandler = start_cdata_section
    p.EndCdataSectionHandler = end_cdata_section
    p.DefaultHandler = default_handler
    p.DefaultHandlerExpand = default_handler_expand
    p.NotStandaloneHandler = not_stand_alone
    p.ExternalEntityRefHandler = external_entity_ref
    p.CommentHandler = comment
    p.SkippedEntityHandler = skipped_entity
    return p


def parseXmlStr(xmlStr, builder=None):
    data = StringIO.StringIO(xmlStr)
    p = initParser()
    if builder:
        validator = builder.build()
        def start_element(name, attrs, validator=validator):
            print 'Start element:', name, attrs
            validator.start_tag(name)
            pass
        p.StartElementHandler = start_element

        def end_element(name, validator=validator):
            print 'End element:', name
            validator.end_tag(name)
            pass
        p.EndElementHandler = end_element

    try:
        p.ParseFile(data)
    except xml.parsers.expat.ExpatError as e:
        print 'ExpatError', e.args, e.code
    except Exception as e:
        print 'Exception', e.message


doctypeStr = """<?xml version="1.0"?>
<!DOCTYPE person [
  <!ELEMENT pcdata (#PCDATA)>
  <!ELEMENT seq1 (#PCDATA)>
  <!ELEMENT seq2 (#PCDATA)>
  <!ELEMENT seq3 (#PCDATA)>
  <!ELEMENT seq (seq1, seq3)>
  <!ELEMENT opt (opt1 | opt2 | opt3)>
  <!ELEMENT atag (#PCDATA)>
  <!ELEMENT mixed (#PCDATA | atag | pcdata)*>
  <!ELEMENT empty EMPTY>
  <!ELEMENT any ANY>
  <!ELEMENT first_name (#PCDATA)>
  <!ELEMENT middle_name (#PCDATA)>
  <!ELEMENT last_name  (#PCDATA)>
  <!ELEMENT profession (#PCDATA)>
  <!ELEMENT name (first_name, middle_name*, last_name?)>
  <!ELEMENT person     (name, profession*)>
  <!ELEMENT methodResponse (params | fault)>
  <!ELEMENT circle (center, (radius | diameter))>
  <!ELEMENT center ((x, y) | (y, x) | (r, theta ) | (theta , r))>
  <!ELEMENT x (#PCDATA)>
  <!ELEMENT y (#PCDATA)>
  <!ELEMENT r (#PCDATA)>
  <!ELEMENT theta (#PCDATA)>  
  <!ELEMENT radius (#PCDATA)>  
  <!ELEMENT diameter (#PCDATA)>  
]>
<person />"""

builder = initValidatorBuilder(doctypeStr)

def testXmlStr(xmlStr, root):
    print xmlStr
    parseXmlStr(xmlStr, builder.setRoot(root))

xmlStr = """<?xml version="1.0"?>
<person>
  <name>
    <first_name>Alan</first_name>
    <last_name>Turing</last_name>
  </name>
  <profession>computer scientist</profession>
  <profession>mathematician</profession>
  <profession>cryptographer</profession>
</person>"""
# testXmlStr(xmlStr, 'person')

optseq1Str = """<?xml version="1.0"?>
<circle>
  <center>
    <y>10.0</y>
    <x>2.5</x>
  </center>
  <radius>30</radius>
</circle>"""
# testXmlStr(optseq1Str, 'circle')

optseq2Str = """<?xml version="1.0"?>
<circle>
  <center>
    <theta>10.0</theta>
    <r>2.5</r>
  </center>
  <diameter>30</diameter>
</circle>"""
# testXmlStr(optseq2Str, 'circle')

emptyStr = """<?xml version="1.0"?>
<any str="test_empty_tag">
    <empty str="open_close_tag"></empty>
    <empty str="self_close_tag"/>
    <empty str="error_empty_tag_with_child">
        <theta>10</theta>
    </empty>
</any>"""
# testXmlStr(emptyStr, 'any')

seqStr = """<?xml version="1.0"?>
<seq str="well formed">
    <seq1>uno</seq1>
    <seq3>dos</seq3>
</seq>"""
# testXmlStr(seqStr, 'seq')

seqStr = """<?xml version="1.0"?>
<seq str="invalid elements flipped">
    <seq3>dos</seq3>
    <seq1>uno</seq1>
</seq>"""
# testXmlStr(seqStr, 'seq')

seqStr = """<?xml version="1.0"?>
<seq str="invalid elements flipped">
    <seq1>uno</seq1>
</seq>"""
# testXmlStr(seqStr, 'seq')

seqStr = """<?xml version="1.0"?>
<seq str="well formed">
    <seq1>uno</seq1>
    <seq2>uno</seq2>
    <seq3>dos</seq3>
</seq>"""
# testXmlStr(seqStr, 'seq')

xmlStr = """<?xml version="1.0"?>
<any str="well formed">
    <name>
      <first_name>Madonna</first_name>
      <last_name>Ciconne</last_name>
    </name>
    <name>
      <first_name>Madonna</first_name>
      <middle_name>Louise</middle_name>
      <last_name>Ciconne</last_name>
    </name>
    <name>
      <first_name>Madonna</first_name>
      <middle_name>Louise</middle_name>
      <middle_name>Marie</middle_name>
      <last_name>Ciconne</last_name>
    </name>
    <name>
      <first_name>Madonna</first_name>
    </name>
</any>"""
# testXmlStr(xmlStr, 'any')

xmlStr = """<?xml version="1.0"?>
<any str="invalid elements flipped">
    <name>
      <first_name>Madonna</first_name>
      <last_name>Ciconne</last_name>
      <middle_name>Louise</middle_name>
    </name>
</any>"""
# testXmlStr(xmlStr, 'any')

xmlStr = """<?xml version="1.0"?>
<any str="mixed content">
<mixed>The <atag>Turing Machine</atag> is an abstract finite 
state automaton with infinite memory that can be proven equivalent 
to any any other <pcdata>finite state automaton</pcdata> with arbitrarily large memory. 
Thus what is true for a <atag>Turing machine</atag> is true for all equivalent 
machines no matter how implemented.
</mixed></any>"""
testXmlStr(xmlStr, 'any')
