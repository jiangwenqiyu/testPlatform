import jmespath

a = {'retStatus': '1', 'retMessage': '', 'retData': {'helpCode': None, 'helpCodeList': [], 'spuNo': '4714173', 'productUuid': '2100074076', 'skuNoMap': {'脚本属性值1': '15222385'}, 'skuSpecHelpCode': {'脚本属性值1': {'helpCode': 'jbsxz1', 'duoyinIndexs': [0, 2], 'skuNo': '15222385'}}, 'addState': {'structureInfoAddState': 'ADD_OK', 'structureInfoAddStateStr': '已完善', 'multiUnitAddState': 'INIT', 'multiUnitAddStateStr': '待完善', 'basicInfoAddState': 'INIT', 'basicInfoAddStateStr': '待完善', 'manageAddState': 'INIT', 'manageAddStateStr': '待完善', 'marketingAddState': 'INIT', 'marketingAddStateStr': '待完善', 'taxAddState': 'INIT', 'taxAddStateStr': '待完善', 'logisticsAddState': 'INIT', 'logisticsAddStateStr': '待完善', 'packageAddState': 'INIT', 'packageAddStateStr': '待完善', 'supplyGoodsAddState': 'INIT', 'supplyGoodsAddStateStr': '待完善', 'supplyPriceAddState': 'INIT', 'supplyPriceAddStateStr': '待完善', 'salePriceAddState': 'INIT', 'salePriceAddStateStr': '待完善', 'picAddState': 'INIT', 'picAddStateStr': '待完善', 'acceptanceAddState': 'OK', 'acceptanceAddStateStr': '已完成', 'qualificationAddState': 'OK', 'qualificationAddStateStr': '已完成'}}, 'timestamp': 0}

pat = 'retData.skuSpecHelpCode.*.skuNo | [0]'

c = jmespath.search(pat, a)

print(c)

