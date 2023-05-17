## Vertica

| Command                                                                                      | Time |
|----------------------------------------------------------------------------------------------| ------ |
| SELECT COUNT(*) FROM views [8031452]                                                         |0.07944325611782367|
| SELECT count(DISTINCT user_id) FROM views [10000]                                            |7.612572161626752|
| INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (?,?,?,?) |20.425123671226544 |