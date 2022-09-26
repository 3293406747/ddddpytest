/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80028
 Source Host           : localhost:3306
 Source Schema         : test_db

 Target Server Type    : MySQL
 Target Server Version : 80028
 File Encoding         : 65001

  Date: 26/09/2022 12:55:24
*/

-- 创建数据库test_db
DROP DATABASE IF EXISTS `test_db`;
CREATE DATABASE `test_db` CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';
USE `test_db`;

-- 创建user数据表
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `name` varchar(16) NOT NULL,
  `sex` enum('男','女') NOT NULL DEFAULT '男',
  `age` int(0) NOT NULL,
  `phone` varchar(255) NULL DEFAULT NULL,
  `ssn` varchar(255) NOT NULL,
  `card` varchar(255) NULL DEFAULT NULL,
  `createtime` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `updatetime` timestamp(0) NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间'
);

-- 插入数据
INSERT INTO `user` VALUES ('张红霞', '女', 21, '15803456513', '211204196204245151', '375370181699897', DEFAULT, DEFAULT),
('齐霞', '女', 20, '15329524166', '360724194409205386', '4649612116334070', DEFAULT, DEFAULT);