# Ithome ironman crawler


## Usage
```
scrapy crawl ithome \
	-o {{ OUTPUT_FILE_PATH }} \
	-t {{ OUTPUT_TYPE }} \
	-a {{ ITHOME_IRONMAN_PAGE_URL}}
```

## Example
```
scrapy crawl ithome \
	-o tmp.csv \
	-t csv \
	-a ironman_man_page="https://ithelp.ithome.com.tw/users/20151613/ironman/5333"
```
