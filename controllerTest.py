
import pygame


SCREEN_SIZE = (1200, 700)

class TextPrint:
   def __init__(self):
      self._startX = 10
      self._startY = 10
      self._indent = 10
      self.reset()
      self._lineHeight = 15
      self._lineWidth = 300
      self._font = pygame.font.Font(None, 20)
      
   
   def renderJoy(self, joy, screen):
      # Get the joystick of the given number
      joystick = pygame.joystick.Joystick(joy)
      
      # Initialize the joystick if it is not yet
      if not joystick.get_init():
         joystick.init()
  
      # Display the joystick's number
      self.renderText(screen, "Joystick {}".format(joy) )
      self.indent()
  
      # Get the name from the OS for the controller/joystick
      name = joystick.get_name()
      self.renderText(screen, "Joystick name: {}".format(name) )
      
      # Usually axis run in pairs, up/down for one, and left/right for
      # the other.
      axes = joystick.get_numaxes()
      self.renderText(screen, "Number of axes: {}".format(axes) )
      self.indent()
      
      for i in range( axes ):
         axis = joystick.get_axis( i )
         self.renderText(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
      self.unindent()
          
      # Display buttons
      buttons = joystick.get_numbuttons()
      self.renderText(screen, "Number of buttons: {}".format(buttons) )
      self.indent()

      for i in range( buttons ):
         button = joystick.get_button( i )
         self.renderText(screen, "Button {:>2} value: {}".format(i,button) )
      self.unindent()
          
      # Hat switch. All or nothing for direction, not like joysticks.
      # Value comes back in an array.
      hats = joystick.get_numhats()
      self.renderText(screen, "Number of hats: {}".format(hats) )
      self.indent()

      for i in range( hats ):
         hat = joystick.get_hat( i )
         self.renderText(screen, "Hat {} value: {}".format(i, str(hat)) )
      self.unindent()
      
      self.unindent()

   def renderText(self, screen, textString):
      # Render some text at the current location and move down a line
      textBitmap = self._font.render(textString, True, (0,0,0))
      screen.blit(textBitmap, [self._x, self._y])
      self._y += self._lineHeight
       
   def reset(self):
      # Go back to the top left
      self._x = self._startX
      self._y = self._startY
       
   def indent(self):
      # "tab" over
      self._x += self._indent
       
   def unindent(self):
      # undo tab
      self._x -= self._indent
      
   def nextJoy(self):
      # Return to the top and move to the right
      self._x += self._lineWidth
      self._y = self._startY + self._lineHeight
      
      

def main():
   
   # initialize the pygame module
   pygame.init()
   # load and set the logo
   
   pygame.display.set_caption("Joystick Controls")
   
   screen = pygame.display.set_mode(SCREEN_SIZE)
   
   
   textPrint = TextPrint()
   
   #joystick = pygame.joystick.Joystick(0)
   
   
   
   # define a variable to control the main loop
   running = True
   
   # main loop
   while running:
         
      
      # Draw everything
      screen.fill((255,255,255))
      textPrint.reset()
      
      # Get count of joysticks
      joystick_count = pygame.joystick.get_count()
      
      textPrint.renderText(screen, "Number of joysticks: {}".format(joystick_count) )
      textPrint.indent()
    
      # For each joystick:
      for i in range(joystick_count):
         textPrint.renderJoy(i, screen)
         textPrint.nextJoy()
  
      # Flip the display to the monitor
      pygame.display.flip()
      
      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or ESCAPE is pressed
         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False, to exit the main loop
            running = False
         
            
      
      # Update everything
      
if __name__ == "__main__":
   main()