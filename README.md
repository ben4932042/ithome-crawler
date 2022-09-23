# Ithome ironman crawler


## Usage
```
scrapy crawl ithome
```

## Output Data

### User info
- mongo collection name: user_info
- big query table: user_info_tmp, user_info_hist

| column_name       | type | example       | Description|
|-------------------|------|---------------|---------------|
| _id               | int  | 20151613      |ithome 使用者 ID|
| crawl_datetime    | datetime | ISODate("2022-09-20T00:32:35.000Z") |資料爬取時間|
| user_id           | int  | 20151613      |ithome 使用者 ID|
| user_name         | str  | BenLiu        |ithome 使用者名稱|
| ithome_level      | str  | iT邦新手 5 級 |ithome 使用者等級|
| ithome_point      | int  | 90            |ithome 使用者點數|
| user_viewed       | int  | 887           |ithome 使用者總被觀看數|
| user_followed     | int  | 2             |ithome 使用者總被追蹤數|
| ask_question      | int  | 0             |ithome 使用者發問數|
| article           | int  | 21            |ithome 使用者總文章數|
| answer            | int  | 0             |ithome 使用者總回答數|
| invitation_answer | int  | 0             |ithome 使用者總被邀請回答數|
| best_answer       | int  | 0             |ithome 使用者總被最佳解答數|


### Content info
- mongo collection name: content_info
- big query table: content_info_tmp, content_info_hist

| column_name     | type     | example                                        |Description|
|-----------------|----------|------------------------------------------------|----------|
| _id             | str      | 20151613-5333-10287313                         |MONGO 文章索引|
| crawl_datetime  | datetime | ISODate("2022-09-20T00:32:35.000Z")            |資料爬取時間|
| text            | str      |                                                |鐵人賽文章內容|
| user_id         | int      | 20151613                                       |ithome 使用者 ID|
| ironman_id      | int      | 5333                                           |鐵人賽 ID|
| title           | str      | 第二天 Jenkins 之旅： Welcome to Jenkins!        |鐵人賽文章標題|
| like            | int      | 0                                              |鐵人賽文章按讚數|
| comment         | int      | 0                                              |鐵人賽文章留言數|
| view            | int      | 450                                            |鐵人賽文章觀看數|
| article_id      | int      | 10287313                                       |鐵人賽文章 ID|
| article_url     | str      | https://ithelp.ithome.com.tw/articles/10287313 |鐵人賽文章網址|
| create_datetime | datetime | ISODate("2022-09-20T00:32:35.000Z")            |鐵人賽文章發表時間|


- big query table: content_info_tmp, content_info_view_change
| column_name     | type     | example                                        |Description|
|-----------------|----------|------------------------------------------------|----------|
| ironman_id      | int      | 5333                                           |鐵人賽 ID|
| article_id      | int      | 10287313                                       |鐵人賽文章 ID|
| view            | int      | 450                                            |鐵人賽文章觀看數|
| crawl_datetime  | datetime | ISODate("2022-09-20T00:32:35.000Z")            |資料爬取時間|