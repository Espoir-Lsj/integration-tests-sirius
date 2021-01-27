import datetime
api_url = 'http://192.168.10.254:9191/server/api/1.0'
# 管理员帐号
loginName = 'operatorAdmin'
loginPassword = 'Aa888888'
# 供应商帐号
supplierLoginName = 'zonglr'
supplierLoginPassword = 'Aa888888'
supplierName = '上海飞扬医疗器械有限公司'
supplierLoginName02 = 'suyong'
supplierLoginPassword02 = 'Aa123456'
supplierName02 = '嘉事（上海）国润医疗器械有限公司'
# other variable

# 有库存的物资id
goodsId = 249
kitTemplateId = 21

######
# 以下参数不需要修改
######
# 初始部门名称(不需要修改)
initDeptName = '默认部门'
# 新增基础数据的编号，年月日小时，每小时内重复执行不会再次新增
count = int('{0:%Y%m%d%H}'.format(datetime.datetime.now()))