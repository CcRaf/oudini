#! python3
import  os
import  xml.etree.ElementTree   as ETree
from    requirements_set        import RequirementsSet
from    common_section          import CommonSection
from    glossary                import Glossary
from    generator               import Generator


class Document:

    def __init__(self):
        self.common     = None
        self.reqs       = None
        self.glossary   = None

    @classmethod
    def from_xml(cls,
                 i_tree : ETree.ElementTree):
        assert isinstance(i_tree, ETree.ElementTree)

        root = i_tree.getroot()

        # Normalize (lowercase) the XML file tags and attributes
        Document._normalize_tags(root)
        Document._normalize_attr(root)

        obj = cls()

        # Search for common section and glossary
        for base in root:
            if      base.tag == CommonSection.COMMON_TAG_STR:
                assert obj.common is None
                obj.common = CommonSection.from_xml_element(i_elt = base)
            elif    base.tag == Glossary.GLOSSARY_TAG_STR:
                assert obj.glossary is None
                obj.glossary = Glossary.from_xml_element(i_elt = base)
            else:
                pass

        # Common section is not optional
        assert obj.common is not None
        # Glossary is optional

        # Search for requirements section
        for base in root:
            if      base.tag == RequirementsSet.REQ_SET_TAG_STR:
                assert obj.reqs is None
                obj.reqs = RequirementsSet.from_xml_element(i_elt    = base,
                                                            i_common = obj.common)
            else:
                pass

        # Requirements section is not optional
        assert obj.reqs is not None

        return obj

    @staticmethod
    def _normalize_tags(i_root):
        i_root.tag = i_root.tag.lower()
        for child in i_root:
            Document._normalize_tags(child)

    @staticmethod
    def _normalize_attr(i_root):
        for attr in list(i_root.attrib):
            norm_attr = attr.lower()
            if norm_attr != attr:
                i_root.set(norm_attr, i_root.attrib[attr])
                i_root.attrib.pop(attr)

        for child in i_root:
            Document._normalize_attr(child)

    def generate_snippets(self,
                          i_root_folder : str,
                          i_generator   : Generator):
        assert isinstance(i_root_folder, str)
        assert isinstance(i_generator,   Generator)

        os.makedirs(i_root_folder, exist_ok = True)

        # Generate the requirements
        for _, req in self.reqs.reqs.items():
            i_generator.generate_requirement(i_req      = req,
                                             i_filename = req.get_snippet_filename(i_root_folder     = i_root_folder,
                                                                                   i_fallback_format = i_generator.DEFAULT_REQ_FILE_FORMAT))

        # Export the document constants
        i_generator.generate_constants(i_common   = self.common,
                                       i_filename = self.common.get_constants_snippet_filename(i_root_folder     = i_root_folder,
                                                                                               i_fallback_format = i_generator.DEFAULT_CONSTANTS_FILE_FORMAT))

        # If present: export the glossary
        if self.glossary is not None:
            i_generator.generate_glossary(i_glossary = self.glossary,
                                          i_filename = self.common.get_constants_snippet_filename(i_root_folder     = i_root_folder,
                                                                                                  i_fallback_format = i_generator.DEFAULT_GLOSSARY_FILE_FORMAT))


    def __str__(self):
        s = "%s\n%s\n" % (str(self.common), str(self.reqs))

        if self.glossary:
            s += "%s" % (str(self.glossary))

        return s

    def __repr__(self):
        s = "%s\n%s\n" % (repr(self.common), repr(self.reqs))

        if self.glossary:
            s += "%s" % (repr(self.glossary))

        return s