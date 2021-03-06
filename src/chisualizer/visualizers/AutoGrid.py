import chisualizer.Base as Base
from VisualizerBase import VisualizerBase, Rectangle

@Base.xml_register('AutoGrid')
class AutoGrid(VisualizerBase):
  """A grid of elements, each pointing to a memory element."""
  @classmethod
  def from_xml_cls(cls, element, parent):
    new = super(AutoGrid, cls).from_xml_cls(element, parent)
    
    new.offset = new.parse_element_int(element, 'offset', 0)
    new.step = element.get('step', 'row')
    if new.step not in ['row', 'col']: new.parse_error("step must be 'row' or 'col', got '%s'" % new.step) 
    
    new.cells = [[]]
    for child_cell in element:
      if child_cell.tag == "Break":
        if new.cells[-1]: # append new list only if current not empty
          new.cells.append([])
      else:
        new.cells[-1].append(Base.Base.from_xml(child_cell, parent=new))
      
    return new
  
  def instantiate(self, new_parent):
    cloned = super(AutoGrid, self).instantiate(new_parent)
    cloned.step = self.step
    cloned.cells = []
    for cell_ary in self.cells:
      cloned.cells.append([])
      for cell in cell_ary:
        cloned.cells[-1].append(cell.instantiate(cloned))
    return cloned

  def layout_element_cairo(self, cr):
    self.cell_size = []     # size in the step direction, per <Break> group, per cell
    self.maj_size = []      # size in the step direction, per <Break> group 
    self.maj_spacing = []   # size orthogonal to the step direction,
                            # different per <Break> group
    for cell_ary in self.cells:
      this_maj_spacing = 0
      this_maj_size = 0
      self.cell_size.append([])
      for cell in cell_ary:
        cell_x, cell_y = cell.layout_cairo(cr)
        if self.step == 'row':    # cells along x-dir
          this_maj_spacing = max(this_maj_spacing, cell_y)
          this_maj_size = this_maj_size + cell_x
          self.cell_size[-1].append(cell_x)
        elif self.step == 'col':  # cells along y-dir
          this_maj_spacing = max(this_maj_spacing, cell_x)
          this_maj_size = this_maj_size + cell_y
          self.cell_size[-1].append(cell_y)
      self.maj_size.append(this_maj_size)
      self.maj_spacing.append(this_maj_spacing)
      
    self.total_step = max(self.maj_size)    # total size in the step direction
    self.total_maj = sum(self.maj_spacing)  # total size orthogonal the step direction
      
    if self.step == 'row':    # cells along x-dir
      return (self.total_step, self.total_maj)
    elif self.step == 'col':  # cells along y-dir
      return (self.total_maj, self.total_step) 
        
  def draw_element_cairo(self, cr, rect, depth):
    if self.step == 'row':    # cells along x-dir
      origin_x = rect.center_horiz()
      origin_y = rect.center_vert() - self.total_maj / 2
    elif self.step == 'col':  # cells along y-dir
      origin_x = rect.center_horiz() - self.total_maj / 2
      origin_y = rect.center_vert()
    pos_x = origin_x
    pos_y = origin_y
    elements = []
  
    for cell_ary_ind in xrange(len(self.cells)):
      cell_ary = self.cells[cell_ary_ind]
      this_maj_spacing = self.maj_spacing[cell_ary_ind]
      this_maj_size = self.maj_size[cell_ary_ind]
      this_cell_size = self.cell_size[cell_ary_ind]
      
      if self.step == 'row':    # cells along x-dir
        pos_x = origin_x - this_maj_size / 2
      elif self.step == 'col':  # cells along y-dir
        pos_y = origin_y - this_maj_size / 2
        
      for cell_ind in xrange(len(cell_ary)):
        cell = cell_ary[cell_ind]
        cell_size = this_cell_size[cell_ind]
        
        if self.step == 'row':    # cells along x-dir
          cell_rect = Rectangle((pos_x, pos_y),
                                (pos_x + cell_size, pos_y + this_maj_spacing))
        elif self.step == 'col':  # cells along y-dir
          cell_rect = Rectangle((pos_x, pos_y),
                                (pos_x + this_maj_spacing, pos_y + cell_size))

        elements.extend(cell.draw_cairo(cr, cell_rect, depth + 1))
        
        if self.step == 'row':    # cells along x-dir
          pos_x += cell_size
        elif self.step == 'col':  # cells along y-dir
          pos_y += cell_size
          
      if self.step == 'row':    # cells along x-dir
        pos_y += this_maj_spacing
      elif self.step == 'col':  # cells along y-dir
        pos_x += this_maj_spacing

    return elements
