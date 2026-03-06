## 1. Count all lines with `500` HTTP code

```bash
grep -c ' 500 ' sample.log
```

714 lines

 grep on 500 to only get 500 code.

## 2. Count all `GET` requests from `yoko` to `/rrhh` with `200` status

**Command:**
```bash
grep 'yoko' sample.log | grep 'GET' | grep '/rrhh' | grep ' 200 ' | wc -l
```

4 requests

  chain multiple grep filters to match all criteria.

## 3. How many requests go to `/`?

**Command:**
```bash
grep -c ' /"' sample.log
```

717 requests

  match lines ending with ` /"`.

## 4. Count all lines without `5XX` HTTP code

**Command:**
```bash
grep -cvE ' 5[0-9][0-9]' sample.log
```

2191 lines

 We use -v to invert the match and -E for extended regex. The pattern ` [0-9][0-9]` for the 2 digits that will change from 0 to 9 

## 5. Replace all 503 by 500, then count 500 lines

**Command:**
```bash
sed 's/ 503 / 500 /g' sample.log | grep -c ' 500 '
```

1469 lines

 First we use sed to replace all occurrences of 503  with 500, and then count the amount of 500
