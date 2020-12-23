import psycopg2, os

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