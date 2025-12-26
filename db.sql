create database transportdb;

use transportdb;
show tables;
-- 1. 用户表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(50),
    role VARCHAR(20) DEFAULT '员工' -- 例如：管理员、调度员、司机
);

-- 2. 车辆表
CREATE TABLE vehicles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    plate_number VARCHAR(20) NOT NULL UNIQUE, -- 车牌号
    type VARCHAR(50) NOT NULL, -- 车辆类型
    status VARCHAR(20) DEFAULT '空闲' -- 状态：空闲、运输中、维修
);

-- 3. 司机表
CREATE TABLE drivers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(20)
);

-- 4. 运输任务表 (整合了申请和运营管理)
CREATE TABLE transport_tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    client_name VARCHAR(100), -- 客户名称
    need_vehicle_type VARCHAR(50), -- 需要的车型
    need_count INT, -- 需要数量
    plan_mileage DECIMAL(10,2), -- 计划里程
    plan_start_time DATETIME, -- 计划开始时间
    plan_end_time DATETIME, -- 计划结束时间
    -- 实际安排
    vehicle_id INT, -- 安排的车号
    driver_id INT, -- 安排的司机
    real_start_time DATETIME, -- 实际开始时间
    real_end_time DATETIME, -- 实际结束时间
    real_mileage DECIMAL(10,2), -- 实际里程
    fuel_used DECIMAL(10,2), -- 实际耗油量
    status VARCHAR(20) DEFAULT '待安排', -- 状态：待安排、运输中、已完成
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
    FOREIGN KEY (driver_id) REFERENCES drivers(id)
);

-- 5. 事故记录表
CREATE TABLE accidents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    vehicle_id INT NOT NULL, -- 事故车辆
    driver_id INT NOT NULL, -- 当事司机
    accident_time DATETIME NOT NULL, -- 事故时间
    location TEXT, -- 事故地点
    reason TEXT, -- 事故原因
    handle_method TEXT, -- 处理方式
    cost DECIMAL(12,2), -- 处理金额
    other_plate VARCHAR(50), -- 对方车号
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
    FOREIGN KEY (driver_id) REFERENCES drivers(id)
);



-- 插入用户数据
INSERT INTO users (username, password, name, role) VALUES
('root', '123', 'root', '老板'),
('user1', '123', '刘师傅', '司机');

-- 插入车辆数据
INSERT INTO vehicles (plate_number, type, status) VALUES
('京A12345', '轿车', '空闲'),
('京B12345', '大货车', '任务中'),
('京C12345', '小货车', '空闲');

-- 插入司机数据
INSERT INTO drivers (name, phone) VALUES
('张三', '11111111111'),
('李四', '11111111112'),
('王五', '11111111113');

-- 插入运输任务数据
INSERT INTO transport_tasks (client_name, need_vehicle_type, need_count, plan_mileage, plan_start_time, plan_end_time, vehicle_id, driver_id, status) VALUES
('北京食品公司', '大货车', 1, 120.50, '2025-12-02 08:00:00', '2025-12-02 18:00:00', 2, 1, '进行中');

-- 插入事故记录数据
INSERT INTO accidents (vehicle_id, driver_id, accident_time, location, reason, handle_method, cost, other_plate) VALUES
(1, 2, '2025-12-01 14:30:00', '京沪高速入口', '追尾', '保险理赔', 5000.00, '京D12345');
