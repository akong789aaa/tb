# -*- coding: utf-8 -*-
"""
商品类目管理系统 - 增强版
支持更精准的商品分类
"""

import re

class CategoryManager:
    def __init__(self):
        # 构建完整的商品类目树（多级分类）
        self.categories = {
            '电子产品': {
                '手机通讯': ['智能手机', '功能手机', '手机配件', '对讲机', 'iPhone', '华为手机', '小米手机', '三星手机', 'OPPO手机', 'vivo手机'],
                '电脑硬件': ['CPU处理器', '显卡', '主板', '内存', '硬盘', '固态硬盘', 'U盘', '移动硬盘', '存储卡', '电源', '机箱', '散热器', '声卡', '网卡'],
                '电脑办公': ['笔记本电脑', '台式电脑', '平板电脑', '显示器', '打印机', '扫描仪'],
                '数码配件': ['充电器', '数据线', '移动电源', '耳机', '音箱', '相机'],
                '智能设备': ['智能手表', '智能手环', '智能家居', '无人机', '机器人'],
                '影音娱乐': ['电视机', '投影仪', '音响', '播放器', '游戏机']
            },
            '家用电器': {
                '厨房电器': ['冰箱', '微波炉', '烤箱', '空气炸锅', '电饭煲', '榨汁机', '破壁机', '电磁炉', '电水壶', '咖啡机'],
                '生活电器': ['洗衣机', '吸尘器', '扫地机器人', '空气净化器', '加湿器', '电风扇', '取暖器', '除湿机'],
                '制冷电器': ['空调', '冰柜', '制冰机', '冷风机'],
                '热水器': ['电热水器', '燃气热水器', '太阳能热水器', '空气能热水器'],
                '个护电器': ['吹风机', '剃须刀', '电动牙刷', '卷发器', '直发器', '美容仪']
            },
            '服装鞋帽': {
                '男装': ['上衣', '裤子', '外套', '羽绒服', 'T恤', '衬衫', '牛仔裤'],
                '女装': ['连衣裙', '上衣', '裙子', '外套', '羽绒服', 'T恤', '衬衫'],
                '童装': ['婴儿服', '儿童上衣', '儿童裤子', '儿童外套', '儿童鞋'],
                '鞋子': ['运动鞋', '休闲鞋', '皮鞋', '高跟鞋', '凉鞋', '靴子', '拖鞋'],
                '配饰': ['帽子', '围巾', '手套', '腰带', '领带', '袜子']
            },
            '食品饮料': {
                '休闲食品': ['薯片', '坚果', '糖果', '巧克力', '饼干', '肉干'],
                '生鲜果蔬': ['水果', '蔬菜', '肉类', '海鲜', '蛋类', '豆制品'],
                '饮料': ['碳酸饮料', '果汁', '茶饮', '咖啡', '牛奶', '矿泉水'],
                '粮油调味': ['大米', '面粉', '食用油', '盐', '酱油', '醋', '香料'],
                '保健食品': ['维生素', '蛋白粉', '鱼油', '钙片', '益生菌']
            },
            '家居生活': {
                '家具': ['沙发', '床', '餐桌', '书桌', '衣柜', '椅子', '茶几', '鞋柜', '电视柜'],
                '家纺': ['床单', '被套', '枕头', '毛巾', '浴巾', '毛毯', '被子', '四件套'],
                '厨具': ['锅具', '刀具', '餐具', '厨房电器', '保鲜盒', '碗筷', '砧板'],
                '清洁用品': ['扫把', '拖把', '清洁剂', '垃圾桶', '收纳箱', '抹布', '清洁刷'],
                '装饰': ['花瓶', '相框', '挂画', '摆件', '地毯', '窗帘', '香薰', '蜡烛'],
                '塑料制品': ['塑料盆', '塑料桶', '塑料箱', '塑料收纳盒', '塑料衣架', '塑料椅子', '塑料花盆']
            },
            '美妆护肤': {
                '护肤品': ['洁面', '爽肤水', '乳液', '面霜', '精华', '防晒', '面膜', '眼霜'],
                '彩妆': ['粉底', '口红', '眼影', '睫毛膏', '腮红', '眉笔', '粉饼', '遮瑕'],
                '香水': ['男士香水', '女士香水', '中性香水', '香薰'],
                '美发': ['洗发水', '护发素', '发膜', '染发剂', '造型产品'],
                '身体护理': ['沐浴露', '身体乳', '护手霜', '脱毛产品', '止汗露']
            },
            '母婴玩具': {
                '奶粉辅食': ['婴儿奶粉', '成人奶粉', '米粉', '果泥', '肉泥', '营养米粉'],
                '尿裤湿巾': ['纸尿裤', '拉拉裤', '湿巾', '隔尿垫'],
                '喂养用品': ['奶瓶', '奶嘴', '吸奶器', '辅食碗', '水杯', '温奶器'],
                '玩具': ['积木', '玩偶', '遥控车', '拼图', '乐器玩具', '科学玩具', '益智玩具'],
                '童车': ['婴儿车', '自行车', '滑板车', '三轮车', '平衡车', '儿童座椅']
            },
            '运动户外': {
                '运动器材': ['跑步机', '哑铃', '瑜伽垫', '跳绳', '仰卧板', '健身车', '弹力带'],
                '户外装备': ['帐篷', '睡袋', '登山包', '水壶', '手电筒', '户外刀具', '指南针'],
                '运动服饰': ['运动衣', '运动裤', '运动鞋', '运动内衣', '运动袜'],
                '球类': ['篮球', '足球', '乒乓球', '羽毛球', '网球', '排球', '高尔夫球'],
                '游泳': ['泳衣', '泳镜', '泳帽', '浮板', '救生衣', '游泳圈']
            },
            '图书音像': {
                '文学小说': ['古典文学', '现代文学', '外国文学', '科幻小说', '推理小说', '言情小说', '武侠小说'],
                '经管励志': ['经济', '管理', '理财', '职场', '成功励志', '商业'],
                '科技教育': ['计算机', '数学', '物理', '语言学习', '考试辅导', '编程'],
                '艺术设计': ['绘画', '设计', '摄影', '音乐', '舞蹈', '书法'],
                '童书': ['绘本', '童话', '百科全书', '少儿文学', '认知书', '启蒙读物']
            },
            '汽车用品': {
                '装饰': ['座垫', '脚垫', '香水', '挂饰', '方向盘套', '车贴'],
                '保养': ['机油', '添加剂', '防冻液', '玻璃水', '车蜡', '洗车液'],
                '电子': ['行车记录仪', '导航仪', '车载充电器', '倒车雷达', '车载音响'],
                '安全': ['儿童安全座椅', '灭火器', '急救包', '三角警示牌', '安全带'],
                '配件': ['轮胎', '雨刮器', '滤清器', '灯泡', '喇叭', '刹车片']
            },
            '医疗保健': {
                '医疗器械': ['轮椅', '拐杖', '助行器', '病床', '病历车', '医用推车', '治疗车', '抢救车', '送药车', '护理车',
                           '无菌车', '器械车', '病例夹车', '查房车', '病历推车', '收纳车', '医用不锈钢治疗车',
                           '血压计', '血糖仪', '体温计', '雾化器'],
                '医用耗材': ['口罩', '手套', '纱布', '棉签', '绷带', '输液器', '注射器', '创可贴'],
                '护理用品': ['成人纸尿裤', '护理垫', '湿巾', '清洁用品'],
                '康复器材': ['康复训练器', '理疗仪', '按摩器', '牵引器']
            },
            '办公用品': {
                '办公家具': ['办公桌', '办公椅', '文件柜', '保险柜', '白板', '书架', '会议桌'],
                '文具': ['笔', '笔记本', '文件夹', '订书机', '计算器', '胶水', '尺子', '橡皮'],
                '打印耗材': ['墨盒', '硒鼓', '打印纸', '色带', '复印纸'],
                '办公设备': ['复印机', '扫描仪', '投影仪', '会议设备', '考勤机', '碎纸机']
            },
            '工业原料': {
                '塑料原料': ['聚乙烯PE', '聚丙烯PP', '聚氯乙烯PVC', '聚苯乙烯PS', 'ABS塑料', '尼龙PA', '聚碳酸酯PC', '聚甲醛POM', 'PET塑料'],
                '橡胶原料': ['天然橡胶', '合成橡胶', '硅橡胶', '丁腈橡胶', '乳胶'],
                '金属材料': ['钢材', '铝材', '铜材', '不锈钢', '合金材料', '钛合金'],
                '化工产品': ['涂料', '油漆', '胶粘剂', '溶剂', '助剂', '染料'],
                '包装材料': ['塑料袋', '塑料薄膜', '气泡袋', '打包带', '缠绕膜', '塑料瓶', '纸箱']
            },
            '宠物用品': {
                '宠物食品': ['狗粮', '猫粮', '宠物零食', '营养品', '罐头', '冻干', '磨牙棒'],
                '宠物玩具': ['毛绒玩具', '咬胶', '逗猫棒', '漏食球', '飞盘', '猫爬架'],
                '宠物窝垫': ['宠物窝', '宠物垫', '猫抓板', '宠物床', '宠物毯'],
                '宠物洗护': ['宠物沐浴露', '宠物梳', '指甲剪', '宠物牙刷', '除臭剂', '宠物湿巾'],
                '宠物药品': ['驱虫药', '耳药', '眼药', '益生菌', '皮肤病药'],
                '宠物服饰': ['宠物衣服', '宠物项圈', '牵引绳', '宠物鞋', '宠物雨衣']
            },
            '珠宝首饰': {
                '黄金首饰': ['黄金项链', '黄金戒指', '黄金手镯', '黄金耳环', '黄金吊坠'],
                '银饰': ['银项链', '银戒指', '银手镯', '银耳环', '纯银饰品'],
                '钻石珠宝': ['钻戒', '钻石项链', '钻石耳环', '钻石手链'],
                '玉石': ['翡翠', '和田玉', '独山玉', '岫玉', '玉镯', '玉吊坠'],
                '珍珠': ['珍珠项链', '珍珠耳环', '珍珠手链', '珍珠戒指'],
                '手镯': ['金手镯', '银手镯', '玉手镯', '钻石手镯', '情侣手镯'],
                '戒指': ['钻戒', '黄金戒指', '银戒指', '情侣戒指', '对戒'],
                '项链': ['金项链', '银项链', '珍珠项链', '钻石项链', '吊坠项链']
            },
            '乐器': {
                '键盘乐器': ['钢琴', '电子琴', '电钢琴', '电子管风琴', '合成器'],
                '弦乐器': ['吉他', '电吉他', '木吉他', '贝斯', '尤克里里', '小提琴', '中提琴', '大提琴'],
                '民族乐器': ['古筝', '二胡', '琵琶', '笛子', '箫', '扬琴', '古琴'],
                '打击乐器': ['架子鼓', '电子鼓', '非洲鼓', '木琴', '铃鼓'],
                '管乐器': ['口琴', '单簧管', '萨克斯', '小号', '长笛', '竖笛'],
                '乐器配件': ['琴弦', '琴包', '吉他拨片', '调音器', '节拍器', '乐谱']
            },
            '钟表': {
                '手表': ['石英表', '机械表', '电子表', '智能手表', '儿童手表', '运动手表', '女士手表', '男士手表'],
                '挂钟': ['客厅挂钟', '装饰挂钟', '简约挂钟', '复古挂钟', '数字挂钟'],
                '闹钟': ['电子闹钟', '机械闹钟', '智能闹钟', '静音闹钟', '儿童闹钟'],
                '其他钟表': ['落地钟', '台钟', '座钟', '手表配件']
            },
            '礼品定制': {
                '节日礼品': ['圣诞礼物', '新年礼物', '情人节礼物', '七夕礼物', '母亲节礼物', '父亲节礼物'],
                '定制礼品': ['定制照片', '定制刻字', '定制名字项链', '定制抱枕', '定制杯子', '定制T恤'],
                '礼盒包装': ['礼品盒', '礼品袋', '包装纸', '丝带', '贺卡', '礼盒套装'],
                '贺卡': ['生日贺卡', '节日贺卡', '感谢卡', '祝福卡', '定制贺卡']
            },
            '婚庆用品': {
                '喜糖': ['喜糖盒', '巧克力喜糖', '糖果喜糖', '定制喜糖'],
                '喜帖': ['请柬', '喜帖', '定制请柬', '电子请柬'],
                '婚庆布置': ['气球', '鲜花', '花艺', '灯光', '背景板', '红地毯'],
                '婚纱': ['婚纱', '礼服', '伴娘裙', '西服', '晨袍'],
                '婚鞋': ['新娘婚鞋', '新郎婚鞋', '伴娘鞋', '伴郎鞋'],
                '其他婚庆': ['喜字', '红包', '礼金簿', '交杯酒', '誓言本']
            },
            '农耕园艺': {
                '种子': ['蔬菜种子', '花卉种子', '水果种子', '草本种子', '多肉种子'],
                '花苗': ['观赏花苗', '果树苗', '绿植苗', '多肉植物', '盆栽'],
                '园艺工具': ['花铲', '花剪', '园艺手套', '喷壶', '耙子', '铲子', '修枝剪'],
                '花盆': ['塑料花盆', '陶瓷花盆', '水泥花盆', '木花盆', '吊篮花盆'],
                '肥料': ['复合肥', '有机肥', '缓释肥', '液体肥', '生物肥', '土壤调理剂'],
                '土壤': ['营养土', '腐殖土', '泥炭土', '种植基质', '水培营养液']
            },
            '安全防护': {
                '头部防护': ['安全帽', '头盔', '防撞帽', '安全帽配件'],
                '足部防护': ['安全鞋', '绝缘鞋', '防滑鞋', '防穿刺鞋'],
                '眼部防护': ['防护眼镜', '护目镜', '安全眼罩', '防雾眼镜'],
                '身体防护': ['反光衣', '防护服', '防尘服', '防化服', '绝缘衣'],
                '手部防护': ['防护手套', '绝缘手套', '防割手套', '防化手套', '劳保手套'],
                '呼吸防护': ['防尘口罩', '防毒面具', '空气呼吸器', '过滤面罩']
            },
            '消防器材': {
                '灭火器材': ['干粉灭火器', '水基灭火器', '二氧化碳灭火器', '泡沫灭火器', '灭火器箱'],
                '消防报警': ['烟雾报警器', '燃气报警器', '温感报警器', '消防警铃'],
                '消防配件': ['消防水带', '消防栓', '消防枪头', '消防阀', '消防管道'],
                '消防工具': ['消防锹', '消防斧', '消防镐', '消防钩', '应急灯'],
                '应急设备': ['应急包', '逃生绳', '消防面具', '防火毯', '应急广播']
            }
        }

        # 具体产品关键词映射（用于精确识别）
        self.product_keywords = {
            # 电脑硬件
            'CPU处理器': ['core', 'i9', 'i7', 'i5', 'i3', 'ryzen', '锐龙', 'xeon', '至强', 'athlon', '速龙', 'epyc', 'cpu'],
            '显卡': ['rtx', 'gtx', 'geforce', 'radeon', 'rx', 'quadro', 'tesla', '显存', 'gpu', '显卡'],
            '内存': ['ddr', '内存条', 'ram', 'dimm', 'sodimm'],
            '硬盘': ['ssd', '固态', 'hdd', '机械硬盘', 'm.2', 'nvme', 'sata'],
            'U盘': ['u盘', '优盘', 'usb闪存盘', '闪存盘'],
            '移动硬盘': ['移动硬盘', '便携硬盘', '外置硬盘'],
            '存储卡': ['sd卡', 'tf卡', 'micro sd', '存储卡', '内存卡'],
            '主板': ['主板', 'motherboard', 'b660', 'z790', 'b760', 'x670'],
            # 医疗器械（增加更多关键词）
            '治疗车': ['治疗车', '抢救车', '送药车', '护理车', '无菌车', '器械车', '医用推车', '病历车', '病例夹车', '查房车', '病历推车', '收纳车'],
        }

        # 品牌映射
        self.brand_mapping = {
            # 手机
            '苹果': {'category': '电子产品', 'sub_category': '手机通讯', 'keywords': ['iphone', 'apple', 'ipad', 'macbook']},
            '华为': {'category': '电子产品', 'sub_category': '手机通讯', 'keywords': ['华为', 'huawei', 'mate']},
            '小米': {'category': '电子产品', 'sub_category': '手机通讯', 'keywords': ['小米', 'xiaomi', 'redmi', '红米']},
            '三星': {'category': '电子产品', 'sub_category': '手机通讯', 'keywords': ['三星', 'samsung', 'galaxy']},
            'OPPO': {'category': '电子产品', 'sub_category': '手机通讯', 'keywords': ['oppo']},
            'vivo': {'category': '电子产品', 'sub_category': '手机通讯', 'keywords': ['vivo', 'iqoo']},
            '一加': {'category': '电子产品', 'sub_category': '手机通讯', 'keywords': ['一加', 'oneplus']},
            '荣耀': {'category': '电子产品', 'sub_category': '手机通讯', 'keywords': ['荣耀', 'honor']},
            # 电脑硬件
            '英特尔': {'category': '电子产品', 'sub_category': '电脑硬件', 'keywords': ['intel', '英特尔']},
            'AMD': {'category': '电子产品', 'sub_category': '电脑硬件', 'keywords': ['amd']},
            '英伟达': {'category': '电子产品', 'sub_category': '电脑硬件', 'keywords': ['nvidia', '英伟达']},
            '金士顿': {'category': '电子产品', 'sub_category': '电脑硬件', 'keywords': ['金士顿', 'kingston']},
            '闪迪': {'category': '电子产品', 'sub_category': '电脑硬件', 'keywords': ['闪迪', 'sandisk']},
            # 电脑办公
            '联想': {'category': '电子产品', 'sub_category': '电脑办公', 'keywords': ['联想', 'lenovo']},
            '戴尔': {'category': '电子产品', 'sub_category': '电脑办公', 'keywords': ['戴尔', 'dell']},
            '惠普': {'category': '电子产品', 'sub_category': '电脑办公', 'keywords': ['惠普', 'hp']},
            '华硕': {'category': '电子产品', 'sub_category': '电脑办公', 'keywords': ['华硕', 'asus']},
            '宏碁': {'category': '电子产品', 'sub_category': '电脑办公', 'keywords': ['宏碁', 'acer']},
            # 家用电器
            '海尔': {'category': '家用电器', 'sub_category': '厨房电器', 'keywords': ['海尔', 'haier']},
            '美的': {'category': '家用电器', 'sub_category': '厨房电器', 'keywords': ['美的', 'midea']},
            '格力': {'category': '家用电器', 'sub_category': '制冷电器', 'keywords': ['格力', 'gree']},
            '西门子': {'category': '家用电器', 'sub_category': '厨房电器', 'keywords': ['西门子', 'siemens']},
            '飞利浦': {'category': '家用电器', 'sub_category': '个护电器', 'keywords': ['飞利浦', 'philips']},
            '戴森': {'category': '家用电器', 'sub_category': '生活电器', 'keywords': ['戴森', 'dyson']},
            # 宠物
            '皇家': {'category': '宠物用品', 'sub_category': '宠物食品', 'keywords': ['皇家', 'royal canin']},
            '冠能': {'category': '宠物用品', 'sub_category': '宠物食品', 'keywords': ['冠能', 'proplan']},
            '渴望': {'category': '宠物用品', 'sub_category': '宠物食品', 'keywords': ['渴望', 'orijen']},
            # 乐器
            '雅马哈': {'category': '乐器', 'sub_category': '键盘乐器', 'keywords': ['雅马哈', 'yamaha']},
            '罗兰': {'category': '乐器', 'sub_category': '键盘乐器', 'keywords': ['罗兰', 'roland']},
            '吉普森': {'category': '乐器', 'sub_category': '弦乐器', 'keywords': ['吉普森', 'gibson']},
            '芬达': {'category': '乐器', 'sub_category': '弦乐器', 'keywords': ['芬达', 'fender']},
            # 钟表
            '卡西欧': {'category': '钟表', 'sub_category': '手表', 'keywords': ['卡西欧', 'casio']},
            '西铁城': {'category': '钟表', 'sub_category': '手表', 'keywords': ['西铁城', 'citizen']},
            '精工': {'category': '钟表', 'sub_category': '手表', 'keywords': ['精工', 'seiko']},
            '天王': {'category': '钟表', 'sub_category': '手表', 'keywords': ['天王']},
            # 珠宝
            '周大福': {'category': '珠宝首饰', 'sub_category': '黄金首饰', 'keywords': ['周大福']},
            '周生生': {'category': '珠宝首饰', 'sub_category': '黄金首饰', 'keywords': ['周生生']},
            '老凤祥': {'category': '珠宝首饰', 'sub_category': '黄金首饰', 'keywords': ['老凤祥']},
            '周大生': {'category': '珠宝首饰', 'sub_category': '黄金首饰', 'keywords': ['周大生']},
        }

        # 关键词权重映射 - 提高医疗关键词权重
        self.keyword_weights = {
            '医疗保健': {
                'keywords': ['医疗', '医用', '病例', '病历', '治疗车', '抢救车', '送药车', '护理车', '无菌车', '器械车',
                           '医用推车', '病历车', '病例夹车', '查房车', '病历推车', '收纳车', '轮椅', '拐杖', '病床',
                           '血压', '血糖', '体温', '护理', '康复', '理疗', '手术', '诊断', '治疗', '器械', '耗材',
                           '口罩', '纱布', '绷带', '创可贴', '医用手套'],
                'score': 10
            },
            '电子产品': {
                'keywords': ['手机', '电脑', '笔记本', '平板', '显卡', 'cpu', '主板', '内存', '硬盘', '固态', 'u盘', '优盘',
                           '移动硬盘', '存储卡', '电源', '机箱', '散热器', '显示器', '耳机', '相机', '智能', '电视',
                           '音响', '数据线', '充电器'],
                'score': 8
            },
            '工业原料': {
                'keywords': ['塑料', '聚乙烯', '聚丙烯', '聚氯乙烯', '聚苯乙烯', 'abs', '尼龙', '聚碳酸酯', '橡胶', '硅橡胶',
                           '钢材', '铝材', '铜材', '合金', '化工', '涂料', '油漆', '包装材料', '薄膜', '母粒'],
                'score': 7  # 降低工业原料权重，让医疗优先
            },
            '家用电器': {
                'keywords': ['冰箱', '洗衣机', '空调', '热水器', '微波炉', '烤箱', '空气炸锅', '电饭煲', '榨汁机', '吸尘器',
                           '电风扇', '取暖器', '破壁机', '电磁炉', '空气净化器', '加湿器', '吹风机', '剃须刀', '咖啡机', '电水壶'],
                'score': 7
            },
            '宠物用品': {
                'keywords': ['宠物', '狗粮', '猫粮', '狗窝', '猫窝', '逗猫棒', '猫爬架', '牵引绳', '宠物零食', '宠物玩具',
                           '宠物护理', '宠物衣服', '宠物窝', '猫抓板'],
                'score': 6
            },
            '珠宝首饰': {
                'keywords': ['黄金', '银饰', '钻石', '翡翠', '珍珠', '手镯', '戒指', '项链', '吊坠', '白金', '铂金', '金项链', '银项链'],
                'score': 6
            },
            '乐器': {
                'keywords': ['吉他', '钢琴', '电子琴', '小提琴', '架子鼓', '古筝', '二胡', '口琴', '萨克斯', '贝斯', '尤克里里'],
                'score': 6
            },
            '钟表': {
                'keywords': ['手表', '挂钟', '闹钟', '石英表', '机械表', '电子表', '智能手表', '儿童手表'],
                'score': 6
            },
            '办公用品': {
                'keywords': ['办公', '文件柜', '保险柜', '白板', '文具', '打印', '墨盒', '硒鼓', '复印机', '办公桌', '办公椅'],
                'score': 5
            },
            '家居生活': {
                'keywords': ['沙发', '床', '餐桌', '衣柜', '窗帘', '地毯', '厨具', '清洁', '收纳', '装饰', '塑料盆', '塑料桶',
                           '塑料箱', '收纳盒', '衣架', '花盆', '锅具', '餐具'],
                'score': 5
            },
            '礼品定制': {
                'keywords': ['礼品', '定制', '礼盒', '贺卡', '礼物', '个性化', '刻字', '礼品盒'],
                'score': 4
            },
            '婚庆用品': {
                'keywords': ['喜糖', '喜帖', '婚纱', '婚鞋', '婚庆', '请柬', '婚礼', '喜糖盒'],
                'score': 4
            },
            '农耕园艺': {
                'keywords': ['种子', '花苗', '园艺', '花盆', '肥料', '土壤', '绿植', '植物', '营养土'],
                'score': 4
            },
            '安全防护': {
                'keywords': ['安全帽', '防护眼镜', '反光衣', '安全鞋', '防护服', '防尘', '护目镜'],
                'score': 4
            },
            '消防器材': {
                'keywords': ['灭火器', '烟雾报警', '消防栓', '消防水带', '应急', '消防', '防火毯'],
                'score': 4
            },
            '服装鞋帽': {
                'keywords': ['衣服', '裤子', '裙子', '鞋', '帽子', '围巾', '手套', '羽绒服', 't恤', '衬衫', '运动鞋', '休闲鞋'],
                'score': 3
            },
            '食品饮料': {
                'keywords': ['食品', '饮料', '水果', '蔬菜', '肉类', '零食', '奶粉', '咖啡', '茶', '粮油', '调味', '牛奶', '矿泉水'],
                'score': 3
            },
            '美妆护肤': {
                'keywords': ['护肤', '彩妆', '香水', '洗发', '沐浴', '美容', '化妆', '洁面', '精华', '面膜', '口红', '粉底'],
                'score': 3
            },
            '母婴玩具': {
                'keywords': ['婴儿', '宝宝', '玩具', '尿裤', '奶瓶', '童车', '积木', '辅食', '奶粉', '纸尿裤'],
                'score': 3
            },
            '运动户外': {
                'keywords': ['运动', '户外', '健身', '游泳', '登山', '跑步', '球', '器材', '装备', '帐篷', '跑步机'],
                'score': 3
            },
            '图书音像': {
                'keywords': ['书', '小说', '教材', 'cd', 'dvd', '杂志', '绘本', '文学', '艺术', '科技', '计算机', '编程'],
                'score': 3
            },
            '汽车用品': {
                'keywords': ['汽车', '车用', '行车记录', '导航', '机油', '轮胎', '座垫', '脚垫', '行车记录仪'],
                'score': 3
            }
        }

        # 医疗关键词列表（用于最优先匹配）
        self.medical_keywords = [
            '治疗车', '抢救车', '送药车', '护理车', '无菌车', '器械车', '医用推车',
            '病历车', '病例夹车', '查房车', '病历推车', '收纳车', '医用不锈钢',
            '病例夹', '医院器械', '护士病历', '加厚收纳车'
        ]

    def find_category(self, product_name):
        """
        为商品查找合适的类目
        返回: (一级类目, 二级类目, 具体分类)
        """
        product_name_lower = product_name.lower().strip()

        # 如果商品名为空，返回其他
        if not product_name_lower:
            return '其他', '综合', '未知商品'

        # ========== 策略0: 医疗器械最高优先级匹配 ==========
        # 先检查是否是医疗器械（优先级最高，不受"不锈钢"干扰）
        for keyword in self.medical_keywords:
            if keyword in product_name_lower:
                # 在医疗保健类目下查找匹配
                if '医疗保健' in self.categories:
                    for sub_cat, items in self.categories['医疗保健'].items():
                        for item in items:
                            # 尝试精确匹配子类目中的商品
                            if item.lower() in product_name_lower or product_name_lower in item.lower():
                                return '医疗保健', sub_cat, item
                    # 如果没有精确匹配，返回医疗器械子类目
                    return '医疗保健', '医疗器械', self.categories['医疗保健']['医疗器械'][0]

        # ========== 策略1: 产品关键词匹配 ==========
        for item_name, keywords in self.product_keywords.items():
            for keyword in keywords:
                if keyword in product_name_lower:
                    for main_cat, sub_cats in self.categories.items():
                        for sub_cat, items in sub_cats.items():
                            if item_name in items:
                                return main_cat, sub_cat, item_name

        # ========== 策略2: 品牌识别 ==========
        for brand, info in self.brand_mapping.items():
            for keyword in info['keywords']:
                if keyword in product_name_lower:
                    main_cat = info['category']
                    sub_cat = info['sub_category']

                    best_item = None
                    best_score = 0
                    for item in self.categories[main_cat][sub_cat]:
                        score = 0
                        item_lower = item.lower()
                        if item_lower in product_name_lower:
                            score += len(item_lower) * 3
                        if keyword in product_name_lower:
                            score += len(keyword) * 2
                        numbers = re.findall(r'\d+', product_name)
                        if numbers:
                            score += len(numbers) * 2

                        if score > best_score:
                            best_score = score
                            best_item = item

                    if best_item:
                        return main_cat, sub_cat, best_item
                    return main_cat, sub_cat, self.categories[main_cat][sub_cat][0]

        # ========== 策略3: 精确匹配 ==========
        for main_cat, sub_cats in self.categories.items():
            for sub_cat, items in sub_cats.items():
                for item in items:
                    item_lower = item.lower()
                    if item_lower in product_name_lower or product_name_lower in item_lower:
                        return main_cat, sub_cat, item

        # ========== 策略4: 特殊处理"塑料" ==========
        if '塑料' in product_name_lower:
            if any(keyword in product_name_lower for keyword in ['颗粒', '原料', '母粒', '改性', '树脂', 'pe', 'pp', 'pvc', 'ps', 'abs', 'pa', 'pc', 'pom', 'pet']):
                return '工业原料', '塑料原料', self._find_best_match_in_category('工业原料', '塑料原料', product_name_lower)
            elif any(keyword in product_name_lower for keyword in ['盆', '桶', '箱', '收纳盒', '衣架', '椅子', '花盆', '杯', '碗', '盘']):
                return '家居生活', '塑料制品', self._find_best_match_in_category('家居生活', '塑料制品', product_name_lower)
            elif any(keyword in product_name_lower for keyword in ['袋', '膜', '瓶', '打包', '缠绕', '气泡']):
                return '工业原料', '包装材料', self._find_best_match_in_category('工业原料', '包装材料', product_name_lower)
            else:
                return '工业原料', '塑料原料', '塑料原料'

        # ========== 策略5: 加权关键词匹配 ==========
        best_match = None
        best_score = 0
        matched_keyword = ''

        for main_cat, info in self.keyword_weights.items():
            score = 0
            matched = ''
            for keyword in info['keywords']:
                if keyword in product_name_lower:
                    keyword_score = info['score'] + len(keyword) * 2
                    score += keyword_score
                    matched = keyword

            if score > best_score:
                best_score = score
                best_match = main_cat
                matched_keyword = matched

        if best_match and best_score > 5:
            for sub_cat, items in self.categories[best_match].items():
                for item in items:
                    if matched_keyword in item.lower() or any(k in product_name_lower for k in item.split()):
                        return best_match, sub_cat, item
            first_sub = list(self.categories[best_match].keys())[0]
            return best_match, first_sub, self.categories[best_match][first_sub][0]

        # ========== 策略6: 模糊匹配 ==========
        return self._fuzzy_match(product_name_lower)

    def _find_best_match_in_category(self, main_cat, sub_cat, product_name):
        """在指定类目中查找最匹配的商品"""
        if main_cat in self.categories and sub_cat in self.categories[main_cat]:
            for item in self.categories[main_cat][sub_cat]:
                if item.lower() in product_name:
                    return item
            return self.categories[main_cat][sub_cat][0]
        return '塑料制品'

    def _fuzzy_match(self, product_name):
        """模糊匹配"""
        keyword_map = {
            '医疗保健': ['医疗', '医用', '治疗车', '抢救车', '送药车', '护理车', '无菌车', '器械车', '病历车',
                       '轮椅', '拐杖', '病床', '血压', '血糖', '体温', '口罩', '纱布', '绷带', '创可贴'],
            '电子产品': ['手机', '电脑', '平板', '耳机', '相机', '充电', '数据线', '智能', '电视', '音响',
                       '显卡', 'cpu', '内存', '硬盘', 'u盘', '优盘'],
            '家用电器': ['冰箱', '洗衣机', '空调', '热水器', '微波炉', '烤箱', '空气炸锅', '电饭煲', '吸尘器', '电风扇'],
            '工业原料': ['塑料', '聚乙烯', '聚丙烯', '聚氯乙烯', '橡胶', '钢材', '铝材', '铜材', '合金', '化工', '涂料', '油漆'],
            '办公用品': ['办公', '文件柜', '保险柜', '白板', '文具', '打印', '墨盒', '硒鼓', '复印机'],
            '宠物用品': ['宠物', '狗粮', '猫粮', '狗窝', '猫窝', '牵引绳', '宠物玩具', '猫爬架'],
            '珠宝首饰': ['黄金', '银饰', '钻石', '翡翠', '珍珠', '手镯', '戒指', '项链', '吊坠'],
            '乐器': ['吉他', '钢琴', '电子琴', '小提琴', '架子鼓', '古筝', '二胡', '口琴', '萨克斯'],
            '钟表': ['手表', '挂钟', '闹钟', '石英表', '机械表', '电子表'],
            '礼品定制': ['礼品', '定制', '礼盒', '贺卡', '礼物'],
            '婚庆用品': ['喜糖', '喜帖', '婚纱', '婚鞋', '婚庆', '请柬'],
            '农耕园艺': ['种子', '花苗', '园艺', '花盆', '肥料', '土壤', '营养土'],
            '安全防护': ['安全帽', '防护眼镜', '反光衣', '安全鞋', '防护服', '护目镜'],
            '消防器材': ['灭火器', '烟雾报警', '消防栓', '消防水带', '应急', '防火毯'],
            '服装鞋帽': ['衣服', '裤子', '裙子', '鞋', '帽子', '围巾', '手套', '羽绒服', 't恤', '衬衫', '运动鞋'],
            '食品饮料': ['食品', '饮料', '水果', '蔬菜', '肉类', '零食', '咖啡', '茶', '牛奶'],
            '家居生活': ['家具', '床', '沙发', '桌', '椅', '柜', '餐具', '厨具', '装饰', '地毯', '窗帘'],
            '美妆护肤': ['护肤', '彩妆', '香水', '洗发', '沐浴', '美容', '化妆', '洁面', '面膜'],
            '母婴玩具': ['婴儿', '宝宝', '玩具', '尿裤', '奶瓶', '童车', '积木', '纸尿裤'],
            '运动户外': ['运动', '户外', '健身', '游泳', '登山', '跑步', '球', '器材', '帐篷'],
            '图书音像': ['书', '小说', '教材', '绘本', '文学', '艺术', '科技', '编程'],
            '汽车用品': ['汽车', '车用', '行车记录', '导航', '机油', '轮胎', '座垫', '脚垫']
        }

        for main_cat, keywords in keyword_map.items():
            for keyword in keywords:
                if keyword in product_name:
                    for sub_cat, items in self.categories.get(main_cat, {}).items():
                        for item in items:
                            if keyword in item.lower() or item.lower() in keyword:
                                return main_cat, sub_cat, item
                    if main_cat in self.categories:
                        first_sub = list(self.categories[main_cat].keys())[0]
                        first_item = self.categories[main_cat][first_sub][0]
                        return main_cat, first_sub, first_item

        return '其他', '综合', '其他商品'

    def add_product_keywords(self, item_name, keywords):
        """添加产品关键词映射"""
        if item_name not in self.product_keywords:
            self.product_keywords[item_name] = []
        self.product_keywords[item_name].extend(keywords)

    def add_brand(self, brand_name, category, sub_category, keywords):
        """添加品牌映射"""
        self.brand_mapping[brand_name] = {
            'category': category,
            'sub_category': sub_category,
            'keywords': keywords
        }

    def add_category(self, main_cat, sub_cat, items):
        """添加新的类目"""
        if main_cat not in self.categories:
            self.categories[main_cat] = {}
        if sub_cat not in self.categories[main_cat]:
            self.categories[main_cat][sub_cat] = []
        self.categories[main_cat][sub_cat].extend(items)

    def display_categories(self):
        """显示所有类目"""
        print("=" * 80)
        print("商品类目列表（完整版）")
        print("=" * 80)
        for main_cat, sub_cats in self.categories.items():
            print(f"\n【{main_cat}】")
            for sub_cat, items in sub_cats.items():
                display_items = ', '.join(items[:6])
                suffix = '...' if len(items) > 6 else ''
                print(f"  └─ {sub_cat}: {display_items}{suffix}")
        print("=" * 80)


# ================= 使用示例 =================

def search(product):
    # 创建类目管理器
    manager = CategoryManager()

    main_cat, sub_cat, item = manager.find_category(product)
    return main_cat+'/'+sub_cat+'/'+item

if __name__ == "__main__":
    print(search('杯子'))
    print(search('保温杯'))