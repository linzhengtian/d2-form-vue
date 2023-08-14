-- ----------------------------
-- Records of permission_role
-- ----------------------------
INSERT INTO permission_role (id, description, modifier, dept_belong_id, update_datetime, create_datetime, roleName, roleKey, roleSort, status, admin, dataScope, remark, creator_id) VALUES(1, '', 'admin', '1', '2023-08-06 23:12:47.048057000', '2021-02-27 08:48:08.064911000', '超级管理员', 'admin', 1, '1', 1, '1', NULL, 1);
INSERT INTO permission_role (id, description, modifier, dept_belong_id, update_datetime, create_datetime, roleName, roleKey, roleSort, status, admin, dataScope, remark, creator_id) VALUES(2, '', 'admin', '1', '2023-08-06 23:13:20.763026000', '2021-02-27 08:48:47.317214000', '普通角色', 'common', 2, '1', 0, '1', NULL, 1);
INSERT INTO permission_role (id, description, modifier, dept_belong_id, update_datetime, create_datetime, roleName, roleKey, roleSort, status, admin, dataScope, remark, creator_id) VALUES(3, '', 'admin', '1', '2023-08-06 23:13:34.924720000', '2023-08-06 12:28:09.925834000', '北京公司角色', 'beijing', 3, '1', 0, '4', NULL, 1);
INSERT INTO permission_role (id, description, modifier, dept_belong_id, update_datetime, create_datetime, roleName, roleKey, roleSort, status, admin, dataScope, remark, creator_id) VALUES(4, '', 'admin', '1', '2023-08-06 23:14:09.299012000', '2023-08-06 12:29:51.533575000', '上海公司角色', 'shanghai', 4, '1', 0, '3', NULL, 1);
INSERT INTO permission_role (id, description, modifier, dept_belong_id, update_datetime, create_datetime, roleName, roleKey, roleSort, status, admin, dataScope, remark, creator_id) VALUES(5, '', 'admin', '1', '2023-08-06 23:14:33.315436000', '2023-08-06 12:31:24.966461000', '总公司角色', 'total', 5, '1', 0, '2', NULL, 1);
INSERT INTO permission_role (id, description, modifier, dept_belong_id, update_datetime, create_datetime, roleName, roleKey, roleSort, status, admin, dataScope, remark, creator_id) VALUES(6, '', 'admin', '1', '2023-08-06 23:14:43.612852000', '2023-08-06 12:42:05.821236000', '北京研发角色', 'beijingyanfa', 6, '1', 0, '4', NULL, 1);
INSERT INTO permission_role (id, description, modifier, dept_belong_id, update_datetime, create_datetime, roleName, roleKey, roleSort, status, admin, dataScope, remark, creator_id) VALUES(7, '', 'admin', '1', '2023-08-06 23:30:16.496062000', '2023-08-06 12:42:45.783905000', '上海市场角色', 'shanghaishichang', 7, '1', 0, '4', NULL, 1);
-- ----------------------------
-- Records of permission_role_dept
-- ----------------------------
INSERT INTO permission_role_dept (id, role_id, dept_id) VALUES(14, 5, 1);
INSERT INTO permission_role_dept (id, role_id, dept_id) VALUES(15, 5, 2);
INSERT INTO permission_role_dept (id, role_id, dept_id) VALUES(16, 5, 3);
INSERT INTO permission_role_dept (id, role_id, dept_id) VALUES(17, 5, 4);
INSERT INTO permission_role_dept (id, role_id, dept_id) VALUES(18, 5, 6);
INSERT INTO permission_role_dept (id, role_id, dept_id) VALUES(19, 5, 7);
INSERT INTO permission_role_dept (id, role_id, dept_id) VALUES(20, 5, 8);
INSERT INTO permission_role_dept (id, role_id, dept_id) VALUES(21, 5, 9);
INSERT INTO permission_role_dept (id, role_id, dept_id) VALUES(22, 5, 10);
INSERT INTO permission_role_dept (id, role_id, dept_id) VALUES(23, 5, 11);
INSERT INTO permission_role_dept (id, role_id, dept_id) VALUES(24, 5, 12);
INSERT INTO permission_role_dept (id, role_id, dept_id) VALUES(25, 5, 15);
INSERT INTO permission_role_dept (id, role_id, dept_id) VALUES(26, 5, 16);
-- ----------------------------
-- Records of permission_role_menu
-- ----------------------------
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(1, 1, 1);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(2, 1, 2);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(3, 1, 3);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(4, 1, 4);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(5, 1, 5);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(6, 1, 6);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(7, 1, 7);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(8, 1, 8);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(9, 1, 9);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(10, 1, 10);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(21, 1, 11);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(22, 1, 13);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(23, 1, 14);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(24, 1, 15);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(25, 1, 16);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(26, 1, 17);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(27, 1, 18);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(28, 1, 19);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(29, 1, 20);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(30, 1, 21);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(31, 1, 22);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(32, 1, 23);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(33, 1, 24);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(34, 1, 25);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(35, 1, 26);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(36, 1, 27);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(37, 1, 28);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(38, 1, 29);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(39, 1, 30);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(40, 1, 31);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(41, 1, 32);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(42, 1, 33);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(43, 1, 34);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(44, 1, 35);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(45, 1, 36);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(46, 1, 37);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(47, 1, 38);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(48, 1, 39);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(49, 1, 40);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(50, 1, 41);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(51, 1, 42);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(52, 1, 43);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(53, 1, 44);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(54, 1, 45);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(55, 1, 46);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(56, 1, 47);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(57, 1, 48);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(58, 1, 49);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(59, 1, 50);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(60, 1, 51);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(61, 1, 52);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(62, 1, 53);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(63, 1, 54);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(64, 1, 55);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(65, 1, 56);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(66, 1, 57);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(67, 1, 58);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(68, 1, 59);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(69, 1, 60);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(74, 1, 61);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(75, 1, 62);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(76, 1, 63);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(70, 1, 64);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(71, 1, 65);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(79, 1, 66);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(80, 1, 70);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(81, 1, 71);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(82, 1, 72);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(83, 1, 73);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(84, 1, 74);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(85, 1, 75);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(86, 1, 76);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(72, 1, 77);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(73, 1, 78);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(92, 1, 79);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(93, 1, 80);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(94, 1, 81);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(77, 1, 85);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(78, 1, 86);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(95, 1, 87);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(96, 1, 88);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(97, 1, 90);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(98, 1, 91);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(119, 1, 92);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(120, 1, 93);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(121, 1, 94);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(122, 1, 95);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(123, 1, 96);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(100, 1, 97);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(124, 1, 98);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(125, 1, 99);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(126, 1, 100);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(127, 1, 101);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(128, 1, 102);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(129, 1, 103);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(130, 1, 104);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(131, 1, 105);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(132, 1, 106);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(133, 1, 107);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(134, 1, 127);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(115, 1, 128);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(116, 1, 129);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(117, 1, 130);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(118, 1, 131);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(215, 1, 132);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(216, 1, 133);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(217, 1, 134);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(218, 1, 135);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(219, 1, 136);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(99, 2, 97);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(106, 2, 98);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(107, 2, 99);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(108, 2, 100);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(109, 2, 101);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(110, 2, 102);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(111, 2, 103);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(112, 2, 104);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(113, 2, 105);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(114, 2, 106);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(104, 2, 107);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(105, 2, 127);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(101, 2, 128);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(102, 2, 129);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(103, 2, 130);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(220, 2, 131);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(221, 2, 132);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(222, 2, 133);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(223, 2, 134);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(224, 2, 135);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(225, 2, 136);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(136, 3, 97);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(139, 3, 98);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(140, 3, 99);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(141, 3, 100);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(142, 3, 101);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(143, 3, 102);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(144, 3, 103);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(145, 3, 104);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(147, 3, 105);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(148, 3, 106);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(146, 3, 107);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(150, 3, 127);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(135, 3, 128);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(137, 3, 129);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(138, 3, 130);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(149, 3, 131);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(226, 3, 132);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(227, 3, 133);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(228, 3, 134);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(229, 3, 135);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(230, 3, 136);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(152, 4, 97);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(155, 4, 98);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(156, 4, 99);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(157, 4, 100);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(158, 4, 101);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(159, 4, 102);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(160, 4, 103);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(161, 4, 104);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(163, 4, 105);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(164, 4, 106);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(162, 4, 107);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(166, 4, 127);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(151, 4, 128);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(153, 4, 129);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(154, 4, 130);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(165, 4, 131);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(231, 4, 132);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(232, 4, 133);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(233, 4, 134);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(234, 4, 135);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(235, 4, 136);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(168, 5, 97);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(171, 5, 98);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(172, 5, 99);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(173, 5, 100);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(174, 5, 101);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(175, 5, 102);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(176, 5, 103);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(177, 5, 104);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(179, 5, 105);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(180, 5, 106);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(178, 5, 107);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(182, 5, 127);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(167, 5, 128);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(169, 5, 129);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(170, 5, 130);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(181, 5, 131);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(236, 5, 132);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(237, 5, 133);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(238, 5, 134);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(239, 5, 135);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(240, 5, 136);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(184, 6, 97);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(187, 6, 98);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(188, 6, 99);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(189, 6, 100);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(190, 6, 101);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(191, 6, 102);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(192, 6, 103);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(193, 6, 104);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(195, 6, 105);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(196, 6, 106);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(194, 6, 107);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(198, 6, 127);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(183, 6, 128);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(185, 6, 129);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(186, 6, 130);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(197, 6, 131);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(241, 6, 132);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(242, 6, 133);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(243, 6, 134);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(244, 6, 135);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(245, 6, 136);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(200, 7, 97);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(203, 7, 98);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(204, 7, 99);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(205, 7, 100);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(206, 7, 101);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(207, 7, 102);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(208, 7, 103);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(209, 7, 104);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(211, 7, 105);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(212, 7, 106);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(210, 7, 107);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(214, 7, 127);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(199, 7, 128);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(201, 7, 129);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(202, 7, 130);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(213, 7, 131);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(246, 7, 132);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(247, 7, 133);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(248, 7, 134);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(249, 7, 135);
INSERT INTO permission_role_menu (id, role_id, menu_id) VALUES(251, 7, 136);
