from flask import (
    Blueprint, g
)

NAME = 'index'
bp = Blueprint(NAME, __name__, url_prefix='/')


@bp.route('')
def index():
    templates = """
    <!DOCTYPE html>
    <html>
        <head>
        </head>
        <body>
            <a href="/crx/Send">/crx/Send</a>
            <br>
            <a href="/crx/Receive">/crx/Receive</a>
            <br>
            <a href="/manual/Send">/manual/Send</a>
            <br>
            <a href="/manual/Receive">/manual/Receive</a>
            <br> 
        </body>
    </html>
    """
    return templates
