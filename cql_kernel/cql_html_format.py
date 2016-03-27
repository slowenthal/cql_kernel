import cgi

BLACK = 'black'
GREEN = 'green'
RED = 'red'
DARK_MAGENTA = 'dark_magenta'
BLUE = 'blue'
CYAN = '#92C7C7'

DEFAULT_VALUE_COLORS = dict(
    default=BLACK,
    text=BLACK,
    error=RED,
    blob=DARK_MAGENTA,
    timestamp=GREEN,
    date=GREEN,
    time=GREEN,
    int=GREEN,
    float=GREEN,
    decimal=GREEN,
    inet=GREEN,
    boolean=GREEN,
    uuid=GREEN,
    collection=BLUE
)

def getColor(color):
    return DEFAULT_VALUE_COLORS.get(color, DEFAULT_VALUE_COLORS['default'])

def getColumnColor(name, table_meta):
    # Not efficient, but there are usually only a few key columns
    if name in name in [col.name for col in table_meta.partition_key]:
        return RED
    elif name in name in [col.name for col in table_meta.clustering_key]:
        return CYAN
    else:
        return DEFAULT_VALUE_COLORS['default']

def print_formatted_result_html(writeresult, formatted_names, formatted_values, table_meta):

    writeresult('<table><tr>')
    writeresult(''.join('<td style="font-weight:bold;color:%s">%s</td>' % (getColumnColor(name.strval, table_meta), name.strval) for name in formatted_names))
    writeresult('</tr>')

    for row in formatted_values:
        writeresult('<tr><td>')
        writeresult('</td><td>'.join(cgi.escape(v.strval) for v in row))
        writeresult('</td></tr>')

    writeresult('</table>')
