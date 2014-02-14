class ChiselApi:
  """
  API definition to interface with running Chisel RTL.
  Subclass this for particular implementations to interface with, like the
  emulator over stdin/stdout.
  """
  def get_nodes_list(self):
    """Returns a list of API-accessible nodes in the circuit.
    Depending on the optimization level during synthesis, some nodes may not
    be accessible."""
    raise NotImplementedError
  
  def get_node_value(self, node):
    """Returns the current value of a node in the circuit as a integer type.
    This can be used to access an memory array by subscripting the address
    in brackets"""
    raise NotImplementedError
  
  def get_node_type(self, node):
    """Returns the Chisel type of a node.
    """
    raise NotImplementedError
  
  def get_node_width(self, node):
    """Returns the bit-width of a node. Raises an error for non-node types
    (like modules).
    """
    raise NotImplementedError
  
  def set_node_value(self, node, value):
    """Sets a node's value, and propagates it through the circuit.
    Only meaningful on registers, as other values will be overridden when
    propagation occurs.
    Value may either be an integer type or a string representation of an 
    integer (which will be parsed).
    """
    raise NotImplementedError
  