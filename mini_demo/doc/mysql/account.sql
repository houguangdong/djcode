/*
 Navicat Premium Data Transfer

 Source Server         : vmware-mysql
 Source Server Type    : MySQL
 Source Server Version : 50638
 Source Host           : 192.168.109.128:3306
 Source Schema         : jpzmgtest

 Target Server Type    : MySQL
 Target Server Version : 50638
 File Encoding         : 65001

 Date: 14/12/2017 16:40:44
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for accounts_0
-- ----------------------------
DROP TABLE IF EXISTS `accounts_0`;
CREATE TABLE `accounts_0`  (
  `account_number` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '账号名',
  `account_pwd` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码',
  `add_time` int(11) NOT NULL,
  `login_time` int(11) NOT NULL,
  `openid` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`account_number`)
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for accounts_mapping_0
-- ----------------------------
DROP TABLE IF EXISTS `accounts_mapping_0`;
CREATE TABLE `accounts_mapping_0`  (
  `openid` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `account_number` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '账号名',
  `openkey` varchar(72) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`openid`)
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for account_users_0
-- ----------------------------
DROP TABLE IF EXISTS `account_users_0`;
CREATE TABLE `account_users_0`  (
  `openid` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `user_info` mediumblob NOT NULL,
  PRIMARY KEY (`openid`)
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;


-- ----------------------------
-- Table structure for account_login_check_0
-- ----------------------------
DROP TABLE IF EXISTS `account_login_check_0`;
CREATE TABLE `account_login_check_0`  (
  `openid` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `openkey` varchar(72) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `channel_id` int(11) NOT NULL,
  `platform_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `app_version` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `build_version` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `res_version` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `uid` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `age_stage` int(11) NOT NULL,
  `istourist` int(11) NOT NULL,
  `enter_game` int(11) NOT NULL,
  `refresh_play_time` int(11) NOT NULL,
  `play_time` int(11) NOT NULL,
  `refresh_week_time` int(11) NOT NULL,
  `recharge_week_money` int(11) NOT NULL,
  `refresh_month_time` int(11) NOT NULL,
  `recharge_month_money` int(11) NOT NULL,
  PRIMARY KEY (`openid`)
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;


SET FOREIGN_KEY_CHECKS = 1;