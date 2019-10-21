from fdfs_client.client import Fdfs_client
from django.core.files.storage import Storage
from django.conf import settings


class FDFSStorage(Storage):
    """fast DFS文件上传类"""

    def __init__(self, client_conf=None, base_url=None):
        """定义初始化参数"""
        if client_conf is None:
            self.client_conf = settings.FDFS_CLIENT_CONF

        if base_url is None:
            self.base_url = settings.FDFS_URL

    def _open(self, name, mode='rb'):
        """打开文件时使用者里不需要"""
        pass

    def _save(self, name, content):
        """保存文件时使用
        :param name: 选择上传文件的名称
        :param content: 包含上传文件的File对象
        """
        # 创建一个Fdfs_client对象
        client = Fdfs_client(self.client_conf)

        # 上传文件到fast FDFS系统中去
        res = client.upload_by_buffer(content.read())

        # dict
        # {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id,
        #     'Status': 'Upload successed.',
        #     'Local file name': '',
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # }
        if res.get('Status') != 'Upload successed.':
            # s上传失败
            raise Exception('上传文件到fast dfs失败')

        # 获取返回的文件id
        filename = res.get('Remote file_id')
        return filename

    def exists(self, name):
        """Django判断文件名是否可用"""
        return False

    def url(self, name):
        return self.base_url + name
