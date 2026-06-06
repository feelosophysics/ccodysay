PRAGMA foreign_keys = ON;

INSERT INTO CATEGORY (id, name) VALUES(1, '컴퓨터과학');
INSERT INTO CATEGORY (id, name) VALUES(2, '과학/수학');
INSERT INTO CATEGORY (id, name) VALUES(3, '인문/철학');
INSERT INTO CATEGORY (id, name) VALUES(4, '경제/경영');
INSERT INTO CATEGORY (id, name) VALUES(5, '문학/소설');
INSERT INTO CATEGORY (id, name) VALUES(6, '예술/대중문화');
INSERT INTO CATEGORY (id, name) VALUES(7, '역사');
INSERT INTO CATEGORY (id, name) VALUES(8, '에세이/시');
INSERT INTO CATEGORY (id, name) VALUES(9, '언어/외국어');
INSERT INTO CATEGORY (id, name) VALUES(10, '자기계발');

--

INSERT INTO MEMBER (id, name, email, phone, join_date) VALUES (1, '이영희', 'younghee@example.com', '010-1234-5678', '2025-01-10');
INSERT INTO MEMBER (id, name, email, phone, join_date) VALUES (2, '김철수', 'chulsoo@example.com', '010-2345-6789', '2025-02-15');
INSERT INTO MEMBER (id, name, email, phone, join_date) VALUES (3, '박민수', 'minsoo@example.com', '010-3456-7890', '2025-03-01');
INSERT INTO MEMBER (id, name, email, phone, join_date) VALUES (4, '최지우', 'jiwoo@example.com', '010-4567-8901', '2025-04-12');
INSERT INTO MEMBER (id, name, email, phone, join_date) VALUES (5, '정다은', 'daeun@example.com', '010-5678-9012', '2025-05-20');
INSERT INTO MEMBER (id, name, email, phone, join_date) VALUES (6, '강동원', 'dongwon@example.com', '010-6789-0123', '2025-06-05');
INSERT INTO MEMBER (id, name, email, phone, join_date) VALUES (7, '한소희', 'sohee@example.com', NULL, '2025-07-22'); -- 전화번호가 없는 회원 (NULL 허용 검증)
INSERT INTO MEMBER (id, name, email, phone, join_date) VALUES (8, '송강호', 'kangho@example.com', '010-8901-2345', '2025-08-30');
INSERT INTO MEMBER (id, name, email, phone, join_date) VALUES (9, '아이유', 'iu@example.com', '010-9012-3456', '2025-09-18');
INSERT INTO MEMBER (id, name, email, phone, join_date) VALUES (10, '임영웅', 'hero@example.com', '010-0123-4567', '2025-10-05');
INSERT INTO MEMBER (id, name, email, phone, join_date) VALUES (12, '고길동', 'gildong_go@example.com', '010-7777-7777', '2025-11-20'); -- 도서를 한 번도 대여하지 않은 휴면 회원 (Query 13 검증용)

--

INSERT INTO BOOK (id, title, category_id, author, price, published_date) VALUES (1, '밑바닥부터 시작하는 딥러닝', 1, '사이토 고키', 28000, '2016-12-01');
INSERT INTO BOOK (id, title, category_id, author, price, published_date) VALUES (2, '클린 코드', 1, '로버트 C. 마틴', 33000, '2013-12-24');
INSERT INTO BOOK (id, title, category_id, author, price, published_date) VALUES (3, '코스모스', 2, '칼 세이건', 19500, '2006-12-20');
INSERT INTO BOOK (id, title, category_id, author, price, published_date) VALUES (4, '사피엔스', 7, '유발 하라리', 22000, '2011-01-01'); 
INSERT INTO BOOK (id, title, category_id, author, price, published_date) VALUES (5, '코딩 인터뷰 189가지 질문과 해답', 1, '스티븐 하우이', 35000, '2017-11-15');
INSERT INTO BOOK (id, title, category_id, author, price, published_date) VALUES (6, '리팩토링', 1, '마틴 파울러', 42000, '2000-08-01');
INSERT INTO BOOK (id, title, category_id, author, price, published_date) VALUES (7, 'SQL 안티패턴', 1, '레오나르드 르우프', 25000, '2016-05-01');
INSERT INTO BOOK (id, title, category_id, author, price, published_date) VALUES (8, 'Python 알고리즘 인터뷰', 1, '박상길', 29000, '2020-03-15');
INSERT INTO BOOK (id, title, category_id, author, price, published_date) VALUES (9, '해커스 토익 스타트', 9, '해커스어학연구소', 15000, '2023-02-10');
INSERT INTO BOOK (id, title, category_id, author, price, published_date) VALUES (10, '혼자 공부하는 파이썬', 1, '윤성우', 23000, '2019-07-01');
INSERT INTO BOOK (id, title, category_id, author, price, published_date) VALUES (11, 'Java의 정석', 1, '남궁성', 32000, '2005-01-01'); -- 2005년 발행된 고전 프로그래밍 서적 (Query 20 검증용)


--

-- 건 1: 이영희(1)가 딥러닝 책(1)을 대여하여 정상 반납함.
INSERT INTO RENTAL (id, member_id, book_id, rental_date, return_date, status) 
VALUES (1, 1, 1, '2026-04-01', '2026-04-10', 'RETURNED');

-- 건 2: 이영희(1)가 클린 코드(2)를 대여하여 정상 반납함. (다독 회원 시나리오)
INSERT INTO RENTAL (id, member_id, book_id, rental_date, return_date, status) 
VALUES (2, 1, 2, '2026-04-15', '2026-04-28', 'RETURNED');

-- 건 3: 김철수(2)가 코스모스(3)를 대여했으나 기한이 한참 지나 연체됨. (2026-04-10 대여 후 무소식 -> 연체 시나리오)
INSERT INTO RENTAL (id, member_id, book_id, rental_date, return_date, status) 
VALUES (3, 2, 3, '2026-04-10', NULL, 'OVERDUE');

-- 건 4: 박민수(3)가 정의란 무엇인가(4)를 대여하여 반납함.
INSERT INTO RENTAL (id, member_id, book_id, rental_date, return_date, status) 
VALUES (4, 3, 4, '2026-04-20', '2026-05-02', 'RETURNED');

-- 건 5: 최지우(4)가 부의 시나리오(5)를 최근에 빌려가서 열심히 읽는 중. (정상 대여 시나리오)
INSERT INTO RENTAL (id, member_id, book_id, rental_date, return_date, status) 
VALUES (5, 4, 5, '2026-05-20', NULL, 'RENTED');

-- 건 6: 정다은(5)이 해리 포터(6)를 대여하여 반납함.
INSERT INTO RENTAL (id, member_id, book_id, rental_date, return_date, status) 
VALUES (6, 5, 6, '2026-05-01', '2026-05-12', 'RETURNED');

-- 건 7: 강동원(6)이 사피엔스(7)를 빌려갔으나 반납 기한이 지나 연체됨.
INSERT INTO RENTAL (id, member_id, book_id, rental_date, return_date, status) 
VALUES (7, 6, 7, '2026-04-25', NULL, 'OVERDUE');

-- 건 8: 한소희(7)가 총균쇠(8)를 최근에 빌려감. (정상 대여)
INSERT INTO RENTAL (id, member_id, book_id, rental_date, return_date, status) 
VALUES (8, 7, 8, '2026-05-22', NULL, 'RENTED');

-- 건 9: 송강호(8)가 데미안(9)을 대여하여 반납함.
INSERT INTO RENTAL (id, member_id, book_id, rental_date, return_date, status) 
VALUES (9, 8, 9, '2026-05-05', '2026-05-15', 'RETURNED');

-- 건 10: 아이유(9)가 원씽(10)을 빌려서 현재 읽는 중. (정상 대여)
INSERT INTO RENTAL (id, member_id, book_id, rental_date, return_date, status) 
VALUES (10, 9, 10, '2026-05-21', NULL, 'RENTED');

-- 건 11: 아이유(9)가 딥러닝 책(1)도 함께 대여함. (인기 있는 책의 다회차 대여 검증용)
INSERT INTO RENTAL (id, member_id, book_id, rental_date, return_date, status) 
VALUES (11, 9, 1, '2026-05-22', NULL, 'RENTED');

-- 건 12: 임영웅(10)이 코스모스(3)를 이전에 빌렸다가 정상 반납함.
INSERT INTO RENTAL (id, member_id, book_id, rental_date, return_date, status) 
VALUES (12, 10, 3, '2026-05-01', '2026-05-10', 'RETURNED');

-- 건 13: 이영희(1)가 사피엔스(7)를 이전에 빌렸다가 반납함. (이영희 회원의 3번째 거래)
INSERT INTO RENTAL (id, member_id, book_id, rental_date, return_date, status) 
VALUES (13, 1, 7, '2026-04-20', '2026-05-01', 'RETURNED');

-- 건 14: 김철수(2)가 정의란 무엇인가(4)를 대여했다가 정상 반납함.
INSERT INTO RENTAL (id, member_id, book_id, rental_date, return_date, status) 
VALUES (14, 2, 4, '2026-05-02', '2026-05-14', 'RETURNED');

-- 건 15: 박민수(3)가 클린 코드(2)를 아주 최근에 대여함.
INSERT INTO RENTAL (id, member_id, book_id, rental_date, return_date, status) 
VALUES (15, 3, 2, '2026-05-23', NULL, 'RENTED');