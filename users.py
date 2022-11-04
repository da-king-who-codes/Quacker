from flask import render_template
class UserPage:
  def __init__(self, name, app):
    self.app = app
    self.name = name
  def show_user(self):
    @self.app.route(f'/{self.name.lower()}')
    def show():
      return render_template("user_page.html", name=self.name)
      