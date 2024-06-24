CREATE TABLE info_stock (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'id',
    stock_code VARCHAR(20) NOT NULL COMMENT '股票编码',
    stock_name VARCHAR(100) NOT NULL COMMENT '股票名称'
)  COMMENT '股票信息表';

CREATE TABLE info_dict_item (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'id',
    dict_key VARCHAR(32) NOT NULL COMMENT '字典key',
    dict_item VARCHAR(32) NOT NULL COMMENT '字典项',
    dict_value VARCHAR(128) NOT NULL COMMENT '字典值',
    dict_comment VARCHAR(128) NOT NULL COMMENT '字典项备注'
)  COMMENT '字典信息表';