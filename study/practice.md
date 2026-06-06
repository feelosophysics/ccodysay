select m.name
from member m
inner join rental r on r.member_id = m.id
inner join book b on b.id = r.book_id
where b.title = '사피엔스';

SELECT id, name, email
FROM MEMBER
WHERE id IN (
    SELECT member_id
    FROM RENTAL
    WHERE book_id = (
        SELECT id
        FROM BOOK
        WHERE title = '사피엔스'
    )
);

select m.id, m.name, m.email
from member m
where id in (
select member_id
from rental
where book_id = (
select id
from book
where title = '사피엔스'));