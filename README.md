# KindleDXPush

This project was created by [@blahgeek][1], now maintained by [@lord63][2].

## Intro

As we all know, we can use Amazon's free 3G network to deliver our docs, but we need
to manually click the deliver buttom in the browser. This script is born to rescue
us from this boring thing. Config this script, add it to the `crontab` and you'are done.
All your docs will be sent to your kindle automatically.


## Requirement

* Python 2.7(I haven't test it using python 3)
* Requests lib
* BeautifulSoup lib
* Linux platform(I haven't test it on windows)

## Feature

* It has a log file, you can check which file you've delivered.

* Use sqlite database, don't worry about that a doc will be missed or delivered twice.

## Usage

touch a new python file named `config.py`, including those:

    EMAIL = "xxx@gmail.com"  # your amazon's username
    PASSWORD = "xxxxxx"      # your amazon's password
    COUNT = 15               # check how many docs every time that whether those files have been delivered or not. 

just run it

    $ python main.py
    Login...
    Delivering...
    delivering YOUR DOC
    Done. Save to db.
    delivering YOUR DOC
    Done. Save to db.

## Wiki

see [wiki](https://github.com/lord63/kindledxpush/wiki)

## License

MIT


[1]: https://github.com/blahgeek
[2]: https://github.com/lord63
