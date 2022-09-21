# Ithome ironman crawler


## Usage
```
scrapy crawl ithome
```

## Output Data
### User info
- mongo collection name: user

| column_name       | type | example       |
|-------------------|------|---------------|
| user_id           | int  | 20151613      |
| user_name         | str  | BenLiu        |
| ithome_level      | str  | iT邦新手 5 級 |
| ithome_point      | int  | 90            |
| user_viewed       | int  | 887           |
| user_followed     | int  | 2             |
| ask_question      | int  | 0             |
| article           | int  | 21            |
| answer            | int  | 0             |
| invitation_answer | int  | 0             |
| best_answer       | int  | 0             |


### Content info
- mongo collection name: devops_group

| column_name     | type     | example                                        |
|-----------------|----------|------------------------------------------------|
| user_id         | int      | 20151613                                       |
| ironman_id      | int      | BenLiu                                         |
| title           | str      | 第二天 Jenkins 之旅： Welcome to Jenkins!      |
| like            | int      | 0                                              |
| comment         | int      | 0                                              |
| view            | int      | 450                                            |
| article_id      | int      | 10287313                                       |
| article_url     | str      | https://ithelp.ithome.com.tw/articles/10287313 |
| create_datetime | datetime |                                                |