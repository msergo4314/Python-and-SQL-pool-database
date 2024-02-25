# A2 CIS*2750
# Martin Sergo W24 
import sys, os, Physics # sys used to get argv, os for file operations, Physics for phylib library access

# web server imports
from http.server import HTTPServer, BaseHTTPRequestHandler
# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl

# handler for our web-server - handles both GET and POST requests
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # parse the URL to get the path and form data
        path = urlparse(self.path).path

        if path == "/shoot.html" and os.path.exists(path[1:]):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            
            with open("shoot.html", "rb") as file:
                content = file.read()
            self.send_header("Content-length", len(content))
            self.end_headers()
            self.wfile.write(content)

        elif path.startswith("/table-") and path.endswith(".svg"):    
            filename = path.lstrip("/") #remove / from string
            # print("name of file: "+filename)
            if os.path.exists(filename):
                self.send_response(200)
                self.send_header("Content-type", "image/svg+xml")
                with open(filename, "rb") as file:
                    content = file.read()
                self.send_header("Content-length", len(content))
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                content = "404: requested file %s not found" % (self.path[1::] if self.path != '/' else "index.html")
                self.send_header("Content-length", len(content))
                self.end_headers()
                print(self.path)
                self.wfile.write(bytes(content, "utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            content = "404: requested file %s not found" % (self.path[1::] if self.path != '/' else "index.html")
            self.send_header("Content-length", len(content))
            self.end_headers()
            print(self.path)
            self.wfile.write(bytes(content, "utf-8"))

    def do_POST(self):
        path  = urlparse(self.path).path
        # receive form data from shoot.html
        if path == "/display.html":
            import math
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = dict(parse_qsl(post_data))

            if len(form_data) != 8:
                self.send_response(400)
                response_content = '<H3>Form fields are not fully filled. Try again.</H3>\
                <a href = "shoot.html", title = "return">back to previous page</a>'
                self.send_header("Content-type", "text/html")
                self.send_header("Content-length", len(response_content))
                self.end_headers()
                self.wfile.write(bytes(response_content, "utf-8"))
                return
            VEL_MAX = 1e5
            acceptable_responses = ((1, 15), (28.5, 1321.5), (28.5, 2671.5), (0, 15), (28.5, 2671.5), (28.5, 2671.5), (-VEL_MAX, VEL_MAX), (-VEL_MAX, VEL_MAX))
            # len(form_data) must be 8
            for i, (key,value) in enumerate(form_data.items()):
                current_value = float(value)
                if current_value < acceptable_responses[i][0] or current_value > acceptable_responses[i][1]:
                    self.send_response(400)
                    response_content = '<H3>Form fields are not in the range of valid numbers. Try again.</H3>\
                    <a href = "shoot.html", title = "return">back to previous page</a>'
                    self.send_header("Content-type", "text/html")
                    self.send_header("Content-length", len(response_content))
                    self.end_headers()
                    self.wfile.write(bytes(response_content, "utf-8"))
                    return

            still_ball_number = int(form_data.get('sb_number', ''))
            still_ball_x = float(form_data.get('sb_x', ''))
            still_ball_y = float(form_data.get('sb_y', ''))

            rolling_ball_number = int(form_data.get('rb_number', ''))
            rolling_ball_x = float(form_data.get('rb_x', ''))
            rolling_ball_y = float(form_data.get('rb_y', ''))
            rolling_ball_dx = float(form_data.get('rb_dx', ''))
            rolling_ball_dy = float(form_data.get('rb_dy', ''))

            # delete any SVGs currently existing
            delete_SVGs_in_pwd()
            rolling_ball_a_x = 0.0
            rolling_ball_a_y = 0.0
            # still ball has no velocity or acceleration yet

            # compute acceleration of rolling ball like in phylib bounce C function
            # print(f"length of vector with side lengths {rolling_ball_dx} and {rolling_ball_dy}: {math.hypot(rolling_ball_dx, rolling_ball_dy)}")
            rolling_ball_speed = math.hypot(rolling_ball_dx, rolling_ball_dy)
            if (rolling_ball_speed > Physics.VEL_EPSILON):
                rolling_ball_a_x = -rolling_ball_dx * Physics.DRAG / rolling_ball_speed
                rolling_ball_a_y = -rolling_ball_dy * Physics.DRAG / rolling_ball_speed
            # print("rolling ball ax:" + str(rolling_ball_a_x))
            # print("rolling ball ay:" + str(rolling_ball_a_y))
            sb = Physics.StillBall(still_ball_number, \
            Physics.Coordinate(still_ball_x, still_ball_y))

            rb = Physics.RollingBall(rolling_ball_number, \
            Physics.Coordinate(rolling_ball_x, rolling_ball_y), \
            Physics.Coordinate(rolling_ball_dx, rolling_ball_dy), \
            Physics.Coordinate(rolling_ball_a_x, rolling_ball_a_y))

            # create new Table object and add balls
            table = Physics.Table()
            table += sb
            table += rb
            
            # write all the table segment data to svg files
            self.write_table_to_files(table)
            # Construct the HTML response
            response_content = self.generate_display_html(sb, rb)

            # Send the HTML response
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(response_content))
            self.end_headers()
            self.wfile.write(bytes(response_content, "utf-8"))
        else:
            self.send_response(404)
            response_content = f"404: requested file \"{self.path[1:]}\" not found"
            self.send_header("content-length", len(response_content))
            self.send_header("content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(response_content, "utf-8"))
        return

    def generate_display_html(self, still_ball, rolling_ball):
        if not(isinstance(still_ball, Physics.StillBall) and isinstance(rolling_ball, Physics.RollingBall)):
            return '<H1><b>error occured</b></H1>'

        from re import match # useful for matching the SVG strings
        # Construct the HTML content dynamically using the received form data
        count_svg_files = 0
        svg_pattern = r"^table-\d+\.svg$"
        
        files_in_directory = os.listdir()
        # Iterate over the files and delete those matching the svg pattern
        for file_name in files_in_directory:
            if match(svg_pattern, file_name):
                count_svg_files += 1

        html_file = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Phylib shoot info</title>
            <style>
                body{{
                    color: darkred;
                    //background-color: #2d302e;
                    background-color: #e5dbcf;
                }}
                h1{{
                    color: green;
                    font-size: 4.5rem;
                    font-family: 'mv boli', sans-serif;
                    margin-top: 0;
                    margin-bottom: 0;
                }}
                h2{{
                    color: #0f3b5f;
                    font-size: 3rem;
                    font-family: "Times New Roman", 'arial', serif;
                    margin-top: 0;
                    margin-bottom: 0
                }}
                p{{
                    //color: aquamarine;
                    color: #0f3b5f
                    font-family: "Protest Revolution","helvetica", serif;
                    font-weight: bold;
                    font-size: 2rem;
                    line-height: 0.5;
                }}
                a{{
                    font-size: 2rem;
                    color: rgba(10, 10, 10, 0.75);
                }}
                figcaption {{
                    font-weight: bold;
                    color: #cc9752;
                    font-family: "comic sans MS", "Comic Sans", cursive;
                    font-size: 1.7rem;
                    //text-align: center;
                    order: -1;
                }}
                * {{
                    box-sizing: border-box;
                }}
                .column{{
                    float: left;
                    width: 40%;
                    text-align: center;
                    padding: 5px;
                    margin-left: 5%;
                    margin-right: 5%;
                }}
                .row::after{{
                    content = "";
                    display = table;
                    clear: both;
                }}
                img{{
                    width: 100%;
                    height: auto;
                }}
                hr {{
                    margin: 5px auto;
                    width: 100%;
                }}
            </style>
        </head>
        <body> 
            <a href="#" onclick="window.history.back(); return false;" title="back to Shoot.html"> <big>Back to previous</big></a>
            <h1>Phylib Table Segment Viewer</h1>
            <h2>Original form data recieved:</h2>
                <p>Still Ball Number: {still_ball.obj.still_ball.number}</p>
                <p>Still Ball X: {still_ball.obj.still_ball.pos.x}</p>
                <p>Still Ball Y: {still_ball.obj.still_ball.pos.y}</p>
                <p>Rolling Ball Number: {rolling_ball.obj.rolling_ball.number}</p>
                <p>Rolling Ball X: {rolling_ball.obj.rolling_ball.pos.x}</p>
                <p>Rolling Ball Y: {rolling_ball.obj.rolling_ball.pos.y}</p>
                <p>Rolling Ball ΔX: {rolling_ball.obj.rolling_ball.vel.x}</p>
                <p>Rolling Ball ΔY: {rolling_ball.obj.rolling_ball.vel.y}</p>"""

        for i in range(count_svg_files):
            if i % 2 == 0:
                html_file += '<hr><div class="row">'
            html_file += f'<div class="column"><figure>\
                <img src= "table-{i}.svg" tile = "Table {i}" alt="Table {i} should be here" />\
                <figcaption>SVG image {i+1}:</figcaption>\
            </figure></div>'
            if i % 2 == 0:
                html_file += '</div>'
        
        html_file += "\n</body>\n</html>"
        return html_file
        
    def write_table_to_files(self, table):
        if type(table) != Physics.Table:
            print('invalid type')
            return
        i = 0
        if table:
            with open(f'table-{i}.svg', 'w') as file:
                file.write(table.svg())
        while (table):
            i += 1
            file_name = f'table-{i}.svg'
            table = table.segment()
            if table:
                with open(file_name, 'w') as file:
                    file.write(table.svg())
        return

# no need to make this a class method
def delete_SVGs_in_pwd():
    from re import match
    # Define the file name pattern to match
    svg_pattern = r"^table-\d+\.svg$"
    # Get a list of all files in the current directory
    files_in_directory = os.listdir()
    # print(str(svg_pattern))
    # Iterate over the files and delete those matching the svg pattern
    for file_name in files_in_directory:
        if match(svg_pattern, file_name):
            os.remove(file_name)
            # print("removed file:" + file_name)
    return

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Need a command line argument!")
        # need to use exit instead of return
        sys.exit(1)  # Exit the script

    port_num = int(sys.argv[1]) + int(5e4)
    # d is for daemon
    httpd = HTTPServer(('localhost', port_num), MyHandler)
    # delete any SVG files currently existing
    delete_SVGs_in_pwd()
    print("Server listing in port: ", port_num)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nCanceled with Ctrl + C')
        httpd.shutdown()