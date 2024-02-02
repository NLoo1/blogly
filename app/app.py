
from .__init__ import create_app
from .models import db

app = create_app()
db.app = app

if __name__ == '__main__':
    app.run(debug=True)
