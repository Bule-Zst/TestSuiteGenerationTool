import configparser
import os

configureFilePath = "./default.cfg"
config = ""


def init():
    global  config
    if not os.path.exists(configureFilePath):
        with open( configureFilePath, "w" ):
            pass
    config = configparser.RawConfigParser()
    config.read(configureFilePath)
    if not "default" in config.sections():
        config.add_section( "default" )


def destory():
    global config
    with open( configureFilePath, "w" ) as fout:
        config.write(fout)


def get( key, fallback=None ):
    key = key.lower()
    init()
    if key not in config.options("default") and fallback is None:
        raise Exception("not have fallback")
    tmp = config.get( "default", key, fallback=fallback )
    destory()
    return tmp


def set( key, value ):
    init()
    config.set( "default", key, value )
    destory()

if __name__ == '__main__':
    init()
    config.get( "default", "aa" )
    destory()
    # print( config_raw.getboolean("Default", "aa" ) )

# # 读取配置文件中 [DEFAULT]
# defaults = config_raw.defaults()
# print defaults
#
# # 读取指定section下的value值
# a_float = config_raw.getfloat('Section1', 'a_float')
# print "-- number : %f type is : %s"%(a_float ,type(a_float))
#
# # 设置指定section下的value值
# # 此时没有写入文件，保存在内存实例中
# a_float = 2.14159
# config_raw.set('Section1', 'a_float', a_float)
# a_float = config_raw.getfloat('Section1', 'a_float')
# print "-- number : %f type is : %s"%(a_float ,type(a_float))