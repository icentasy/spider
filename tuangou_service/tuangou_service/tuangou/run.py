import sys
sys.path.append("../")

from tuangou import settings
from tuangou.api import app
import tuangou.api.deal
import tuangou.api.city


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, processes=4, debug=settings.DEBUG)
