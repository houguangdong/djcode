SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for users_0
-- ----------------------------
DROP TABLE IF EXISTS `users_0`;
CREATE TABLE `users_0`
(
    `uid`         varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
    `openid`      varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
    `username`    varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
--     `gender`      varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    `icons`       int(11)                                                      NULL DEFAULT NULL,
--     `state`       int(11)                                                      NULL DEFAULT NULL,  /* 账号状态 0 正常，1 冻结，2 注销 */
    `channel_id`  int(12)                                                      NOT NULL,            /* 渠道 */
    `add_time`    int(11)                                                      NOT NULL,
    `login_time`  int(11)                                                      NOT NULL,
    `login_ip`    varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    `session_key` varchar(64),
    PRIMARY KEY (`uid`)
) ENGINE = InnoDB
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_general_ci
  ROW_FORMAT = Compact;