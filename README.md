# Python DataCamp to Trello scrape

Accesses [the list of all courses](https://www.datacamp.com/courses/all) on
DataCamp and uploads each course with its link and description to a trello
board. Requires a xml file structured like so:

```xml
<info>
    <key>(key here)<\key>
    <secret>(secret here)<\secret>
<\info>
```

These two values are obtained from [here](https://trello.com/app-key)
