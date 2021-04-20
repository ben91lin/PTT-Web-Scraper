import pytest
import re
from bs4 import BeautifulSoup
from article_viewer import PttArticleViewer

@pytest.fixture
def instance():
    return PttArticleViewer(headers = { 'cookie': 'over18=1;' })

def test_instance(instance):
    assert isinstance(instance, PttArticleViewer)

def test_meta(instance):
    instance.get('https://www.ptt.cc/bbs/Gossiping/M.1119243418.A.790.html')
    assert instance.meta() == {
        'datetime': 'Mon Jun 20 13:04:48 2005',
        'timestamp': 1119243888.0,
        'author_ip': '220.137.87.186',
        'author_id': 'MCI',
        'author_nickname': '步步步步步步步步',
        'title': 'Re: (問題)華航空難留言'
    }
    
def test_content(instance):
    instance.get('https://www.ptt.cc/bbs/Gossiping/M.1119243418.A.790.html')
    assert instance.content() == '''<div class="bbs-screen bbs-content" id="main-content">
<span class="f2">※ 引述《suandfly (槍兵￼ ￼N￾ ￾ ￼ ￼NＩ》之銘言：
</span><span class="f6">: ※ 引述《certifi (i miss you)》之銘言：
</span><span class="f6">: : 看到這邊，就知道是垃圾
</span><span class="f6">: : 1998年
</span><span class="f6">: : 2月16日華航空中巴士a300-600r在中正機場重飛失敗，墜毀
</span><span class="f6">: : 2月19日R-CH-1在白沙灣，墜毀
</span><span class="f6">: : 2月24日t-38台東外海墜毀，駕駛跳傘逃生
</span><span class="f6">: : 3月2日德安航空貝爾412型直昇機在澎湖外海降落於鑽油平台，失速墜毀
</span><span class="f6">: : 3月17日陸軍輕航隊th-55型直昇機，在歸仁迫降失敗，墜毀
</span><span class="f6">: : 3月18日國華SAAB300型客機在新竹機場離場時，於海中墜毀
</span><span class="f6">: : 3月20日F-16-B澎湖外海墜毀
</span><span class="f6">: : 每4年發生一次空難--又是只取有利的樣本
</span><span class="f6">: 講到空難
</span><span class="f6">: 我也來暴個八卦
</span><span class="f6">: 還記得當年有一架直昇機
</span><span class="f6">: 掉到德基水庫吧
</span><span class="f6">: 據說....
</span><span class="f6">: 是飛行員...學長帶著學弟兩架直昇機
</span><span class="f6">: 去完蜻蜓點水....
</span><span class="f6">: 結果沒點好就下去了....
</span><span class="f6">: ORZ..
</span>講到直升機空難 民國63年陸軍昌x演習曾經發生一次有史以來最嚴重的空難
當時兩架直升機上包括官階最高的陸軍總司令于上將 還有好幾位中將
總共二十幾顆星星隕落
據說當時生還者中唯一意識清楚的是官階最小的高上尉 也是于上將的侍從官
他負傷把于上將從殘骸中拖出來 然後跑到公路上求救
不過于上將後半輩子半身不遂 有點像阿甘的劇情 不過于上將家人始終很感謝高
直到于上將晚年過世後還有連絡 也有一說是幾位將軍用肉身保護總司令
總司令才能幸運生還 至於這位高上尉後來一直升到聯勤總司令 也當了上將
目前在某個服務老榮民的單位當主委 這位高將軍在921時也擔任中部救災指揮官
前陣子看到新聞說他有可能是國防部長的黑馬人選
我想可能是那些被他幫助過的人在天上保佑他吧!

--
<span class="f2">※ 發信站: 批踢踢實業坊(ptt.cc) 
</span>◆ From: 220.137.87.186
</div>'''

def test_comments(instance):
    instance.get('https://www.ptt.cc/bbs/Gossiping/M.1119243418.A.790.html')
    assert isinstance(instance.comments(), list)
    assert isinstance(instance.comments()[0], dict)
    assert instance.comments()[0] == {
        'comment_datetime': '06/20',
        'tag': '推',
        'commentor_id': 'saitoh',
        'commentor_ip': '220.130.172.76',
        'comment': '高上尉是高滑助嗎?'
    }

#TODO try other test to respond web updated.
def test_hrefs(instance):
    instance.get('https://www.ptt.cc/bbs/Beauty/M.1618533391.A.AAA.html')
    assert instance.hrefs() == {
        'comment_hrefs': [],
        'article_hrefs': ['https://i.imgur.com/fPCHCvT.jpg', 'https://i.imgur.com/wSMKEXS.jpg', 'https://i.imgur.com/KkErEoJ.jpg', 'https://i.imgur.com/7GBL0kN.jpg', 'https://i.imgur.com/dgE23MT.jpg', 'https://i.imgur.com/UYOUmNk.jpg', 'https://i.imgur.com/Vp8whlS.jpg']
        }
    instance.get('https://www.ptt.cc/bbs/joke/M.1618416499.A.B18.html')
    assert instance.hrefs() == {
        'comment_hrefs': [],
        'article_hrefs': ['https://imgur.com/a/O59cE5x', 'https://i.imgur.com/1IhledD.gif', 'https://i.imgur.com/XFWtfSQ.gif', 'https://i.imgur.com/L2UjHQP.gif', 'https://i.imgur.com/MUWC8kY.gif', 'https://i.imgur.com/YpZq4wc.gif', 'https://i.imgur.com/wFuYnhX.gif', 'https://i.imgur.com/nH90DWP.gif', 'https://i.imgur.com/Mv5QCet.gif', 'https://i.imgur.com/bRgskP1.gif', 'https://i.imgur.com/Vh1xMg9.gif', 'https://i.imgur.com/TWRa3P4.gif', 'https://i.imgur.com/6ypHjpJ.gif', 'https://i.imgur.com/A0oMYvM.gif', 'https://i.imgur.com/d3j3nXr.gif', 'https://i.imgur.com/17eOAJd.gif', 'https://i.imgur.com/S8DaOYR.gif', 'https://i.imgur.com/iGKxB3Y.gif', 'https://i.imgur.com/iR4jIIj.gif', 'https://i.imgur.com/7BoXtGP.gif', 'https://i.imgur.com/WwfJQCD.gif', 'https://i.imgur.com/cqbprLW.gif', 'https://i.imgur.com/4Xb1pni.jpg']
        }
    instance.get('https://www.ptt.cc/bbs/Beauty/M.1618447251.A.51A.html')
    assert instance.hrefs() == {
        'comment_hrefs': ['https://i.imgur.com/s2Vc9Uu.jpg', 'https://youtu.be/k6LTVYwf_Q4'],
        'article_hrefs': ['https://i.imgur.com/3ikHZhF.jpg', 'https://i.imgur.com/uq6gFDf.jpg', 'https://i.imgur.com/VpUnZgC.jpg', 'https://i.imgur.com/FpRnWpi.jpg', 'https://i.imgur.com/OTDj5vK.jpg', 'https://i.imgur.com/uyOAXqM.jpg', 'https://i.imgur.com/QDEfRtz.jpg', 'https://i.imgur.com/YgdPMzU.jpg', 'https://i.imgur.com/OJwYNwB.jpg', 'https://i.imgur.com/u562cb1.jpg', 'https://i.imgur.com/WZg9FcA.jpg', 'https://i.imgur.com/tET4bSf.jpg', 'https://i.imgur.com/uyp42dg.jpg', 'https://i.imgur.com/y2ErUM3.jpg']
    }
    