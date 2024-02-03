-- Write query to find the number of grade A's given by the teacher who has graded the most assignments


SELECT state, COUNT(*) as count
FROM assignments
GROUP BY state
ORDER BY state;