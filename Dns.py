
class Dns():
    def __init__(self):
        self.ip = "8.8.8.8"
        self.dnsResolver = {
            "www.google.com": "206.160.74.213.80",
            "www.globo.com.br": "128.28.110.71.80",
            "www.youtube.com": "186.254.39.192.80",
            "www.facebook.com": "75.96.27.18.80",
            "www.twitter.com": "87.208.74.154.80",
            "www.uff.br": "130.125.99.157.80",
            "www.instagram.com": "220.171.28.94.80",
            "www.github.com": "92.170.228.200.80",
            "www.ligamagic.com.br": "133.188.176.251.80",
            "www.nytimes.com": "108.96.103.167.80",
            "www.theguardian.com": "16.221.8.140.80",
            "www.imdb.com": "23.104.179.123.80",
            "www.washingtonpost.com": "215.144.163.221.80",
            "www.mercedes-benz.com.br": "39.229.161.77.80",
            "www.ferrari.com": "177.22.101.70.80"
        }

    def resolveDnsReq(self, url):
        return self.dnsResolver[url]
