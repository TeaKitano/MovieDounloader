import PySimpleGUI as sg
from yt_dlp import YoutubeDL

#ファイルが存在するかチェック　開けてみてエラーならFalse、開いたら閉じてTrue返す
#file_name:チェックするファイル名
def checkfile(file_name):
    try:
        f=open(file_name)
    except OSError:
        return False
    else:
        f.close()
        return True

#動画としてダウンロード
#url:ダウンロード元
#file_name:出力のファイル名
def dl_mov(url,file_name):
    result=1
    file_name="./movie/"+file_name+".mp4"#保存場所とファイル名指定　プログラムが存在するディレクトリ内にmovieディレクトリがあればそこに、無ければ作成して保存。
    if checkfile(file_name):#同名ファイルがないことを確認　あったら2を返して終了
        return 2
    ydl_opts = {'format': 'best' ,'outtmpl': file_name,"ignoreerrors": True}#ダウンロードオプション指定　今回は最高品質で動画DL　エラー吐いたら無視(返り値1)
    with YoutubeDL(ydl_opts) as ydl:
        result=ydl.download([url])
    return result  #result=0なら成功　それ以外で失敗



#音源としてダウンロード
#url:ダウンロード元
#file_name:出力のファイル名
def dl_sound(url,file_name):
    file_name="./sound/"+file_name+".m4a"#保存場所とファイル名指定　プログラムが存在するディレクトリ内にsoundディレクトリがあればそこに、無ければ作成して保存。
    if checkfile(file_name):#同名ファイルがないことを確認　あったら2を返して終了
        return 2
    ydl_opts = {'format': 'm4a' ,'outtmpl': file_name,"ignoreerrors": True}#ダウンロードオプション指定　今回はm4a形式の音源ファイル
    with YoutubeDL(ydl_opts) as ydl:
        result=ydl.download([url])
    return result #result=0なら成功　それ以外で失敗


#ダウンロード制御
def dounload(values):
    url=values[0]#ダウンロード元URL
    if str(values[1])=="['音源']":
        DLtype=1 #DLtype=0なら動画、DLtype=1なら音声
    elif str(values[1])=="['動画']":
        DLtype=0
    else:
        DLtype=2
    name=values[2]#出力ファイル名

    if name=="":#出力ファイル名が空ならemptyに仮置き
        name="empty"

    if url=="":#URLが空だった場合エラーはいて終了
        sg.popup('URLを入力してください')
    elif DLtype==0:#動画DL
        result=dl_mov(url,name)
        if result==0:
            sg.popup("ダウンロードに成功しました")
        elif result==1:
            sg.popup("不正なURLです")
        else:
            sg.popup("同名ファイルが存在します。ファイル名を変えてください")

    elif DLtype==1:#音源DL
        result=dl_sound(url,name)
        if result==0:
            sg.popup("ダウンロードに成功しました")
        elif result==1:
            sg.popup("不正なURLです")
        else:
            sg.popup("同名ファイルが存在します。ファイル名を変えてください")
    else:
        sg.popup("ファイル形式を選択してください")#ダウンロード選択無しの時のエラー




#gui制御
def dounload_gui():

    file_type=["動画","音源"]#ダウンロードタイプの選択肢
    layout=[[sg.Text("youtubeから動画、音声をダウンロードするアプリケーションになります。")],
    [[sg.Text('URLを入れてください'), sg.Input()]],[sg.Text("ダウンロードしたいファイル形式を選択してください")],
    [sg.Listbox(file_type, size=(None, 2))],[[sg.Text('ダウンロードファイルの名前を入力してください'), sg.Input()]],
    [sg.Button("ダウンロード",size=(15,1)),sg.Button("終了",size=(15,1))]] #gui設計


    window=sg.Window("MovieDounloader",layout)
    while True:
        event,values=window.read()#eventと入力を取得　valuesは[ダウンロード元URL,動画か音源か,保存ファイル名]のリスト
        if event==sg.WIN_CLOSED or event=="終了":
            break
        if event=="ダウンロード":#ダウンロードボタンが押されたとき実行
            dounload(values)#ダウンロード制御関数
            

#main
if __name__ == '__main__':
     dounload_gui()