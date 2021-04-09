import datetime

api_url = 'http://192.168.10.254:9191/server/api/1.0'
# 管理员帐号
loginName = 'operatorAdmin'
loginPassword = 'Aa888888'
# 供应商帐号
supplierLoginName = 'phyl123'
supplierLoginPassword = 'Aa123456'
supplierName = '谱慧医疗'

supplierLoginName02 = 'operatorAdmin'
supplierLoginPassword02 = 'Aa888888'
supplierName02 = '嘉事（上海）国润医疗器械有限公司'
# other variable

# 有库存的物资id
goodsId = 320
kitTemplateId = 3

#订单类型
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
