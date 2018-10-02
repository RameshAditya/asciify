'''
def resolve():
	- utility function that downloads an image/video file in case
	  it is a url.
	- otherwise returns the path as it is.
'''
def resolve(path):
    import urllib.request

    resolved_path = path
    if path.startswith('http://') or path.startswith('https://'):
        filename = 'asciify-input-file.{}'.format(path.split('.')[-1])
        urllib.request.urlretrieve(path, filename)
        resolved_path = filename

    return resolved_path