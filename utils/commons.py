from django.http import StreamingHttpResponse
import os
import zipfile


def zipDir(dirpath, outFullName, name):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "a", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(name + fpath, filename))
    zip.close()


def download_response(filepath):
    """
        to download files
    """
    def file_iterator(filepath, chunk_size=262144):
        with open(filepath, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(filepath),
                                     content_type='application/octet-stream; charset=UTF-8')  # application/vnd.ms-excel
    response['Content-Disposition'] = 'attachment;filename="%s"' % (os.path.basename(filepath))
    response['Content-Length'] = os.path.getsize(filepath)
    return response
