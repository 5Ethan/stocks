CREATE TABLE info_stock (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'id',
    stock_code VARCHAR(20) NOT NULL COMMENT '股票编码',
    stock_name VARCHAR(100) NOT NULL COMMENT '股票名称'
)  COMMENT '股票信息表';