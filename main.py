import ccxt
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import talib as ta_lib
import os
import time

# تنظیمات ایمیل
from_email = os.getenv('EMAIL_SENDER')  # ایمیل ارسال کننده از GitHub Secrets
password = os.getenv('EMAIL_PASSWORD')  # رمز عبور ایمیل از GitHub Secrets
email_receiver = os.getenv('EMAIL_RECEIVER')  # ایمیل گیرنده از GitHub Secrets

def send_email(subject, body):
    """ تابع ارسال ایمیل """
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = email_receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(from_email, password)
    server.sendmail(from_email, email_receiver, msg.as_string())
    server.quit()

def fetch_data(symbol, timeframe='30m', max_retries=5):
    """ دریافت داده‌ها از KuCoin با تلاش مجدد در صورت قطع اتصال """
    attempt = 0
    while attempt < max_retries:
        try:
            exchange = ccxt.kucoin()  # استفاده از صرافی KuCoin
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            attempt += 1
            if attempt < max_retries:
                print(f"Retrying... Attempt {attempt + 1}/{max_retries}")
                time.sleep(10)  # زمان انتظار برای تلاش مجدد
            else:
                print(f"Max retries reached for {symbol}. Moving to next symbol.")
                return None  # اگر بعد از چندین تلاش موفق نشد، مقدار None برگرداند

def calculate_zigzag(df):
    """ محاسبه ZigZag با استفاده از TA-Lib """
    df['zigzag'] = ta_lib.CDLDOJI(df['open'], df['high'], df['low'], df['close'])
    return df

def find_patterns(df):
    """ پیدا کردن الگوها در داده‌ها """
    patterns = []
    for index, row in df.iterrows():
        if row['zigzag'] != 0:  # زمانی که الگوی زیگزاگ پیدا شد
            patterns.append(f"{df['timestamp'][index]} - Zigzag detected")
    return patterns

def main():
    """ اجرای اصلی برنامه """
    symbols = ['BTC/USDT', 'XRP/USDT', 'ETH/USDT', 'DOGE/USDT', 'SOL/USDT', 'HBAR/USDT', 'LTC/USDT', 'SUI/USDT', 'PEPE/USDT', 'ADA/USDT', 'SOLV/USDT', 'BNB/USDT', 'XLM/USDT', 'SHIB/USDT', 'ENA/USDT', 'TRX/USDT', 'LINK/USDT', 'AIXBT/USDT', 'PNUT/USDT', 'WIF/USDT', 'WLD/USDT', 'RUNE/USDT', 'ALGO/USDT', 'AVAX/USDT', 'NEIRO/USDT', 'EOS/USDT', 'VET/USDT', 'NEAR/USDT', 'SAND/USDT', 'MOVE/USDT', 'BONK/USDT', 'FET/USDT', 'APT/USDT', 'DOT/USDT', 'FIL/USDT', 'AAVE/USDT', 'UNI/USDT', 'TAO/USDT', 'FLOKI/USDT', 'USUAL/USDT', 'CRV/USDT', 'PHA/USDT', 'TIA/USDT', 'AMP/USDT', 'PENGU/USDT', 'ARB/USDT', 'INJ/USDT', 'CGPT/USDT', 'SEI/USDT', 'IOTA/USDT', 'BCH/USDT', 'RENDER/USDT', 'ZEN/USDT', 'OP/USDT', 'BIO/USDT', 'TON/USDT', 'JASMY/USDT', 'GMT/USDT', 'ICP/USDT', 'ATOM/USDT', 'PENDLE/USDT', 'ETC/USDT', 'RAY/USDT', 'KDA/USDT', 'RSR/USDT', 'BOME/USDT', 'POL/USDT', 'CFX/USDT', 'GRT/USDT', 'VANA/USDT', 'ZRO/USDT', 'IO/USDT', 'ETHFI/USDT', 'STX/USDT', 'ENS/USDT', 'WBTC/USDT', 'COOKIE/USDT', 'TURBO/USDT', 'DYDX/USDT', 'ZK/USDT', 'SUSHI/USDT', 'JUP/USDT', 'BLZ/USDT', 'LDO/USDT', 'ORDI/USDT', 'NOT/USDT', 'EIGEN/USDT', 'OM/USDT', 'THETA/USDT', 'AR/USDT', 'NEO/USDT', 'COW/USDT', 'APE/USDT', 'MANA/USDT', 'MKR/USDT', 'KAIA/USDT', 'CAKE/USDT', 'ARKM/USDT', 'STRK/USDT', 'MEME/USDT', 'EDU/USDT', 'BAL/USDT', 'XAI/USDT', 'CHZ/USDT', 'MANTA/USDT', 'DASH/USDT', 'FTT/USDT', 'BLUR/USDT', 'PROM/USDT', 'SUPER/USDT', 'EGLD/USDT', 'ROSE/USDT', 'ONE/USDT', 'CETUS/USDT', 'LPT/USDT', 'AGLD/USDT', 'FIDA/USDT', 'XTZ/USDT', 'ALT/USDT', 'LUMIA/USDT', 'W/USDT', 'JTO/USDT', 'AXS/USDT', 'LUNC/USDT', 'PYR/USDT', 'COMP/USDT', 'PEOPLE/USDT', 'ME/USDT', 'DOGS/USDT', 'ZRX/USDT', 'PYTH/USDT', 'LUNA/USDT', 'LQTY/USDT', 'QNT/USDT', 'STG/USDT', 'SNX/USDT', 'BB/USDT', 'IOST/USDT', 'ASTR/USDT', 'TRB/USDT', 'SSV/USDT', 'ZIL/USDT', 'PIXEL/USDT', 'MINA/USDT', 'PORTAL/USDT', 'LISTA/USDT', 'IMX/USDT', 'YFI/USDT', 'CELO/USDT', 'ACX/USDT', 'DEXE/USDT', 'WOO/USDT', '1INCH/USDT', 'CKB/USDT', 'FLOW/USDT', 'SCR/USDT', 'ATA/USDT', 'AEVO/USDT', 'VANRY/USDT', 'ONT/USDT', 'ENJ/USDT', 'ANKR/USDT', 'QKC/USDT', 'MAGIC/USDT', 'COTI/USDT', 'AVA/USDT', 'HMSTR/USDT', 'ZEC/USDT', 'DYM/USDT', 'FXS/USDT', 'METIS/USDT', 'SKL/USDT', 'UTK/USDT', 'GAS/USDT', 'OMNI/USDT', 'QTUM/USDT', 'LRC/USDT', 'KSM/USDT', 'YGG/USDT', 'ACH/USDT', 'GMX/USDT', 'DENT/USDT', 'GLMR/USDT', 'CYBER/USDT', 'POLYX/USDT', 'ACE/USDT', 'TRU/USDT', 'CVX/USDT', 'WIN/USDT', 'JST/USDT', 'HIGH/USDT', 'C98/USDT', 'MBL/USDT', 'REZ/USDT', 'RVN/USDT', 'STORJ/USDT', 'BAT/USDT', 'CATI/USDT', 'CLV/USDT', 'DEGO/USDT', 'XEC/USDT', 'TLM/USDT', 'ID/USDT', 'TNSR/USDT', 'SLP/USDT', 'SXP/USDT', 'ILV/USDT', 'ORCA/USDT', 'FLUX/USDT', 'TFUEL/USDT', 'KAVA/USDT', 'POND/USDT', 'MOVR/USDT', 'MASK/USDT', 'PAXG/USDT', 'BICO/USDT', 'USTC/USDT', 'CHR/USDT', 'ELF/USDT', 'IOTX/USDT', 'API3/USDT', 'NTRN/USDT', 'ICX/USDT', 'HIFI/USDT', 'TWT/USDT', 'DGB/USDT', 'STRAX/USDT', 'OSMO/USDT', 'ALPHA/USDT', 'CVC/USDT', 'NMR/USDT', 'NFP/USDT', 'OGN/USDT', 'SCRT/USDT', 'CELR/USDT', 'RDNT/USDT', 'LSK/USDT', 'UMA/USDT', 'AUCTION/USDT', 'AUDIO/USDT', 'BANANA/USDT', 'ARPA/USDT', 'COMBO/USDT', 'SYN/USDT', 'REQ/USDT', 'SLF/USDT', 'RPL/USDT', 'DUSK/USDT', 'HFT/USDT', 'ALICE/USDT', 'RLC/USDT', 'SUN/USDT', 'GLM/USDT', 'KNC/USDT', 'WAXP/USDT', 'AMB/USDT', 'MAV/USDT', 'G/USDT', 'CTSI/USDT', 'LINA/USDT', 'VIDT/USDT', 'OXT/USDT', 'T/USDT', 'DODO/USDT', 'BAND/USDT', 'MTL/USDT', 'ADX/USDT', 'VOXEL/USDT', 'PUNDIX/USDT', 'TUSD/USDT', 'AERGO/USDT', 'ALPINE/USDT', 'DIA/USDT', 'ERN/USDT', 'BURGER/USDT', 'PERP/USDT', 'NKN/USDT', 'QI/USDT', 'CREAM/USDT', 'SYS/USDT', 'GTC/USDT', 'BSW/USDT', 'XNO/USDT', 'HARD/USDT', 'DCR/USDT', 'LTO/USDT', 'SFP/USDT', 'USDP/USDT', 'FORTH/USDT', 'GNS/USDT', 'DATA/USDT', 'QUICK/USDT', 'KMD/USDT', 'WAN/USDT', 'LOKA/USDT', 'XEM/USDT', 'WAVES/USDT', 'ETHUP/USDT', 'BTCUP/USDT', 'OMG/USDT', 'XMR/USDT', 'HNT/USDT', 'BULL/USDT', 'EPX/USDT', 'POLS/USDT', 'UNFI/USDT', 'BOND/USDT', 'REN/USDT', 'BSV/USDT', 'BTT/USDT', 'REEF/USDT', 'LOOM/USDT', 'KEY/USDT']
    timeframes = ['30m', '1h', '2h', '4h', '1d']
    
    results = []
    for symbol in symbols:
        for timeframe in timeframes:
            df = fetch_data(symbol, timeframe)
            if df is None:
                continue  # اگر دریافت داده‌ها با خطا مواجه شد، به ارز بعدی برو

            df = calculate_zigzag(df)
            patterns = find_patterns(df)
            if patterns:
                results.append(f"{symbol} {timeframe}: {', '.join(patterns)}")

    if results:
        # اگر الگوی زیگزاگ پیدا شد، ایمیل ارسال شود
        send_email("ZigZag Patterns Detected", "\n".join(results))
    else:
        # اگر هیچ الگویی پیدا نشد، ایمیل "موقعیتی یافت نشد" ارسال شود
        send_email("ZigZag Patterns: No Signals Found", "هیچ موقعیتی یافت نشد")

if __name__ == "__main__":
    main()
