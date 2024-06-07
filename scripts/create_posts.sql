DROP TABLE IF EXISTS posts;


CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    content VARCHAR NOT NULL,
    published BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);


INSERT INTO posts (title, content, published)
    VALUES ('First Post', 'This is the first post.', TRUE);
INSERT INTO posts (title, content, published)
    VALUES ('Second Post', 'This is the second post.', FALSE);
INSERT INTO posts (title, content, published)
    VALUES ('Third Post', 'This is the third post.', TRUE);
