import sys
sys.path.append("../")

from resource_console import settings
from resource_console.api import app
from resource_console.middleware import TestMiddleware
import resource_console.api.url


if __name__ == "__main__":
    app.run(host="0.0.0.0", processes=4, debug=settings.DEBUG)
