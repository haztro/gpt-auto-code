import json 

test = str({
  "description": "Add the Folium Map to the HTML template",
  "code": "html_template = '''\n<!DOCTYPE html>\n<html lang=\\"en\\">\n<head>\n    <meta charset=\\"UTF-8\\">\n    <meta name=\\"viewport\\", content=\\"width=device-width, initial-scale=1.0\\">\n    <title>Brisbane River Ferries Tracker</title>\n    <link rel=\\"stylesheet\\" href=\\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\\">\n    <script src=\\"https://code.jquery.com/jquery-3.2.1.slim.min.js\\" integrity=\\"sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN\\" crossorigin=\\"anonymous\\"></script>\n    <script src=\\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\\" integrity=\\"sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa\\" crossorigin=\\"anonymous\\"></script>\n</head>\n<body>\n    <div class=\\"container\\">\n        <h1>Brisbane River Ferries Tracker</h1>\n        <div id=\\"map\\" style=\\"width: 100%; height: 600px\\"></div>\n    </div>\n    <script>{% raw %}{{map}}{% endraw %}</script> \n</body>\n</html>\n'''\n\nwith open('index.html', 'w') as f:\n    f.write(html_template.format(map=map.render()))"
})


testj = json.loads(test)