import datetime

api_url = 'http://192.168.10.254:9191/server/api/1.0'
# 管理员帐号
loginName = 'operatorAdmin'
loginPassword = 'Aa888888'
# 经销商账号
supplierLoginName = 'dealer'
supplierLoginPassword = 'Aa888888'
supplierName = '谱慧医疗'
# 供应商帐号
supplierLoginName02 = 'supplier'
supplierLoginPassword02 = 'Aa888888'
# supplierName02 = '嘉事（上海）国润医疗器械有限公司'
# other variable

# 数据库
database = "sirius_int"
user = "sirius_test"
password = "123456"
host = "192.168.10.253"
port = "5432"
schema = 'sirius'

# 订单类型
Ordertpye = 'adhoc'

######
# 以下参数不需要修改
######
# 初始部门名称(不需要修改)
initDeptName = '默认部门'
departmentName = '默认部门'
# 初始角色分类名（不需要修改）
initRoleTypeName = '默认角色分类'
# 初始角色名称（不需要修改）
initRoleName = '默认角色'
# 初始用户名称（不需要修改）
initLoginName = 'defaultLoginName'
# 初始密码（不需要修改）
initialPassword = 'Aa888888'
# 新增基础数据的编号，年月日小时，每小时内重复执行不会再次新增
count = int('{0:%Y%m%d%H}'.format(datetime.datetime.now()))
