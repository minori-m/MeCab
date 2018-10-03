// このプログラムはwebサーバーにPOSTで認証トークンを送信し、機能トークンを受け取る。
// 機能トークンをSocketIOで渡し、サーバーと接続する。
// 接続したサーバーからオリジナルの文字を受け取り、puppeteerで韻ノートへ送信。結果を受け取り
// google-home-notifierでGoogle Homeへ送信する。
// google home settings
var googlehome = require('google-home-notifier');
var language = 'ja';
googlehome.ip('192.168.123.45');
googlehome.device('Google Home', language);
// server settings
const BaseUrl = 'https://iotwebappraiot.azurewebsites.net/';
const aiaiUrl = BaseUrl + 'getRyme/';
const authQuery = {
    authToken: "D462253D54FB3C4BE77AE1992341A279",
    user: "nullo"
}
// InNote setting
const addressOfInNote = 'http://in-note.com/';
// serverから機能トークンを得る
const axios = require('axios');
axios.post(aiaiUrl, authQuery)
    .then((res) => {
        if (res.data != "err") {
            //サーバー認証用クエリに機能トークンを設定
            let funcQuery = {
                query: {
                    token: res.data
                }
            };
            //ソケット通信開始
            startSocket(funcQuery);
        } else {
            console.log('auth error:', err);
        }
    })
    .catch(err => {
        console.log('err:', err);
    });
// socket.IO通信の開始とイベント登録
function startSocket(funcQuery) {
    // socket IOを接続先（Azureサーバー）指定で読み込む
    const io = require('socket.io-client');
    let socket = io(BaseUrl, funcQuery);
    // 機能トークンの認証結果がサーバーから返ってくる
    socket.on('join', (result) => {
        console.log("join:" + result.data);
    });
    socket.on('ifttt', (origin) => {
        console.log("\nI received original word:\n" + origin + "\n");
        // サーバから受け取った語句をwebサービスの韻ノートに送り、韻を受け取る
        (async () => {
            const say = await getAndModifyRyme(origin)
                .catch(() => 'ごめん、韻が見つからなかったよ');
            sayGoogleHome(say);
        })();
    });
}
//sayの内容をgoogle homeへ送信する。（話させる）
function sayGoogleHome(say) {
    try {
        googlehome.notify(say, (res) => {
            console.log(res);
        });
        //error
    } catch (err) {
        console.log(err);
    }
}
// 韻ノートにoriginから韻を得て、発話内容に加工する。
async function getAndModifyRyme(origin) {
    label = "exec"
    console.time(label);
    getRyme = new ScrapeRymeInNote();
    let data = await getRyme.scrapeRhyme(origin, addressOfInNote);
    let say = origin + "\n";
    for (let i = 0; i < data.length; i++) {
        say += (i + 1) + ": " + data[i] + "　(" + data[i] + ")\n";
    }
    console.log(say);
    console.timeEnd(label);
    return say;
}
//　韻ノートからスクレイピングするクラス
class ScrapeRymeInNote {
    //　アクセス
    async _initPuppeteer(puppeteer, address) {
        const browser = await puppeteer.launch({
            headless: true,
            executablePath: '/usr/bin/chromium-browser',
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        const page = await browser.newPage();
        await page.goto(address, { waitUntil: "domcontentloaded" });
        return { page: page, browser: browser };
    }
    //　データ入手
    async _getRhyme(origin, page) {
        await page.type("body > div.main > div.main-search > div > input", origin);//　テキスト入力
        //検索ボタンクリック
        await page.evaluate(() => {
            document.querySelector("body > div.main > div.main-search > div > button").click();
        });
        await page.waitFor('span[class="word-main"]', { timeout: 10000 });// 画面遷移を待つ    
        // 結果のテキストを入手
        let data = await page.$$eval('span.word-main', items => {
            // 得た複数の結果を配列化して返す
            const resultNumber = 4;
            let texts = [];
            for (let i = 0; i < resultNumber; i++) {
                if (items[i]) {
                    texts.push(items[i].textContent);
                }
            }
            return texts;
        });
        return data;
    }
    //originキーワードから韻を入手する公開関数
    async scrapeRhyme(origin, address) {
        const puppeteer = require('puppeteer');
        const pupp = await this._initPuppeteer(puppeteer, address);
        let data = await this._getRhyme(origin, pupp.page);
        await pupp.browser.close();
        return data;
    }
}