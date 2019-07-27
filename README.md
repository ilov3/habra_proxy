### https://habr.com site web proxy

Very basic implementation of initial task with following limitations:
1) Proxies only GET requests
2) Login/Register pages misses styles
3) PEP8 maximum line length not met

### Installation / startup

If docker installed:
1) docker build --tag=habr_proxy .
2) docker run -p 8080:8080 habr_proxy
3) Open browser on http://127.0.0.1:8080

To run tests inside container:
1) docker build -f Dockerfile.test --tag habr_proxy_tests .
2) docker run habr_proxy_tests

If no docker installed :( :
1) Make virtualenv with python 3.7
2) pip install -r requirements.txt
3) Run python -m aiohttp.web -H 0.0.0.0 -P 8080 proxy:init_app
4) Open browser on http://127.0.0.1:8080

To run tests:
1) Run python tests.py