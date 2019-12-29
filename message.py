#這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

#TemplateSendMessage - ConfirmTemplate(確認介面訊息)
def Confirm_Word(name,df):
    
    text = name
    for d in df:
        if not d['pos']:text += '\n'
        else :
            text += '\n' + d['pos'] + '\n'
        num = 1
        for m in d['def']:
            text += '  {num}.{d} \n'.format(num = num, d=m['zh_def'])
            num+= 1
            
    message = [TextSendMessage(text=text),
        TemplateSendMessage(
        alt_text=name+' 的其他資訊',
        template=ConfirmTemplate(
            text=name+' 的其他資訊',
            actions=[
                MessageTemplateAction(
                    label=name + ' 發音',
                    text= name + ' 發音'
                ),
                MessageTemplateAction(
                    label=name + ' 例句',
                    text=name + ' 例句'
                )
            ]
        )
    )]
    return message

def Pronounce(df, accent):
    text = []
    s = ''
    if accent == '英式':
        for d in df:
            if not d['pos'] or not d['pronounce']['pronounce_uk']:
                continue
            if s == '': s = '(英式發音) [' + d['pos']
            else : s += ', '+ d['pos']
            text.append(AudioSendMessage(
                original_content_url=d['pronounce']['pronounce_uk'],
                duration=20
            ))

    elif accent == '美式':
        for d in df:
            if not d['pos'] or not d['pronounce']['pronounce_us']:
                continue
            if s == '': s = '(美式發音) [' + d['pos']
            else : s += ', '+ d['pos']
            text.append(AudioSendMessage(
                original_content_url=d['pronounce']['pronounce_us'],
                duration=20
            ))

    s += ']'
    text.insert(0,TextSendMessage(text=s))
    return text

def Example(df):
    text = ''
    for pos in df:
        text += '\n{pos}\n'.format(pos = pos['pos'])
        num = 1
        for m in pos['def']:
            text += '\n({num}){mean}\n'.format(num = num,mean = m['zh_def'])
            if not m['ex']:
                text += '\n'
                continue
            for ex in m['ex']:
                text += '{en_ex}\n'.format(en_ex = ex['eng'])
                if not ex['trans']:
                    text+= '\n'
                    continue
                text += '{trans}\n'.format(trans = ex['trans'])
            num+=1

    return TextSendMessage(text=text)

def Confirm_Pronounce(df):

    message = TemplateSendMessage(
        alt_text=df + ' 發音',
        template=ConfirmTemplate(
            text=df + ' 發音',
            actions=[
                MessageTemplateAction(
                    label="英式",
                    text=df + ' 英式',
                ),
                MessageTemplateAction(
                    label="美式",
                    text=df + ' 美式'
                )
            ]
        )
    )
    return message
