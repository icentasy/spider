import sys
sys.path.append("../")

from auth_service import settings
from auth_service.api import app
import auth_service.api.url


if __name__ == "__main__":
    app.run(host="0.0.0.0", processes=4, debug=settings.DEBUG)
