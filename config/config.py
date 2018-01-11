import os
import configparser


# 定义内部获取的方法
def read_property(section, key):
    # 获取文件的当前路径（绝对路径）
    cur_path = os.path.dirname(os.path.realpath(__file__))

    # 获取config.ini的路径
    config_path = os.path.join(cur_path, 'config.ini')

    # 读取配置文件
    conf = configparser.ConfigParser()
    conf.read(config_path)

    return conf.get(section, key)


# 保存在变量中
db_host = str(read_property("db", "db_host"))
db_port = int(read_property("db", "db_port"))
db_user = str(read_property("db", "db_user"))
db_pass = str(read_property("db", "db_pass"))
db_name = str(read_property("db", "db_name"))
db_charset = str(read_property("db", "db_charset"))
