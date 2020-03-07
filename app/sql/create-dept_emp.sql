CREATE TABLE `dept_emp` (
   `emp_no` int(11) NOT NULL,
   `dept_no` char(4) NOT NULL,
   `from_date` date NOT NULL,
   `to_date` date NOT NULL,
   PRIMARY KEY (`emp_no`,`dept_no`), KEY `emp_no` (`emp_no`),
   KEY `dept_no` (`dept_no`),
   CONSTRAINT `dept_emp_ibfk_1` FOREIGN KEY (`emp_no`)
      REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,
   CONSTRAINT `dept_emp_ibfk_2` FOREIGN KEY (`dept_no`)
      REFERENCES `departments` (`dept_no`) ON DELETE CASCADE
) ENGINE=InnoDB