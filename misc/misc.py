import re

def django_static_file_ref_update(file):
    data = open(file, 'r').read()
    file_paths = re.findall('".{1,255}?"', data)
    file_paths = [re.sub('"', '', x) for x in file_paths]
    keep_file_exts = ['.css', '.js', '.svg', '.png']
    keep_file_exts = ['\\' + x for x in keep_file_exts]
    keep_file_exts = '|'.join(keep_file_exts)

    file_exts = []
    for x in file_paths:
        try:
            file_exts.append(re.search('\\..{1,5}',x).group(0))
        except:
            pass

    file_exts = list(set(file_exts))

    file_paths = [x for x in file_paths if bool(re.findall(keep_file_exts, x))]
    file_paths = [x for x in file_paths if x[0]!='.']
    file_paths = list(set(file_paths))

    for x in file_paths:
        print('~~~~~~')
        print(x)
        new_path = "{% static '" + x + "' %}"
        data = re.sub(x, new_path, data)
        print(new_path)
    
    new_file = file.split('.')
    new_file = new_file[0] + '_NEW.' + new_file[1]

    f = open(new_file, "w")
    f.write(data)
    f.close()

if __name__ ==  '__main__':
    path = ''
    django_static_file_ref_update(path)