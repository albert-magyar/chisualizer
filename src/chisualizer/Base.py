import xml.etree.ElementTree as etree
import logging

# a registry of all visualization descriptors which can be instantiated
# indexed by name which it can be instantiated under.
xml_registry = {}
def xml_register(name=None):
  def wrap(cls):
    local_name = name
    if local_name == None:
      local_name = cls.__name__
    if local_name in xml_registry:
      raise NameError("Attempting to re-register a XML descriptor '%s'" %
                      local_name)
    xml_registry[local_name] = cls
    logging.debug("Registered XML descriptor class '%s'" % local_name)
    return cls
  return wrap

class VisualizerDescriptor(object):
  """An visualizer descriptor file."""
  def __init__(self, filename):
    """Initialize this descriptor from a file."""
    self.registry = {}
    self.parse_from_xml(filename)

  def parse_from_xml(self, filename):
    """Parse this descriptor from an XML file."""
    root = etree.parse(filename).getroot()
    for child in root:
      elt = Base.from_xml(child, container=self)
      ref = child.get('ref', None)
      if ref:
        if ref not in self.registry:
          self.registry[ref] = elt
          logging.debug("Registered '%s'", ref)
        else:
          raise NameError("Found object with duplicate ref '%s'", ref)

class Base(object):
  """Abstract base class for visualizer descriptor objects."""
  @staticmethod
  def from_xml(element, **kwargs):
    assert 'container' in kwargs, "from_xml must have container argument"
    assert isinstance(element, etree.Element)
    if element.tag in xml_registry:
      return xml_registry[element.tag].from_xml_cls(element, **kwargs)
    else:
      raise NameError("Unknown class '%s'" % element.tag)
      
  @classmethod
  def from_xml_cls(cls, element, container=None, **kwargs):
    """Initializes this descriptor from a XML etree Element."""
    new = cls()
    assert container, "from_xml_cls must have container"
    new.container = container
    return new
