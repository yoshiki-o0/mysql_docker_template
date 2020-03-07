CREATE TABLE `titles` (
    `emp_no` int(11) NOT NULL,
    `title` varchar(50) NOT NULL,
    `from_date` date NOT NULL,
    `to_date` date DEFAULT NULL,
    PRIMARY KEY (`emp_no`,`title`,`from_date`), KEY `emp_no` (`emp_no`),
    CONSTRAINT `titles_ibfk_1` FOREIGN KEY (`emp_no`)
        REFERENCES `employees` (`emp_no`) ON DELETE CASCADE
) ENGINE=InnoDB