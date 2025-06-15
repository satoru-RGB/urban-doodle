from app import create_app

# アプリケーションインスタンスを作成
app = create_app()

# このスクリプトが直接実行された場合にのみサーバーを起動
if __name__ == '__main__':
    # デバッグモードでアプリケーションを実行
    app.run(debug=True)
