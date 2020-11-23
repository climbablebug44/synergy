import pygame


class keyBinding:
  def __init__(self):
    self.bindings = [pygame.K_a, pygame.K_d, pygame.K_b, pygame.K_q, pygame.K_e, pygame.K_w, pygame.K_s, pygame.K_SPACE, pygame.K_r, pygame.K_f, pygame.K_t, pygame.K_z, 0, pygame.K_c]
    
    
  def get(self):
    try:
      with open('assets/keys.bin','r') as fp:
        self.bindings = fp.read()
      self.bindings = eval(self.bindings)
      return self.bindings
    except FileNotFoundError:
      return self.bindings
    
  def change(self, newL):
    self.bindings = newL
    self.commit()
    
  def commit(self):
    with open('assets/keys.bin','r') as fp:
      fp.write(self.bindings.__str__())
